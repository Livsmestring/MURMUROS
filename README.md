# MURMUROS

[![CI/CD Pipeline](https://github.com/Livsmestring/MURMUROS/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Livsmestring/MURMUROS/actions/workflows/ci-cd.yml)

> Historier blir til identitet. Identitet blir til mestring.

## Om prosjektet

MURMUROS er et initiativ for livsmestring, kreativ utfoldelse og identitetsutvikling for ungdom.

Gjennom historiefortelling, kunst, musikk og teknologi får deltakere mulighet til å utforske egne styrker, uttrykke følelser og utvikle sin unike stemme.

Prosjektet kombinerer menneskelige erfaringer med kreative og digitale verktøy for å skape trygg refleksjon, tilhørighet og personlig vekst.

## Visjon

Å skape en verden hvor alle unge mennesker blir sett, hørt og verdsatt.

## Misjon

Å utvikle verktøy og metoder som hjelper ungdom med å bygge identitet, mestring og håp gjennom kreativitet og teknologi.

## Kjerneverdier

* Respekt
* Inkludering
* Kreativitet
* Mestring
* Trygghet
* Samarbeid
* Innovasjon

## MURMUROS-modellen

```
Historie
    ↓
Refleksjon
    ↓
Arketype
    ↓
Artist DNA
    ↓
Musikk DNA
    ↓
Visuelt DNA
    ↓
Avatar
    ↓
Kreativt uttrykk
    ↓
Mestring
```

## Repository-struktur

Planlagt struktur — mappene opprettes etter hvert som funksjonalitet kommer på plass:

```
MURMUROS/
├── docs/
├── onboarding/
├── archetypes/
├── schemas/
├── core/
├── data/
├── website/
├── assets/
├── supabase/
│
├── README.md
├── LICENSE
├── CONTRIBUTING.md
└── SECURITY.md
```

Se [CONTRIBUTING.md](CONTRIBUTING.md) for hvordan du bidrar, og [SECURITY.md](SECURITY.md) for sikkerhetspolicy.

## Database (Supabase)

Backend-databasen kjører på Supabase-prosjektet **murmur-os-dev** (`gbbcvshngmbggozixniy`, org devbynorth). Skjema og RLS-policyer er versjonert som migrasjoner i [`supabase/migrations`](supabase/migrations), koblet til det aktive prosjektet via [`supabase/config.toml`](supabase/config.toml).

For at GitHub → Supabase-koblingen skal være aktiv (automatisk migrasjonsdeploy ved push til `main`, samt PR-baserte preview branches), må en repo-eier koble repoet til prosjektet i Supabase-dashbordet **én gang**: Project Settings → Integrations → GitHub. Dette OAuth-steget kan ikke gjøres via API/CLI.

Lokalt oppsett: kopier `.env.example` til `.env` og hent nøkkelverdiene fra [prosjektets API-innstillinger](https://supabase.com/dashboard/project/gbbcvshngmbggozixniy/settings/api).

## Utviklingsområder

### Livsmestring

Verktøy for refleksjon, identitet og personlig utvikling.

### Historiefortelling

Trygge rammer for å dele erfaringer og perspektiver.

### Kreativitet

Musikk, kunst, design og visuelle uttrykk.

### Teknologi

AI, digitale arbeidsflyter og moderne verktøy for læring og utvikling.

## Målgrupper

* Ungdom
* Skoler
* Ungdomsklubber
* Kulturhus
* Frivillige organisasjoner
* Kommuner
* Kreative miljøer

## Roadmap

### MVP 0.1

* Dokumentasjon
* Onboarding-system
* Archetype Library
* Data-modeller

### MVP 0.2

* Story Engine
* Artist DNA Engine
* Dashboard

### MVP 0.3

* Avatar System
* Musikkidentitet
* Pilotprosjekt

### v1.0

* MURMUROS Plattform
* Ungdomsportal
* Kreativt dashboard
* Samarbeidsverktøy

## DevByNorth

MURMUROS utvikles av DevByNorth som en del av arbeidet med kreativ teknologi, livsmestring og fremtidens digitale verktøy for ungdom.

## Lisens

© DevByNorth. Alle rettigheter forbeholdes.

Se LICENSE-filen for detaljer.
