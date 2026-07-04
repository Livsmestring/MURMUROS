'use strict';

/**
 * The MURMUROS model: the ordered process pipeline the platform implements.
 * Each stage feeds the next, from a young person's story through to mastery.
 * See README.md / CLAUDE.md for the canonical description.
 */
const PIPELINE_STAGES = [
  'Historie', // Story
  'Refleksjon', // Reflection
  'Arketype', // Archetype
  'Artist DNA',
  'Musikk DNA',
  'Visuelt DNA',
  'Avatar',
  'Kreativt uttrykk', // Creative expression
  'Mestring', // Mastery
];

/**
 * Return the stage that follows the given stage in the pipeline, or null if
 * the given stage is the last one (or is not a known stage).
 *
 * @param {string} stage - A pipeline stage name.
 * @returns {string|null} The next stage, or null.
 */
function nextStage(stage) {
  const index = PIPELINE_STAGES.indexOf(stage);
  if (index === -1 || index === PIPELINE_STAGES.length - 1) {
    return null;
  }
  return PIPELINE_STAGES[index + 1];
}

module.exports = { PIPELINE_STAGES, nextStage };
