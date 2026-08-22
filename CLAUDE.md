# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MURMUROS is a Norwegian-language youth empowerment platform ("livsmestring" = life coping/mastery skills) developed by DevByNorth. It combines storytelling, music, art, and technology to support identity development and personal growth in young people.

The project is in **MVP 0.1** — documentation plus early scaffolding: a Node.js package (`package.json`, `index.js` with the pipeline-stage model, a JS test), a standalone Python MIDI prototype with pytest suites, and CI that validates all of it.

## The MURMUROS Model

The core process pipeline the platform implements:

```
Historie (Story)
    ↓
Refleksjon
    ↓
Arketype (Archetype)
    ↓
Artist DNA
    ↓
Musikk DNA
    ↓
Visuelt DNA
    ↓
Avatar
    ↓
Kreativt uttrykk (Creative Expression)
    ↓
Mestring (Mastery)
```

All features built should map to one or more of these pipeline stages.

## Planned Repository Structure

Per the README, the intended layout is:

```
MURMUROS/
├── docs/
├── onboarding/
├── archetypes/
├── schemas/
├── core/
├── data/
├── website/
└── assets/
```

`core/` now exists (agent infrastructure); create the others as features are implemented.

## CI/CD Pipeline

Defined in `.github/workflows/ci-cd.yml`, triggered on push to `main`, all PRs, and a nightly schedule:

1. **Lint YAML**: `yamllint --strict .github/`
2. **Python Tests**: `pip install -r requirements-dev.txt` → `python -m pytest -q`
3. **Build and Test (Node)**: `npm ci` → `npm test` (Node 20)
4. **Static Analysis**: `npm run lint` (ESLint 10, flat config in `eslint.config.js`)
5. **Deploy**: `npm run deploy:staging` placeholder (only on `main`)

CodeQL security scanning runs via the repository's CodeQL "default setup" (Settings → Code security), so no CodeQL job is defined in the workflow — adding one would conflict with default setup.

## Existing Code

### `core/` + `agents.py` + `demo.py` (Python)

The Murmur agent prototype. `core/blackboard.py` has the event model (`Event`, validated and immutable) and the async pub/sub board (`MurmurBlackboard`) agents communicate through — never directly with each other. `agents.py` implements the Observer → Architect → Pedagogue/Growth chain, mapping to the pipeline stages (Historie/Refleksjon → Arketype/DNA → Kreativt uttrykk/Mestring, with user override). `python demo.py` runs one full cycle. Tested by `tests/test_blackboard.py` and `tests/test_agents.py`.

### `index.js`

The MURMUROS pipeline-stage model as a Node module (`PIPELINE_STAGES`, `nextStage()`). Tested by `test/pipeline.test.js` (`npm test`).

### `generate_midi.py`

A standalone Python utility that generates a MIDI bassline file (`bassline.mid`). Uses the `mido` library; tested by the pytest suites.

```bash
pip install -r requirements-dev.txt
python generate_midi.py
python -m pytest -q
```

This is not yet integrated into the main platform — it is a standalone creative tool prototype.

### `generate_animal_signal.py`

A second standalone MIDI prototype, same pattern as `generate_midi.py`: a multi-track "Animal Signal PsyTech" sketch (132 BPM, D minor) mapping animal calls onto musical roles — wolf howl → lead, bird calls → arpeggio, whale song → pad, frog sounds → bass stabs, raven calls → transition accents — for the Musikk DNA pipeline stage. Tested by `tests/test_generate_animal_signal.py`.

## Development Notes

- **Language**: The project content and documentation is in Norwegian. Code identifiers and commit messages may use English.
- **Commands**: `npm test`, `npm run lint`, `python -m pytest -q`. The `deploy:staging` script is a placeholder until real deployment exists.
- **Dependabot** is configured for npm, pip and GitHub Actions (`.github/dependabot.yml`), so keep dependency versions explicit.
- The `shared-ci-cd.yml` workflow is a reusable template parameterised for other repositories — do not modify it to add MURMUROS-specific logic.
