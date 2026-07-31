# Sikkerhetsaudit — MURMUROS

**Dato:** 2026-07-31
**Omfang:** Hele repoet (`Livsmestring/MURMUROS`), arbeidstre + full git-historikk (17 commits).
**Type:** Kun rapport — ingen endringer er utført.
**Verktøy:** gitleaks 8.18.4, `npm audit`, `pip-audit`, manuelle mønstersøk, kodegjennomgang.

---

## 0. Kartlegging av repoet

| Aspekt | Funn |
|--------|------|
| **Struktur** | Ett flatt repo (ingen monorepo/workspaces). MVP 0.1 — hovedsakelig dokumentasjon + tidlig scaffolding. |
| **Runtimes** | **Python 3.11** (`generate_midi.py` + `mido`; `core.py`/`agents.py`/`main.py` async pub/sub-demo; `pytest`). **Node ≥16** (`index.js` pipeline-modell; JSON Schema-validering med `ajv`; `eslint`). |
| **Prod-avhengigheter** | Kun `ajv` (JSON Schema). Treet er rent (ingen kjente sårbarheter). |
| **Dev-avhengigheter** | `eslint@8` (npm), `mido` + `pytest` (Python). |
| **Nettverk/tjenester** | **Ingen.** Ingen HTTP-server, ingen API-ruter, ingen webhooks, ingen utgående kall. `core.py` er en in-memory `asyncio`-kø, ikke en nettverkstjeneste. |
| **Database** | **Ingen.** Ingen Supabase, SQL eller ORM i repoet. |
| **Frontend/bundle** | **Ingen.** Ingen Next.js/React, ingen klientbundle, ingen miljøvariabler i bruk. |
| **Deploy** | Ingen reell deploy. `deploy:staging` er en placeholder (`echo`). CI-deploy-jobb er gated til `main`, men er en no-op. CodeQL «default setup» dekker Python + Actions. |

**Konsekvens for auditet:** Sjekkpunktene om klient/server-lekkasje (§2), endepunkter (§3) og database (§4) er i praksis **ikke relevante (N/A)** for dette repoet i dag — se begrunnelse under hver seksjon. Funnene ligger derfor i CI/CD, avhengigheter og git-hygiene.

---

## Sammendrag av funn

| # | Alvorlighet | Funn | Fil |
|---|-------------|------|-----|
| F1 | **Middels** | Template-/kommandoinjeksjon: `inputs.*-command` interpoleres rått i `run:` | `.github/workflows/shared-ci-cd.yml` |
| F2 | **Middels** | Gjenbrukbar workflow mangler eksplisitt `permissions:` (arver bred token-tilgang) | `.github/workflows/shared-ci-cd.yml` |
| F3 | **Middels** | GitHub Actions pinnet med flyttbar tag, ikke SHA (supply-chain) | begge workflows |
| F4 | **Middels** (nominelt *Høy*, kun dev) | 9 høye npm-sårbarheter i `eslint@8`-treet (`brace-expansion` DoS) | `package-lock.json` |
| F5 | **Lav** | `pytest 8.4.2` sårbar (PYSEC-2026-1845); versjonslås `<9` blokkerer fiksen | `requirements-dev.txt` |
| F6 | **Lav** | `.gitignore` mangler `.env*` — ingen vern mot fremtidig hemmelighet-commit | `.gitignore` |
| F7 | **Lav** | `ajv` deklarert som prod-avhengighet, men brukes kun i tester | `package.json:16-18` |
| F8 | **Lav** | CI bruker `npm install` i stedet for `npm ci` (ikke lockfile-tro) | `.github/workflows/ci-cd.yml:56` |

**Ingen kritiske funn. Ingen hemmeligheter funnet.**

---

## Detaljerte funn

### F1 — Middels: Kommandoinjeksjon via workflow-inputs
**Fil:** `.github/workflows/shared-ci-cd.yml:43-50` (også `secrets: API_KEY` linje 21-23)

```yaml
- name: Build the project
  if: ${{ inputs.build-command }}
  run: ${{ inputs.build-command }}      # linje 44
- name: Run tests
  run: ${{ inputs.test-command }}       # linje 47
- name: Deploy the project
  run: ${{ inputs.deploy-command }}     # linje 50
```

**Hvorfor det er et problem:** `inputs.*` interpoleres direkte inn i `run:`-skallet. Dette er GitHubs klassiske «script injection»-mønster. Kaller en workflow denne med input som stammer fra upålitelig kilde (f.eks. grenavn, PR-tittel, issue-tekst), kan vilkårlige shell-kommandoer kjøres på runneren — med tilgang til `secrets.API_KEY` og `GITHUB_TOKEN`. Selv om `workflow_call`-inputs normalt kommer fra en «betrodd» kallende workflow, er dette en injeksjonsflate som bør lukkes i en delt/gjenbrukbar mal.

**Foreslått fiks:** Send kommandoene via `env:` og referer dem som miljøvariabler i skriptet, aldri via direkte `${{ }}`-interpolering i `run:`:
```yaml
- name: Run tests
  env:
    TEST_CMD: ${{ inputs.test-command }}
  run: $TEST_CMD
```
Alternativt valider/whiteliste tillatte kommandoer. *(Merk: CLAUDE.md ber om at denne malen ikke MURMUROS-tilpasses — fiksen er en generisk herding, ikke prosjektspesifikk logikk.)*

---

### F2 — Middels: Gjenbrukbar workflow uten `permissions:`
**Fil:** `.github/workflows/shared-ci-cd.yml` (hele filen — ingen `permissions:`-blokk)

**Hvorfor det er et problem:** `ci-cd.yml` setter forbilledlig `permissions: contents: read` (linje 12-13), men den delte `shared-ci-cd.yml` har ingen `permissions:`-blokk. Da arver `GITHUB_TOKEN` repoets/organisasjonens standard, som i mange oppsett er `read-write`. Kombinert med F1 øker dette skadepotensialet ved en injeksjon eller kompromittert action.

**Foreslått fiks:** Legg til minste-privilegium øverst i `shared-ci-cd.yml`:
```yaml
permissions:
  contents: read
```
og løft eksplisitt kun de rettighetene et konkret steg trenger.

---

### F3 — Middels: Actions pinnet med tag i stedet for SHA
**Filer/linjer:**
- `.github/workflows/ci-cd.yml`: `actions/checkout@v3` (22, 42, 77, 108), `actions/setup-node@v3` (46), `actions/setup-python@v5` (25)
- `.github/workflows/shared-ci-cd.yml`: `actions/checkout@v3` (32), `actions/setup-node@v3` (35)

**Hvorfor det er et problem:** Flyttbare tags (`@v3`) kan repekes til ny kode. Blir en action-utgivers konto eller tag kompromittert, kjører ondsinnet kode i CI med `GITHUB_TOKEN` og evt. secrets. SHA-pinning gir uforanderlig referanse.

**Foreslått fiks:** Pinn til full commit-SHA med versjonskommentar, f.eks.:
```yaml
uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
```
Dependabot (`github-actions`, ukentlig) er allerede konfigurert og vil da holde SHA-ene oppdatert.

---

### F4 — Middels (nominelt Høy, kun dev): npm-sårbarheter i eslint-treet
**Fil:** `package-lock.json` (transitivt under `eslint@8.57.1`, devDependency)

`npm audit` rapporterer **9 høye** funn, alle med samme rot: `brace-expansion` (GHSA-mh99-v99m-4gvg, DoS/OOM), kaskadet gjennom `minimatch → @eslint/eslintrc → eslint`, `glob → rimraf → flat-cache → file-entry-cache`. `fixAvailable` peker på `eslint@10` (semver-major).

**Kontekst / reelt risikonivå:** Dette er **kun dev-avhengigheter** (en linter), ikke i noen prod-runtime eller bundle. Prod-treet (`ajv`) er rent. `package.json` har allerede en `overrides`-pinning av `brace-expansion` til `^1.1.18` (den bakportede vedlikeholds-utgaven på v1-linja), så den *installerte* koden er patchet — men `npm audit` flagger den fortsatt fordi rådataenes versjonsområde (`<=5.0.7`) ikke skiller ut bakport-grenen. Reell utnyttbarhet her (linting av eget, betrodd innhold) er lav.

**Foreslått fiks (valgfritt, avveid):** Oppgrader til `eslint@9`/`10` for å fjerne funnet helt — men det krever **Node ≥18** (CI kjører i dag Node 16). Dvs. det henger sammen med en beslutning om å heve Node-målet. Inntil da er `overrides`-pinningen en rimelig midlertidig demping.

---

### F5 — Lav: Sårbar `pytest` (dev), og versjonslås blokkerer fiksen
**Fil:** `requirements-dev.txt:3`

```
pytest>=8,<9
```
`pip-audit` finner `pytest 8.4.2` → **PYSEC-2026-1845**, fikset i **9.0.3**. Låsen `<9` gjør at den patchede versjonen aldri kan installeres.

**Hvorfor det er et problem:** Kun dev/test-verktøy (lav reell risiko), men versjonslåsen sementerer den sårbare versjonen.

**Foreslått fiks:** Løsne låsen til å tillate fiksen, f.eks. `pytest>=9.0.3` (verifiser at testsuiten fortsatt kjører — pytest 9 har enkelte breaking changes). `mido` har ingen kjente sårbarheter.

---

### F6 — Lav: `.gitignore` mangler `.env*`
**Fil:** `.gitignore`

**Hvorfor det er et problem:** Ingen `.env`-fil er committet i dag (verifisert i historikk), men det finnes ingen ignore-regel som hindrer at en `.env` med hemmeligheter ved et uhell blir committet senere.

**Foreslått fiks:** Legg til:
```
.env
.env.*
!.env.example
```

---

### F7 — Lav: `ajv` som prod-avhengighet brukes kun i tester
**Fil:** `package.json:16-18`

**Hvorfor det er et problem:** `ajv` importeres kun i `test/archetype.test.js`, ikke i `index.js` eller annen kjøretidskode. Å deklarere det under `dependencies` blåser opp prod-avhengighetsflaten unødvendig.

**Foreslått fiks:** Flytt `ajv` til `devDependencies`.

---

### F8 — Lav: CI bruker `npm install` i stedet for `npm ci`
**Fil:** `.github/workflows/ci-cd.yml:56`

**Hvorfor det er et problem:** `npm install` kan endre `package-lock.json` og hente andre transitive versjoner enn låst, noe som svekker reproduserbarhet og gjør supply-chain mindre forutsigbar i CI.

**Foreslått fiks:** Bruk `npm ci` i CI (krever at lockfilen er committet — den er det).

---

## Sjekkliste-status

### 1. Hemmeligheter — ✅ Rent
- **gitleaks (arbeidstre, `--no-git`):** `no leaks found`.
- **gitleaks (full historikk, 17 commits):** `no leaks found`.
- **Manuelt søk** etter `sk-`, `sbp_`, `whsec_`, `eyJ…`, `-----BEGIN`: ingen treff (utenom `package-lock.json`-integritetshasher, som ikke er hemmeligheter).
- **.env i historikk:** ingen `.env`/secret/`.pem`/`.key`-filer noensinne lagt til.

### 2. Klient/server-lekkasje — ⚪ N/A
Ingen frontend/bundle, ingen Next.js, ingen klientkomponenter, ingen `NEXT_PUBLIC_`-variabler — faktisk **ingen miljøvariabler i bruk** i det hele tatt. Ingen service-role-nøkler finnes. Ingenting kan lekke til en klientbundle som ikke eksisterer.

### 3. Endepunkter — ⚪ N/A
Ingen route handlers, API-ruter, HTTP-server, webhooks eller CORS-konfigurasjon i repoet. `core.py`/`agents.py` er en lokal `asyncio`-pub/sub-demo uten nettverk. Dermed ingen auth-/rate-limit-/signatur-/CORS-flater å vurdere.

### 4. Database — ⚪ N/A
Ingen Supabase, database, ORM eller SQL. Ingen RLS-policies å vurdere. Manuelt søk etter SQL med strenginterpolering: ingen treff.

### 5. Avhengigheter — ⚠️ Se F4, F5
- **npm:** 9 høye (alle dev, `brace-expansion`-kjede) — F4. Prod-tre (`ajv`) rent.
- **pip:** `pytest 8.4.2` (PYSEC-2026-1845) — F5. `mido` rent.
- **Prod vs dev:** i hovedsak korrekt skilt (`ajv` prod, `eslint` dev), men se F7.

### 6. CI/CD — ⚠️ Se F1, F2, F3
- **Write-permissions:** `ci-cd.yml` har korrekt `contents: read` ✅. `shared-ci-cd.yml` mangler `permissions:` — F2.
- **Actions med tag i stedet for SHA:** F3.
- **Secrets i logger / `pull_request_target`:** `ci-cd.yml` bruker `pull_request` (ikke `pull_request_target`) ✅ — ingen secret-eksponering mot fork-PR-er. Ingen `secrets` ekkoes i noe steg. Kommandoinjeksjon i den delte malen — F1.

### 7. Git-hygiene — ✅ Rent (+ F6)
- Ingen `.gitignore`-oppførte filer (`node_modules/`, `*.mid`, `__pycache__/`, `*.pyc`) finnes i historikken.
- Forbedring: legg til `.env*` — F6.

---

## Positive observasjoner
- ✅ Ingen hemmeligheter i arbeidstre eller historikk (gitleaks + manuelt).
- ✅ `ci-cd.yml` bruker minste-privilegium `permissions: contents: read`.
- ✅ Bruker `pull_request` (ikke `pull_request_target`) — trygt mot fork-PR-secret-lekkasje.
- ✅ Dependabot konfigurert for både npm (daglig) og GitHub Actions (ukentlig).
- ✅ Deploy-jobb er gated til `main`.
- ✅ Ingen farlige kodemønstre: ingen `eval`/`exec`/`subprocess`/`os.system`/`pickle` (Python), ingen `eval`/`child_process`/`new Function` (JS), ingen rå SQL, ingen utgående nettverkskall.
- ✅ Prod-avhengighetstre (`ajv`) uten kjente sårbarheter.

---

## Prioritert tiltaksliste (ingen utført)
1. **F1 + F2** — herd `shared-ci-cd.yml`: flytt `inputs.*-command` til `env:`, og legg til `permissions: contents: read`.
2. **F3** — SHA-pinn alle actions (Dependabot vedlikeholder dem videre).
3. **F4** — planlegg eslint 9/10 + Node ≥18 (henger sammen med Node-mål-beslutning); `overrides`-pinning demper i mellomtiden.
4. **F5** — løsne `pytest`-låsen slik at 9.0.3 kan installeres.
5. **F6, F7, F8** — små herdinger: `.env*` i `.gitignore`, `ajv` → devDependencies, `npm ci` i CI.
