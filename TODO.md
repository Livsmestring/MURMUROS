# TODO

Konkrete, kortsiktige oppgaver. Se [ROADMAP.md](ROADMAP.md) for de større fasene og [README.md](README.md) for MURMUROS-modellen.

## Nå

- [ ] **Avklar stack for fremtidig frontend** (`website/`): masterprompten som florerer i noen økter refererer til et *annet* repo (`livsmestring-hjemmeside`, Next.js/TypeScript/Tailwind/Supabase/Vercel). Avklar med Daniel om dette skal gjelde MURMUROS sin `website/`-mappe, eller om det hører hjemme i et separat repo.

## Snart

- [ ] Onboarding-system (mappe `onboarding/`)
- [ ] Archetype Library (mappe `archetypes/`)
- [ ] Data-modeller / schemas (mappe `schemas/`)
- [ ] Koble `generate_midi.py`/`generate_animal_signal.py` til Murmur-agentene (`agents.py`) som en del av Musikk DNA-steget

## Senere

- [ ] Story Engine (MVP 0.2)
- [ ] Artist DNA Engine (MVP 0.2)
- [ ] Internt dashboard (MVP 0.2)
- [ ] Avatar System (MVP 0.3)
- [ ] Ekte deploy-oppsett (erstatte `deploy:staging`-placeholderen i `package.json`)

## Fullført

- [x] CI/CD-pipeline modernisert
- [x] Sikkerhetshardening fra audit (`audit/06-sikkerhet.md`)
- [x] Murmur-agent-infrastruktur (blackboard + agentkjede)
- [x] `ROADMAP.md` og `TODO.md` opprettet
- [x] Animal Signal PsyTech-prototype (`generate_animal_signal.py`)
