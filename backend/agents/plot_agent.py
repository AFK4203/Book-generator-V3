from typing import Dict, Any, List
from mistralai.models.chat_completion import ChatMessage
from .base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)

class PlotAgent(BaseAgent):
    """Plot Agent - Structures the story and implements plot utility enhancements"""
    
    def __init__(self):
        super().__init__("Plot Agent")
        
    async def process(self, story_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process plot structure and create comprehensive story framework"""
        
        await self.update_status("working", 0, "Analyzing plot requirements")
        
        # Extract plot elements
        plot_elements = self.extract_plot_elements(story_data)
        
        await self.update_status("working", 20, "Creating story structure framework")
        
        # Create story structure
        story_structure = await self.create_story_structure(plot_elements, story_data)
        
        await self.update_status("working", 40, "Implementing plot utility enhancements")
        
        # Implement plot enhancements
        plot_enhancements = await self.implement_plot_enhancements(plot_elements, story_data)
        
        await self.update_status("working", 60, "Generating chapter outlines")
        
        # Generate chapter outlines
        chapter_outlines = await self.generate_chapter_outlines(story_structure, plot_enhancements, story_data)
        
        await self.update_status("working", 80, "Creating plot consistency framework")
        
        # Create consistency framework
        consistency_framework = await self.create_plot_consistency_framework(chapter_outlines, story_data)
        
        await self.update_status("completed", 100, "Plot structure complete")
        
        return {
            "plot_elements": plot_elements,
            "story_structure": story_structure,
            "plot_enhancements": plot_enhancements,
            "chapter_outlines": chapter_outlines,
            "consistency_framework": consistency_framework,
            "total_chapters": len(chapter_outlines),
            "plot_complexity": self.assess_plot_complexity(plot_elements)
        }
    
    def extract_plot_elements(self, story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract all plot-related elements from story data"""
        
        plot_elements = {
            "basic_structure": {
                "central_theme": story_data.get("central_theme", ""),
                "main_premise": story_data.get("main_premise", ""),
                "negative_prompt": story_data.get("negative_prompt", "")
            },
            "enhancement_tools": {
                "foreshadowing_seeds": story_data.get("foreshadowing_seeds", []),
                "timebombs": story_data.get("timebombs", []),
                "red_herrings": story_data.get("red_herrings", []),
                "chekovs_guns": story_data.get("chekovs_guns", []),
                "multi_arc_threads": story_data.get("multi_arc_threads", []),
                "power_balance_shifts": story_data.get("power_balance_shifts", []),
                "dramatic_irony_layers": story_data.get("dramatic_irony_layers", []),
                "reversal_markers": story_data.get("reversal_markers", []),
                "thematic_echo_scenes": story_data.get("thematic_echo_scenes", []),
                "crossroad_moments": story_data.get("crossroad_moments", []),
                "plot_flashbacks": story_data.get("plot_flashbacks", []),
                "interwoven_timelines": story_data.get("interwoven_timelines", []),
                "symbolic_motif_tracking": story_data.get("symbolic_motif_tracking", []),
                "location_stakes": story_data.get("location_stakes", []),
                "npc_catalysts": story_data.get("npc_catalysts", []),
                "parallel_plot_mirror": story_data.get("parallel_plot_mirror", []),
                "plot_twists_by_role": story_data.get("plot_twists_by_role", [])
            },
            "characters": story_data.get("characters", []),
            "world_context": {
                "current_conflict": story_data.get("current_conflict", ""),
                "factions": story_data.get("factions", ""),
                "world_challenges": story_data.get("world_challenges", ""),
                "world_changes": story_data.get("world_changes", "")
            },
            "generation_settings": {
                "total_chapters": story_data.get("total_chapters", 10),
                "min_words_per_chapter": story_data.get("min_words_per_chapter", 900)
            }
        }
        
        return plot_elements
    
    async def create_story_structure(self, plot_elements: Dict[str, Any], story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive story structure"""
        
        system_prompt = """You are an expert plot structure agent. Your task is to create a comprehensive story structure that incorporates all the provided plot elements into a cohesive, engaging narrative framework.

Focus on:
1. Classic story structure (setup, confrontation, resolution)
2. Character arc integration
3. Pacing and tension management
4. Thematic development
5. Plot utility enhancement integration
6. Satisfying narrative progression

Create a detailed structure that will guide chapter-by-chapter story development."""
        
        story_context = self.format_story_context(story_data)
        plot_context = self.format_plot_elements(plot_elements)
        total_chapters = plot_elements["generation_settings"]["total_chapters"]
        
        user_prompt = f"""Create a comprehensive story structure for this {total_chapters}-chapter story:

STORY FOUNDATION:
{story_context}

PLOT ELEMENTS:
{plot_context}

Create a detailed story structure including:

1. OVERALL STRUCTURE
   - Three-act breakdown with chapter ranges
   - Major story beats and turning points
   - Climax and resolution positioning

2. TENSION AND PACING
   - How tension builds throughout the story
   - Pacing guidelines for different chapters
   - Relief points and escalation moments

3. CHARACTER ARC INTEGRATION
   - How character development aligns with plot
   - Character growth moments and challenges
   - Relationship development throughout the story

4. THEMATIC DEVELOPMENT
   - How themes unfold chapter by chapter
   - Symbolic moments and thematic reinforcement
   - Theme resolution in the climax and ending

5. PLOT ENHANCEMENT INTEGRATION
   - Where to place foreshadowing and setup elements
   - Timing of reveals and plot twists
   - Chekhov's guns placement and payoff

6. CONFLICT PROGRESSION
   - Internal and external conflict development
   - How conflicts interact and compound
   - Resolution strategies for different conflict types

Make this structure actionable for generating {total_chapters} chapters with proper pacing and development."""
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt)
        ]
        
        response = await self.call_mistral(messages, temperature=0.5, max_tokens=3500)
        
        return {
            "structure_framework": response,
            "total_chapters": total_chapters,
            "structure_type": "three_act" if total_chapters >= 6 else "simple_arc"
        }
    
    async def implement_plot_enhancements(self, plot_elements: Dict[str, Any], story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Implement all plot utility enhancements"""
        
        system_prompt = """You are implementing advanced plot utility enhancements to create sophisticated storytelling. Your task is to take the provided plot enhancement elements and create a detailed implementation plan.

Focus on:
1. Strategic placement of each enhancement type
2. How enhancements work together synergistically
3. Timing and pacing of reveals and payoffs
4. Integration with character development and themes
5. Creating layers of meaning and engagement

Create a comprehensive implementation guide for sophisticated plot development."""
        
        enhancements = plot_elements.get("enhancement_tools", {})
        story_context = self.format_story_context(story_data)
        total_chapters = plot_elements["generation_settings"]["total_chapters"]
        
        # Format enhancements for analysis
        enhancement_context = self.format_enhancements_for_implementation(enhancements)
        
        user_prompt = f"""Implement these plot enhancements for the {total_chapters}-chapter story:

STORY CONTEXT:
{story_context}

PLOT ENHANCEMENTS:
{enhancement_context}

Create a detailed implementation plan:

1. FORESHADOWING STRATEGY
   - Where to place early hints and setup
   - How to make foreshadowing subtle but noticeable on re-read
   - Connection to major reveals and plot twists

2. TENSION MECHANISMS
   - Timebomb placement for maximum impact
   - How to build and release tension throughout
   - Multiple tension layers for complex engagement

3. MISDIRECTION TACTICS
   - Red herring placement and execution
   - How to make false clues believable
   - Maintaining fairness while misleading readers

4. PAYOFF PLANNING
   - Chekhov's gun setup and execution
   - Ensuring all planted elements have satisfying payoffs
   - Timing reveals for maximum impact

5. CHARACTER INTEGRATION
   - How plot enhancements serve character development
   - Character-specific plot enhancement opportunities
   - Relationship dynamics enhanced by plot tools

6. THEMATIC REINFORCEMENT
   - How plot enhancements support central themes
   - Symbolic and metaphorical layer integration
   - Thematic echo and parallel development

7. CHAPTER-SPECIFIC ASSIGNMENTS
   - Which enhancements appear in which chapters
   - How enhancements build across the story
   - Climax and resolution enhancement integration

Make this practical and actionable for story generation."""
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt)
        ]
        
        response = await self.call_mistral(messages, temperature=0.6)
        
        return {
            "enhancement_implementation": response,
            "enhancement_count": self.count_enhancements(enhancements),
            "complexity_level": self.assess_enhancement_complexity(enhancements)
        }
    
    async def generate_chapter_outlines(self, story_structure: Dict[str, Any], plot_enhancements: Dict[str, Any], story_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate detailed outlines for each chapter"""
        
        system_prompt = """You are creating detailed chapter outlines for a story. Each outline should provide clear guidance for story generation while maintaining narrative flow and engagement.

For each chapter, include:
1. Chapter purpose and role in overall story
2. Key scenes and story beats
3. Character focus and development
4. Plot advancement and revelations
5. Thematic elements and symbolism
6. Specific plot enhancements to include
7. Emotional tone and pacing
8. Connection to previous and next chapters

Create outlines that will result in engaging, well-paced chapters."""
        
        story_context = self.format_story_context(story_data)
        structure_content = story_structure.get("structure_framework", "")
        enhancement_content = plot_enhancements.get("enhancement_implementation", "")
        total_chapters = story_data.get("total_chapters", 10)
        min_words = story_data.get("min_words_per_chapter", 900)
        
        user_prompt = f"""Create detailed outlines for all {total_chapters} chapters:

STORY CONTEXT:
{story_context}

STORY STRUCTURE:
{structure_content[:1500]}...

PLOT ENHANCEMENTS:
{enhancement_content[:1500]}...

TARGET: {min_words} words minimum per chapter

Create {total_chapters} detailed chapter outlines in this format:

CHAPTER [NUMBER]: [TITLE]
Purpose: [Chapter's role in the story]
Key Scenes: [2-3 major scenes/beats]
Character Focus: [Which characters are featured]
Plot Development: [What moves the story forward]
Enhancements: [Which plot tools are used]
Emotional Arc: [Chapter's emotional journey]
Connects: [How it links to other chapters]
Word Target: {min_words} words minimum

Make each outline detailed enough to guide story generation but flexible enough to allow creative development."""
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt)
        ]
        
        response = await self.call_mistral(messages, temperature=0.6, max_tokens=4000)
        
        # Parse the response into individual chapter outlines
        outlines = self.parse_chapter_outlines(response, total_chapters)
        
        return outlines
    
    async def create_plot_consistency_framework(self, chapter_outlines: List[Dict[str, Any]], story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create framework for maintaining plot consistency"""
        
        system_prompt = """You are creating a plot consistency framework to ensure story coherence throughout generation and validation.

Focus on:
1. Timeline and chronology tracking
2. Character knowledge and memory consistency
3. Plot thread continuity
4. Cause and effect relationships
5. Thematic consistency
6. World rule adherence

Create a comprehensive framework for maintaining story integrity."""
        
        story_context = self.format_story_context(story_data)
        outlines_summary = self.format_outlines_for_consistency(chapter_outlines)
        
        user_prompt = f"""Create a plot consistency framework for this story:

STORY CONTEXT:
{story_context}

CHAPTER OUTLINES SUMMARY:
{outlines_summary}

Create a comprehensive consistency framework:

1. TIMELINE TRACKING
   - Key events and their sequence
   - Time passage between chapters
   - Important dates and deadlines

2. CHARACTER KNOWLEDGE MATRIX
   - What each character knows at each point
   - Information reveals and discoveries
   - Secret knowledge and when it's revealed

3. PLOT THREAD CONTINUITY
   - Major plot threads and their progression
   - Subplot development and resolution
   - Thread interaction and convergence

4. CAUSE AND EFFECT CHAINS
   - How actions lead to consequences
   - Character decisions and their impacts
   - Environmental factors affecting plot

5. CONSISTENCY CHECKPOINTS
   - Key points to verify in each chapter
   - Common consistency pitfalls to avoid
   - Validation questions for each chapter

6. RESOLUTION TRACKING
   - Which conflicts get resolved when
   - How plot threads tie together
   - Satisfaction of reader expectations

Make this framework practical for story validation and consistency checking."""
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt)
        ]
        
        response = await self.call_mistral(messages, temperature=0.4)
        
        return {
            "consistency_framework": response,
            "total_chapters": len(chapter_outlines),
            "tracking_complexity": "high" if len(chapter_outlines) > 15 else "moderate"
        }
    
    def format_plot_elements(self, plot_elements: Dict[str, Any]) -> str:
        """Format plot elements for analysis"""
        
        formatted_sections = []
        
        # Basic structure
        basic = plot_elements.get("basic_structure", {})
        if any(basic.values()):
            formatted_sections.append("BASIC STRUCTURE:")
            for key, value in basic.items():
                if value:
                    formatted_sections.append(f"  {key.replace('_', ' ').title()}: {value}")
        
        # Enhancement tools
        enhancements = plot_elements.get("enhancement_tools", {})
        enhancement_count = sum(1 for tools in enhancements.values() if tools)
        if enhancement_count > 0:
            formatted_sections.append(f"\nPLOT ENHANCEMENTS: {enhancement_count} types defined")
        
        # Characters
        characters = plot_elements.get("characters", [])
        if characters:
            formatted_sections.append(f"\nCHARACTERS: {len(characters)} characters")
        
        # World context
        world = plot_elements.get("world_context", {})
        world_count = sum(1 for value in world.values() if value)
        if world_count > 0:
            formatted_sections.append(f"\nWORLD CONTEXT: {world_count} elements defined")
        
        return "\n".join(formatted_sections)
    
    def format_enhancements_for_implementation(self, enhancements: Dict[str, Any]) -> str:
        """Format enhancements for implementation analysis"""
        
        formatted = []
        
        for category, items in enhancements.items():
            if items:
                category_name = category.replace('_', ' ').title()
                if isinstance(items, list) and len(items) > 0:
                    formatted.append(f"{category_name}: {len(items)} items")
                    for item in items[:2]:  # Show first 2 items as examples
                        if isinstance(item, dict):
                            content = item.get('content') or item.get('seed') or item.get('twist') or 'Defined'
                            formatted.append(f"  - {content[:100]}...")
        
        return "\n".join(formatted) if formatted else "No plot enhancements defined"
    
    def parse_chapter_outlines(self, response: str, total_chapters: int) -> List[Dict[str, Any]]:
        """Parse the Mistral response into structured chapter outlines"""
        
        outlines = []
        
        # Simple parsing - in a production system, this would be more sophisticated
        lines = response.split('\n')
        current_chapter = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('CHAPTER'):
                if current_chapter:
                    outlines.append({
                        "chapter_number": current_chapter,
                        "outline_content": "\n".join(current_content),
                        "word_target": 900
                    })
                
                # Extract chapter number
                try:
                    current_chapter = int(line.split(':')[0].replace('CHAPTER', '').strip())
                    current_content = [line]
                except:
                    current_chapter = len(outlines) + 1
                    current_content = [line]
            elif current_chapter:
                current_content.append(line)
        
        # Add the last chapter
        if current_chapter:
            outlines.append({
                "chapter_number": current_chapter,
                "outline_content": "\n".join(current_content),
                "word_target": 900
            })
        
        # Ensure we have the right number of chapters
        while len(outlines) < total_chapters:
            outlines.append({
                "chapter_number": len(outlines) + 1,
                "outline_content": f"Chapter {len(outlines) + 1}: Continue story development",
                "word_target": 900
            })
        
        return outlines[:total_chapters]
    
    def format_outlines_for_consistency(self, outlines: List[Dict[str, Any]]) -> str:
        """Format chapter outlines for consistency analysis"""
        
        summary = []
        
        for outline in outlines[:5]:  # Show first 5 chapters as example
            chapter_num = outline.get("chapter_number", "Unknown")
            content = outline.get("outline_content", "")[:200]
            summary.append(f"Chapter {chapter_num}: {content}...")
        
        if len(outlines) > 5:
            summary.append(f"... and {len(outlines) - 5} more chapters")
        
        return "\n\n".join(summary)
    
    def count_enhancements(self, enhancements: Dict[str, Any]) -> int:
        """Count total number of plot enhancements"""
        
        total = 0
        for items in enhancements.values():
            if isinstance(items, list):
                total += len(items)
        return total
    
    def assess_enhancement_complexity(self, enhancements: Dict[str, Any]) -> str:
        """Assess complexity of plot enhancements"""
        
        count = self.count_enhancements(enhancements)
        
        if count == 0:
            return "minimal"
        elif count <= 5:
            return "moderate"
        elif count <= 15:
            return "high"
        else:
            return "very_high"
    
    def assess_plot_complexity(self, plot_elements: Dict[str, Any]) -> str:
        """Assess overall plot complexity"""
        
        factors = 0
        
        # Check characters
        characters = plot_elements.get("characters", [])
        if len(characters) > 3:
            factors += 1
        
        # Check enhancements
        enhancement_count = self.count_enhancements(plot_elements.get("enhancement_tools", {}))
        if enhancement_count > 10:
            factors += 1
        
        # Check world elements
        world_context = plot_elements.get("world_context", {})
        if sum(1 for v in world_context.values() if v) > 2:
            factors += 1
        
        # Check chapter count
        if plot_elements["generation_settings"]["total_chapters"] > 20:
            factors += 1
        
        if factors >= 3:
            return "very_high"
        elif factors >= 2:
            return "high"
        elif factors >= 1:
            return "moderate"
        else:
            return "simple"