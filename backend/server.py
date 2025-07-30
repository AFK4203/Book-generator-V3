from fastapi import FastAPI, APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
import asyncio
import json

# Import models
from models import (
    StoryData, GenerateStoryRequest, GenerateStoryResponse, 
    StoryProgressResponse, ChapterPreviewResponse, DownloadStoryResponse,
    StoryGenerationSession, AgentStatus
)

# Import agents
from agents.master_orchestrator import MasterOrchestratorAgent
from agents.worldbuilding_agent import WorldbuildingAgent
from agents.character_agent import CharacterAgent
from agents.plot_agent import PlotAgent
from agents.story_generator_agent import StoryGeneratorAgent
from agents.sequential_checker_agent import SequentialCheckerAgent
from agents.document_formatter_agent import DocumentFormatterAgent

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Book Generator V2 API", version="2.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Initialize agents
agents = {
    "master_orchestrator": MasterOrchestratorAgent(),
    "worldbuilding": WorldbuildingAgent(),
    "character": CharacterAgent(),
    "plot": PlotAgent(),
    "story_generator": StoryGeneratorAgent(),
    "sequential_checker": SequentialCheckerAgent(),
    "document_formatter": DocumentFormatterAgent()
}

# WebSocket connections for real-time updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_update(self, session_id: str, data: dict):
        message = {
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat(),
            **data
        }
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except:
                pass

manager = ConnectionManager()

# Story generation sessions storage
active_sessions: Dict[str, Dict[str, Any]] = {}

@api_router.get("/")
async def root():
    return {"message": "Book Generator V2 API - Multi-Agent Story Generation System"}

@api_router.get("/agents")
async def get_agents():
    """Get status of all AI agents"""
    agent_statuses = []
    for name, agent in agents.items():
        status = agent.get_status()
        agent_statuses.append(status)
    
    return {
        "agents": agent_statuses,
        "total_agents": len(agents),
        "system_ready": all(agent.status != "error" for agent in agents.values())
    }

@api_router.post("/story/generate", response_model=GenerateStoryResponse)
async def generate_story(request: GenerateStoryRequest):
    """Start story generation process with all 7 AI agents"""
    
    session_id = str(uuid.uuid4())
    story_data = request.story_data
    
    # Create generation session
    session = StoryGenerationSession(
        id=session_id,
        story_data=story_data,
        current_phase="initialized",
        progress=0.0
    )
    
    # Store session
    await db.story_sessions.insert_one(session.dict())
    active_sessions[session_id] = {
        "session": session,
        "agent_results": {},
        "task": None
    }
    
    # Get estimated time from Master Orchestrator
    try:
        master_result = await agents["master_orchestrator"].process(story_data.dict())
        estimated_time = master_result.get("time_estimate_minutes", 30)
    except Exception as e:
        logging.error(f"Master Orchestrator failed: {str(e)}")
        estimated_time = 30
    
    # Start generation process in background
    task = asyncio.create_task(run_story_generation(session_id, story_data))
    active_sessions[session_id]["task"] = task
    
    return GenerateStoryResponse(
        session_id=session_id,
        message="Story generation started",
        estimated_time_minutes=estimated_time
    )

@api_router.get("/story/{session_id}/progress", response_model=StoryProgressResponse)
async def get_story_progress(session_id: str):
    """Get real-time progress of story generation"""
    
    if session_id not in active_sessions:
        session_doc = await db.story_sessions.find_one({"id": session_id})
        if not session_doc:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = StoryGenerationSession(**session_doc)
        return StoryProgressResponse(
            session_id=session_id,
            current_phase=session.current_phase,
            progress=session.progress,
            agent_statuses=session.agent_statuses,
            estimated_completion_time=session.estimated_completion_time,
            error_message=session.error_message
        )
    
    session_data = active_sessions[session_id]
    session = session_data["session"]
    
    # Get current agent statuses
    current_agent_statuses = []
    for name, agent in agents.items():
        status = agent.get_status()
        current_agent_statuses.append(AgentStatus(**status))
    
    return StoryProgressResponse(
        session_id=session_id,
        current_phase=session.current_phase,
        progress=session.progress,
        agent_statuses=current_agent_statuses,
        estimated_completion_time=session.estimated_completion_time,
        error_message=session.error_message
    )

@api_router.get("/story/{session_id}/preview", response_model=ChapterPreviewResponse)
async def get_story_preview(session_id: str):
    """Get preview of generated chapters"""
    
    session_doc = await db.story_sessions.find_one({"id": session_id})
    if not session_doc:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = StoryGenerationSession(**session_doc)
    
    total_words = sum(ch.word_count for ch in session.chapters)
    
    return ChapterPreviewResponse(
        session_id=session_id,
        chapters=session.chapters,
        total_word_count=total_words
    )

@api_router.get("/story/{session_id}/download", response_model=DownloadStoryResponse)
async def download_story(session_id: str):
    """Download completed story as KDP-ready .docx file"""
    
    session_doc = await db.story_sessions.find_one({"id": session_id})
    if not session_doc:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = StoryGenerationSession(**session_doc)
    
    if not session.generated_document_path:
        raise HTTPException(status_code=400, detail="Story not ready for download")
    
    if not os.path.exists(session.generated_document_path):
        raise HTTPException(status_code=404, detail="Generated file not found")
    
    file_name = os.path.basename(session.generated_document_path)
    total_words = sum(ch.word_count for ch in session.chapters)
    
    return DownloadStoryResponse(
        session_id=session_id,
        download_url=f"/api/story/{session_id}/file",
        file_name=file_name,
        total_chapters=len(session.chapters),
        total_words=total_words
    )

@api_router.get("/story/{session_id}/file")
async def download_file(session_id: str):
    """Download the actual .docx file"""
    
    session_doc = await db.story_sessions.find_one({"id": session_id})
    if not session_doc:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = StoryGenerationSession(**session_doc)
    
    if not session.generated_document_path or not os.path.exists(session.generated_document_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        session.generated_document_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=os.path.basename(session.generated_document_path)
    )

@api_router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket for real-time story generation updates"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle any client messages if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@api_router.delete("/story/{session_id}")
async def cancel_story_generation(session_id: str):
    """Cancel ongoing story generation"""
    
    if session_id in active_sessions:
        task = active_sessions[session_id].get("task")
        if task and not task.done():
            task.cancel()
        
        del active_sessions[session_id]
    
    # Update database
    await db.story_sessions.update_one(
        {"id": session_id},
        {"$set": {"current_phase": "cancelled", "error_message": "Generation cancelled by user"}}
    )
    
    return {"message": "Story generation cancelled"}

async def run_story_generation(session_id: str, story_data: StoryData):
    """Run the complete story generation process"""
    
    try:
        session_data = active_sessions[session_id]
        session = session_data["session"]
        agent_results = session_data["agent_results"]
        
        # Phase 1: Master Orchestrator
        await update_session_phase(session_id, "orchestration", 5)
        await manager.send_update(session_id, {"phase": "orchestration", "message": "Master Orchestrator analyzing requirements"})
        
        orchestrator_result = await agents["master_orchestrator"].process(story_data.dict())
        agent_results["orchestrator"] = orchestrator_result
        
        # Phase 2: Worldbuilding
        await update_session_phase(session_id, "worldbuilding", 15)
        await manager.send_update(session_id, {"phase": "worldbuilding", "message": "Worldbuilding Agent developing world context"})
        
        worldbuilding_result = await agents["worldbuilding"].process(story_data.dict())
        agent_results["worldbuilding"] = worldbuilding_result
        
        # Phase 3: Character Development
        await update_session_phase(session_id, "character_development", 30)
        await manager.send_update(session_id, {"phase": "character_development", "message": "Character Agent developing character profiles"})
        
        character_result = await agents["character"].process(story_data.dict(), {"worldbuilding_result": worldbuilding_result})
        agent_results["character"] = character_result
        
        # Phase 4: Plot Structuring
        await update_session_phase(session_id, "plot_structuring", 45)
        await manager.send_update(session_id, {"phase": "plot_structuring", "message": "Plot Agent structuring story framework"})
        
        plot_result = await agents["plot"].process(
            story_data.dict(), 
            {"worldbuilding_result": worldbuilding_result, "character_result": character_result}
        )
        agent_results["plot"] = plot_result
        
        # Phase 5: Story Generation
        await update_session_phase(session_id, "story_generation", 50)
        await manager.send_update(session_id, {"phase": "story_generation", "message": "Story Generator Agent writing chapters"})
        
        story_result = await agents["story_generator"].process(
            story_data.dict(),
            {
                "worldbuilding_result": worldbuilding_result,
                "character_result": character_result,
                "plot_result": plot_result
            }
        )
        agent_results["story_generator"] = story_result
        
        # Phase 6: Sequential Validation
        await update_session_phase(session_id, "sequential_validation", 85)
        await manager.send_update(session_id, {"phase": "sequential_validation", "message": "Sequential Checker Agent validating chapters"})
        
        validation_result = await agents["sequential_checker"].process(
            story_data.dict(),
            {
                "story_generation_result": story_result,
                "worldbuilding_result": worldbuilding_result,
                "character_result": character_result,
                "plot_result": plot_result
            }
        )
        agent_results["sequential_validation"] = validation_result
        
        # Phase 7: Document Formatting
        await update_session_phase(session_id, "document_formatting", 95)
        await manager.send_update(session_id, {"phase": "document_formatting", "message": "Document Formatter Agent creating KDP-ready file"})
        
        format_result = await agents["document_formatter"].process(
            story_data.dict(),
            {
                "sequential_validation_result": validation_result,
                "story_generation_result": story_result
            }
        )
        agent_results["document_formatter"] = format_result
        
        # Complete generation
        await update_session_phase(session_id, "completed", 100)
        
        # Update session with final results
        validated_chapters = validation_result.get("validated_chapters", [])
        document_path = format_result.get("document_path", "")
        
        # Convert chapters to Chapter objects for database storage
        from models import Chapter
        chapter_objects = []
        for ch in validated_chapters:
            chapter_obj = Chapter(
                chapter_number=ch.get("chapter_number", 1),
                title=ch.get("title", f"Chapter {ch.get('chapter_number', 1)}"),
                content=ch.get("content", ""),
                word_count=ch.get("word_count", 0),
                validation_status=ch.get("validation_status", "validated")
            )
            chapter_objects.append(chapter_obj)
        
        # Update database
        await db.story_sessions.update_one(
            {"id": session_id},
            {
                "$set": {
                    "current_phase": "completed",
                    "progress": 100.0,
                    "chapters": [ch.dict() for ch in chapter_objects],
                    "generated_document_path": document_path,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        await manager.send_update(session_id, {
            "phase": "completed", 
            "message": f"Story generation complete! {len(chapter_objects)} chapters generated.",
            "download_ready": True,
            "document_path": document_path
        })
        
    except Exception as e:
        logging.error(f"Story generation failed for session {session_id}: {str(e)}")
        
        await db.story_sessions.update_one(
            {"id": session_id},
            {
                "$set": {
                    "current_phase": "error",
                    "error_message": str(e),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        await manager.send_update(session_id, {
            "phase": "error",
            "message": f"Generation failed: {str(e)}"
        })
    
    finally:
        # Clean up active session
        if session_id in active_sessions:
            del active_sessions[session_id]

async def update_session_phase(session_id: str, phase: str, progress: float):
    """Update session phase and progress"""
    
    await db.story_sessions.update_one(
        {"id": session_id},
        {
            "$set": {
                "current_phase": phase,
                "progress": progress,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    if session_id in active_sessions:
        active_sessions[session_id]["session"].current_phase = phase
        active_sessions[session_id]["session"].progress = progress

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    logger.info("Book Generator V2 API starting up...")
    logger.info("7 AI agents initialized and ready")
    
    # Ensure generated stories directory exists
    os.makedirs("/app/generated_stories", exist_ok=True)

@app.on_event("shutdown")
async def shutdown_db_client():
    """Cleanup on shutdown"""
    client.close()
    logger.info("Book Generator V2 API shutting down...")