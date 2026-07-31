# Sikkerhetsaudit — MURMUROS

**Dato:** 2026-07-31  
**Revisor:** Claude Code (automatisert + manuell gjennomgang)  
**Revisjon gjelder:** `Livsmestring/MURMUROS`, alle branches inkl. full git-historikk

---

## Kartlegging av repoet

| Dimensjon | Status |
|---|---|
| **Stadium** | MVP 0.1 — primært dokumentasjon og scaffolding |
| **Applikasjonskode** | `generate_midi.py` (Python, 36 linjer) — eneste kjørbare fil i HEAD |
| **Runtime** | Ingen server, ingen database, ingen frontend-bundle |
| **Deploy-mål** | Ingen aktiv deploy; `npm run deploy:staging` er placeholder i CI |
| **Avhengigheter** | `mido` (Python, kun i CI); `eslint ^8.57.1` kun på usammenslåtte branches |
| **CI/CD** | `.github/workflows/ci-cd.yml` (3 plattformjobber + deploy) + `shared-ci-cd.yml` (gjenbrukbar mal) |
| **Hemmeligheter i kode** | Ingen funnet |
| **Supabase / RLS / Next.js** | Ikke implementert — seksjoner 2, 3, 4 i mandatet er ikke-appliserbare på dette stadiet |

Repoet har ingen API-ruter, ingen klientbundle, ingen database og ingen påloggingsflyt. Alle sikkerhetsfunn i denne revisjonen gjelder derfor utelukkende CI/CD-pipeline og git-hygiene.

---

## Funn

### 🔴 HØYT — CI/CD

---

#### F-01 · `ci-cd.yml` mangler `permissions:`-blokk

**Fil:** `.github/workflows/ci-cd.yml` — hele filen (ingen `permissions:` deklarert)  
**Alvorlighet:** Høy

**Problem:**  
Uten en eksplisitt `permissions:`-blokk arver alle jobs den organisasjonsvide standardverdien for `GITHUB_TOKEN`. Dersom organisasjonen (eller GitHub sin policy-endring) lar skriverettigheter stå som standard, vil enhver CI-jobb — inkludert jobber som kjøres på PRs fra eksterne forks via `pull_request`-triggeren — ha rett til å pushe kode, opprette releases og slette branches. Selv med read-only standard vil CodeQL-jobben mangle nødvendig `security-events: write`, slik at sikkerhetsresultater ikke lastes opp til GitHub Security-fanen.

En tidligere iterasjon av denne filen (commit `4b95a8d`, en usammenslått branch) inkluderte eksplisitt:

```yaml
permissions:
  contents: read
```

Dette ble droppet i den nåværende HEAD-versjonen.

**Foreslått fiks:**  
Legg til et workflow-nivå `permissions:`-direktiv med minste nødvendige rettigheter, og gi CodeQL-jobben et job-nivå override:

```yaml
permissions:
  contents: read

jobs:
  security-scan:
    permissions:
      contents: read
      security-events: write
```

---

### 🟠 MIDDELS — CI/CD

---

#### F-02 · GitHub Actions referert med mutable tag, ikke SHA

**Fil:** `.github/workflows/ci-cd.yml` linje 19, 23, 51, 54, 71, 88, 92, 97, 107  
**Fil:** `.github/workflows/shared-ci-cd.yml` linje 32, 35  
**Alvorlighet:** Middels

**Problem:**  
Alle actions er referert med semantisk tag (f.eks. `actions/checkout@v3`, `actions/setup-python@v5`, `github/codeql-action/init@v2`). Tags er mutable — en kompromittert vedlikeholder kan flytte tagen til en ny, ondsinnet commit uten å endre workflow-filen. Dette er et klassisk supply chain-angrep mot CI-systemer.

**Eksempler på nåværende referanser:**
```yaml
uses: actions/checkout@v3
uses: github/codeql-action/init@v2
uses: github/codeql-action/analyze@v2
```

**Foreslått fiks:**  
Pin alle actions til en spesifikk commit-SHA med en kommentar som angir tag-ekvivalenten:

```yaml
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
uses: github/codeql-action/init@v3@...  # pin SHA
```

Bruk Dependabot (allerede konfigurert for `github-actions`) til å holde SHA-er oppdatert automatisk — det er riktig kombinasjon av "låst versjon" og automatiske oppgraderinger.

---

#### F-03 · `static-analysis`-jobben kjører `npx eslint .` uten lokal konfig eller installasjon

**Fil:** `.github/workflows/ci-cd.yml` linje 81  
**Alvorlighet:** Middels

**Problem:**  
`npx eslint .` laster ned ESLint fra npm på kjøretidspunkt dersom det ikke er lokalt installert, og kjører det deretter i CI-miljøet med GITHUB_TOKEN tilgjengelig. To konsekvenser:

1. **Supply chain:** `npx` henter fra npm uten integritetssjekk. I teorien kan en kompromittert `eslint`-pakke eksfiltrere GITHUB_TOKEN eller andre secrets til en ekstern server.
2. **Ingen konfig → jobb feiler:** Det finnes ingen `.eslintrc.*`- eller `eslint.config.*`-fil i HEAD. ESLint uten config vil returnere feil eller advarsler som er konfigurasjonsavhengige. En `.eslintrc.json` eksisterer kun på en usammenslått branch (`commit 2ae6014`).

**Foreslått fiks:**  
Legg ESLint inn som en fastlåst `devDependency` i `package.json` og kjør via `npm run lint` (ikke `npx`). Legg til en `eslint.config.*`-fil i HEAD. Alternativt: guard-sjekk som allerede er gjort for `npm test`-steget.

---

#### F-04 · CodeQL scanner kun JavaScript; Python dekkes ikke

**Fil:** `.github/workflows/ci-cd.yml` linje 93  
**Alvorlighet:** Middels

**Problem:**  
`codeql-action/init` er konfigurert med `languages: 'javascript'`. Eneste reelle kode i HEAD er imidlertid Python (`generate_midi.py`). Python skannes ikke for sikkerhetssårbarheter via CodeQL. Dersom fremtidig Python-kode introduserer f.eks. shell-injeksjon (`subprocess` med brukerinput) eller usikker filoperasjoner, fanges det ikke opp.

En earlier branch-versjon (`commit b8581d5`) brukte en matrix-strategi som inkluderte Python:

```yaml
matrix:
  language: ['python', 'javascript']
```

**Foreslått fiks:**  
Bytt til matrise-scanning som nevnt over, eller bruk GitHub sin CodeQL "default setup" i repository-innstillingene (som automatisk oppdager languages).

---

#### F-05 · Ingen automatisk hemmelighets-skanning i PR-pipeline

**Fil:** `.github/workflows/ci-cd.yml`  
**Alvorlighet:** Middels

**Problem:**  
Det finnes ingen trufflehog-, gitleaks- eller GitHub Secret Scanning-step i CI-pipelinen. Dersom en utvikler ved en feil committer en API-nøkkel eller passord, fanges det ikke automatisk opp av noen workflow. `music-tools-agent-`-repoet har TruffleHog som eget workflow, men det er ikke implementert her.

Manuell gjennomgang av full git-historikk (`git log -p --all`) avdekket **ingen faktiske hemmeligheter** i dette repoet — men mangelen på automatisering betyr at fremtidige lekkasjer ikke fanges.

**Foreslått fiks:**  
Legg til et TruffleHog- eller gitleaks-steg i PR-workflowen:

```yaml
- name: Secret Scan
  uses: trufflesecurity/trufflehog@main  # pin til SHA
  with:
    path: ./
    base: ${{ github.event.repository.default_branch }}
    head: HEAD
```

---

### 🟡 LAV — CI/CD og git-hygiene

---

#### F-06 · `shared-ci-cd.yml` deklarerer `API_KEY`-secret men bruker den aldri

**Fil:** `.github/workflows/shared-ci-cd.yml` linje 22–23  
**Alvorlighet:** Lav

**Problem:**  
Workflowen aksepterer en secret kalt `API_KEY` som valgfri input, men refererer aldri til `${{ secrets.API_KEY }}` noe sted i workflow-kroppen. Denne «døde» secret-deklarasjonen er forvirrende: en fremtidig bidragsyter kan tro den er i bruk og sende den videre gjennom en usikker `run:`-kommando (f.eks. `echo $API_KEY`), eller hensikten med secreten er uklar.

**Foreslått fiks:**  
Fjern secret-deklarasjonen inntil den faktisk trengs, eller dokumenter tydelig i kommentar hva den skal brukes til og hvem som setter den.

---

#### F-07 · Python-avhengigheter i CI installeres uten versjons-pinning

**Fil:** `.github/workflows/ci-cd.yml` linje 58  
**Alvorlighet:** Lav

**Problem:**  
CI-steget kjører `pip install mido pytest` uten versjonsangivelse. Fremtidige builds kan dermed hente nyere versjoner automatisk, noe som kan:

- Introdusere en fremtidig sårbarhet i en ny versjon av `mido` uten at CI-pipelinen gir varsel
- Bryte tester dersom en ny versjon av pytest eller mido endrer API

`pip-audit` kjørt mot installert `mido`-versjon i dette miljøet viste **ingen kjente sårbarheter** per 2026-07-31.

**Foreslått fiks:**  
Legg `mido>=1.3,<2` og `pytest>=8,<9` i en `requirements-dev.txt` (filen eksisterer allerede på usammenslåtte branches, commit `8c85c84`) og bruk `pip install -r requirements-dev.txt` i CI.

---

#### F-08 · Ingen `.gitignore` i HEAD

**Fil:** Rot-katalogen — ingen `.gitignore` finnes  
**Alvorlighet:** Lav

**Problem:**  
En `.gitignore`-fil fantes i tidligere branches/commits (f.eks. `commit 121f13c`) men er ikke tilstede i HEAD på verken `main` eller den nåværende feature-branchen. Uten den kan følgende ved et uhell committes:

- `bassline.mid` — generert MIDI-fil fra `generate_midi.py`
- `__pycache__/`, `*.pyc`, `.pytest_cache/` — Python-mellomfiler
- `node_modules/` — når JS-avhengigheter legges til

Disse filene er ikke sensitive, men de øker støyen i historikken og gjør diffs vanskeligere å lese.

**Foreslått fiks:**  
Opprett `.gitignore` med minimum:

```
__pycache__/
*.py[cod]
.pytest_cache/
*.mid
node_modules/
npm-debug.log*
```

---

## Sammendrag

| ID | Alvorlighet | Funn | Status |
|---|---|---|---|
| F-01 | 🔴 Høy | Manglende `permissions:` i `ci-cd.yml` | Ufikset |
| F-02 | 🟠 Middels | Actions referert med mutable tag, ikke SHA | Ufikset |
| F-03 | 🟠 Middels | `npx eslint .` uten lokal installasjon eller konfig | Ufikset |
| F-04 | 🟠 Middels | CodeQL dekker ikke Python | Ufikset |
| F-05 | 🟠 Middels | Ingen hemmelighets-skanning i PR-pipeline | Ufikset |
| F-06 | 🟡 Lav | `API_KEY`-secret deklarert men aldri brukt | Ufikset |
| F-07 | 🟡 Lav | Python-avhengigheter uten versjons-pinning | Ufikset |
| F-08 | 🟡 Lav | Ingen `.gitignore` i HEAD | Ufikset |

**Positive funn:**
- Ingen hemmeligheter eller API-nøkler funnet i worktree eller full git-historikk (`git log -p --all`)
- Ingen `.env`-filer commitet, verken i HEAD eller historikk
- `pip-audit` mot `mido`: ingen kjente sårbarheter (2026-07-31)
- `pull_request`-triggeren (ikke `pull_request_target`) er korrekt konfigurert — forks får ikke tilgang til secrets
- `private: true` i historisk `package.json` hindrer utilsiktet npm-publisering

**Ikke-appliserbare seksjoner (pga. MVP 0.1-stadium):**
- Klient/server-lekkasje: ingen klientbundle
- API-endepunkter: ingen route handlers
- Database: ingen Supabase/RLS
- `npm audit`: ingen `package.json` i HEAD
