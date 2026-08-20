# TODO

Konkrete, kortsiktige oppgaver. Se [ROADMAP.md](ROADMAP.md) for de større fasene og [README.md](README.md) for MURMUROS-modellen.

## Nå

- [ ] **Animal Signal PsyTech-prototype**: ny standalone MIDI-generator (parallelt med `generate_midi.py`) som realiserer briefen "Dark organic Animal Signal PsyTech" — 132 BPM, D-moll, ulvehyl-lead (D–F–A–C), fuglekall-arpeggioer, hval-subpad, frosk-bass-stabs, ravn-transisjoner. Testet med pytest, samme mønster som `generate_midi.py`.
- [ ] **Avklar stack for fremtidig frontend** (`website/`): masterprompten som florerer i noen økter refererer til et *annet* repo (`livsmestring-hjemmeside`, Next.js/TypeScript/Tailwind/Supabase/Vercel). Avklar med Daniel om dette skal gjelde MURMUROS sin `website/`-mappe, eller om det hører hjemme i et separat repo.

## Snart

- [ ] Onboarding-system (mappe `onboarding/`)
- [ ] Archetype Library (mappe `archetypes/`)
- [ ] Data-modeller / schemas (mappe `schemas/`)
- [ ] Koble `generate_midi.py`/Animal Signal-prototypen til Murmur-agentene (`agents.py`) som en del av Musikk DNA-steget

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
