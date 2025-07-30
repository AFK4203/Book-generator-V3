from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import asyncio
import logging
from datetime import datetime
from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all story generation agents"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.client = MistralAsyncClient(api_key=os.getenv("MISTRAL_API_KEY"))
        self.model = os.getenv("MISTRAL_MODEL", "mistral-large-latest")
        self.max_retries = 3
        self.status = "ready"
        self.progress = 0.0
        self.message = ""
        
    async def update_status(self, status: str, progress: float = None, message: str = ""):
        """Update agent status"""
        self.status = status
        if progress is not None:
            self.progress = progress
        self.message = message
        logger.info(f"{self.agent_name}: {status} - {message} ({progress}%)")
        
    async def call_mistral(self, 
                          messages: List[ChatMessage], 
                          temperature: float = 0.7,
                          max_tokens: Optional[int] = None) -> str:
        """Make a call to Mistral API with retry logic"""
        
        for attempt in range(self.max_retries):
            try:
                await self.update_status("working", message=f"Calling Mistral API (attempt {attempt + 1})")
                
                response = await self.client.chat(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                content = response.choices[0].message.content
                if content:
                    return content.strip()
                else:
                    raise Exception("Empty response from Mistral API")
                    
            except Exception as e:
                logger.error(f"{self.agent_name} - Mistral API call failed (attempt {attempt + 1}): {str(e)}")
                if attempt == self.max_retries - 1:
                    await self.update_status("error", message=f"Failed after {self.max_retries} attempts: {str(e)}")
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    @abstractmethod
    async def process(self, story_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process the story data and return results"""
        pass
    
    def create_system_prompt(self) -> str:
        """Create the system prompt for this agent"""
        return f"You are {self.agent_name}, a professional story development agent."
    
    def format_story_context(self, story_data: Dict[str, Any]) -> str:
        """Format story data into context for the agent"""
        context_parts = []
        
        # Core story elements
        if story_data.get("central_theme"):
            context_parts.append(f"CENTRAL THEME: {story_data['central_theme']}")
        if story_data.get("main_premise"):
            context_parts.append(f"MAIN PREMISE: {story_data['main_premise']}")
        if story_data.get("negative_prompt"):
            context_parts.append(f"THINGS TO AVOID: {story_data['negative_prompt']}")
        if story_data.get("genres"):
            context_parts.append(f"GENRES: {story_data['genres']}")
        
        # World context
        if story_data.get("world_summary"):
            context_parts.append(f"WORLD: {story_data['world_summary']}")
        
        # Characters
        characters = story_data.get("characters", [])
        if characters:
            char_list = []
            for char in characters:
                if isinstance(char, dict) and char.get("name"):
                    char_info = f"- {char['name']}"
                    if char.get("archetype"):
                        char_info += f" ({char['archetype']})"
                    if char.get("backstory_one_sentence"):
                        char_info += f": {char['backstory_one_sentence']}"
                    char_list.append(char_info)
            if char_list:
                context_parts.append(f"CHARACTERS:\n" + "\n".join(char_list))
        
        # Generation settings
        context_parts.append(f"TARGET: {story_data.get('total_chapters', 10)} chapters, {story_data.get('min_words_per_chapter', 900)} words per chapter minimum")
        
        return "\n\n".join(context_parts)
    
    async def validate_output(self, output: str) -> bool:
        """Validate the agent's output"""
        return len(output.strip()) > 0
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_name": self.agent_name,
            "status": self.status,
            "progress": self.progress,
            "message": self.message
        }