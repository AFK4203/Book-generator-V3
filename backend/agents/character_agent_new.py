from typing import Dict, Any, List
from mistralai import SystemMessage, UserMessage
from .base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)

class CharacterAgent(BaseAgent):
    """Character Agent - Develops deep, complex character profiles and relationships"""
    
    def __init__(self):
        super().__init__("Character Agent")
        
    async def process(self, story_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process character development and create comprehensive character profiles"""
        
        await self.update_status("working", 0, "Analyzing character requirements")
        
        # Extract and validate characters
        characters = story_data.get("characters", [])
        if not characters:
            await self.update_status("error", 0, "No characters provided for development")
            return {"error": "No characters found"}
        
        await self.update_status("working", 20, f"Developing {len(characters)} character profiles")
        
        # Develop each character
        developed_characters = []
        for i, character in enumerate(characters):
            progress = 20 + (i / len(characters)) * 60
            await self.update_status("working", progress, f"Developing character: {character.get('name', 'Unnamed')}")
            
            developed_char = await self.develop_character_profile(character, story_data, characters)
            developed_characters.append(developed_char)
        
        await self.update_status("working", 80, "Creating character relationship dynamics")
        
        # Create relationship dynamics
        relationship_dynamics = await self.create_relationship_dynamics(developed_characters, story_data)
        
        await self.update_status("working", 90, "Generating character arcs and development paths")
        
        # Generate character arcs
        character_arcs = await self.generate_character_arcs(developed_characters, story_data)
        
        await self.update_status("completed", 100, "Character development complete")
        
        return {
            "developed_characters": developed_characters,
            "relationship_dynamics": relationship_dynamics,
            "character_arcs": character_arcs,
            "character_count": len(developed_characters),
            "development_completeness": self.assess_character_completeness(developed_characters)
        }
    
    async def develop_character_profile(self, character: Dict[str, Any], story_data: Dict[str, Any], all_characters: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Develop a comprehensive profile for a single character"""
        
        system_prompt = """You are an expert character development agent. Your task is to take basic character information and develop it into a rich, complex, three-dimensional character profile.

Focus on:
1. Psychological depth and complexity
2. Internal consistency and believability
3. Character motivations and conflicts
4. Unique voice and personality traits
5. Character growth potential
6. Relationships with other characters
7. Role in the story's themes

Create a comprehensive character profile that will guide consistent character portrayal throughout the story."""
        
        # Format character data
        char_basic_info = self.format_character_basics(character)
        story_context = self.format_story_context(story_data)
        other_characters = self.format_other_characters(character, all_characters)
        
        user_prompt = f"""Develop this character into a rich, complex profile:

STORY CONTEXT:
{story_context}

CHARACTER BASICS:
{char_basic_info}

OTHER CHARACTERS IN STORY:
{other_characters}

Develop a comprehensive character profile including:

1. CORE IDENTITY
   - Enhanced backstory with specific details
   - Core personality traits and contradictions
   - Unique worldview and beliefs
   - Internal conflicts and struggles

2. PSYCHOLOGICAL PROFILE
   - Emotional patterns and triggers
   - Coping mechanisms and defense strategies
   - Hidden fears and desires
   - Mental and emotional wounds

3. RELATIONSHIPS & SOCIAL DYNAMICS
   - How they interact with different types of people
   - Leadership style or following tendencies
   - Trust issues and loyalty patterns
   - Communication style and quirks

4. CHARACTER VOICE & MANNERISMS
   - Speech patterns and vocabulary
   - Physical habits and tics
   - Personal style and preferences
   - Unique quirks that make them memorable

5. STORY FUNCTION
   - Their role in the main plot
   - Character arc and growth journey
   - Thematic significance
   - Conflict sources and story catalyst moments

6. PRACTICAL DETAILS
   - How they would react in different situations
   - Decision-making patterns
   - Moral boundaries and limits
   - Skills and abilities relevant to the story

Make this character feel like a real, complex person with depth and contradictions."""
        
        messages = [
            SystemMessage(content=system_prompt),
            UserMessage(content=user_prompt)
        ]
        
        response = await self.call_mistral(messages, temperature=0.7, max_tokens=3000)
        
        # Merge developed profile with original character data
        developed_character = character.copy()
        developed_character["developed_profile"] = response
        developed_character["development_timestamp"] = "2025-01-27"
        
        return developed_character
    
    async def create_relationship_dynamics(self, characters: List[Dict[str, Any]], story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed relationship dynamics between characters"""
        
        system_prompt = """You are creating relationship dynamics between characters in a story. Focus on creating complex, realistic relationships that will drive plot and character development.

Consider:
1. How each character sees and interacts with others
2. Power dynamics and hierarchies
3. Romantic, familial, and platonic relationships
4. Conflicts and alliances
5. How relationships change over time
6. Hidden relationships or secrets

Create detailed relationship maps and interaction guidelines."""
        
        story_context = self.format_story_context(story_data)
        characters_summary = self.format_characters_for_relationships(characters)
        
        user_prompt = f"""Create detailed relationship dynamics for these characters:

STORY CONTEXT:
{story_context}

CHARACTERS:
{characters_summary}

Create comprehensive relationship dynamics including:

1. RELATIONSHIP MATRIX
   - How each character views every other character
   - Relationship types (ally, enemy, romantic interest, mentor, etc.)
   - Power dynamics between characters

2. CONFLICT SOURCES
   - What creates tension between characters
   - Competing goals and motivations
   - Past history that affects current relationships

3. ALLIANCE PATTERNS
   - Who naturally works together
   - Temporary alliances vs. long-term bonds
   - How alliances might shift during the story

4. HIDDEN RELATIONSHIPS
   - Secret connections or past history
   - Unspoken feelings or attractions
   - Family connections or shared secrets

5. RELATIONSHIP EVOLUTION
   - How relationships will change throughout the story
   - Growth opportunities and breaking points
   - Reconciliation or permanent rifts

6. INTERACTION GUIDELINES
   - How characters should speak to each other
   - Body language and behavior patterns
   - Specific dynamics in group scenes

Make these relationships feel natural and complex, with room for growth and conflict."""
        
        messages = [
            SystemMessage(content=system_prompt),
            UserMessage(content=user_prompt)
        ]
        
        response = await self.call_mistral(messages, temperature=0.6)
        
        return {
            "relationship_analysis": response,
            "character_count": len(characters),
            "relationship_complexity": "high" if len(characters) > 2 else "moderate"
        }
    
    async def generate_character_arcs(self, characters: List[Dict[str, Any]], story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate character development arcs for the story"""
        
        system_prompt = """You are creating character development arcs that show how each character will grow and change throughout the story.

Focus on:
1. Character starting points and end goals
2. Internal conflicts that drive growth
3. External challenges that force change
4. Specific moments of character development
5. How character growth serves the story themes
6. Realistic pacing of character change

Create detailed arc plans that can guide character development across all chapters."""
        
        story_context = self.format_story_context(story_data)
        characters_summary = self.format_characters_for_arcs(characters)
        total_chapters = story_data.get("total_chapters", 10)
        
        user_prompt = f"""Create character development arcs for this {total_chapters}-chapter story:

STORY CONTEXT:
{story_context}

CHARACTERS:
{characters_summary}

Create detailed character arcs including:

1. CHARACTER ARC OVERVIEW
   - Starting state for each character
   - End state and growth achieved
   - Arc type (positive change, negative fall, flat arc, etc.)

2. DEVELOPMENT MILESTONES
   - Key moments of character growth or change
   - Which chapters will feature major character developments
   - Triggering events that force character evolution

3. INTERNAL JOURNEY
   - Emotional and psychological changes
   - Belief systems that will be challenged
   - Personal revelations and insights

4. EXTERNAL CHALLENGES
   - Obstacles that force character growth
   - Relationships that catalyze change
   - Situations that test character limits

5. THEMATIC CONNECTION
   - How each character's growth serves story themes
   - Personal journeys that mirror larger story messages
   - Character development that reinforces central conflicts

6. PACING GUIDELINES
   - Gradual vs. sudden character changes
   - Setbacks and regression moments
   - Final character growth payoffs

Make these arcs feel earned and realistic, with proper buildup and payoff."""
        
        messages = [
            SystemMessage(content=system_prompt),
            UserMessage(content=user_prompt)
        ]
        
        response = await self.call_mistral(messages, temperature=0.6)
        
        return {
            "character_arcs": response,
            "total_chapters": total_chapters,
            "arc_complexity": self.assess_arc_complexity(characters)
        }
    
    def format_character_basics(self, character: Dict[str, Any]) -> str:
        """Format character basic information for analysis"""
        
        basics = []
        
        # Required fields
        basics.append(f"Name: {character.get('name', 'Unnamed')}")
        basics.append(f"Archetype: {character.get('archetype', 'Not specified')}")
        basics.append(f"Backstory: {character.get('backstory_one_sentence', 'Not provided')}")
        
        # Optional fields that are filled
        optional_fields = [
            'internal_conflict', 'external_conflict', 'relationships_map', 'personal_symbol',
            'core_belief', 'emotional_triggers', 'coping_mechanism', 'biggest_regret'
        ]
        
        for field in optional_fields:
            value = character.get(field, "")
            if value and value.strip():
                basics.append(f"{field.replace('_', ' ').title()}: {value}")
        
        return "\n".join(basics)
    
    def format_other_characters(self, current_character: Dict[str, Any], all_characters: List[Dict[str, Any]]) -> str:
        """Format other characters for relationship context"""
        
        other_chars = []
        current_name = current_character.get('name', '')
        
        for char in all_characters:
            if char.get('name', '') != current_name:
                char_info = f"- {char.get('name', 'Unnamed')} ({char.get('archetype', 'Unknown archetype')})"
                if char.get('backstory_one_sentence'):
                    char_info += f": {char.get('backstory_one_sentence')}"
                other_chars.append(char_info)
        
        return "\n".join(other_chars) if other_chars else "No other characters defined"
    
    def format_characters_for_relationships(self, characters: List[Dict[str, Any]]) -> str:
        """Format all characters for relationship analysis"""
        
        char_summaries = []
        
        for char in characters:
            summary = f"- {char.get('name', 'Unnamed')} ({char.get('archetype', 'Unknown')})"
            if char.get('backstory_one_sentence'):
                summary += f"\n  Background: {char.get('backstory_one_sentence')}"
            if char.get('internal_conflict'):
                summary += f"\n  Internal Conflict: {char.get('internal_conflict')}"
            char_summaries.append(summary)
        
        return "\n\n".join(char_summaries)
    
    def format_characters_for_arcs(self, characters: List[Dict[str, Any]]) -> str:
        """Format characters for arc development"""
        
        char_arcs = []
        
        for char in characters:
            arc_info = f"- {char.get('name', 'Unnamed')} ({char.get('archetype', 'Unknown')})"
            arc_info += f"\n  Current State: {char.get('backstory_one_sentence', 'Not defined')}"
            
            if char.get('internal_conflict'):
                arc_info += f"\n  Internal Challenge: {char.get('internal_conflict')}"
            if char.get('arc_in_one_word'):
                arc_info += f"\n  Arc Type: {char.get('arc_in_one_word')}"
            
            char_arcs.append(arc_info)
        
        return "\n\n".join(char_arcs)
    
    def assess_character_completeness(self, characters: List[Dict[str, Any]]) -> float:
        """Assess how complete the character development is"""
        
        if not characters:
            return 0.0
        
        total_score = 0
        required_fields = ['name', 'archetype', 'backstory_one_sentence']
        
        for char in characters:
            char_score = 0
            
            # Check required fields
            for field in required_fields:
                if char.get(field) and char.get(field).strip():
                    char_score += 1
            
            # Check if character has developed profile
            if char.get('developed_profile'):
                char_score += 2
            
            total_score += char_score / 5  # Max score of 5 per character
        
        return total_score / len(characters)
    
    def assess_arc_complexity(self, characters: List[Dict[str, Any]]) -> str:
        """Assess the complexity of character arcs"""
        
        if len(characters) <= 1:
            return "simple"
        elif len(characters) <= 3:
            return "moderate"
        else:
            return "complex"