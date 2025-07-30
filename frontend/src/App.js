import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Enhanced Collapsible Section Component
const CollapsibleSection = ({ title, children, isOpen, onToggle, className = "", required = false, optional = false }) => (
  <div className={`border border-gray-600 rounded-xl mb-6 overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 ${className}`}>
    <button
      onClick={onToggle}
      className="w-full px-6 py-4 text-left font-semibold bg-gradient-to-r from-gray-700 to-gray-800 hover:from-gray-600 hover:to-gray-700 flex justify-between items-center transition-all duration-200 group"
    >
      <div className="flex items-center space-x-3">
        <span className="text-lg">{title}</span>
        {required && (
          <span className="px-2 py-1 text-xs bg-red-500 text-white rounded-full font-medium">
            REQUIRED
          </span>
        )}
        {optional && (
          <span className="px-2 py-1 text-xs bg-blue-500 text-white rounded-full font-medium">
            OPTIONAL
          </span>
        )}
      </div>
      <div className={`text-2xl transform transition-transform duration-200 ${isOpen ? 'rotate-45' : ''} group-hover:scale-110`}>
        {isOpen ? "×" : "+"}
      </div>
    </button>
    {isOpen && (
      <div className="p-6 bg-gradient-to-br from-gray-800 to-gray-900 border-t border-gray-600">
        {children}
      </div>
    )}
  </div>
);

// Enhanced Input Field Component
const InputField = ({ label, value, onChange, placeholder, type = "text", className = "", required = false }) => (
  <div className={`mb-6 ${className}`}>
    <label className="block text-sm font-semibold text-gray-200 mb-3 flex items-center space-x-2">
      <span>{label}</span>
      {required && <span className="text-red-400 text-lg">*</span>}
    </label>
    {type === "textarea" ? (
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full px-4 py-3 bg-gray-700 border-2 border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 resize-none hover:border-gray-500"
        rows={4}
      />
    ) : (
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full px-4 py-3 bg-gray-700 border-2 border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 hover:border-gray-500"
      />
    )}
  </div>
);

// Enhanced Select Field Component
const SelectField = ({ label, value, onChange, options, placeholder, className = "", required = false }) => (
  <div className={`mb-6 ${className}`}>
    <label className="block text-sm font-semibold text-gray-200 mb-3 flex items-center space-x-2">
      <span>{label}</span>
      {required && <span className="text-red-400 text-lg">*</span>}
    </label>
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full px-4 py-3 bg-gray-700 border-2 border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 hover:border-gray-500"
    >
      <option value="">{placeholder}</option>
      {options.map((option, index) => (
        <option key={index} value={option}>{option}</option>
      ))}
    </select>
  </div>
);

// Enhanced Slider Component
const SliderField = ({ label, value, onChange, min, max, className = "" }) => (
  <div className={`mb-8 ${className}`}>
    <label className="block text-sm font-semibold text-gray-200 mb-4">
      {label}: <span className="text-blue-400 font-bold text-lg">{value.toLocaleString()}</span>
    </label>
    <div className="relative">
      <input
        type="range"
        min={min}
        max={max}
        value={value}
        onChange={(e) => onChange(parseInt(e.target.value))}
        className="w-full h-3 bg-gray-700 rounded-lg appearance-none cursor-pointer slider-enhanced"
      />
      <div className="flex justify-between text-xs text-gray-400 mt-2">
        <span>{min}</span>
        <span>{max.toLocaleString()}</span>
      </div>
    </div>
  </div>
);

// Enhanced Tab Component
const TabButton = ({ active, onClick, children, icon }) => (
  <button
    onClick={onClick}
    className={`flex items-center space-x-3 px-6 py-4 rounded-xl font-semibold transition-all duration-300 ${
      active 
        ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg transform scale-105' 
        : 'bg-gray-700 text-gray-300 hover:bg-gray-600 hover:text-white hover:scale-102'
    }`}
  >
    {icon && <span className="text-xl">{icon}</span>}
    <span>{children}</span>
  </button>
);

const StoryGeneratorApp = () => {
  // Main tab state
  const [activeTab, setActiveTab] = useState('worldbuilding');
  
  // Collapsible sections state
  const [collapsedSections, setCollapsedSections] = useState({
    // KDP Metadata
    kdpMetadata: false,
    
    // Worldbuilding sections
    coreStoryIdea: true,
    worldStructure: false,
    societyCulture: false,
    conflictPower: false,
    culturalMindset: false,
    modernTech: false,
    worldThemes: false,
    physicalDetails: false,
    storyUtility: false,
    
    // Character sections
    characterBasics: true,
    psychologicalLayers: false,
    lifeImpact: false,
    darkCorners: false,
    socialDynamics: false,
    quirksHabits: false,
    narrativeDesign: false,
    mentalHealth: false,
    plotUtility: false,
    
    // Plot sections
    foreshadowing: false,
    timebombs: false,
    redHerrings: false,
    chekovsGuns: false,
    multiArc: false,
    powerBalance: false,
    dramaticIrony: false,
    reversals: false,
    thematicEcho: false,
    crossroads: false,
    flashbacks: false,
    timelines: false,
    symbolicMotif: false,
    locationStakes: false,
    npcCatalyst: false,
    parallelPlot: false,
    plotTwists: false
  });

  // Comprehensive story data state
  const [storyData, setStoryData] = useState({
    // Core Story Idea (REQUIRED)
    centralTheme: '',
    mainPremise: '',
    negativePrompt: '',
    
    // Worldbuilding Context (OPTIONAL)
    worldSummary: '',
    genres: '', // Changed from array to string
    timePeriodSetting: '',
    culturalInfluences: '',
    
    // Core World Structure (OPTIONAL)
    geography: '',
    climate: '',
    timePeriod: '',
    technologyLevel: '',
    magicRules: '',
    physicsRules: '',
    
    // Society & Culture (OPTIONAL)
    governance: '',
    lawsJustice: '',
    economicSystem: '',
    culturalNorms: '',
    religions: '',
    festivals: '',
    socialHierarchy: '',
    languages: '',
    
    // Conflict & Power Dynamics (OPTIONAL)
    currentConflict: '',
    factions: '',
    hiddenPowers: '',
    lawEnforcement: '',
    weaponsCombat: '',
    
    // Cultural Mindset & Psychology (OPTIONAL)
    viewOfDeath: '',
    viewOfTime: '',
    honorVsSurvival: '',
    individualVsCollective: '',
    emotionExpression: '',
    
    // Modern/Tech World Specifics (OPTIONAL)
    mediaPropaganda: '',
    surveillanceLevel: '',
    internetAccess: '',
    popularCulture: '',
    
    // World Themes & Emotional Tone (OPTIONAL)
    emotionalVibe: '',
    symbolicMotifs: '',
    historicalTrauma: '',
    powerOverTruth: '',
    
    // Physical Detail Ideas (OPTIONAL)
    architectureStyle: '',
    fashionTrends: '',
    transportation: '',
    foodCulture: '',
    streetSounds: '',
    
    // Story Utility-Specific (OPTIONAL)
    worldChallenges: '',
    worldRewards: '',
    deathTriggers: '',
    worldChanges: '',
    
    // Characters with expanded fields
    characters: [{
      id: 1,
      // Character Basics (REQUIRED)
      name: '',
      archetype: '',
      backstoryOneSentence: '',
      
      // All other character fields are OPTIONAL
      internalConflict: '',
      externalConflict: '',
      relationshipsMap: '',
      personalSymbol: '',
      coreBelief: '',
      emotionalTriggers: '',
      comfortZones: '',
      copingMechanism: '',
      desireVsNeed: '',
      biggestRegret: '',
      emotionalArmor: '',
      definingChildhoodMoment: '',
      firstMajorBetrayal: '',
      pastLoveOrLoss: '',
      familyRole: '',
      educationStreetSmarts: '',
      criminalRecord: '',
      lineNeverCross: '',
      worstThingDone: '',
      justificationWrongdoing: '',
      villainOrigin: '',
      selfDestructTrait: '',
      publicVsPrivate: '',
      roleInGroup: '',
      loveLanguage: '',
      treatmentOfWeak: '',
      jealousyTriggers: '',
      loyaltyLevel: '',
      weirdHabit: '',
      physicalTics: '',
      obsessions: '',
      voicePattern: '',
      whatMakesLaugh: '',
      whatMakesCry: '',
      symbolMotif: '',
      arcInOneWord: '',
      themeConnection: '',
      peakCollapse: '',
      endingFeeling: '',
      coreWound: '',
      fear: '',
      maskVsTrueSelf: '',
      arcType: '',
      neverAdmitOutLoud: '',
      beliefAboutSelf: '',
      beliefAboutWorld: '',
      primaryCoping: '',
      emotionalBlindSpot: '',
      triggerPoints: '',
      emotionalDefense: '',
      moralDilemma: '',
      unconsciousFear: '',
      sourceOfShame: '',
      recurringNegativeThought: '',
      greatestInsecurity: '',
      selfSabotage: '',
      pretendToBe: '',
      cantForgiveThemselves: '',
      personalHell: '',
      valueMostDeepDown: '',
      breaksSpiritually: '',
      coreMotivationUnderneath: '',
      seekFromOthers: '',
      howHandleLoss: '',
      respondToAuthority: '',
      painHideMost: '',
      attachmentType: '',
      fightFlightResponse: '',
      dealWithBoredom: '',
      reactToPraise: '',
      dieToProtect: '',
      fearBecoming: '',
      mentalHealthTags: [],
      traumaResponseStyle: '',
      memoryTriggers: '',
      innerMonologueStyle: '',
      chapterRange: '',
      plotRole: '',
      secrets: ''
    }],
    
    // Plot Utility Enhancements (ALL OPTIONAL)
    foreshadowingSeeds: [{ id: 1, seed: '' }],
    timebombs: [{ id: 1, bomb: '' }],
    redHerrings: [{ id: 1, herring: '' }],
    chekovsGuns: [{ id: 1, gun: '' }],
    multiArcThreads: [{ id: 1, thread: '' }],
    powerBalanceShifts: [{ id: 1, shift: '' }],
    dramaticIronyLayers: [{ id: 1, irony: '' }],
    reversalMarkers: [{ id: 1, reversal: '' }],
    thematicEchoScenes: [{ id: 1, echo: '' }],
    crossroadMoments: [{ id: 1, crossroad: '' }],
    plotFlashbacks: [{ id: 1, flashback: '' }],
    interwovenTimelines: [{ id: 1, timeline: '' }],
    symbolicMotifTracking: [{ id: 1, motif: '' }],
    locationStakes: [{ id: 1, location: '' }],
    npcCatalysts: [{ id: 1, catalyst: '' }],
    parallelPlotMirror: [{ id: 1, mirror: '' }],
    plotTwistsByRole: [{ id: 1, twist: '', role: 'world' }],
    
    // Generation settings
    totalChapters: 10,
    minWordsPerChapter: 900
  });

  // Options arrays
  const characterArchetypes = [
    'The Mentor', 'The Rival', 'The Wild Card', 'The Innocent', 'The Traitor',
    'The Hero', 'The Anti-Hero', 'The Villain', 'The Trickster', 'The Guardian',
    'The Herald', 'The Shapeshifter', 'The Shadow', 'The Ally', 'The Threshold Guardian'
  ];

  const arcTypes = [
    'Positive change', 'Negative fall', 'Flat arc', 'Redemption arc',
    'Corruption arc', 'Growth arc', 'Disillusionment arc', 'Testing arc'
  ];

  const attachmentTypes = [
    'Secure', 'Anxious', 'Avoidant', 'Fearful-avoidant', 'Disorganized'
  ];

  const mentalHealthOptions = [
    'PTSD', 'Dissociation', 'Perfectionism', 'Anxiety disorder', 'Depression',
    'Compulsive lying', 'OCD', 'Bipolar disorder', 'Narcissistic traits',
    'Borderline traits', 'ADHD', 'Autism spectrum', 'Eating disorder',
    'Substance abuse', 'Anger issues', 'Trust issues'
  ];

  const plotTwistRoles = ['World', 'Character', 'Goal', 'Loyalties', 'Assumptions'];

  // Toggle section collapse
  const toggleSection = (section) => {
    setCollapsedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  // Generic list management functions
  const addToList = (listName, newItem) => {
    setStoryData(prev => ({
      ...prev,
      [listName]: [...prev[listName], { ...newItem, id: Date.now() }]
    }));
  };

  const removeFromList = (listName, id) => {
    setStoryData(prev => ({
      ...prev,
      [listName]: prev[listName].filter(item => item.id !== id)
    }));
  };

  const updateListItem = (listName, id, field, value) => {
    setStoryData(prev => ({
      ...prev,
      [listName]: prev[listName].map(item =>
        item.id === id ? { ...item, [field]: value } : item
      )
    }));
  };

  // Character management
  const addCharacter = () => {
    const newCharacter = {
      id: Date.now(),
      name: '', archetype: '', backstoryOneSentence: '', internalConflict: '',
      externalConflict: '', relationshipsMap: '', personalSymbol: '', coreBelief: '',
      emotionalTriggers: '', comfortZones: '', copingMechanism: '', desireVsNeed: '',
      biggestRegret: '', emotionalArmor: '', definingChildhoodMoment: '',
      firstMajorBetrayal: '', pastLoveOrLoss: '', familyRole: '', educationStreetSmarts: '',
      criminalRecord: '', lineNeverCross: '', worstThingDone: '', justificationWrongdoing: '',
      villainOrigin: '', selfDestructTrait: '', publicVsPrivate: '', roleInGroup: '',
      loveLanguage: '', treatmentOfWeak: '', jealousyTriggers: '', loyaltyLevel: '',
      weirdHabit: '', physicalTics: '', obsessions: '', voicePattern: '', whatMakesLaugh: '',
      whatMakesCry: '', symbolMotif: '', arcInOneWord: '', themeConnection: '',
      peakCollapse: '', endingFeeling: '', coreWound: '', fear: '', maskVsTrueSelf: '',
      arcType: '', neverAdmitOutLoud: '', beliefAboutSelf: '', beliefAboutWorld: '',
      primaryCoping: '', emotionalBlindSpot: '', triggerPoints: '', emotionalDefense: '',
      moralDilemma: '', unconsciousFear: '', sourceOfShame: '', recurringNegativeThought: '',
      greatestInsecurity: '', selfSabotage: '', pretendToBe: '', cantForgiveThemselves: '',
      personalHell: '', valueMostDeepDown: '', breaksSpiritually: '', coreMotivationUnderneath: '',
      seekFromOthers: '', howHandleLoss: '', respondToAuthority: '', painHideMost: '',
      attachmentType: '', fightFlightResponse: '', dealWithBoredom: '', reactToPraise: '',
      dieToProtect: '', fearBecoming: '', mentalHealthTags: [], traumaResponseStyle: '',
      memoryTriggers: '', innerMonologueStyle: '', chapterRange: '', plotRole: '', secrets: ''
    };
    setStoryData(prev => ({
      ...prev,
      characters: [...prev.characters, newCharacter]
    }));
  };

  const removeCharacter = (id) => {
    if (storyData.characters.length > 1) {
      setStoryData(prev => ({
        ...prev,
        characters: prev.characters.filter(char => char.id !== id)
      }));
    }
  };

  const updateCharacter = (id, field, value) => {
    setStoryData(prev => ({
      ...prev,
      characters: prev.characters.map(char =>
        char.id === id ? { ...char, [field]: value } : char
      )
    }));
  };

  // Multi-Select Checkbox Component for mental health tags
  const MultiSelectField = ({ label, options, selectedValues, onChange, className = "" }) => (
    <div className={`mb-6 ${className}`}>
      <label className="block text-sm font-semibold text-gray-200 mb-3">{label}</label>
      <div className="grid grid-cols-2 gap-3 max-h-40 overflow-y-auto bg-gray-700 p-4 rounded-lg border-2 border-gray-600">
        {options.map((option, index) => (
          <label key={index} className="flex items-center space-x-3 text-sm cursor-pointer hover:bg-gray-600 p-2 rounded-md transition-colors">
            <input
              type="checkbox"
              checked={selectedValues.includes(option)}
              onChange={(e) => {
                if (e.target.checked) {
                  onChange([...selectedValues, option]);
                } else {
                  onChange(selectedValues.filter(v => v !== option));
                }
              }}
              className="w-4 h-4 text-blue-600 bg-gray-800 border-gray-600 rounded focus:ring-blue-500 focus:ring-2"
            />
            <span className="text-gray-300">{option}</span>
          </label>
        ))}
      </div>
    </div>
  );

  // Tab navigation
  const tabs = [
    { id: 'worldbuilding', label: 'Worldbuilding Context', icon: '🌍' },
    { id: 'characters', label: 'Character Expansion', icon: '👥' },
    { id: 'psychological', label: 'Psychological Layers', icon: '🧠' },
    { id: 'plot', label: 'Plot Utility Enhancements', icon: '📚' },
    { id: 'generation', label: 'Generation Dashboard', icon: '🚀' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-900 to-purple-900 shadow-2xl">
        <div className="container mx-auto px-6 py-6">
          <h1 className="text-4xl font-bold text-center bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            ✨ Advanced Story Generation Platform ✨
          </h1>
          <p className="text-center text-gray-300 mt-2 text-lg">
            Powered by Multi-Agent AI • Create Professional Stories with Intelligence
          </p>
        </div>
      </div>

      <div className="flex h-screen">
        {/* Left Sidebar */}
        <div className="w-1/3 bg-gradient-to-b from-gray-800 to-gray-900 border-r border-gray-700 overflow-y-auto shadow-2xl">
          {/* Tab Navigation */}
          <div className="p-6 border-b border-gray-700 bg-gradient-to-r from-gray-800 to-gray-700">
            <div className="grid grid-cols-1 gap-3">
              {tabs.map(tab => (
                <TabButton
                  key={tab.id}
                  active={activeTab === tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  icon={tab.icon}
                >
                  {tab.label}
                </TabButton>
              ))}
            </div>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {activeTab === 'worldbuilding' && (
              <div>
                {/* KDP Metadata Hub */}
                <CollapsibleSection
                  title="📋 KDP Metadata Hub"
                  isOpen={!collapsedSections.kdpMetadata}
                  onToggle={() => toggleSection('kdpMetadata')}
                  className="mb-8"
                  optional={true}
                >
                  <div className="text-center p-8 bg-gradient-to-r from-blue-900/20 to-purple-900/20 rounded-lg border border-blue-500/30">
                    <div className="text-6xl mb-4">📖</div>
                    <p className="text-gray-300 text-lg">KDP Publishing Settings</p>
                    <p className="text-gray-400 text-sm mt-2">
                      Amazon KDP metadata and publishing configuration will be available here
                    </p>
                  </div>
                </CollapsibleSection>

                {/* Core Story Idea */}
                <CollapsibleSection
                  title="💡 Core Story Idea"
                  isOpen={!collapsedSections.coreStoryIdea}
                  onToggle={() => toggleSection('coreStoryIdea')}
                  required={true}
                >
                  <InputField
                    label="Central Moral/Theme"
                    value={storyData.centralTheme}
                    onChange={(value) => setStoryData(prev => ({ ...prev, centralTheme: value }))}
                    placeholder="What is the central moral or theme of your story?"
                    type="textarea"
                    required={true}
                  />

                  <InputField
                    label="Main Premise / Logline"
                    value={storyData.mainPremise}
                    onChange={(value) => setStoryData(prev => ({ ...prev, mainPremise: value }))}
                    placeholder="Describe your story in one compelling sentence"
                    type="textarea"
                    required={true}
                  />

                  <div className="mb-6">
                    <label className="block text-sm font-semibold text-red-300 mb-3 flex items-center space-x-2">
                      <span>⚠️ Negative Prompt (Things to avoid)</span>
                    </label>
                    <textarea
                      value={storyData.negativePrompt}
                      onChange={(e) => setStoryData(prev => ({ ...prev, negativePrompt: e.target.value }))}
                      placeholder="e.g., Avoid cliches, no magic, no romance"
                      className="w-full px-4 py-3 bg-red-900/20 border-2 border-red-500/50 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-red-400 transition-all duration-200 resize-none"
                      rows={3}
                    />
                  </div>

                  <InputField
                    label="Story World Summary"
                    value={storyData.worldSummary}
                    onChange={(value) => setStoryData(prev => ({ ...prev, worldSummary: value }))}
                    placeholder="e.g., modern Tokyo, post-apocalyptic desert, cyberpunk mega-city"
                    type="textarea"
                  />

                  <InputField
                    label="Genre(s)"
                    value={storyData.genres}
                    onChange={(value) => setStoryData(prev => ({ ...prev, genres: value }))}
                    placeholder="e.g., Crime, Romance, Sci-fi, Thriller (or any custom genres you want)"
                  />

                  <InputField
                    label="Time Period / Setting"
                    value={storyData.timePeriodSetting}
                    onChange={(value) => setStoryData(prev => ({ ...prev, timePeriodSetting: value }))}
                    placeholder="Helps define technology, society, culture, tone"
                  />

                  <InputField
                    label="Cultural Influences"
                    value={storyData.culturalInfluences}
                    onChange={(value) => setStoryData(prev => ({ ...prev, culturalInfluences: value }))}
                    placeholder="e.g., Japanese, Slavic, urban Western, dystopian influences"
                  />
                </CollapsibleSection>

                {/* Core World Structure */}
                <CollapsibleSection
                  title="🏗️ Core World Structure"
                  isOpen={!collapsedSections.worldStructure}
                  onToggle={() => toggleSection('worldStructure')}
                  optional={true}
                >
                  <InputField
                    label="Geography & Environment"
                    value={storyData.geography}
                    onChange={(value) => setStoryData(prev => ({ ...prev, geography: value }))}
                    placeholder="Urban, rural, wasteland, floating cities, underwater, forests?"
                    type="textarea"
                  />

                  <InputField
                    label="Climate & Weather Patterns"
                    value={storyData.climate}
                    onChange={(value) => setStoryData(prev => ({ ...prev, climate: value }))}
                    placeholder="Hot, stormy, rain-soaked neon city, eternal winter?"
                    type="textarea"
                  />

                  <InputField
                    label="Time Period"
                    value={storyData.timePeriod}
                    onChange={(value) => setStoryData(prev => ({ ...prev, timePeriod: value }))}
                    placeholder="Historical, modern, near-future, dystopian, timeless myth?"
                  />

                  <InputField
                    label="Technology Level"
                    value={storyData.technologyLevel}
                    onChange={(value) => setStoryData(prev => ({ ...prev, technologyLevel: value }))}
                    placeholder="Smartphones, cybernetic limbs, or spears and smoke signals?"
                    type="textarea"
                  />

                  <InputField
                    label="Magic / Supernatural Rules"
                    value={storyData.magicRules}
                    onChange={(value) => setStoryData(prev => ({ ...prev, magicRules: value }))}
                    placeholder="Only if applicable — or specify 'No supernatural' to ground the tone"
                    type="textarea"
                  />

                  <InputField
                    label="Physics Rules (if broken)"
                    value={storyData.physicsRules}
                    onChange={(value) => setStoryData(prev => ({ ...prev, physicsRules: value }))}
                    placeholder="Any laws of nature that don't apply in this world?"
                    type="textarea"
                  />
                </CollapsibleSection>

                {/* Society & Culture */}
                <CollapsibleSection
                  title="🏛️ Society & Culture"
                  isOpen={!collapsedSections.societyCulture}
                  onToggle={() => toggleSection('societyCulture')}
                  optional={true}
                >
                  <InputField
                    label="Governance / Political Systems"
                    value={storyData.governance}
                    onChange={(value) => setStoryData(prev => ({ ...prev, governance: value }))}
                    placeholder="Dictators, councils, gangs, corporations, AI overlords?"
                    type="textarea"
                  />

                  <InputField
                    label="Laws & Justice System"
                    value={storyData.lawsJustice}
                    onChange={(value) => setStoryData(prev => ({ ...prev, lawsJustice: value }))}
                    placeholder="Fair? Corrupt? Brutal? Vigilante-run?"
                    type="textarea"
                  />

                  <InputField
                    label="Economic System"
                    value={storyData.economicSystem}
                    onChange={(value) => setStoryData(prev => ({ ...prev, economicSystem: value }))}
                    placeholder="Rich-poor divide? Barter system? Crypto? Syndicate-controlled black market?"
                    type="textarea"
                  />

                  <InputField
                    label="Cultural Norms & Taboos"
                    value={storyData.culturalNorms}
                    onChange={(value) => setStoryData(prev => ({ ...prev, culturalNorms: value }))}
                    placeholder="What's considered respectful? What gets you shunned?"
                    type="textarea"
                  />

                  <InputField
                    label="Major Religions / Belief Systems"
                    value={storyData.religions}
                    onChange={(value) => setStoryData(prev => ({ ...prev, religions: value }))}
                    placeholder="One god, many gods, no gods, ancestral spirits, tech cults?"
                    type="textarea"
                  />

                  <InputField
                    label="Cultural Festivals or Rituals"
                    value={storyData.festivals}
                    onChange={(value) => setStoryData(prev => ({ ...prev, festivals: value }))}
                    placeholder="Dia de los Muertos, blood moon hunts, corporate evaluation weeks"
                    type="textarea"
                  />

                  <InputField
                    label="Social Hierarchies / Castes"
                    value={storyData.socialHierarchy}
                    onChange={(value) => setStoryData(prev => ({ ...prev, socialHierarchy: value }))}
                    placeholder="Royalty? Slums? Classism? Are certain people 'lesser' by default?"
                    type="textarea"
                  />

                  <InputField
                    label="Languages & Dialects"
                    value={storyData.languages}
                    onChange={(value) => setStoryData(prev => ({ ...prev, languages: value }))}
                    placeholder="Do different regions or classes speak differently?"
                    type="textarea"
                  />
                </CollapsibleSection>

                {/* Conflict & Power Dynamics */}
                <CollapsibleSection
                  title="⚔️ Conflict & Power Dynamics"
                  isOpen={!collapsedSections.conflictPower}
                  onToggle={() => toggleSection('conflictPower')}
                  optional={true}
                >
                  <InputField
                    label="Current Major Conflict"
                    value={storyData.currentConflict}
                    onChange={(value) => setStoryData(prev => ({ ...prev, currentConflict: value }))}
                    placeholder="War? Rebellion? Cold war tension? Corporate wars? Ethnic cleansing?"
                    type="textarea"
                  />

                  <InputField
                    label="Faction Breakdown"
                    value={storyData.factions}
                    onChange={(value) => setStoryData(prev => ({ ...prev, factions: value }))}
                    placeholder="Names, symbols, ideologies of groups (political parties, cults, gangs, rebellion cells)"
                    type="textarea"
                  />

                  <InputField
                    label="Hidden Power Structures"
                    value={storyData.hiddenPowers}
                    onChange={(value) => setStoryData(prev => ({ ...prev, hiddenPowers: value }))}
                    placeholder="Who's really in charge behind the curtain? Corrupt priesthood? Secret families?"
                    type="textarea"
                  />

                  <InputField
                    label="Law Enforcement Style"
                    value={storyData.lawEnforcement}
                    onChange={(value) => setStoryData(prev => ({ ...prev, lawEnforcement: value }))}
                    placeholder="Peacekeepers, brutal cops, AI drones, mafia-led security?"
                    type="textarea"
                  />

                  <InputField
                    label="Weapons / Combat Culture"
                    value={storyData.weaponsCombat}
                    onChange={(value) => setStoryData(prev => ({ ...prev, weaponsCombat: value }))}
                    placeholder="Guns, blades, psychic powers, dirty street brawls?"
                    type="textarea"
                  />
                </CollapsibleSection>

                {/* Cultural Mindset & Psychology */}
                <CollapsibleSection
                  title="🧭 Cultural Mindset & Psychology"
                  isOpen={!collapsedSections.culturalMindset}
                  onToggle={() => toggleSection('culturalMindset')}
                  optional={true}
                >
                  <InputField
                    label="How Do People View Death?"
                    value={storyData.viewOfDeath}
                    onChange={(value) => setStoryData(prev => ({ ...prev, viewOfDeath: value }))}
                    placeholder="Honored? Feared? Celebrated? Ignored?"
                    type="textarea"
                  />

                  <InputField
                    label="View of Time"
                    value={storyData.viewOfTime}
                    onChange={(value) => setStoryData(prev => ({ ...prev, viewOfTime: value }))}
                    placeholder="Linear like the West? Circular like Eastern beliefs? Time loops? Timeless void?"
                    type="textarea"
                  />

                  <InputField
                    label="Honor vs. Survival Society?"
                    value={storyData.honorVsSurvival}
                    onChange={(value) => setStoryData(prev => ({ ...prev, honorVsSurvival: value }))}
                    placeholder="Do people value reputation or just staying alive?"
                    type="textarea"
                  />

                  <InputField
                    label="Individual vs. Collective Thinking?"
                    value={storyData.individualVsCollective}
                    onChange={(value) => setStoryData(prev => ({ ...prev, individualVsCollective: value }))}
                    placeholder="Are people expected to sacrifice for others, or look out for #1?"
                    type="textarea"
                  />

                  <InputField
                    label="How is Emotion Expressed?"
                    value={storyData.emotionExpression}
                    onChange={(value) => setStoryData(prev => ({ ...prev, emotionExpression: value }))}
                    placeholder="Stoicism? Loud mourning? Repression? Constant drama?"
                    type="textarea"
                  />
                </CollapsibleSection>

                {/* Modern/Tech World Specifics */}
                <CollapsibleSection
                  title="💻 Modern/Tech World Specifics"
                  isOpen={!collapsedSections.modernTech}
                  onToggle={() => toggleSection('modernTech')}
                  optional={true}
                >
                  <InputField
                    label="Media & Propaganda"
                    value={storyData.mediaPropaganda}
                    onChange={(value) => setStoryData(prev => ({ ...prev, mediaPropaganda: value }))}
                    placeholder="How are people influenced? News? Memes? Mind implants?"
                    type="textarea"
                  />

                  <InputField
                    label="Surveillance Level"
                    value={storyData.surveillanceLevel}
                    onChange={(value) => setStoryData(prev => ({ ...prev, surveillanceLevel: value }))}
                    placeholder="Private lives or 24/7 watched? Black mirror-style or no tech at all?"
                    type="textarea"
                  />

                  <InputField
                    label="Internet / Info Access"
                    value={storyData.internetAccess}
                    onChange={(value) => setStoryData(prev => ({ ...prev, internetAccess: value }))}
                    placeholder="Free or restricted? Truthful or controlled by the powerful?"
                    type="textarea"
                  />

                  <InputField
                    label="Popular Culture"
                    value={storyData.popularCulture}
                    onChange={(value) => setStoryData(prev => ({ ...prev, popularCulture: value }))}
                    placeholder="What's trending? Fashion, slang, music, idols, subcultures"
                    type="textarea"
                  />
                </CollapsibleSection>

                {/* World Themes & Emotional Tone */}
                <CollapsibleSection
                  title="🎭 World Themes & Emotional Tone"
                  isOpen={!collapsedSections.worldThemes}
                  onToggle={() => toggleSection('worldThemes')}
                  optional={true}
                >
                  <InputField
                    label="Emotional Vibe of the World"
                    value={storyData.emotionalVibe}
                    onChange={(value) => setStoryData(prev => ({ ...prev, emotionalVibe: value }))}
                    placeholder="Hopeful, tense, decaying, cold, grimy, playful, absurd?"
                    type="textarea"
                  />

                  <InputField
                    label="Symbolic Motifs in the World"
                    value={storyData.symbolicMotifs}
                    onChange={(value) => setStoryData(prev => ({ ...prev, symbolicMotifs: value }))}
                    placeholder="mirrors, chains, masks, blood, neon, snow, rust, birds — recurring symbolic imagery"
                    type="textarea"
                  />

                  <InputField
                    label="Historical Trauma / Legacy"
                    value={storyData.historicalTrauma}
                    onChange={(value) => setStoryData(prev => ({ ...prev, historicalTrauma: value }))}
                    placeholder="Did this world survive a war, plague, collapse, revolution? It shapes everything"
                    type="textarea"
                  />

                  <InputField
                    label="Who Has Power Over Truth?"
                    value={storyData.powerOverTruth}
                    onChange={(value) => setStoryData(prev => ({ ...prev, powerOverTruth: value }))}
                    placeholder="Very important in political thrillers and noir. Can people even access facts?"
                    type="textarea"
                  />
                </CollapsibleSection>

                {/* Physical Detail Ideas for Visual Storytelling */}
                <CollapsibleSection
                  title="🎨 Physical Detail Ideas for Visual Storytelling"
                  isOpen={!collapsedSections.physicalDetails}
                  onToggle={() => toggleSection('physicalDetails')}
                  optional={true}
                >
                  <InputField
                    label="Architecture Style"
                    value={storyData.architectureStyle}
                    onChange={(value) => setStoryData(prev => ({ ...prev, architectureStyle: value }))}
                    placeholder="Shinto shrines next to glass skyscrapers? Cyberpunk with Edo rooflines?"
                    type="textarea"
                  />

                  <InputField
                    label="Fashion Trends"
                    value={storyData.fashionTrends}
                    onChange={(value) => setStoryData(prev => ({ ...prev, fashionTrends: value }))}
                    placeholder="Streetwear, ceremonial robes, tactical gear, vintage '80s, all black everything?"
                    type="textarea"
                  />

                  <InputField
                    label="Transportation"
                    value={storyData.transportation}
                    onChange={(value) => setStoryData(prev => ({ ...prev, transportation: value }))}
                    placeholder="Foot? Maglev trains? Pirate ships? Urban bikes? Portal jumps?"
                    type="textarea"
                  />

                  <InputField
                    label="Food Culture"
                    value={storyData.foodCulture}
                    onChange={(value) => setStoryData(prev => ({ ...prev, foodCulture: value }))}
                    placeholder="What do people eat? Are certain meals sacred? Is food scarce?"
                    type="textarea"
                  />

                  <InputField
                    label="Street Sounds & Smells"
                    value={storyData.streetSounds}
                    onChange={(value) => setStoryData(prev => ({ ...prev, streetSounds: value }))}
                    placeholder="Oil, incense, blood, sewage, perfume, rain on neon — add for immersion"
                    type="textarea"
                  />
                </CollapsibleSection>

                {/* Story Utility-Specific */}
                <CollapsibleSection
                  title="🎯 Story Utility-Specific"
                  isOpen={!collapsedSections.storyUtility}
                  onToggle={() => toggleSection('storyUtility')}
                  optional={true}
                >
                  <InputField
                    label="How the World Challenges the Protagonist"
                    value={storyData.worldChallenges}
                    onChange={(value) => setStoryData(prev => ({ ...prev, worldChallenges: value }))}
                    placeholder="What does this world demand from them emotionally or morally?"
                    type="textarea"
                  />

                  <InputField
                    label="What the World Rewards"
                    value={storyData.worldRewards}
                    onChange={(value) => setStoryData(prev => ({ ...prev, worldRewards: value }))}
                    placeholder="Loyalty? Ruthlessness? Intelligence? Obedience? Performance?"
                    type="textarea"
                  />

                  <InputField
                    label="What Would Get You Killed Here?"
                    value={storyData.deathTriggers}
                    onChange={(value) => setStoryData(prev => ({ ...prev, deathTriggers: value }))}
                    placeholder="Saying the wrong name? Loving the wrong person? Crossing a district line?"
                    type="textarea"
                  />

                  <InputField
                    label="What's Changing in This World Right Now?"
                    value={storyData.worldChanges}
                    onChange={(value) => setStoryData(prev => ({ ...prev, worldChanges: value }))}
                    placeholder="Something shifting beneath the surface — ripe for drama"
                    type="textarea"
                  />
                </CollapsibleSection>
              </div>
            )}

            {activeTab === 'characters' && (
              <div>
                <div className="text-center mb-8">
                  <h2 className="text-3xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                    👥 Character Expansion
                  </h2>
                  <p className="text-gray-300 text-lg">
                    Elevate your characters from flat to rich, complex personalities
                  </p>
                </div>

                {storyData.characters.map((character, index) => (
                  <div key={character.id} className="mb-10 p-6 bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl border-2 border-gray-600 shadow-2xl">
                    <div className="flex justify-between items-center mb-6">
                      <h3 className="text-2xl font-bold text-blue-300 flex items-center space-x-3">
                        <span className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm">
                          {index + 1}
                        </span>
                        <span>{character.name || 'Unnamed Character'}</span>
                      </h3>
                      {storyData.characters.length > 1 && (
                        <button
                          onClick={() => removeCharacter(character.id)}
                          className="bg-red-600 hover:bg-red-700 text-white p-2 rounded-lg transition-colors duration-200 transform hover:scale-105"
                        >
                          🗑️ Remove
                        </button>
                      )}
                    </div>

                    {/* Character Basics */}
                    <CollapsibleSection
                      title="📝 Character Basics"
                      isOpen={!collapsedSections.characterBasics}
                      onToggle={() => toggleSection('characterBasics')}
                      required={true}
                    >
                      <InputField
                        label="Character Name"
                        value={character.name}
                        onChange={(value) => updateCharacter(character.id, 'name', value)}
                        placeholder="Enter character name"
                        required={true}
                      />

                      <SelectField
                        label="Character Archetype"
                        value={character.archetype}
                        onChange={(value) => updateCharacter(character.id, 'archetype', value)}
                        options={characterArchetypes}
                        placeholder="Select character archetype"
                        required={true}
                      />

                      <InputField
                        label="Backstory in One Sentence"
                        value={character.backstoryOneSentence}
                        onChange={(value) => updateCharacter(character.id, 'backstoryOneSentence', value)}
                        placeholder="Forces clarity — like a clean logline just for the character"
                        type="textarea"
                        required={true}
                      />

                      <InputField
                        label="Internal Conflict"
                        value={character.internalConflict}
                        onChange={(value) => updateCharacter(character.id, 'internalConflict', value)}
                        placeholder="What do they struggle with emotionally or morally?"
                        type="textarea"
                      />

                      <InputField
                        label="External Conflict"
                        value={character.externalConflict}
                        onChange={(value) => updateCharacter(character.id, 'externalConflict', value)}
                        placeholder="Who or what opposes them physically or socially?"
                        type="textarea"
                      />

                      <InputField
                        label="Relationships Map"
                        value={character.relationshipsMap}
                        onChange={(value) => updateCharacter(character.id, 'relationshipsMap', value)}
                        placeholder="e.g., 'Enemies with X', 'Secretly loves Y', 'Owes life to Z'"
                        type="textarea"
                      />

                      <InputField
                        label="Personal Symbol / Icon / Object"
                        value={character.personalSymbol}
                        onChange={(value) => updateCharacter(character.id, 'personalSymbol', value)}
                        placeholder="e.g., a pocket watch, a tattoo, a necklace from childhood"
                        type="textarea"
                      />
                    </CollapsibleSection>

                    {/* Add a shortened version of other sections for better UI... */}
                    <div className="text-center mt-6 p-4 bg-blue-900/20 rounded-lg border border-blue-500/30">
                      <p className="text-blue-300 font-medium">💡 Advanced Character Details</p>
                      <p className="text-gray-400 text-sm mt-1">
                        Switch to "Psychological Layers" tab for deep character psychology and development options
                      </p>
                    </div>
                  </div>
                ))}

                <button
                  onClick={addCharacter}
                  className="w-full py-4 px-6 bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 rounded-xl text-white font-bold text-lg transition-all duration-300 transform hover:scale-105 shadow-lg"
                >
                  ➕ Add New Character
                </button>
              </div>
            )}

            {activeTab === 'psychological' && (
              <div>
                <div className="text-center mb-8">
                  <h2 className="text-3xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                    🧠 Psychological Layers
                  </h2>
                  <p className="text-gray-300 text-lg">
                    Deep psychological complexity for advanced character development
                  </p>
                </div>

                {storyData.characters.map((character, index) => (
                  <div key={character.id} className="mb-10 p-6 bg-gradient-to-br from-purple-900/20 to-pink-900/20 rounded-2xl border-2 border-purple-600/30 shadow-2xl">
                    <h3 className="text-2xl font-bold text-purple-300 mb-6 flex items-center space-x-3">
                      <span className="bg-purple-600 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm">
                        {index + 1}
                      </span>
                      <span>{character.name || `Character ${index + 1}`} - Psychological Profile</span>
                    </h3>

                    {/* Core Psychological Foundations */}
                    <div className="mb-8 p-4 bg-gray-800/50 rounded-lg">
                      <h4 className="text-lg font-semibold text-purple-300 mb-4 flex items-center space-x-2">
                        <span>🧩</span>
                        <span>Core Psychological Foundations</span>
                      </h4>
                      
                      <InputField
                        label="Core Wound / Trauma"
                        value={character.coreWound}
                        onChange={(value) => updateCharacter(character.id, 'coreWound', value)}
                        placeholder="Something from the past that still affects them emotionally"
                        type="textarea"
                      />

                      <InputField
                        label="Fear"
                        value={character.fear}
                        onChange={(value) => updateCharacter(character.id, 'fear', value)}
                        placeholder="Literal or symbolic — what are they terrified of losing?"
                        type="textarea"
                      />

                      <InputField
                        label="Mask vs. True Self"
                        value={character.maskVsTrueSelf}
                        onChange={(value) => updateCharacter(character.id, 'maskVsTrueSelf', value)}
                        placeholder="How they appear vs. who they are underneath"
                        type="textarea"
                      />

                      <SelectField
                        label="Character Arc Type"
                        value={character.arcType}
                        onChange={(value) => updateCharacter(character.id, 'arcType', value)}
                        options={arcTypes}
                        placeholder="Select arc type"
                      />

                      <InputField
                        label="What they'd never admit out loud"
                        value={character.neverAdmitOutLoud}
                        onChange={(value) => updateCharacter(character.id, 'neverAdmitOutLoud', value)}
                        placeholder="This one is gold for deep POV writing and reveals"
                        type="textarea"
                      />
                    </div>

                    {/* Mental Health Tags */}
                    <div className="mb-8 p-4 bg-gray-800/50 rounded-lg">
                      <h4 className="text-lg font-semibold text-purple-300 mb-4 flex items-center space-x-2">
                        <span>🏥</span>
                        <span>Mental Health Tags (Optional & Used Respectfully)</span>
                      </h4>
                      
                      <MultiSelectField
                        label="Mental Health Tags"
                        options={mentalHealthOptions}
                        selectedValues={character.mentalHealthTags}
                        onChange={(value) => updateCharacter(character.id, 'mentalHealthTags', value)}
                      />

                      <InputField
                        label="Trauma Response Style"
                        value={character.traumaResponseStyle}
                        onChange={(value) => updateCharacter(character.id, 'traumaResponseStyle', value)}
                        placeholder="Fight / Flight / Freeze / Fawn — or complex combinations of them"
                        type="textarea"
                      />

                      <SelectField
                        label="Love Style / Attachment Type"
                        value={character.attachmentType}
                        onChange={(value) => updateCharacter(character.id, 'attachmentType', value)}
                        options={attachmentTypes}
                        placeholder="Select attachment type"
                      />
                    </div>

                    <div className="text-center p-4 bg-purple-900/20 rounded-lg border border-purple-500/30">
                      <p className="text-purple-300 font-medium">🔬 More Psychology Options Available</p>
                      <p className="text-gray-400 text-sm mt-1">
                        This is a condensed view. Full psychological profiling with 50+ detailed fields will be available in the complete character system.
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'plot' && (
              <div>
                <div className="text-center mb-8">
                  <h2 className="text-3xl font-bold mb-4 bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent">
                    📚 Plot Utility Enhancements
                  </h2>
                  <p className="text-gray-300 text-lg">The Juicy Add-ons for sophisticated storytelling</p>
                </div>

                {/* Simplified Plot Tools Preview */}
                <div className="grid grid-cols-1 gap-6">
                  {[
                    { id: 'foreshadowing', title: '🔮 Foreshadowing Seeds', desc: 'Early hints for future reveals' },
                    { id: 'timebombs', title: '💣 Timebombs/Countdown', desc: 'Ticking clock elements' },
                    { id: 'redHerrings', title: '🐟 Red Herrings', desc: 'Misleading clues and distractions' },
                    { id: 'chekovsGuns', title: '🔫 Chekhov\'s Guns', desc: 'Elements that must pay off later' },
                    { id: 'plotTwists', title: '🌀 Plot Twists by Role', desc: 'Categorized plot twists' }
                  ].map((tool, index) => (
                    <div key={tool.id} className="p-6 bg-gradient-to-r from-gray-800 to-gray-700 rounded-xl border border-gray-600 hover:border-blue-500 transition-all duration-300">
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="text-xl font-bold text-white mb-2">{tool.title}</h3>
                          <p className="text-gray-400">{tool.desc}</p>
                        </div>
                        <div className="text-3xl opacity-50">📝</div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="text-center mt-8 p-6 bg-green-900/20 rounded-lg border border-green-500/30">
                  <p className="text-green-300 font-medium text-lg">🚀 17 Advanced Plot Tools Ready</p>
                  <p className="text-gray-400 mt-2">
                    All 17 sophisticated plot enhancement tools (Foreshadowing, Timebombs, Red Herrings, Chekhov's Guns, Multi-Arc Threads, etc.) 
                    will be fully functional when the backend multi-agent system is implemented.
                  </p>
                </div>
              </div>
            )}

            {activeTab === 'generation' && (
              <div>
                <div className="text-center mb-8">
                  <h2 className="text-3xl font-bold mb-4 bg-gradient-to-r from-yellow-400 to-red-400 bg-clip-text text-transparent">
                    🚀 Generation Dashboard
                  </h2>
                  <p className="text-gray-300 text-lg">Multi-Agent AI Story Generation Control Center</p>
                </div>
                
                {/* Generation Controls */}
                <div className="mb-8 p-6 bg-gradient-to-br from-blue-900/30 to-purple-900/30 rounded-2xl border-2 border-blue-500/30 shadow-xl">
                  <h3 className="text-xl font-bold text-blue-300 mb-6 flex items-center space-x-2">
                    <span>⚙️</span>
                    <span>Story Configuration</span>
                  </h3>
                  
                  <SliderField
                    label="Total Chapters in Book"
                    value={storyData.totalChapters}
                    onChange={(value) => setStoryData(prev => ({ ...prev, totalChapters: value }))}
                    min={1}
                    max={1000}
                  />

                  <SliderField
                    label="Minimum Words per Chapter"
                    value={storyData.minWordsPerChapter}
                    onChange={(value) => setStoryData(prev => ({ ...prev, minWordsPerChapter: value }))}
                    min={300}
                    max={5000}
                  />
                </div>

                {/* Agent Progress Dashboard */}
                <div className="mb-8 p-6 bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl border-2 border-gray-600 shadow-xl">
                  <h3 className="text-xl font-bold text-green-300 mb-6 flex items-center space-x-2">
                    <span>🤖</span>
                    <span>Multi-Agent System Status</span>
                  </h3>
                  <div className="grid grid-cols-1 gap-4">
                    {[
                      { name: 'Master Orchestrator', icon: '🎯', status: 'Ready', color: 'blue' },
                      { name: 'Worldbuilding Agent', icon: '🌍', status: 'Ready', color: 'green' },
                      { name: 'Character Agent', icon: '👥', status: 'Ready', color: 'purple' },
                      { name: 'Plot Agent', icon: '📚', status: 'Ready', color: 'yellow' },
                      { name: 'Story Generator Agent', icon: '✍️', status: 'Ready', color: 'red' },
                      { name: 'Sequential Checker Agent', icon: '🔍', status: 'Ready', color: 'pink' },
                      { name: 'Document Formatter Agent', icon: '📄', status: 'Ready', color: 'indigo' }
                    ].map((agent, index) => (
                      <div key={index} className="flex items-center justify-between p-4 bg-gray-700 rounded-lg border border-gray-600">
                        <div className="flex items-center space-x-3">
                          <span className="text-2xl">{agent.icon}</span>
                          <span className="text-white font-medium">{agent.name}</span>
                        </div>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium bg-${agent.color}-600 text-white`}>
                          {agent.status}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* AI Information */}
                <div className="mb-8 p-6 bg-gradient-to-br from-purple-900/30 to-blue-900/30 rounded-2xl border-2 border-purple-500/30">
                  <h3 className="text-xl font-bold text-purple-300 mb-4 flex items-center space-x-2">
                    <span>🧠</span>
                    <span>AI Engine Information</span>
                  </h3>
                  <div className="bg-gray-800 p-4 rounded-lg">
                    <p className="text-white font-semibold mb-2">🎯 Powered by Mistral AI</p>
                    <p className="text-gray-300 text-sm mb-2">
                      <strong>API:</strong> Mistral API with advanced language models
                    </p>
                    <p className="text-gray-300 text-sm mb-2">
                      <strong>Agents:</strong> 7 specialized AI agents for story generation
                    </p>
                    <p className="text-gray-300 text-sm">
                      <strong>Features:</strong> Sequential validation, auto-correction, KDP formatting
                    </p>
                  </div>
                </div>

                {/* Generate Button */}
                <div className="text-center">
                  <button className="w-full py-6 px-8 bg-gradient-to-r from-green-500 via-blue-600 to-purple-600 hover:from-green-600 hover:via-blue-700 hover:to-purple-700 rounded-2xl text-white font-bold text-2xl transition-all duration-300 transform hover:scale-105 shadow-2xl border-2 border-white/20">
                    ✨ Generate Complete Story Book ✨
                  </button>

                  <div className="mt-6 text-center text-gray-300">
                    <div className="grid grid-cols-3 gap-4 mt-4">
                      <div className="bg-green-900/20 p-3 rounded-lg border border-green-500/30">
                        <p className="text-green-400 font-semibold">🔄 Sequential Processing</p>
                        <p className="text-xs text-gray-400">Agents work in perfect coordination</p>
                      </div>
                      <div className="bg-blue-900/20 p-3 rounded-lg border border-blue-500/30">
                        <p className="text-blue-400 font-semibold">🛡️ Auto-Validation</p>
                        <p className="text-xs text-gray-400">Sequential Checker ensures quality</p>
                      </div>
                      <div className="bg-purple-900/20 p-3 rounded-lg border border-purple-500/30">
                        <p className="text-purple-400 font-semibold">📖 KDP Ready</p>
                        <p className="text-xs text-gray-400">Professional .docx output</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right Content Area */}
        <div className="flex-1 bg-gradient-to-br from-gray-900 via-black to-gray-800 p-8 flex items-center justify-center">
          <div className="text-center max-w-2xl">
            <div className="w-full max-w-lg mx-auto bg-gradient-to-br from-gray-800 to-gray-900 border-4 border-dashed border-gray-600 rounded-3xl flex items-center justify-center mb-8 shadow-2xl" style={{height: '400px'}}>
              <div className="text-gray-400 text-center">
                <div className="text-8xl mb-6 animate-pulse">📖</div>
                <p className="text-2xl mb-4 font-bold text-white">Your Book Preview</p>
                <p className="text-lg text-gray-300">
                  Complete the forms and click "Generate Complete Story Book" to begin.
                </p>
                <div className="mt-6 text-sm text-gray-500">
                  AI-powered • Multi-agent system • Professional quality
                </div>
              </div>
            </div>
            
            {/* Stats Display */}
            <div className="grid grid-cols-2 gap-6">
              <div className="bg-gradient-to-br from-blue-900/40 to-blue-700/40 p-6 rounded-2xl border border-blue-500/30 shadow-xl">
                <div className="text-blue-400 font-bold text-lg mb-2">📚 Chapters</div>
                <div className="text-4xl font-bold text-white">{storyData.totalChapters.toLocaleString()}</div>
                <div className="text-blue-300 text-sm mt-1">Total chapters to generate</div>
              </div>
              <div className="bg-gradient-to-br from-green-900/40 to-green-700/40 p-6 rounded-2xl border border-green-500/30 shadow-xl">
                <div className="text-green-400 font-bold text-lg mb-2">📝 Words/Chapter</div>
                <div className="text-4xl font-bold text-white">{storyData.minWordsPerChapter.toLocaleString()}</div>
                <div className="text-green-300 text-sm mt-1">Minimum words per chapter</div>
              </div>
            </div>

            {/* Estimated word count */}
            <div className="mt-6 p-4 bg-purple-900/20 rounded-lg border border-purple-500/30">
              <p className="text-purple-300 font-medium">
                📊 Estimated Total: {(storyData.totalChapters * storyData.minWordsPerChapter).toLocaleString()} words
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <StoryGeneratorApp />
    </div>
  );
}

export default App;