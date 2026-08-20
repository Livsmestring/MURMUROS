# Roadmap

Dette dokumentet beskriver de planlagte fasene for MURMUROS. Se [README.md](README.md) for visjon, verdier og MURMUROS-modellen, og [TODO.md](TODO.md) for konkrete, kortsiktige oppgaver.

Alt arbeid skal kunne knyttes til ett eller flere steg i MURMUROS-modellen:

```
Historie → Refleksjon → Arketype → Artist DNA → Musikk DNA → Visuelt DNA → Avatar → Kreativt uttrykk → Mestring
```

## MVP 0.1 — Fundament (pågår)

Dokumentasjon og tidlig scaffolding.

- [x] Prosjektdokumentasjon (README, CONTRIBUTING, SECURITY, LICENSE)
- [x] CI/CD-pipeline (yamllint, pytest, npm test, ESLint)
- [x] Pipeline-stage-modell (`index.js` — `PIPELINE_STAGES`, `nextStage()`)
- [x] Murmur-agent-prototype (`core/blackboard.py`, `agents.py`, `demo.py`)
- [x] Standalone MIDI-prototype (`generate_midi.py`)
- [x] `ROADMAP.md` og `TODO.md` som egne filer
- [ ] Onboarding-system
- [ ] Archetype Library
- [ ] Data-modeller (`schemas/`)

## MVP 0.2 — Story Engine

- [ ] Story Engine (fanger og strukturerer historier/refleksjoner)
- [ ] Artist DNA Engine (kobler arketype til artistisk identitet)
- [ ] Dashboard (intern oversikt over deltakerreiser)

## MVP 0.3 — Identitet og lyd

- [ ] Avatar System (visuelt DNA → avatar)
- [ ] Musikkidentitet (Musikk DNA-generering, bygger videre på MIDI-prototypen)
- [ ] Pilotprosjekt med ekte(fiktive) testbrukere

## v1.0 — MURMUROS Plattform

- [ ] Ungdomsportal
- [ ] Kreativt dashboard
- [ ] Samarbeidsverktøy
- [ ] `website/` og `assets/`-struktur på plass

## Åpne avklaringer

- Stack/arkitektur for en fremtidig frontend/plattform (`website/`) er ikke besluttet. Se TODO.md.
