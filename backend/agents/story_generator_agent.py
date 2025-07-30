from typing import Dict, Any, List
from mistralai.models.chat_completion import ChatMessage
from .base_agent import BaseAgent
import logging
import asyncio

logger = logging.getLogger(__name__)

class StoryGeneratorAgent(BaseAgent):
    """Story Generator Agent - Creates the actual story content chapter by chapter"""
    
    def __init__(self):
        super().__init__("Story Generator Agent")
        
    async def process(self, story_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate complete story content based on all prepared elements"""
        
        await self.update_status("working", 0, "Initializing story generation")
        
        # Get context from other agents
        world_context = context.get("worldbuilding_result", {}) if context else {}
        character_context = context.get("character_result", {}) if context else {}
        plot_context = context.get("plot_result", {}) if context else {}
        
        # Extract chapter outlines
        chapter_outlines = plot_context.get("chapter_outlines", [])
        total_chapters = len(chapter_outlines)
        
        if not chapter_outlines:
            # Create basic outlines if none provided
            total_chapters = story_data.get("total_chapters", 10)
            chapter_outlines = await self.create_basic_outlines(story_data, total_chapters)
        
        await self.update_status("working", 10, f"Generating {total_chapters} chapters")
        
        # Generate each chapter
        generated_chapters = []
        for i, outline in enumerate(chapter_outlines):
            progress = 10 + (i / total_chapters) * 80
            chapter_num = outline.get("chapter_number", i + 1)
            
            await self.update_status("working", progress, f"Writing Chapter {chapter_num}")
            
            chapter = await self.generate_chapter(
                outline, 
                story_data, 
                world_context, 
                character_context, 
                plot_context,
                generated_chapters  # Previous chapters for context
            )
            
            generated_chapters.append(chapter)
        
        await self.update_status("working", 90, "Finalizing story content")
        
        # Create story summary and metadata
        story_metadata = await self.create_story_metadata(generated_chapters, story_data)
        
        await self.update_status("completed", 100, f"Generated {len(generated_chapters)} chapters")
        
        return {
            "chapters": generated_chapters,
            "story_metadata": story_metadata,
            "total_chapters": len(generated_chapters),
            "total_words": sum(ch.get("word_count", 0) for ch in generated_chapters),
            "generation_completed": True
        }
    
    async def generate_chapter(self, 
                              outline: Dict[str, Any], 
                              story_data: Dict[str, Any],
                              world_context: Dict[str, Any],
                              character_context: Dict[str, Any],
                              plot_context: Dict[str, Any],
                              previous_chapters: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a single chapter based on its outline and context"""
        
        chapter_number = outline.get("chapter_number", 1)
        target_words = story_data.get("min_words_per_chapter", 900)
        
        system_prompt = f"""You are an expert story writer generating Chapter {chapter_number} of a {story_data.get('total_chapters', 10)}-chapter story. 

Your task is to write engaging, high-quality prose that:
1. Follows the provided outline and story context
2. Maintains consistency with previous chapters
3. Develops characters naturally and believably
4. Advances the plot in meaningful ways
5. Incorporates world details seamlessly
6. Maintains the story's tone and genre
7. Reaches the target word count of at least {target_words} words
8. Ends with appropriate tension/resolution for the chapter's purpose

Write in vivid, engaging prose with:
- Rich sensory details
- Natural dialogue
- Clear scene progression
- Emotional depth
- Proper pacing

Focus on showing rather than telling, and make every scene serve the story."""
        
        # Prepare comprehensive context
        story_context = self.format_comprehensive_context(
            story_data, world_context, character_context, plot_context, outline, previous_chapters
        )
        
        user_prompt = f"""Write Chapter {chapter_number} based on this context:

{story_context}

CHAPTER OUTLINE:
{outline.get('outline_content', f'Chapter {chapter_number}: Continue the story')}

REQUIREMENTS:
- Minimum {target_words} words
- Rich, engaging prose
- Consistent with story context
- Proper chapter structure with natural flow
- Ends appropriately for the chapter's purpose

Write the complete chapter content now."""
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt)
        ]
        
        # Generate chapter content
        chapter_content = await self.call_mistral(messages, temperature=0.8, max_tokens=4000)
        
        # Create chapter title if not provided
        chapter_title = await self.generate_chapter_title(chapter_content, chapter_number, story_data)
        
        # Count words
        word_count = len(chapter_content.split())
        
        return {
            "chapter_number": chapter_number,
            "title": chapter_title,
            "content": chapter_content,
            "word_count": word_count,
            "outline_used": outline.get("outline_content", ""),
            "generation_timestamp": "2025-01-27",
            "meets_word_target": word_count >= target_words
        }
    
    async def generate_chapter_title(self, chapter_content: str, chapter_number: int, story_data: Dict[str, Any]) -> str:
        """Generate an appropriate title for the chapter"""
        
        system_prompt = """You are creating a chapter title that captures the essence of the chapter's content. The title should be:
1. Evocative and intriguing
2. Relevant to the chapter's main events or themes
3. Consistent with the story's tone and genre
4. Not too long (2-8 words typically)
5. Engaging enough to make readers want to read the chapter

Generate a single, compelling chapter title."""
        
        # Use first 500 words of chapter for title generation
        content_preview = chapter_content[:500] + "..." if len(chapter_content) > 500 else chapter_content
        story_context = self.format_story_context(story_data)
        
        user_prompt = f"""Generate a title for Chapter {chapter_number} based on this content:

STORY CONTEXT:
{story_context}

CHAPTER CONTENT PREVIEW:
{content_preview}

Generate a compelling chapter title (2-8 words) that captures the essence of this chapter."""
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt)
        ]
        
        try:
            title = await self.call_mistral(messages, temperature=0.6, max_tokens=50)
            # Clean up the title
            title = title.strip().strip('"').strip("'")
            return title if title else f"Chapter {chapter_number}"
        except:
            return f"Chapter {chapter_number}"
    
    async def create_basic_outlines(self, story_data: Dict[str, Any], total_chapters: int) -> List[Dict[str, Any]]:
        """Create basic chapter outlines if none were provided by Plot Agent"""
        
        system_prompt = """You are creating basic chapter outlines for a story. Each outline should provide enough guidance for story generation while maintaining proper pacing and development.

Create simple but effective outlines that:
1. Establish clear story progression
2. Develop characters naturally
3. Build tension appropriately
4. Include satisfying story beats
5. Lead to a proper conclusion

Keep outlines concise but informative."""
        
        story_context = self.format_story_context(story_data)
        
        user_prompt = f"""Create {total_chapters} basic chapter outlines for this story:

{story_context}

Create {total_chapters} outlines in this format:

Chapter 1: [Title/Purpose]
- [Key events/scenes]
- [Character focus]
- [Plot development]

Continue for all {total_chapters} chapters, ensuring proper story progression and pacing."""
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt)
        ]
        
        response = await self.call_mistral(messages, temperature=0.6)
        
        # Parse into outline objects
        outlines = []
        for i in range(total_chapters):
            outlines.append({
                "chapter_number": i + 1,
                "outline_content": f"Chapter {i + 1}: Continue story development",
                "word_target": story_data.get("min_words_per_chapter", 900)
            })
        
        return outlines
    
    async def create_story_metadata(self, chapters: List[Dict[str, Any]], story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create metadata about the generated story"""
        
        total_words = sum(ch.get("word_count", 0) for ch in chapters)
        avg_words_per_chapter = total_words / len(chapters) if chapters else 0
        
        # Count chapters that meet word target
        target_words = story_data.get("min_words_per_chapter", 900)
        chapters_meeting_target = sum(1 for ch in chapters if ch.get("word_count", 0) >= target_words)
        
        return {
            "total_chapters": len(chapters),
            "total_words": total_words,
            "average_words_per_chapter": int(avg_words_per_chapter),
            "chapters_meeting_target": chapters_meeting_target,
            "target_achievement_rate": chapters_meeting_target / len(chapters) if chapters else 0,
            "story_length_category": self.categorize_story_length(total_words),
            "generation_summary": f"Generated {len(chapters)} chapters with {total_words:,} total words"
        }
    
    def format_comprehensive_context(self, 
                                   story_data: Dict[str, Any],
                                   world_context: Dict[str, Any],
                                   character_context: Dict[str, Any],
                                   plot_context: Dict[str, Any],
                                   outline: Dict[str, Any],
                                   previous_chapters: List[Dict[str, Any]]) -> str:
        """Format all available context for chapter generation"""
        
        context_parts = []
        
        # Basic story context
        basic_context = self.format_story_context(story_data)
        context_parts.append(f"STORY FOUNDATION:\n{basic_context}")
        
        # World context
        if world_context and world_context.get("world_bible"):
            world_bible = world_context["world_bible"].get("world_bible_content", "")
            if world_bible:
                context_parts.append(f"WORLD CONTEXT:\n{world_bible[:1000]}...")
        
        # Character context
        if character_context and character_context.get("developed_characters"):
            char_info = []
            for char in character_context["developed_characters"][:3]:  # Top 3 characters
                name = char.get("name", "Unknown")
                profile = char.get("developed_profile", "")
                if profile:
                    char_info.append(f"{name}: {profile[:300]}...")
            
            if char_info:
                context_parts.append(f"CHARACTER PROFILES:\n" + "\n\n".join(char_info))
        
        # Plot context
        if plot_context:
            if plot_context.get("story_structure"):
                structure = plot_context["story_structure"].get("structure_framework", "")
                if structure:
                    context_parts.append(f"STORY STRUCTURE:\n{structure[:500]}...")
            
            if plot_context.get("plot_enhancements"):
                enhancements = plot_context["plot_enhancements"].get("enhancement_implementation", "")
                if enhancements:
                    context_parts.append(f"PLOT ENHANCEMENTS:\n{enhancements[:500]}...")
        
        # Previous chapters summary
        if previous_chapters:
            recent_chapters = previous_chapters[-2:]  # Last 2 chapters
            chapter_summaries = []
            for ch in recent_chapters:
                ch_num = ch.get("chapter_number", "Unknown")
                ch_title = ch.get("title", "Untitled")
                ch_content = ch.get("content", "")
                summary = ch_content[:200] + "..." if len(ch_content) > 200 else ch_content
                chapter_summaries.append(f"Chapter {ch_num} - {ch_title}:\n{summary}")
            
            context_parts.append(f"PREVIOUS CHAPTERS:\n" + "\n\n".join(chapter_summaries))
        
        return "\n\n" + "="*50 + "\n\n".join(context_parts)
    
    def categorize_story_length(self, total_words: int) -> str:
        """Categorize story by length"""
        
        if total_words < 5000:
            return "short_story"
        elif total_words < 15000:
            return "long_short_story"
        elif total_words < 40000:
            return "novella"
        elif total_words < 80000:
            return "novel"
        else:
            return "long_novel"