import React from 'react';

// Component for Plot Utility Enhancements - Additional Sections
const PlotEnhancements = ({ 
  storyData, 
  collapsedSections, 
  toggleSection, 
  addToList, 
  removeFromList, 
  updateListItem 
}) => {

  const CollapsibleSection = ({ title, children, isOpen, onToggle, className = "" }) => (
    <div className={`border border-gray-600 rounded-lg mb-4 ${className}`}>
      <button
        onClick={onToggle}
        className="w-full px-4 py-3 text-left font-semibold bg-gray-700 hover:bg-gray-600 rounded-t-lg flex justify-between items-center"
      >
        <span>{title}</span>
        <span className="text-xl">{isOpen ? "−" : "+"}</span>
      </button>
      {isOpen && (
        <div className="p-4 bg-gray-800 rounded-b-lg">
          {children}
        </div>
      )}
    </div>
  );

  return (
    <>
      {/* Dynamic Power Balance */}
      <CollapsibleSection
        title="6. Dynamic Power Balance"
        isOpen={!collapsedSections.powerBalance}
        onToggle={() => toggleSection('powerBalance')}
      >
        <p className="text-gray-400 text-sm mb-4">
          A system to track how power/control shifts between characters or factions. Eg: Protagonist gains leverage, antagonist regains control, third party flips it.
        </p>
        {storyData.powerBalanceShifts.map((shift, index) => (
          <div key={shift.id} className="mb-4 p-3 bg-gray-700 rounded-lg">
            <div className="flex justify-between items-start mb-2">
              <label className="text-sm font-medium text-gray-300">Power Balance Shift {index + 1}</label>
              {storyData.powerBalanceShifts.length > 1 && (
                <button
                  onClick={() => removeFromList('powerBalanceShifts', shift.id)}
                  className="text-red-400 hover:text-red-300 text-xl font-bold"
                >×</button>
              )}
            </div>
            <textarea
              value={shift.shift}
              onChange={(e) => updateListItem('powerBalanceShifts', shift.id, 'shift', e.target.value)}
              placeholder="Describe how power dynamics shift and between whom"
              className="w-full px-3 py-2 bg-gray-600 border border-gray-500 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows={2}
            />
          </div>
        ))}
        <button
          onClick={() => addToList('powerBalanceShifts', { shift: '' })}
          className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 rounded-md text-white font-medium"
        >
          Add Power Balance Shift
        </button>
      </CollapsibleSection>

      {/* Dramatic Irony Layers */}
      <CollapsibleSection
        title="7. Dramatic Irony Layers"
        isOpen={!collapsedSections.dramaticIrony}
        onToggle={() => toggleSection('dramaticIrony')}
      >
        <p className="text-gray-400 text-sm mb-4">
          Info the audience knows that characters don't (or vice versa). Use to build suspense or emotional damage.
        </p>
        {storyData.dramaticIronyLayers.map((irony, index) => (
          <div key={irony.id} className="mb-4 p-3 bg-gray-700 rounded-lg">
            <div className="flex justify-between items-start mb-2">
              <label className="text-sm font-medium text-gray-300">Dramatic Irony {index + 1}</label>
              {storyData.dramaticIronyLayers.length > 1 && (
                <button
                  onClick={() => removeFromList('dramaticIronyLayers', irony.id)}
                  className="text-red-400 hover:text-red-300 text-xl font-bold"
                >×</button>
              )}
            </div>
            <textarea
              value={irony.irony}
              onChange={(e) => updateListItem('dramaticIronyLayers', irony.id, 'irony', e.target.value)}
              placeholder="Describe what the audience knows that characters don't, or vice versa"
              className="w-full px-3 py-2 bg-gray-600 border border-gray-500 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows={2}
            />
          </div>
        ))}
        <button
          onClick={() => addToList('dramaticIronyLayers', { irony: '' })}
          className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 rounded-md text-white font-medium"
        >
          Add Dramatic Irony Layer
        </button>
      </CollapsibleSection>

      {/* Reversal Markers */}
      <CollapsibleSection
        title="8. Reversal Markers"
        isOpen={!collapsedSections.reversals}
        onToggle={() => toggleSection('reversals')}
      >
        <p className="text-gray-400 text-sm mb-4">
          Key scenes where characters reverse their beliefs, positions, alliances. Track cause and effect that led to these reversal moments.
        </p>
        {storyData.reversalMarkers.map((reversal, index) => (
          <div key={reversal.id} className="mb-4 p-3 bg-gray-700 rounded-lg">
            <div className="flex justify-between items-start mb-2">
              <label className="text-sm font-medium text-gray-300">Reversal Marker {index + 1}</label>
              {storyData.reversalMarkers.length > 1 && (
                <button
                  onClick={() => removeFromList('reversalMarkers', reversal.id)}
                  className="text-red-400 hover:text-red-300 text-xl font-bold"
                >×</button>
              )}
            </div>
            <textarea
              value={reversal.reversal}
              onChange={(e) => updateListItem('reversalMarkers', reversal.id, 'reversal', e.target.value)}
              placeholder="Describe the character reversal and what causes it"
              className="w-full px-3 py-2 bg-gray-600 border border-gray-500 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows={2}
            />
          </div>
        ))}
        <button
          onClick={() => addToList('reversalMarkers', { reversal: '' })}
          className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 rounded-md text-white font-medium"
        >
          Add Reversal Marker
        </button>
      </CollapsibleSection>

      {/* Thematic Echo Scenes */}
      <CollapsibleSection
        title="9. Thematic Echo Scenes"
        isOpen={!collapsedSections.thematicEcho}
        onToggle={() => toggleSection('thematicEcho')}
      >
        <p className="text-gray-400 text-sm mb-4">
          Scenes that mirror earlier ones with altered emotional/ethical weight. Eg: A betrayal scene echoed later by a sacrifice in the same place.
        </p>
        {storyData.thematicEchoScenes.map((echo, index) => (
          <div key={echo.id} className="mb-4 p-3 bg-gray-700 rounded-lg">
            <div className="flex justify-between items-start mb-2">
              <label className="text-sm font-medium text-gray-300">Thematic Echo Scene {index + 1}</label>
              {storyData.thematicEchoScenes.length > 1 && (
                <button
                  onClick={() => removeFromList('thematicEchoScenes', echo.id)}
                  className="text-red-400 hover:text-red-300 text-xl font-bold"
                >×</button>
              )}
            </div>
            <textarea
              value={echo.echo}
              onChange={(e) => updateListItem('thematicEchoScenes', echo.id, 'echo', e.target.value)}
              placeholder="Describe the original scene and how it will be echoed later with different weight"
              className="w-full px-3 py-2 bg-gray-600 border border-gray-500 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows={2}
            />
          </div>
        ))}
        <button
          onClick={() => addToList('thematicEchoScenes', { echo: '' })}
          className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 rounded-md text-white font-medium"
        >
          Add Thematic Echo Scene
        </button>
      </CollapsibleSection>

      {/* Character Crossroad Moments */}
      <CollapsibleSection
        title="10. Character Crossroad Moments"
        isOpen={!collapsedSections.crossroads}
        onToggle={() => toggleSection('crossroads')}
      >
        <p className="text-gray-400 text-sm mb-4">
          Moral or emotional decisions that define character development. Could go either way—track what leads to each choice.
        </p>
        {storyData.crossroadMoments.map((crossroad, index) => (
          <div key={crossroad.id} className="mb-4 p-3 bg-gray-700 rounded-lg">
            <div className="flex justify-between items-start mb-2">
              <label className="text-sm font-medium text-gray-300">Crossroad Moment {index + 1}</label>
              {storyData.crossroadMoments.length > 1 && (
                <button
                  onClick={() => removeFromList('crossroadMoments', crossroad.id)}
                  className="text-red-400 hover:text-red-300 text-xl font-bold"
                >×</button>
              )}
            </div>
            <textarea
              value={crossroad.crossroad}
              onChange={(e) => updateListItem('crossroadMoments', crossroad.id, 'crossroad', e.target.value)}
              placeholder="Describe the moral/emotional decision and what leads to it"
              className="w-full px-3 py-2 bg-gray-600 border border-gray-500 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows={2}
            />
          </div>
        ))}
        <button
          onClick={() => addToList('crossroadMoments', { crossroad: '' })}
          className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 rounded-md text-white font-medium"
        >
          Add Crossroad Moment
        </button>
      </CollapsibleSection>

      {/* Plot-Driven Flashbacks / Visions */}
      <CollapsibleSection
        title="11. Plot-Driven Flashbacks / Visions"
        isOpen={!collapsedSections.flashbacks}
        onToggle={() => toggleSection('flashbacks')}
      >
        <p className="text-gray-400 text-sm mb-4">
          Not random nostalgia, but reveals that re-contextualize what the reader/viewer thinks they know.
        </p>
        {storyData.plotFlashbacks.map((flashback, index) => (
          <div key={flashback.id} className="mb-4 p-3 bg-gray-700 rounded-lg">
            <div className="flex justify-between items-start mb-2">
              <label className="text-sm font-medium text-gray-300">Plot Flashback {index + 1}</label>
              {storyData.plotFlashbacks.length > 1 && (
                <button
                  onClick={() => removeFromList('plotFlashbacks', flashback.id)}
                  className="text-red-400 hover:text-red-300 text-xl font-bold"
                >×</button>
              )}
            </div>
            <textarea
              value={flashback.flashback}
              onChange={(e) => updateListItem('plotFlashbacks', flashback.id, 'flashback', e.target.value)}
              placeholder="Describe the flashback/vision and what it reveals or re-contextualizes"
              className="w-full px-3 py-2 bg-gray-600 border border-gray-500 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows={2}
            />
          </div>
        ))}
        <button
          onClick={() => addToList('plotFlashbacks', { flashback: '' })}
          className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 rounded-md text-white font-medium"
        >
          Add Plot Flashback
        </button>
      </CollapsibleSection>

      {/* Interwoven Timelines or Perspectives */}
      <CollapsibleSection
        title="12. Interwoven Timelines or Perspectives"
        isOpen={!collapsedSections.timelines}
        onToggle={() => toggleSection('timelines')}
      >
        <p className="text-gray-400 text-sm mb-4">
          If relevant: switching POVs or timelines to create tension, contrast, or deeper world insight.
        </p>
        {storyData.interwovenTimelines.map((timeline, index) => (
          <div key={timeline.id} className="mb-4 p-3 bg-gray-700 rounded-lg">
            <div className="flex justify-between items-start mb-2">
              <label className="text-sm font-medium text-gray-300">Interwoven Timeline {index + 1}</label>
              {storyData.interwovenTimelines.length > 1 && (
                <button
                  onClick={() => removeFromList('interwovenTimelines', timeline.id)}
                  className="text-red-400 hover:text-red-300 text-xl font-bold"
                >×</button>
              )}
            </div>
            <textarea
              value={timeline.timeline}
              onChange={(e) => updateListItem('interwovenTimelines', timeline.id, 'timeline', e.target.value)}
              placeholder="Describe the timeline/POV switch and its purpose"
              className="w-full px-3 py-2 bg-gray-600 border border-gray-500 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows={2}
            />
          </div>
        ))}
        <button
          onClick={() => addToList('interwovenTimelines', { timeline: '' })}
          className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 rounded-md text-white font-medium"
        >
          Add Interwoven Timeline
        </button>
      </CollapsibleSection>

      {/* Symbolic Motif Tracking */}
      <CollapsibleSection
        title="13. Symbolic Motif Tracking"
        isOpen={!collapsedSections.symbolicMotif}
        onToggle={() => toggleSection('symbolicMotif')}
      >
        <p className="text-gray-400 text-sm mb-4">
          Symbols/imagery that repeat for emotional or thematic weight (cigarettes, clocks, blood, etc.). Great for unspoken storytelling.
        </p>
        {storyData.symbolicMotifTracking.map((motif, index) => (
          <div key={motif.id} className="mb-4 p-3 bg-gray-700 rounded-lg">
            <div className="flex justify-between items-start mb-2">
              <label className="text-sm font-medium text-gray-300">Symbolic Motif {index + 1}</label>
              {storyData.symbolicMotifTracking.length > 1 && (
                <button
                  onClick={() => removeFromList('symbolicMotifTracking', motif.id)}
                  className="text-red-400 hover:text-red-300 text-xl font-bold"
                >×</button>
              )}
            </div>
            <textarea
              value={motif.motif}
              onChange={(e) => updateListItem('symbolicMotifTracking', motif.id, 'motif', e.target.value)}
              placeholder="Describe the symbol/imagery and its thematic significance"
              className="w-full px-3 py-2 bg-gray-600 border border-gray-500 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows={2}
            />
          </div>
        ))}
        <button
          onClick={() => addToList('symbolicMotifTracking', { motif: '' })}
          className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 rounded-md text-white font-medium"
        >
          Add Symbolic Motif
        </button>
      </CollapsibleSection>

      {/* Location-based Stakes System */}
      <CollapsibleSection
        title="14. Location-based Stakes System"
        isOpen={!collapsedSections.locationStakes}
        onToggle={() => toggleSection('locationStakes')}
      >
        <p className="text-gray-400 text-sm mb-4">
          Some places in the world carry emotional or political significance—track which scenes have to happen there and why.
        </p>
        {storyData.locationStakes.map((location, index) => (
          <div key={location.id} className="mb-4 p-3 bg-gray-700 rounded-lg">
            <div className="flex justify-between items-start mb-2">
              <label className="text-sm font-medium text-gray-300">Location Stakes {index + 1}</label>
              {storyData.locationStakes.length > 1 && (
                <button
                  onClick={() => removeFromList('locationStakes', location.id)}
                  className="text-red-400 hover:text-red-300 text-xl font-bold"
                >×</button>
              )}
            </div>
            <textarea
              value={location.location}
              onChange={(e) => updateListItem('locationStakes', location.id, 'location', e.target.value)}
              placeholder="Describe the location, its significance, and why key scenes must happen there"
              className="w-full px-3 py-2 bg-gray-600 border border-gray-500 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows={2}
            />
          </div>
        ))}
        <button
          onClick={() => addToList('locationStakes', { location: '' })}
          className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 rounded-md text-white font-medium"
        >
          Add Location Stakes
        </button>
      </CollapsibleSection>

      {/* NPC Catalyst Tracker */}
      <CollapsibleSection
        title="15. NPC Catalyst Tracker"
        isOpen={!collapsedSections.npcCatalyst}
        onToggle={() => toggleSection('npcCatalyst')}
      >
        <p className="text-gray-400 text-sm mb-4">
          Supporting or minor characters that unknowingly shift the main plot's direction. "The bartender gave a name." Boom—snowball starts rolling.
        </p>
        {storyData.npcCatalysts.map((catalyst, index) => (
          <div key={catalyst.id} className="mb-4 p-3 bg-gray-700 rounded-lg">
            <div className="flex justify-between items-start mb-2">
              <label className="text-sm font-medium text-gray-300">NPC Catalyst {index + 1}</label>
              {storyData.npcCatalysts.length > 1 && (
                <button
                  onClick={() => removeFromList('npcCatalysts', catalyst.id)}
                  className="text-red-400 hover:text-red-300 text-xl font-bold"
                >×</button>
              )}
            </div>
            <textarea
              value={catalyst.catalyst}
              onChange={(e) => updateListItem('npcCatalysts', catalyst.id, 'catalyst', e.target.value)}
              placeholder="Describe the NPC and how they unknowingly shift the plot"
              className="w-full px-3 py-2 bg-gray-600 border border-gray-500 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows={2}
            />
          </div>
        ))}
        <button
          onClick={() => addToList('npcCatalysts', { catalyst: '' })}
          className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 rounded-md text-white font-medium"
        >
          Add NPC Catalyst
        </button>
      </CollapsibleSection>

      {/* Parallel Plot Mirror */}
      <CollapsibleSection
        title="16. Parallel Plot Mirror"
        isOpen={!collapsedSections.parallelPlot}
        onToggle={() => toggleSection('parallelPlot')}
      >
        <p className="text-gray-400 text-sm mb-4">
          A secondary story arc (maybe even a historical or background one) that mirrors or contrasts the main arc. This could be from another generation, from the villain's POV, etc.
        </p>
        {storyData.parallelPlotMirror.map((mirror, index) => (
          <div key={mirror.id} className="mb-4 p-3 bg-gray-700 rounded-lg">
            <div className="flex justify-between items-start mb-2">
              <label className="text-sm font-medium text-gray-300">Parallel Plot Mirror {index + 1}</label>
              {storyData.parallelPlotMirror.length > 1 && (
                <button
                  onClick={() => removeFromList('parallelPlotMirror', mirror.id)}
                  className="text-red-400 hover:text-red-300 text-xl font-bold"
                >×</button>
              )}
            </div>
            <textarea
              value={mirror.mirror}
              onChange={(e) => updateListItem('parallelPlotMirror', mirror.id, 'mirror', e.target.value)}
              placeholder="Describe the parallel plot and how it mirrors or contrasts the main story"
              className="w-full px-3 py-2 bg-gray-600 border border-gray-500 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows={2}
            />
          </div>
        ))}
        <button
          onClick={() => addToList('parallelPlotMirror', { mirror: '' })}
          className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 rounded-md text-white font-medium"
        >
          Add Parallel Plot Mirror
        </button>
      </CollapsibleSection>
    </>
  );
};

export default PlotEnhancements;