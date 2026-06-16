# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MURMUROS is a Norwegian-language youth empowerment platform ("livsmestring" = life coping/mastery skills) developed by DevByNorth. It combines storytelling, music, art, and technology to support identity development and personal growth in young people.

The project is in **MVP 0.1** — primarily documentation and scaffolding. The planned tech stack is Node.js/npm (reflected in CI/CD), but no `package.json` or application code exists yet.

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

## Languages

The repo currently contains **Python** (`generate_midi.py`) and scaffolding for **JavaScript/Node.js**. Both are detected automatically by the CI pipeline.

## Commands

```bash
# Python
pip install -r requirements.txt
python generate_midi.py          # generates bassline.mid

# JavaScript (when source files are added)
npm install
npm test
npm run lint                     # runs eslint .
npm run deploy:staging           # placeholder until deploy is configured
```

## CI/CD Pipeline

Defined in `.github/workflows/ci-cd.yml`, triggered on push to `main`, all PRs, and daily at 02:00 UTC:

1. **detect-languages** — checks for `.py` files and `package.json` to conditionally gate later steps
2. **build-and-test** — `npm install` + `npm test` (JS) and `pip install -r requirements.txt` (Python)
3. **static-analysis** — `eslint .` (JS) and `flake8` with max line length 100 (Python)
4. **security-scan** — GitHub CodeQL scanning for both `javascript` and `python`
5. **deploy** — `npm run deploy:staging`, runs only on `main`

Node.js target: **20 LTS**. Python target: **3.11**.

Action versions: `actions/checkout@v4`, `actions/setup-node@v4`, `actions/setup-python@v5`, `github/codeql-action@v3`.

**Dependabot** monitors npm (daily), pip (weekly), and GitHub Actions (weekly).

## Existing Code

### `generate_midi.py`

Standalone Python utility — generates a 4-note MIDI bassline (A2, C3, D3, E3) and writes `bassline.mid`. Not yet integrated into the platform.

## Development Notes

- **Language**: Project content and documentation is in Norwegian. Code identifiers and commit messages may use English.
- **ESLint** is configured in `.eslintrc.json` (env: node + es2022, extends `eslint:recommended`). Add rules there when JS source is introduced.
- **Flake8** runs at `--max-line-length=100`. Add a `setup.cfg` or `tox.ini` `[flake8]` section to extend configuration.
- The `shared-ci-cd.yml` workflow is a reusable template for other repositories — do not add MURMUROS-specific logic to it.
