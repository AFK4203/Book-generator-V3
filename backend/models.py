from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

# Base Models
class BaseModelWithId(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Character Model
class Character(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    # Character Basics (REQUIRED)
    name: str
    archetype: str
    backstory_one_sentence: str
    
    # Optional character fields
    internal_conflict: Optional[str] = ""
    external_conflict: Optional[str] = ""
    relationships_map: Optional[str] = ""
    personal_symbol: Optional[str] = ""
    core_belief: Optional[str] = ""
    emotional_triggers: Optional[str] = ""
    comfort_zones: Optional[str] = ""
    coping_mechanism: Optional[str] = ""
    desire_vs_need: Optional[str] = ""
    biggest_regret: Optional[str] = ""
    emotional_armor: Optional[str] = ""
    defining_childhood_moment: Optional[str] = ""
    first_major_betrayal: Optional[str] = ""
    past_love_or_loss: Optional[str] = ""
    family_role: Optional[str] = ""
    education_street_smarts: Optional[str] = ""
    criminal_record: Optional[str] = ""
    line_never_cross: Optional[str] = ""
    worst_thing_done: Optional[str] = ""
    justification_wrongdoing: Optional[str] = ""
    villain_origin: Optional[str] = ""
    self_destruct_trait: Optional[str] = ""
    public_vs_private: Optional[str] = ""
    role_in_group: Optional[str] = ""
    love_language: Optional[str] = ""
    treatment_of_weak: Optional[str] = ""
    jealousy_triggers: Optional[str] = ""
    loyalty_level: Optional[str] = ""
    weird_habit: Optional[str] = ""
    physical_tics: Optional[str] = ""
    obsessions: Optional[str] = ""
    voice_pattern: Optional[str] = ""
    what_makes_laugh: Optional[str] = ""
    what_makes_cry: Optional[str] = ""
    symbol_motif: Optional[str] = ""
    arc_in_one_word: Optional[str] = ""
    theme_connection: Optional[str] = ""
    peak_collapse: Optional[str] = ""
    ending_feeling: Optional[str] = ""
    core_wound: Optional[str] = ""
    fear: Optional[str] = ""
    mask_vs_true_self: Optional[str] = ""
    arc_type: Optional[str] = ""
    never_admit_out_loud: Optional[str] = ""
    belief_about_self: Optional[str] = ""
    belief_about_world: Optional[str] = ""
    primary_coping: Optional[str] = ""
    emotional_blind_spot: Optional[str] = ""
    trigger_points: Optional[str] = ""
    emotional_defense: Optional[str] = ""
    moral_dilemma: Optional[str] = ""
    unconscious_fear: Optional[str] = ""
    source_of_shame: Optional[str] = ""
    recurring_negative_thought: Optional[str] = ""
    greatest_insecurity: Optional[str] = ""
    self_sabotage: Optional[str] = ""
    pretend_to_be: Optional[str] = ""
    cant_forgive_themselves: Optional[str] = ""
    personal_hell: Optional[str] = ""
    value_most_deep_down: Optional[str] = ""
    breaks_spiritually: Optional[str] = ""
    core_motivation_underneath: Optional[str] = ""
    seek_from_others: Optional[str] = ""
    how_handle_loss: Optional[str] = ""
    respond_to_authority: Optional[str] = ""
    pain_hide_most: Optional[str] = ""
    attachment_type: Optional[str] = ""
    fight_flight_response: Optional[str] = ""
    deal_with_boredom: Optional[str] = ""
    react_to_praise: Optional[str] = ""
    die_to_protect: Optional[str] = ""
    fear_becoming: Optional[str] = ""
    mental_health_tags: List[str] = []
    trauma_response_style: Optional[str] = ""
    memory_triggers: Optional[str] = ""
    inner_monologue_style: Optional[str] = ""
    chapter_range: Optional[str] = ""
    plot_role: Optional[str] = ""
    secrets: Optional[str] = ""

# Plot Element Models
class PlotElement(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    category: str

class PlotTwist(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    twist: str
    role: str  # world, character, goal, loyalties, assumptions

# Story Data Model
class StoryData(BaseModelWithId):
    # Core Story Idea (REQUIRED)
    central_theme: str
    main_premise: str
    negative_prompt: str
    
    # Worldbuilding Context (OPTIONAL)
    world_summary: Optional[str] = ""
    genres: Optional[str] = ""  # Free text input
    time_period_setting: Optional[str] = ""
    cultural_influences: Optional[str] = ""
    
    # Core World Structure (OPTIONAL)
    geography: Optional[str] = ""
    climate: Optional[str] = ""
    time_period: Optional[str] = ""
    technology_level: Optional[str] = ""
    magic_rules: Optional[str] = ""
    physics_rules: Optional[str] = ""
    
    # Society & Culture (OPTIONAL)
    governance: Optional[str] = ""
    laws_justice: Optional[str] = ""
    economic_system: Optional[str] = ""
    cultural_norms: Optional[str] = ""
    religions: Optional[str] = ""
    festivals: Optional[str] = ""
    social_hierarchy: Optional[str] = ""
    languages: Optional[str] = ""
    
    # Conflict & Power Dynamics (OPTIONAL)
    current_conflict: Optional[str] = ""
    factions: Optional[str] = ""
    hidden_powers: Optional[str] = ""
    law_enforcement: Optional[str] = ""
    weapons_combat: Optional[str] = ""
    
    # Cultural Mindset & Psychology (OPTIONAL)
    view_of_death: Optional[str] = ""
    view_of_time: Optional[str] = ""
    honor_vs_survival: Optional[str] = ""
    individual_vs_collective: Optional[str] = ""
    emotion_expression: Optional[str] = ""
    
    # Modern/Tech World Specifics (OPTIONAL)
    media_propaganda: Optional[str] = ""
    surveillance_level: Optional[str] = ""
    internet_access: Optional[str] = ""
    popular_culture: Optional[str] = ""
    
    # World Themes & Emotional Tone (OPTIONAL)
    emotional_vibe: Optional[str] = ""
    symbolic_motifs: Optional[str] = ""
    historical_trauma: Optional[str] = ""
    power_over_truth: Optional[str] = ""
    
    # Physical Detail Ideas (OPTIONAL)
    architecture_style: Optional[str] = ""
    fashion_trends: Optional[str] = ""
    transportation: Optional[str] = ""
    food_culture: Optional[str] = ""
    street_sounds: Optional[str] = ""
    
    # Story Utility-Specific (OPTIONAL)
    world_challenges: Optional[str] = ""
    world_rewards: Optional[str] = ""
    death_triggers: Optional[str] = ""
    world_changes: Optional[str] = ""
    
    # Characters
    characters: List[Character] = []
    
    # Plot Utility Enhancements (ALL OPTIONAL)
    foreshadowing_seeds: List[PlotElement] = []
    timebombs: List[PlotElement] = []
    red_herrings: List[PlotElement] = []
    chekovs_guns: List[PlotElement] = []
    multi_arc_threads: List[PlotElement] = []
    power_balance_shifts: List[PlotElement] = []
    dramatic_irony_layers: List[PlotElement] = []
    reversal_markers: List[PlotElement] = []
    thematic_echo_scenes: List[PlotElement] = []
    crossroad_moments: List[PlotElement] = []
    plot_flashbacks: List[PlotElement] = []
    interwoven_timelines: List[PlotElement] = []
    symbolic_motif_tracking: List[PlotElement] = []
    location_stakes: List[PlotElement] = []
    npc_catalysts: List[PlotElement] = []
    parallel_plot_mirror: List[PlotElement] = []
    plot_twists_by_role: List[PlotTwist] = []
    
    # Generation settings
    total_chapters: int = 10
    min_words_per_chapter: int = 900

# Agent Status Model
class AgentStatus(BaseModel):
    agent_name: str
    status: str  # ready, working, completed, error
    progress: float = 0.0  # 0.0 to 1.0
    message: Optional[str] = ""
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

# Chapter Model
class Chapter(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    chapter_number: int
    title: str
    content: str
    word_count: int
    character_focus: List[str] = []  # Character names that are focus of this chapter
    plot_elements_used: List[str] = []  # Plot elements referenced
    validation_status: str = "pending"  # pending, validated, needs_revision
    validation_feedback: Optional[str] = ""
    revision_count: int = 0

# Story Generation Session Model
class StoryGenerationSession(BaseModelWithId):
    story_data: StoryData
    agent_statuses: List[AgentStatus] = []
    chapters: List[Chapter] = []
    current_phase: str = "initialized"  # initialized, worldbuilding, characters, plotting, generating, validating, formatting, completed
    progress: float = 0.0
    estimated_completion_time: Optional[datetime] = None
    error_message: Optional[str] = ""
    generated_document_path: Optional[str] = ""

# API Request/Response Models
class GenerateStoryRequest(BaseModel):
    story_data: StoryData

class GenerateStoryResponse(BaseModel):
    session_id: str
    message: str
    estimated_time_minutes: int

class StoryProgressResponse(BaseModel):
    session_id: str
    current_phase: str
    progress: float
    agent_statuses: List[AgentStatus]
    estimated_completion_time: Optional[datetime]
    error_message: Optional[str] = ""

class ChapterPreviewResponse(BaseModel):
    session_id: str
    chapters: List[Chapter]
    total_word_count: int

class DownloadStoryResponse(BaseModel):
    session_id: str
    download_url: str
    file_name: str
    total_chapters: int
    total_words: int