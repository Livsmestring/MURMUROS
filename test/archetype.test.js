'use strict';

// Schema / data-model validation for the MURMUROS Archetype Library.
// Every file in archetypes/ must validate against schemas/archetype.schema.json,
// and its creative-DNA sections must map onto the pipeline stages in index.js.
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');

const { PIPELINE_STAGES } = require('../index');

const ROOT = path.join(__dirname, '..');
const SCHEMA_PATH = path.join(ROOT, 'schemas', 'archetype.schema.json');
const ARCHETYPES_DIR = path.join(ROOT, 'archetypes');

const schema = JSON.parse(fs.readFileSync(SCHEMA_PATH, 'utf8'));
const ajv = new Ajv({ allErrors: true });

// Which archetype DNA field belongs to which pipeline stage.
const DNA_STAGE_MAP = {
  artistDNA: 'Artist DNA',
  musikkDNA: 'Musikk DNA',
  visueltDNA: 'Visuelt DNA',
};

function archetypeFiles() {
  return fs
    .readdirSync(ARCHETYPES_DIR)
    .filter((name) => name.endsWith('.json'))
    .sort();
}

function loadArchetype(file) {
  return JSON.parse(fs.readFileSync(path.join(ARCHETYPES_DIR, file), 'utf8'));
}

let passed = 0;

function test(name, fn) {
  fn();
  passed += 1;
  console.log(`  ok - ${name}`);
}

test('archetype schema is itself a valid JSON Schema', () => {
  // ajv.compile throws if the schema document is malformed.
  const validate = ajv.compile(schema);
  assert.strictEqual(typeof validate, 'function');
});

test('the archetype library is not empty', () => {
  assert.ok(archetypeFiles().length > 0, 'expected at least one archetype file');
});

test('every archetype validates against the schema', () => {
  const validate = ajv.compile(schema);
  for (const file of archetypeFiles()) {
    const data = loadArchetype(file);
    const valid = validate(data);
    assert.ok(
      valid,
      `${file} failed schema validation: ${ajv.errorsText(validate.errors)}`
    );
  }
});

test('each archetype id matches its file name', () => {
  for (const file of archetypeFiles()) {
    const data = loadArchetype(file);
    assert.strictEqual(
      data.id,
      path.basename(file, '.json'),
      `id "${data.id}" does not match file name "${file}"`
    );
  }
});

test('archetype ids are unique across the library', () => {
  const ids = archetypeFiles().map((file) => loadArchetype(file).id);
  assert.strictEqual(new Set(ids).size, ids.length, 'duplicate archetype id found');
});

test('musikkDNA tempo range is ordered (min <= max)', () => {
  // A cross-field constraint the JSON Schema cannot express on its own.
  for (const file of archetypeFiles()) {
    const { tempo } = loadArchetype(file).musikkDNA;
    assert.ok(
      tempo.min <= tempo.max,
      `${file}: tempo.min (${tempo.min}) must be <= tempo.max (${tempo.max})`
    );
  }
});

test('each archetype DNA section maps to a known pipeline stage', () => {
  for (const file of archetypeFiles()) {
    const data = loadArchetype(file);
    for (const [field, stage] of Object.entries(DNA_STAGE_MAP)) {
      assert.ok(field in data, `${file} missing DNA field "${field}"`);
      assert.ok(
        PIPELINE_STAGES.includes(stage),
        `pipeline stage "${stage}" for DNA field "${field}" is not in the model`
      );
    }
  }
});

test('a malformed archetype is rejected by the schema', () => {
  // Guards that the schema actually catches bad data (missing required fields,
  // wrong id shape, out-of-range tempo).
  const validate = ajv.compile(schema);
  const bad = {
    id: 'Not Valid Id',
    navn: 'Ugyldig',
    styrker: [],
    musikkDNA: { tempo: { min: 5, max: 999 }, toneart: [], instrumenter: [] },
  };
  assert.strictEqual(validate(bad), false, 'expected malformed archetype to be invalid');
});

console.log(`\n${passed} passing`);
