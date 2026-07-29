'use strict';

// Aggregates the project's test suites so `npm test` runs them all.
// Requiring a suite executes its tests (each throws on failure, which
// propagates and fails the process).
require('./pipeline.test');
require('./archetype.test');
