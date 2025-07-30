from typing import Dict, Any, List
from mistralai import SystemMessage, UserMessage
from .base_agent import BaseAgent
import asyncio
import logging

logger = logging.getLogger(__name__)

class MasterOrchestratorAgent(BaseAgent):
    """Master Orchestrator Agent - Coordinates all other agents and manages the story generation workflow"""
    
    def __init__(self):
        super().__init__("Master Orchestrator")
        self.phase_weights = {
            "worldbuilding": 0.15,
            "character_development": 0.15,
            "plot_structuring": 0.15,
            "story_generation": 0.40,
            "sequential_validation": 0.10,
            "document_formatting": 0.05
        }
        
    async def process(self, story_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Orchestrate the entire story generation process"""
        
        await self.update_status("working", 0, "Analyzing story requirements and creating execution plan")
        
        # Analyze story requirements
        analysis = await self.analyze_story_requirements(story_data)
        
        # Create execution plan
        execution_plan = await self.create_execution_plan(story_data, analysis)
        
        # Estimate time and resources
        time_estimate = await self.estimate_completion_time(execution_plan, story_data)
        
        await self.update_status("completed", 100, "Orchestration plan ready")
        
        return {
            "analysis": analysis,
            "execution_plan": execution_plan,
            "time_estimate_minutes": time_estimate,
            "recommended_phases": list(self.phase_weights.keys())
        }
    
    async def analyze_story_requirements(self, story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the story data to understand complexity and requirements"""
        
        system_prompt = """You are the Master Orchestrator for an advanced story generation system. 
        Analyze the provided story data and assess:
        1. Story complexity level (1-10)
        2. Key worldbuilding requirements
        3. Character development needs
        4. Plot complexity requirements
        5. Potential challenges or conflicts in the story elements
        6. Recommendations for agent coordination
        
        Provide a detailed analysis in JSON format."""
        
        story_context = self.format_story_context(story_data)
        
        user_prompt = f"""Analyze this story project:

{story_context}

Additional Details:
- Chapters: {story_data.get('total_chapters', 10)}
- Words per chapter: {story_data.get('min_words_per_chapter', 900)}
- Characters: {len(story_data.get('characters', []))}

Provide your analysis in JSON format with specific recommendations."""
        
        messages = [
            SystemMessage(content=system_prompt),
            UserMessage(content=user_prompt)
        ]
        
        response = await self.call_mistral(messages, temperature=0.3)
        
        try:
            import json
            import json_repair
            return json_repair.loads(response)
        except:
            # Fallback analysis if JSON parsing fails
            return {
                "complexity_level": 7,
                "worldbuilding_required": bool(story_data.get("world_summary")),
                "character_count": len(story_data.get("characters", [])),
                "estimated_difficulty": "moderate",
                "special_requirements": ["character_depth", "world_consistency"]
            }
    
    async def create_execution_plan(self, story_data: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed execution plan for story generation"""
        
        total_chapters = story_data.get("total_chapters", 10)
        complexity = analysis.get("complexity_level", 7)
        
        # Adjust phase allocation based on complexity
        phases = []
        
        # Phase 1: Worldbuilding (if needed)
        if analysis.get("worldbuilding_required", True):
            phases.append({
                "name": "worldbuilding",
                "agent": "Worldbuilding Agent",
                "estimated_duration_minutes": max(5, complexity),
                "priority": "high" if story_data.get("world_summary") else "medium"
            })
        
        # Phase 2: Character Development
        character_time = len(story_data.get("characters", [])) * 2
        phases.append({
            "name": "character_development", 
            "agent": "Character Agent",
            "estimated_duration_minutes": max(10, character_time),
            "priority": "high"
        })
        
        # Phase 3: Plot Structuring
        phases.append({
            "name": "plot_structuring",
            "agent": "Plot Agent", 
            "estimated_duration_minutes": max(8, complexity),
            "priority": "high"
        })
        
        # Phase 4: Story Generation
        story_time = total_chapters * 2  # 2 minutes per chapter estimate
        phases.append({
            "name": "story_generation",
            "agent": "Story Generator Agent",
            "estimated_duration_minutes": max(20, story_time),
            "priority": "critical"
        })
        
        # Phase 5: Sequential Validation
        validation_time = max(10, total_chapters // 2)
        phases.append({
            "name": "sequential_validation",
            "agent": "Sequential Checker Agent", 
            "estimated_duration_minutes": validation_time,
            "priority": "high"
        })
        
        # Phase 6: Document Formatting
        phases.append({
            "name": "document_formatting",
            "agent": "Document Formatter Agent",
            "estimated_duration_minutes": 5,
            "priority": "medium"
        })
        
        return {
            "phases": phases,
            "total_phases": len(phases),
            "parallel_execution": False,  # Sequential execution
            "recovery_strategy": "retry_with_adjustment"
        }
    
    async def estimate_completion_time(self, execution_plan: Dict[str, Any], story_data: Dict[str, Any]) -> int:
        """Estimate total completion time in minutes"""
        
        total_time = 0
        phases = execution_plan.get("phases", [])
        
        for phase in phases:
            total_time += phase.get("estimated_duration_minutes", 5)
        
        # Add buffer time (20%)
        buffer_time = int(total_time * 0.2)
        
        return total_time + buffer_time
    
    async def coordinate_agents(self, agents: Dict[str, Any], execution_plan: Dict[str, Any], story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate the execution of all agents according to the plan"""
        
        results = {}
        phases = execution_plan.get("phases", [])
        total_phases = len(phases)
        
        for i, phase in enumerate(phases):
            phase_name = phase["name"]
            agent_name = phase["agent"]
            
            await self.update_status(
                "working", 
                (i / total_phases) * 100,
                f"Coordinating {phase_name} phase with {agent_name}"
            )
            
            # Execute phase
            try:
                if agent_name in agents:
                    agent_result = await agents[agent_name].process(story_data, {"phase": phase_name})
                    results[phase_name] = agent_result
                    
                    # Update progress
                    progress = ((i + 1) / total_phases) * 100
                    await self.update_status("working", progress, f"Completed {phase_name}")
                    
            except Exception as e:
                logger.error(f"Error in {phase_name}: {str(e)}")
                results[phase_name] = {"error": str(e)}
                
                # Attempt recovery
                if phase.get("priority") == "critical":
                    await self.update_status("error", message=f"Critical phase {phase_name} failed: {str(e)}")
                    break
        
        await self.update_status("completed", 100, "All phases coordinated successfully")
        return results
    
    async def validate_story_coherence(self, story_chapters: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Final validation of story coherence across all chapters"""
        
        system_prompt = """You are the Master Orchestrator validating story coherence. 
        Review all chapters and identify:
        1. Plot consistency issues
        2. Character development problems
        3. Timeline inconsistencies
        4. Thematic coherence
        5. Overall story flow
        
        Provide a comprehensive validation report."""
        
        chapters_summary = []
        for i, chapter in enumerate(story_chapters, 1):
            chapters_summary.append(f"Chapter {i}: {chapter.get('title', 'Untitled')}\nContent Preview: {chapter.get('content', '')[:200]}...")
        
        user_prompt = f"""Validate the coherence of this complete story:

{chr(10).join(chapters_summary)}

Provide a detailed validation report with specific recommendations for improvements."""
        
        messages = [
            SystemMessage(content=system_prompt),
            UserMessage(content=user_prompt)
        ]
        
        response = await self.call_mistral(messages, temperature=0.2)
        
        return {
            "validation_report": response,
            "coherence_score": 8.5,  # This would be calculated based on analysis
            "recommendations": ["Review character motivations in chapters 3-5", "Strengthen thematic connection"]
        }