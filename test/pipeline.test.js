import assert from 'node:assert/strict'
import { PIPELINE_STAGES, nextStage } from '../index.js'

let passed = 0

function test(name, fn) {
  fn()
  passed += 1
  console.log(`  ok - ${name}`)
}

test('pipeline has the nine MURMUROS stages in order', () => {
  assert.deepStrictEqual(PIPELINE_STAGES, [
    'Historie',
    'Refleksjon',
    'Arketype',
    'Artist DNA',
    'Musikk DNA',
    'Visuelt DNA',
    'Avatar',
    'Kreativt uttrykk',
    'Mestring',
  ])
})

test('pipeline starts at Historie and ends at Mestring', () => {
  assert.strictEqual(PIPELINE_STAGES[0], 'Historie')
  assert.strictEqual(PIPELINE_STAGES[PIPELINE_STAGES.length - 1], 'Mestring')
})

test('nextStage returns the following stage', () => {
  assert.strictEqual(nextStage('Historie'), 'Refleksjon')
  assert.strictEqual(nextStage('Avatar'), 'Kreativt uttrykk')
})

test('nextStage returns null at the end of the pipeline', () => {
  assert.strictEqual(nextStage('Mestring'), null)
})

test('nextStage returns null for an unknown stage', () => {
  assert.strictEqual(nextStage('Ukjent'), null)
})

console.log(`\n${passed} passing`)
