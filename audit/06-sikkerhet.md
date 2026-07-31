# Sikkerhetsaudit — MURMUROS

**Dato:** 2026-07-31 (oppdatert etter remediering)
**Revisor:** Claude Code (automatisert + manuell gjennomgang)
**Revisjon gjelder:** `Livsmestring/MURMUROS`, branch `claude/test-coverage-analysis-wn6c7z`, alle branches inkl. full git-historikk

> Dette er en re-audit. Forrige versjon av denne rapporten (samme dato) identifiserte 8 funn i CI/CD-pipelinen. Alle 8 er siden rettet i commit `0fe1872` ("Harden CI/CD: permissions, SHA-pinned actions, secret scan, extensible structure"). Denne versjonen re-verifiserer hvert funn mot gjeldende kode og oppdaterer status.

---

## Kartlegging av repoet

| Dimensjon | Status |
|---|---|
| **Stadium** | MVP 0.1 — primært dokumentasjon og scaffolding |
| **Applikasjonskode** | `generate_midi.py` (Python) + `test_generate_midi.py` — eneste kjørbare filer i HEAD |
| **Runtime** | Ingen server, ingen database, ingen frontend-bundle |
| **Deploy-mål** | Ingen aktiv deploy; `npm run --if-present deploy:staging` er placeholder i CI |
| **Avhengigheter** | `mido`, `pytest` (Python, pinnet i `requirements-dev.txt`); ingen JS-avhengigheter i HEAD ennå |
| **CI/CD** | `.github/workflows/ci-cd.yml` (5 jobber: secret-scan, python, javascript, codeql, deploy) + `shared-ci-cd.yml` (gjenbrukbar mal) |
| **Hemmeligheter i kode** | Ingen funnet (verifisert på nytt) |
| **Supabase / RLS / Next.js** | Ikke implementert — seksjoner 2, 3, 4 i mandatet er fortsatt ikke-appliserbare |

Repoet har ingen API-ruter, ingen klientbundle, ingen database og ingen påloggingsflyt. Sikkerhetsbildet er derfor fortsatt utelukkende et CI/CD- og git-hygiene-spørsmål.

---

## Status på tidligere funn

### ✅ F-01 · Manglende `permissions:`-blokk — **RETTET**

**Fil:** `.github/workflows/ci-cd.yml` linje 10–11

```yaml
permissions:
  contents: read
```

Workflow-nivå `permissions: contents: read` er nå på plass. CodeQL-jobben har et eksplisitt job-nivå override (`security-events: write`, linje 89–91) begrenset til kun den jobben. GITHUB_TOKEN er nå read-only som standard for `secret-scan`, `python`, `javascript` og `deploy`.

**Verifisert:** Ja — lest direkte fra filen.

---

### ✅ F-02 · Actions referert med mutable tag — **RETTET**

**Fil:** `.github/workflows/ci-cd.yml` og `shared-ci-cd.yml`, alle `uses:`-linjer

Alle actions er nå pinnet til full commit-SHA med versjonskommentar, f.eks.:

```yaml
uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1  # v7.0.1
uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97  # v7.0.0
uses: actions/setup-node@820762786026740c76f36085b0efc47a31fe5020  # v7.0.0
uses: github/codeql-action/init@a2983b8bed1923f44751c5c43237f479442827b3  # v3.37.4
uses: trufflesecurity/trufflehog@6f3c981e7b77f235fd2702dd74af25fc4b72bf11  # v3.96.0
```

**Sideeffekt:** Oppgraderingen fra `codeql-action@v2` til `v3.37.4` løste også Dependabot-alarmen ("1 high") som GitHub rapporterte ved forrige push mot en deprecated v2-action.

**Merk:** Dependabot for `github-actions` (konfigurert i `.github/dependabot.yml`) vil fortsatt kunne foreslå oppdateringer av disse SHA-ene — det er tilsiktet og riktig kombinasjon av låst versjon + automatisk varsling.

---

### ✅ F-03 · `npx eslint .` uten lokal konfig — **RETTET**

**Fil:** `.github/workflows/ci-cd.yml`, `javascript`-jobben, linje 76–82

Lint-steget kjører nå betinget:

```yaml
- name: Lint (ESLint)
  run: |
    if [ -f package.json ] && npm run 2>/dev/null | grep -q '^\s*lint'; then
      npm run lint
    else
      echo "No lint script yet — skipping ESLint"
    fi
```

Kjører kun `npm run lint` (ikke `npx eslint` direkte) og kun dersom et `lint`-script faktisk finnes i `package.json`. Ingen runtime-nedlasting fra npm i CI før dette er reelt konfigurert.

---

### ✅ F-04 · CodeQL dekket ikke Python — **RETTET**

**Fil:** `.github/workflows/ci-cd.yml`, `codeql`-jobben, linje 84–98

```yaml
strategy:
  fail-fast: false
  matrix:
    language: [python, javascript-typescript]  # ← add languages here
```

Matrise-scanning er implementert. Begge relevante språk dekkes, og utvidelsespunktet er tydelig kommentert.

---

### ✅ F-05 · Ingen automatisk hemmelighets-skanning — **RETTET**

**Fil:** `.github/workflows/ci-cd.yml`, `secret-scan`-jobben, linje 16–25

TruffleHog kjører nå som egen jobb, først i pipelinen, med `fetch-depth: 0` (full historikk) og `--only-verified` for å redusere falske positiver. `deploy`-jobben har `secret-scan` i sin `needs`-liste, så en funnet hemmelighet blokkerer utrulling.

**Ny manuell verifisering (denne revisjonen):** Manuelt søk etter `sk-`, `sbp_`, `whsec_`, `eyJ`, `-----BEGIN` i arbeidstreet og full `git log -p --all` ga **ingen treff**. `gitleaks` var ikke tilgjengelig i dette miljøet for automatisert kjøring — TruffleHog-jobben i CI dekker dette hullet fremover, men en ekstern `gitleaks`-kjøring anbefales som engangsverifisering utenfor dette miljøet dersom det er ønskelig med et andre verktøy som kryssjekk.

---

### ✅ F-06 · Ubrukt `API_KEY`-secret — **RETTET**

**Fil:** `.github/workflows/shared-ci-cd.yml`

`secrets: API_KEY:`-blokken er fjernet fra `workflow_call`-inputs. Filen inneholder ikke lenger noen dødt secret-deklarasjon.

---

### ✅ F-07 · Python-avhengigheter uten pinning — **RETTET**

**Fil:** `requirements-dev.txt` (ny fil) + `.github/workflows/ci-cd.yml` linje 39

```
mido>=1.3,<2
pytest>=8,<10
```

CI installerer nå via `pip install -r requirements-dev.txt` i stedet for `pip install mido pytest`.

**Ny verifisering:** `pip-audit -r requirements-dev.txt` kjørt på nytt i denne revisjonen — **ingen kjente sårbarheter**.

---

### ✅ F-08 · Ingen `.gitignore` — **RETTET**

**Fil:** `.gitignore` (ny fil)

```
__pycache__/
*.py[cod]
.pytest_cache/
*.mid
node_modules/
npm-debug.log*
```

**Ny verifisering:** Gjennomgikk alle filer som noensinne har eksistert i git-historikken (`git log --all` + `git ls-tree -r` per commit) mot disse mønstrene — ingen `.mid`-filer, `__pycache__`, `.pyc`-filer eller `node_modules` er noensinne committet. `.gitignore` er derfor forebyggende, ikke opprydding av eksisterende problem.

---

## Nye observasjoner fra denne re-auditen

Ingen nye kritiske eller høye funn. To lave observasjoner verdt å notere for videre oppfølging:

### 🟡 O-01 · `gitleaks` ikke tilgjengelig for uavhengig verifisering i dette miljøet

**Alvorlighet:** Lav (informativ, ikke en sårbarhet)

Mandatet ba om at gitleaks kjøres i tillegg til manuelt søk. Verktøyet var ikke installert i dette CLI-miljøet, og kunne derfor ikke kjøres direkte mot verken arbeidstre eller full historikk her. TruffleHog dekker samme kategori (og kjører nå automatisk i CI via F-05-fiksen), men er et annet regelsett enn gitleaks. Vurder å kjøre gitleaks manuelt én gang via et miljø som har verktøyet installert, som en uavhengig kryssjekk av CI-scanneren.

### 🟡 O-02 · Ingen `CODEOWNERS` eller branch protection verifisert

**Alvorlighet:** Lav (utenfor kodebasen, kunne ikke verifiseres)

Denne revisjonen dekker kun det som er synlig i repoets filtre (workflows, kode, git-historikk). Branch protection-regler, required reviewers og GitHub Environment-secrets for `deploy`-jobben er repository-innstillinger som ikke er en del av git-historikken og kunne derfor ikke revideres herfra. Anbefaling: verifiser i GitHub Settings → Branches at `main` krever PR-review og grønn CI før merge, siden `deploy`-jobben kjører automatisk på push til `main`.

---

## Sammendrag

| ID | Alvorlighet | Funn | Status |
|---|---|---|---|
| F-01 | 🔴 Høy | Manglende `permissions:` i `ci-cd.yml` | ✅ Rettet (commit `0fe1872`) |
| F-02 | 🟠 Middels | Actions referert med mutable tag, ikke SHA | ✅ Rettet (commit `0fe1872`) |
| F-03 | 🟠 Middels | `npx eslint .` uten lokal installasjon eller konfig | ✅ Rettet (commit `0fe1872`) |
| F-04 | 🟠 Middels | CodeQL dekket ikke Python | ✅ Rettet (commit `0fe1872`) |
| F-05 | 🟠 Middels | Ingen hemmelighets-skanning i PR-pipeline | ✅ Rettet (commit `0fe1872`) |
| F-06 | 🟡 Lav | `API_KEY`-secret deklarert men aldri brukt | ✅ Rettet (commit `0fe1872`) |
| F-07 | 🟡 Lav | Python-avhengigheter uten versjons-pinning | ✅ Rettet (commit `0fe1872`) |
| F-08 | 🟡 Lav | Ingen `.gitignore` i HEAD | ✅ Rettet (commit `0fe1872`) |
| O-01 | 🟡 Lav | Gitleaks ikke kjørbart i dette miljøet (informativ) | Åpen — anbefalt engangskryssjekk |
| O-02 | 🟡 Lav | Branch protection / CODEOWNERS ikke verifiserbart herfra | Åpen — sjekkes i GitHub Settings |

**Positive funn (re-verifisert i denne revisjonen):**
- Ingen hemmeligheter eller API-nøkler funnet i worktree eller full git-historikk
- Ingen `.env`-filer noensinne committet
- `pip-audit` mot `requirements-dev.txt`: ingen kjente sårbarheter
- `pull_request`-triggeren (ikke `pull_request_target`) er korrekt brukt — forks får ikke tilgang til secrets
- Ingen filer som matcher `.gitignore`-mønstre finnes noensinne i historikken
- CI-pipelinen har nå least-privilege `permissions`, SHA-pinnede actions, automatisk secret-scanning og full CodeQL-språkdekning

**Ikke-appliserbare seksjoner (pga. MVP 0.1-stadium, uendret siden forrige revisjon):**
- Klient/server-lekkasje: ingen klientbundle
- API-endepunkter: ingen route handlers
- Database: ingen Supabase/RLS
- `npm audit`: ingen `package.json` i HEAD ennå
