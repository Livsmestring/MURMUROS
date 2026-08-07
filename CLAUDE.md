# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MURMUROS is a Norwegian-language youth empowerment platform ("livsmestring" = life coping/mastery skills) developed by DevByNorth. It combines storytelling, music, art, and technology to support identity development and personal growth in young people.

## The MURMUROS Model

The core process pipeline the platform implements:

```
Historie (Story) → Refleksjon → Arketype → Artist DNA
→ Musikk DNA → Visuelt DNA → Avatar → Kreativt uttrykk → Mestring
```

All features should map to one or more of these stages. The pipeline is implemented in `index.js` as `PIPELINE_STAGES` (CJS module, kept as `.cjs` to coexist with the ESM root).

## Repository Structure

```
MURMUROS/
├── packages/
│   └── config/          # @murmuros/config — Zod env validation
│       └── src/
│           ├── env.ts
│           └── env.test.ts
├── index.js             # PIPELINE_STAGES and nextStage() — CJS, not yet migrated
├── generate_midi.py     # Standalone MIDI prototype (mido, not integrated)
├── eslint.config.js     # ESLint flat config (ESM)
├── pnpm-workspace.yaml  # Monorepo workspace root
└── .github/
    ├── workflows/
    │   ├── ci.yml       # Primary CI: lint → typecheck → test
    │   └── ci-cd.yml    # Legacy pipeline (kept for reference)
    └── dependabot.yml
```

## Commands

```bash
# Install all workspace dependencies
pnpm install

# Lint (eslint flat config, covers JS + TS)
pnpm lint

# Typecheck (runs tsc --noEmit in each package)
pnpm typecheck

# Test (runs vitest in each package)
pnpm test

# Run a single package's tests
pnpm --filter @murmuros/config test

# Python utility
pip install -r requirements-dev.txt
python generate_midi.py   # outputs bassline.mid
```

## Monorepo Setup

Package manager: **pnpm 10** with workspaces (`pnpm-workspace.yaml`).  
Node target: **22**. TypeScript target: **ES2022 / NodeNext**.

- Root `package.json` has `"type": "module"` — all `.js` files at root are ESM.  
  `index.js` is CJS legacy; ignore ESM/CJS conflict until it is migrated.
- Workspace packages live under `packages/`. Each has its own `package.json`, `tsconfig.json`, and declares its own deps.
- `eslint.config.js` uses the flat config format. Do not add `.eslintrc.*` files — they conflict.
- `zod` is a production dep of `packages/config` (declared there); `eslint`, `typescript-eslint`, `@eslint/js`, `globals`, `vitest` are root devDeps.

## CI

`.github/workflows/ci.yml` — triggered on push to `main` and all PRs:

1. `pnpm install --frozen-lockfile`
2. `pnpm lint`
3. `pnpm typecheck`
4. `pnpm test`

Uses `pnpm/action-setup@v4` (pnpm 10) and `actions/setup-node@v4` (Node 22).

## Development Notes

- **Language**: Project content and documentation is in Norwegian. Code identifiers and commit messages may use English.
- The `shared-ci-cd.yml` workflow is a reusable template for other repositories — do not add MURMUROS-specific logic to it.
- Dependabot monitors npm (daily) and GitHub Actions (weekly).
