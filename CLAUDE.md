# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MURMUROS is a Norwegian-language youth empowerment platform ("livsmestring" = life coping/mastery skills) developed by DevByNorth. It combines storytelling, music, art, and technology to support identity development and personal growth in young people.

The project is in **MVP 0.1** — primarily documentation and scaffolding. The planned tech stack is Node.js/npm, but no `package.json` or application code exists yet; CI currently validates only the content that exists (YAML and Python).

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

None of these directories exist yet — create them as features are implemented.

## CI/CD Pipeline

Defined in `.github/workflows/ci-cd.yml`, triggered on push to `main` and all PRs:

1. **Lint YAML**: `yamllint -d relaxed --strict .github/`
2. **Check Python**: `python -m compileall -q .`

The pipeline validates only what currently exists in the repository. When the Node.js application is introduced (`package.json`), reintroduce build/test (`npm test`), linting (ESLint), CodeQL security scanning and the staging deploy job. Target a current LTS Node.js version (20+) at that point — Node 16 is end-of-life.

## Existing Code

### `generate_midi.py`

A standalone Python utility that generates a MIDI bassline file (`bassline.mid`). Uses the `mido` library.

```bash
pip install mido
python generate_midi.py
```

This is not yet integrated into the main platform — it is a standalone creative tool prototype.

## Development Notes

- **Language**: The project content and documentation is in Norwegian. Code identifiers and commit messages may use English.
- **No build or test commands exist yet.** When adding `package.json`, wire `npm test` and `npm run deploy:staging` to real scripts to keep CI green.
- **Dependabot** is configured for both npm and GitHub Actions (`.github/dependabot.yml`), so keep dependency versions explicit once `package.json` is introduced.
- The `shared-ci-cd.yml` workflow is a reusable template parameterised for other repositories — do not modify it to add MURMUROS-specific logic.
