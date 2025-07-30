from typing import Dict, Any, List
from mistralai.models.chat_completion import ChatMessage
from .base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)

class WorldbuildingAgent(BaseAgent):
    """Worldbuilding Agent - Develops comprehensive world context and setting details"""
    
    def __init__(self):
        super().__init__("Worldbuilding Agent")
        
    async def process(self, story_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process worldbuilding elements and create detailed world context"""
        
        await self.update_status("working", 0, "Analyzing worldbuilding requirements")
        
        # Extract worldbuilding elements
        world_elements = self.extract_world_elements(story_data)
        
        await self.update_status("working", 25, "Developing world consistency framework")
        
        # Develop world consistency
        consistency_framework = await self.develop_world_consistency(world_elements, story_data)
        
        await self.update_status("working", 50, "Creating detailed world bible")
        
        # Create comprehensive world bible
        world_bible = await self.create_world_bible(world_elements, consistency_framework, story_data)
        
        await self.update_status("working", 75, "Generating world-specific story elements")
        
        # Generate world-specific elements for story integration
        story_integration = await self.create_story_integration_elements(world_bible, story_data)
        
        await self.update_status("completed", 100, "Worldbuilding complete")
        
        return {
            "world_elements": world_elements,
            "consistency_framework": consistency_framework,
            "world_bible": world_bible,
            "story_integration": story_integration,
            "worldbuilding_score": self.assess_worldbuilding_completeness(world_elements)
        }
    
    def extract_world_elements(self, story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract all worldbuilding elements from story data"""
        
        world_elements = {
            "basic_info": {
                "world_summary": story_data.get("world_summary", ""),
                "genres": story_data.get("genres", ""),
                "time_period_setting": story_data.get("time_period_setting", ""),
                "cultural_influences": story_data.get("cultural_influences", "")
            },
            "world_structure": {
                "geography": story_data.get("geography", ""),
                "climate": story_data.get("climate", ""),
                "time_period": story_data.get("time_period", ""),
                "technology_level": story_data.get("technology_level", ""),
                "magic_rules": story_data.get("magic_rules", ""),
                "physics_rules": story_data.get("physics_rules", "")
            },
            "society_culture": {
                "governance": story_data.get("governance", ""),
                "laws_justice": story_data.get("laws_justice", ""),
                "economic_system": story_data.get("economic_system", ""),
                "cultural_norms": story_data.get("cultural_norms", ""),
                "religions": story_data.get("religions", ""),
                "festivals": story_data.get("festivals", ""),
                "social_hierarchy": story_data.get("social_hierarchy", ""),
                "languages": story_data.get("languages", "")
            },
            "conflict_dynamics": {
                "current_conflict": story_data.get("current_conflict", ""),
                "factions": story_data.get("factions", ""),
                "hidden_powers": story_data.get("hidden_powers", ""),
                "law_enforcement": story_data.get("law_enforcement", ""),
                "weapons_combat": story_data.get("weapons_combat", "")
            },
            "psychology_mindset": {
                "view_of_death": story_data.get("view_of_death", ""),
                "view_of_time": story_data.get("view_of_time", ""),
                "honor_vs_survival": story_data.get("honor_vs_survival", ""),
                "individual_vs_collective": story_data.get("individual_vs_collective", ""),
                "emotion_expression": story_data.get("emotion_expression", "")
            },
            "modern_tech": {
                "media_propaganda": story_data.get("media_propaganda", ""),
                "surveillance_level": story_data.get("surveillance_level", ""),
                "internet_access": story_data.get("internet_access", ""),
                "popular_culture": story_data.get("popular_culture", "")
            },
            "themes_tone": {
                "emotional_vibe": story_data.get("emotional_vibe", ""),
                "symbolic_motifs": story_data.get("symbolic_motifs", ""),
                "historical_trauma": story_data.get("historical_trauma", ""),
                "power_over_truth": story_data.get("power_over_truth", "")
            },
            "physical_details": {
                "architecture_style": story_data.get("architecture_style", ""),
                "fashion_trends": story_data.get("fashion_trends", ""),
                "transportation": story_data.get("transportation", ""),
                "food_culture": story_data.get("food_culture", ""),
                "street_sounds": story_data.get("street_sounds", "")
            },
            "story_utility": {
                "world_challenges": story_data.get("world_challenges", ""),
                "world_rewards": story_data.get("world_rewards", ""),
                "death_triggers": story_data.get("death_triggers", ""),
                "world_changes": story_data.get("world_changes", "")
            }
        }
        
        return world_elements
    
    async def develop_world_consistency(self, world_elements: Dict[str, Any], story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Develop a consistency framework for the world"""
        
        system_prompt = """You are an expert worldbuilding agent. Your task is to analyze the provided world elements and create a comprehensive consistency framework that ensures all elements work together harmoniously.

Focus on:
1. Identifying potential contradictions between world elements
2. Creating logical connections between different systems
3. Establishing cause-and-effect relationships
4. Ensuring genre consistency
5. Maintaining thematic coherence

Provide detailed analysis and recommendations in JSON format."""
        
        # Format world elements for analysis
        world_context = self.format_world_elements_for_analysis(world_elements)
        story_context = self.format_story_context(story_data)
        
        user_prompt = f"""Analyze these world elements for consistency and create a framework:

STORY CONTEXT:
{story_context}

WORLD ELEMENTS:
{world_context}

Create a comprehensive consistency framework that addresses:
1. Logical relationships between systems
2. Potential contradictions and how to resolve them
3. Missing elements that should be developed
4. Integration recommendations for story coherence

Provide your analysis in structured JSON format."""
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt)
        ]
        
        response = await self.call_mistral(messages, temperature=0.4)
        
        try:
            import json_repair
            return json_repair.loads(response)
        except:
            return {
                "consistency_level": "moderate",
                "identified_issues": ["Minor timeline inconsistencies"],
                "recommendations": ["Develop technological progression timeline"],
                "integration_points": ["Character backgrounds should reflect world history"]
            }
    
    async def create_world_bible(self, world_elements: Dict[str, Any], consistency_framework: Dict[str, Any], story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive world bible for story consistency"""
        
        system_prompt = """You are creating a comprehensive World Bible for a story. This bible will be used by other agents to maintain consistency throughout the story generation process.

Create a detailed, organized world reference that includes:
1. Complete world overview and history
2. Detailed locations and geography
3. Cultural and social systems
4. Political and economic structures
5. Technology and magic systems (if applicable)
6. Key historical events and timeline
7. Important world rules and limitations
8. Atmospheric details and sensory elements

Make it comprehensive, internally consistent, and perfectly aligned with the story's themes and genre."""
        
        story_context = self.format_story_context(story_data)
        world_context = self.format_world_elements_for_analysis(world_elements)
        
        user_prompt = f"""Create a comprehensive World Bible for this story:

STORY FOUNDATION:
{story_context}

WORLD ELEMENTS:
{world_context}

CONSISTENCY FRAMEWORK:
{str(consistency_framework)}

Create a detailed World Bible that will serve as the authoritative reference for all story elements. Include:

1. WORLD OVERVIEW
   - Core concept and unique aspects
   - Genre-specific elements
   - Overall tone and atmosphere

2. GEOGRAPHY & LOCATIONS
   - Key locations and their significance
   - Environmental details
   - Travel and distance considerations

3. HISTORY & TIMELINE
   - Major historical events
   - How the past shapes the present
   - Timeline of important developments

4. SOCIETY & CULTURE
   - Social structures and hierarchies
   - Cultural norms and taboos
   - Daily life and customs

5. POLITICS & POWER
   - Governing systems
   - Power structures and conflicts
   - Law enforcement and justice

6. ECONOMICS & TECHNOLOGY
   - Economic systems and trade
   - Technology levels and limitations
   - Communication methods

7. MAGIC/SUPERNATURAL (if applicable)
   - Rules and limitations
   - How it affects society
   - Costs and consequences

8. SENSORY WORLD
   - What people see, hear, smell
   - Atmospheric details
   - Environmental storytelling elements

Make this comprehensive and usable for story generation."""
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt)
        ]
        
        response = await self.call_mistral(messages, temperature=0.6, max_tokens=4000)
        
        return {
            "world_bible_content": response,
            "creation_date": "2025-01-27",
            "version": "1.0",
            "completeness_score": self.assess_worldbuilding_completeness(world_elements)
        }
    
    async def create_story_integration_elements(self, world_bible: Dict[str, Any], story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create specific elements for integrating world into story"""
        
        system_prompt = """You are creating specific story integration elements that will help other agents weave the world seamlessly into the narrative.

Focus on creating:
1. Scene-setting elements for different chapter types
2. World-specific conflict opportunities
3. Environmental storytelling opportunities
4. Cultural details that can enhance character interactions
5. World rules that can create plot tension
6. Atmospheric elements for different moods

Make these practical and actionable for story generation."""
        
        story_context = self.format_story_context(story_data)
        world_content = world_bible.get("world_bible_content", "")
        
        user_prompt = f"""Based on this world bible and story context, create practical integration elements:

STORY CONTEXT:
{story_context}

WORLD BIBLE:
{world_content[:2000]}...

Create specific, actionable integration elements:

1. SCENE SETTING TOOLKIT
   - Environmental details for different scenes
   - Sensory details (sounds, smells, textures)
   - Weather and atmospheric elements

2. CONFLICT INTEGRATION
   - How world elements can create obstacles
   - Environmental challenges for characters
   - Social/cultural sources of tension

3. CHARACTER-WORLD INTERACTIONS
   - How characters should interact with this world
   - World-specific mannerisms and behaviors
   - Cultural touchstones and references

4. PLOT ENHANCEMENT OPPORTUNITIES
   - World elements that can drive plot forward
   - Environmental storytelling moments
   - Cultural events or traditions to incorporate

5. CONSISTENCY REMINDERS
   - Key world rules to remember
   - Important limitations and boundaries
   - Essential world facts to maintain

Make this practical for generating {story_data.get('total_chapters', 10)} chapters."""
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt)
        ]
        
        response = await self.call_mistral(messages, temperature=0.7)
        
        return {
            "integration_elements": response,
            "scene_toolkit": "Available for all chapters",
            "consistency_checklist": "Integrated world rules"
        }
    
    def format_world_elements_for_analysis(self, world_elements: Dict[str, Any]) -> str:
        """Format world elements into readable text for analysis"""
        
        formatted_sections = []
        
        for category, elements in world_elements.items():
            if isinstance(elements, dict):
                section_parts = []
                for key, value in elements.items():
                    if value and value.strip():
                        section_parts.append(f"  {key.replace('_', ' ').title()}: {value}")
                
                if section_parts:
                    formatted_sections.append(f"{category.replace('_', ' ').title()}:\n" + "\n".join(section_parts))
        
        return "\n\n".join(formatted_sections)
    
    def assess_worldbuilding_completeness(self, world_elements: Dict[str, Any]) -> float:
        """Assess how complete the worldbuilding is (0.0 to 1.0)"""
        
        total_fields = 0
        filled_fields = 0
        
        for category, elements in world_elements.items():
            if isinstance(elements, dict):
                for key, value in elements.items():
                    total_fields += 1
                    if value and value.strip():
                        filled_fields += 1
        
        if total_fields == 0:
            return 0.0
        
        return filled_fields / total_fields