from typing import Dict, Any, List, Tuple
from mistralai.models.chat_completion import ChatMessage
from .base_agent import BaseAgent
import logging
import re

logger = logging.getLogger(__name__)

class SequentialCheckerAgent(BaseAgent):
    """Sequential Checker Agent - Validates story consistency and auto-fixes issues"""
    
    def __init__(self):
        super().__init__("Sequential Checker Agent")
        self.validation_protocols = [
            "continuity_consistency",
            "character_arc_motivation", 
            "pacing_structure",
            "worldbuilding_lore",
            "prose_technical"
        ]
        
    async def process(self, story_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Validate and auto-fix story chapters sequentially"""
        
        await self.update_status("working", 0, "Initializing sequential validation")
        
        # Get generated chapters
        chapters = context.get("story_generation_result", {}).get("chapters", []) if context else []
        
        if not chapters:
            await self.update_status("error", 0, "No chapters provided for validation")
            return {"error": "No chapters to validate"}
        
        await self.update_status("working", 10, f"Validating {len(chapters)} chapters")
        
        # Validate each chapter sequentially
        validated_chapters = []
        validation_reports = []
        
        for i, chapter in enumerate(chapters):
            progress = 10 + (i / len(chapters)) * 80
            chapter_num = chapter.get("chapter_number", i + 1)
            
            await self.update_status("working", progress, f"Validating Chapter {chapter_num}")
            
            # Validate chapter against all protocols
            validation_result = await self.validate_chapter(
                chapter, 
                story_data, 
                validated_chapters,  # Previously validated chapters
                context
            )
            
            # Auto-fix if issues found
            if validation_result.get("issues_found", 0) > 0:
                await self.update_status("working", progress, f"Auto-fixing Chapter {chapter_num}")
                fixed_chapter = await self.auto_fix_chapter(chapter, validation_result, story_data, context)
                validated_chapters.append(fixed_chapter)
            else:
                validated_chapters.append(chapter)
            
            validation_reports.append(validation_result)
        
        await self.update_status("working", 90, "Creating final validation report")
        
        # Create comprehensive validation report
        final_report = await self.create_final_validation_report(validated_chapters, validation_reports, story_data)
        
        await self.update_status("completed", 100, "Sequential validation complete")
        
        return {
            "validated_chapters": validated_chapters,
            "validation_reports": validation_reports,
            "final_report": final_report,
            "total_issues_found": sum(r.get("issues_found", 0) for r in validation_reports),
            "total_fixes_applied": sum(r.get("fixes_applied", 0) for r in validation_reports),
            "validation_score": final_report.get("overall_score", 8.0)
        }
    
    async def validate_chapter(self, 
                              chapter: Dict[str, Any], 
                              story_data: Dict[str, Any],
                              previous_chapters: List[Dict[str, Any]],
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a single chapter using all protocols"""
        
        chapter_number = chapter.get("chapter_number", 1)
        validation_results = {}
        total_issues = 0
        
        # Run each validation protocol
        for protocol in self.validation_protocols:
            result = await self.run_validation_protocol(
                protocol, chapter, story_data, previous_chapters, context
            )
            validation_results[protocol] = result
            total_issues += result.get("issues", 0)
        
        return {
            "chapter_number": chapter_number,
            "protocol_results": validation_results,
            "issues_found": total_issues,
            "validation_timestamp": "2025-01-27",
            "needs_fixing": total_issues > 0
        }
    
    async def run_validation_protocol(self, 
                                    protocol: str,
                                    chapter: Dict[str, Any],
                                    story_data: Dict[str, Any],
                                    previous_chapters: List[Dict[str, Any]],
                                    context: Dict[str, Any]) -> Dict[str, Any]:
        """Run a specific validation protocol"""
        
        if protocol == "continuity_consistency":
            return await self.validate_continuity_consistency(chapter, story_data, previous_chapters, context)
        elif protocol == "character_arc_motivation":
            return await self.validate_character_arc_motivation(chapter, story_data, previous_chapters, context)
        elif protocol == "pacing_structure":
            return await self.validate_pacing_structure(chapter, story_data, previous_chapters, context)
        elif protocol == "worldbuilding_lore":
            return await self.validate_worldbuilding_lore(chapter, story_data, previous_chapters, context)
        elif protocol == "prose_technical":
            return await self.validate_prose_technical(chapter, story_data, previous_chapters, context)
        else:
            return {"issues": 0, "details": "Unknown protocol"}
    
    async def validate_continuity_consistency(self, 
                                            chapter: Dict[str, Any],
                                            story_data: Dict[str, Any],
                                            previous_chapters: List[Dict[str, Any]],
                                            context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate continuity and consistency (The 'No Holes' Check)"""
        
        system_prompt = """You are a continuity checker for story validation. Your task is to identify ANY continuity or consistency issues in this chapter.

Check for:
1. TIMELINE INTEGRITY
   - Does time passage make sense?
   - Are events in logical sequence?
   - Any contradictions with previous chapters?

2. CHARACTER KNOWLEDGE & MEMORY
   - Do characters only know what they should know?
   - Any forgotten important information?
   - Secrets maintained consistently?

3. OBJECT & LOCATION PERMANENCE
   - Are objects where they were left?
   - Physical descriptions consistent?
   - Character injuries/changes tracked?

Report ALL issues found, even minor ones. Be thorough and specific."""
        
        # Prepare context for validation
        chapter_content = chapter.get("content", "")
        chapter_number = chapter.get("chapter_number", 1)
        
        # Previous chapters summary
        prev_summary = self.create_previous_chapters_summary(previous_chapters)
        story_context = self.format_story_context(story_data)
        
        user_prompt = f"""Validate Chapter {chapter_number} for continuity and consistency:

STORY CONTEXT:
{story_context}

PREVIOUS CHAPTERS SUMMARY:
{prev_summary}

CURRENT CHAPTER CONTENT:
{chapter_content}

Identify ALL continuity and consistency issues. For each issue, provide:
1. Issue type (timeline, character knowledge, object permanence, etc.)
2. Specific problem description
3. Location in chapter where it occurs
4. Severity (minor, moderate, major)
5. Suggested fix

Be thorough and specific in your analysis."""
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt)
        ]
        
        response = await self.call_mistral(messages, temperature=0.2)
        
        # Parse response to count issues
        issues_count = self.count_issues_in_response(response)
        
        return {
            "issues": issues_count,
            "details": response,
            "severity": "high" if issues_count > 3 else "moderate" if issues_count > 0 else "low"
        }
    
    async def validate_character_arc_motivation(self, 
                                              chapter: Dict[str, Any],
                                              story_data: Dict[str, Any],
                                              previous_chapters: List[Dict[str, Any]],
                                              context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate character arc and motivation consistency"""
        
        system_prompt = """You are validating character development and motivation consistency. Check for:

1. CORE MOTIVATION
   - Do character actions align with established motivations?
   - Any unexplained changes in character behavior?
   - Clear reasons for actions against motivation?

2. CHARACTER DEVELOPMENT
   - Does emotional state follow logically from previous events?
   - Is development gradual and earned?
   - No sudden personality shifts?

3. CHARACTER VOICE
   - Dialogue consistent with established personality?
   - Speech patterns maintained?
   - Character-specific mannerisms present?

Identify any character believability issues."""
        
        chapter_content = chapter.get("content", "")
        chapter_number = chapter.get("chapter_number", 1)
        
        # Get character context
        character_context = context.get("character_result", {}) if context else {}
        characters_info = self.format_character_context(character_context)
        
        prev_summary = self.create_previous_chapters_summary(previous_chapters)
        
        user_prompt = f"""Validate Chapter {chapter_number} for character consistency:

CHARACTER PROFILES:
{characters_info}

PREVIOUS CHAPTERS:
{prev_summary}

CURRENT CHAPTER:
{chapter_content}

Identify character consistency issues including:
1. Motivation conflicts
2. Unearned character changes
3. Voice inconsistencies
4. Behavioral contradictions

Provide specific examples and suggested fixes."""
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt)
        ]
        
        response = await self.call_mistral(messages, temperature=0.2)
        issues_count = self.count_issues_in_response(response)
        
        return {
            "issues": issues_count,
            "details": response,
            "severity": "high" if issues_count > 2 else "moderate" if issues_count > 0 else "low"
        }
    
    async def validate_pacing_structure(self, 
                                      chapter: Dict[str, Any],
                                      story_data: Dict[str, Any],
                                      previous_chapters: List[Dict[str, Any]],
                                      context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate pacing and structural elements"""
        
        system_prompt = """You are validating story pacing and structure. Check for:

1. PLOT ADVANCEMENT
   - Does chapter move the story forward meaningfully?
   - Answers old questions while raising new ones?
   - Essential to the overall story?

2. TENSION AND PACING
   - Pacing matches content (fast for action, slower for reflection)?
   - Effective chapter ending?
   - Good balance of scene and sequel?

3. ENGAGEMENT FACTORS
   - Maintains reader interest throughout?
   - Proper story beats and tension management?
   - Satisfying chapter progression?

Identify pacing and engagement issues."""
        
        chapter_content = chapter.get("content", "")
        chapter_number = chapter.get("chapter_number", 1)
        total_chapters = story_data.get("total_chapters", 10)
        
        user_prompt = f"""Validate Chapter {chapter_number} of {total_chapters} for pacing and structure:

CHAPTER CONTENT:
{chapter_content}

CHAPTER POSITION: {chapter_number}/{total_chapters}

Analyze:
1. Plot advancement effectiveness
2. Pacing appropriateness  
3. Tension management
4. Chapter ending strength
5. Reader engagement level

Identify specific pacing or structural issues."""
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt)
        ]
        
        response = await self.call_mistral(messages, temperature=0.3)
        issues_count = self.count_issues_in_response(response)
        
        return {
            "issues": issues_count,
            "details": response,
            "severity": "moderate" if issues_count > 1 else "low"
        }
    
    async def validate_worldbuilding_lore(self, 
                                        chapter: Dict[str, Any],
                                        story_data: Dict[str, Any],
                                        previous_chapters: List[Dict[str, Any]],
                                        context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate worldbuilding and lore consistency"""
        
        system_prompt = """You are validating worldbuilding consistency. Check for:

1. CONSISTENCY OF RULES
   - World rules followed consistently?
   - Magic/tech systems working as established?
   - Any unexplained rule breaks?

2. ORGANIC EXPOSITION
   - World information revealed naturally?
   - No exposition dumps?
   - Information integrated smoothly?

3. WORLD DETAILS
   - Physical descriptions consistent?
   - Cultural elements properly maintained?
   - Environmental storytelling effective?

Identify worldbuilding inconsistencies."""
        
        chapter_content = chapter.get("content", "")
        chapter_number = chapter.get("chapter_number", 1)
        
        # Get world context
        world_context = context.get("worldbuilding_result", {}) if context else {}
        world_info = self.format_world_context(world_context)
        
        user_prompt = f"""Validate Chapter {chapter_number} for worldbuilding consistency:

ESTABLISHED WORLD:
{world_info}

CHAPTER CONTENT:
{chapter_content}

Check for:
1. World rule violations
2. Inconsistent descriptions
3. Exposition quality
4. Cultural accuracy
5. Environmental consistency

Report any worldbuilding issues found."""
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt)
        ]
        
        response = await self.call_mistral(messages, temperature=0.2)
        issues_count = self.count_issues_in_response(response)
        
        return {
            "issues": issues_count,
            "details": response,
            "severity": "high" if issues_count > 2 else "low"
        }
    
    async def validate_prose_technical(self, 
                                     chapter: Dict[str, Any],
                                     story_data: Dict[str, Any],
                                     previous_chapters: List[Dict[str, Any]],
                                     context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate prose quality and technical writing"""
        
        system_prompt = """You are validating prose quality and technical writing. Check for:

1. REPETITIVE LANGUAGE
   - Overused words, phrases, or sentence structures?
   - Repetitive character actions (nodding, shrugging, sighing)?
   - Varied vocabulary and sentence flow?

2. CLARITY AND FLOW
   - Confusing or awkward sentences?
   - Smooth reading experience?
   - Clear scene transitions?

3. SHOW DON'T TELL
   - Showing through action, dialogue, sensory details?
   - Avoiding excessive exposition?
   - Engaging narrative techniques?

Identify prose and technical issues."""
        
        chapter_content = chapter.get("content", "")
        word_count = chapter.get("word_count", 0)
        target_words = story_data.get("min_words_per_chapter", 900)
        
        user_prompt = f"""Validate prose quality for this chapter:

CHAPTER CONTENT ({word_count} words, target: {target_words}):
{chapter_content}

Analyze:
1. Repetitive language patterns
2. Sentence clarity and flow
3. Show vs. tell balance
4. Dialogue quality
5. Overall readability

Identify specific prose issues and suggest improvements."""
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt)
        ]
        
        response = await self.call_mistral(messages, temperature=0.3)
        issues_count = self.count_issues_in_response(response)
        
        # Check word count
        if word_count < target_words:
            issues_count += 1
        
        return {
            "issues": issues_count,
            "details": response,
            "severity": "moderate" if issues_count > 2 else "low",
            "word_count_met": word_count >= target_words
        }
    
    async def auto_fix_chapter(self, 
                              chapter: Dict[str, Any],
                              validation_result: Dict[str, Any],
                              story_data: Dict[str, Any],
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """Auto-fix issues found in chapter validation"""
        
        system_prompt = """You are an expert story editor tasked with fixing the identified issues in this chapter. Your goal is to:

1. Resolve all identified continuity and consistency issues
2. Maintain the chapter's original intent and style
3. Keep the story engaging and well-paced
4. Preserve character voices and development
5. Ensure world consistency
6. Improve prose quality where needed

Make targeted fixes that address specific issues without over-editing. Maintain the author's voice while improving quality."""
        
        chapter_content = chapter.get("content", "")
        chapter_number = chapter.get("chapter_number", 1)
        
        # Compile all validation issues
        all_issues = []
        for protocol, result in validation_result.get("protocol_results", {}).items():
            if result.get("issues", 0) > 0:
                all_issues.append(f"{protocol.replace('_', ' ').title()}: {result.get('details', '')}")
        
        issues_summary = "\n\n".join(all_issues)
        
        user_prompt = f"""Fix Chapter {chapter_number} based on these validation issues:

IDENTIFIED ISSUES:
{issues_summary}

ORIGINAL CHAPTER CONTENT:
{chapter_content}

Rewrite the chapter to fix all identified issues while:
1. Maintaining the original story intent
2. Preserving character voices and style
3. Keeping the engaging narrative flow
4. Addressing all continuity issues
5. Improving prose where needed

Provide the complete revised chapter content."""
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt)
        ]
        
        try:
            fixed_content = await self.call_mistral(messages, temperature=0.6, max_tokens=4000)
            
            # Create fixed chapter
            fixed_chapter = chapter.copy()
            fixed_chapter["content"] = fixed_content
            fixed_chapter["word_count"] = len(fixed_content.split())
            fixed_chapter["validation_status"] = "fixed"
            fixed_chapter["fixes_applied"] = validation_result.get("issues_found", 0)
            fixed_chapter["revision_count"] = chapter.get("revision_count", 0) + 1
            
            return fixed_chapter
            
        except Exception as e:
            logger.error(f"Auto-fix failed for Chapter {chapter_number}: {str(e)}")
            # Return original chapter with error note
            chapter_copy = chapter.copy()
            chapter_copy["validation_status"] = "fix_failed"
            chapter_copy["fix_error"] = str(e)
            return chapter_copy
    
    async def create_final_validation_report(self, 
                                           chapters: List[Dict[str, Any]],
                                           validation_reports: List[Dict[str, Any]],
                                           story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive final validation report"""
        
        total_issues = sum(r.get("issues_found", 0) for r in validation_reports)
        total_fixes = sum(r.get("fixes_applied", 0) for r in validation_reports)
        
        # Calculate overall score
        total_chapters = len(chapters)
        issue_penalty = min(total_issues * 0.5, 3.0)  # Max 3 point penalty
        overall_score = max(10.0 - issue_penalty, 6.0)  # Minimum score of 6.0
        
        # Analyze validation by protocol
        protocol_analysis = {}
        for protocol in self.validation_protocols:
            protocol_issues = sum(
                r.get("protocol_results", {}).get(protocol, {}).get("issues", 0) 
                for r in validation_reports
            )
            protocol_analysis[protocol] = {
                "total_issues": protocol_issues,
                "average_per_chapter": protocol_issues / total_chapters if total_chapters > 0 else 0
            }
        
        return {
            "overall_score": overall_score,
            "total_chapters_validated": total_chapters,
            "total_issues_found": total_issues,
            "total_fixes_applied": total_fixes,
            "fix_success_rate": (total_fixes / total_issues) if total_issues > 0 else 1.0,
            "protocol_analysis": protocol_analysis,
            "chapters_needing_fixes": sum(1 for r in validation_reports if r.get("issues_found", 0) > 0),
            "validation_summary": f"Validated {total_chapters} chapters, found {total_issues} issues, applied {total_fixes} fixes",
            "quality_assessment": self.assess_story_quality(overall_score),
            "recommendations": self.generate_recommendations(protocol_analysis, overall_score)
        }
    
    def count_issues_in_response(self, response: str) -> int:
        """Count the number of issues identified in a validation response"""
        
        # Simple heuristic - count common issue indicators
        issue_indicators = [
            "issue", "problem", "inconsistency", "contradiction", "error",
            "confusing", "unclear", "missing", "incorrect", "inconsistent"
        ]
        
        response_lower = response.lower()
        issue_count = 0
        
        for indicator in issue_indicators:
            issue_count += response_lower.count(indicator)
        
        # Look for numbered lists which often indicate issues
        numbered_issues = len(re.findall(r'\d+\.', response))
        if numbered_issues > issue_count:
            issue_count = numbered_issues
        
        return min(issue_count, 10)  # Cap at 10 to avoid over-counting
    
    def create_previous_chapters_summary(self, previous_chapters: List[Dict[str, Any]]) -> str:
        """Create summary of previous chapters for validation context"""
        
        if not previous_chapters:
            return "No previous chapters"
        
        summaries = []
        for chapter in previous_chapters[-3:]:  # Last 3 chapters
            ch_num = chapter.get("chapter_number", "Unknown")
            ch_title = chapter.get("title", "Untitled")
            ch_content = chapter.get("content", "")
            summary = ch_content[:300] + "..." if len(ch_content) > 300 else ch_content
            summaries.append(f"Chapter {ch_num} - {ch_title}:\n{summary}")
        
        return "\n\n".join(summaries)
    
    def format_character_context(self, character_context: Dict[str, Any]) -> str:
        """Format character context for validation"""
        
        if not character_context or not character_context.get("developed_characters"):
            return "No character profiles available"
        
        char_summaries = []
        for char in character_context["developed_characters"][:3]:
            name = char.get("name", "Unknown")
            archetype = char.get("archetype", "Unknown")
            backstory = char.get("backstory_one_sentence", "")
            char_summaries.append(f"{name} ({archetype}): {backstory}")
        
        return "\n".join(char_summaries)
    
    def format_world_context(self, world_context: Dict[str, Any]) -> str:
        """Format world context for validation"""
        
        if not world_context or not world_context.get("world_bible"):
            return "No world context available"
        
        world_content = world_context["world_bible"].get("world_bible_content", "")
        return world_content[:1000] + "..." if len(world_content) > 1000 else world_content
    
    def assess_story_quality(self, overall_score: float) -> str:
        """Assess overall story quality based on validation score"""
        
        if overall_score >= 9.0:
            return "excellent"
        elif overall_score >= 8.0:
            return "very_good"
        elif overall_score >= 7.0:
            return "good" 
        elif overall_score >= 6.0:
            return "acceptable"
        else:
            return "needs_improvement"
    
    def generate_recommendations(self, protocol_analysis: Dict[str, Any], overall_score: float) -> List[str]:
        """Generate recommendations based on validation results"""
        
        recommendations = []
        
        # Check each protocol for issues
        for protocol, analysis in protocol_analysis.items():
            if analysis.get("total_issues", 0) > 2:
                protocol_name = protocol.replace("_", " ").title()
                recommendations.append(f"Focus on improving {protocol_name} consistency")
        
        # Overall recommendations
        if overall_score < 7.0:
            recommendations.append("Consider additional revision pass for overall quality")
        
        if overall_score >= 8.5:
            recommendations.append("Story shows strong consistency and quality")
        
        return recommendations if recommendations else ["Story meets quality standards"]