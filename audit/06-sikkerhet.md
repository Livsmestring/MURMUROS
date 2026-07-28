# Sikkerhetsaudit — MURMUROS

**Dato:** 2026-07-09
**Omfang:** Hele repoet `Livsmestring/MURMUROS`, gren `claude/merge-request-review-bl05wr` (commit `743943d`), inkludert full git-historikk (17 commits).
**Verktøy:** gitleaks 8.24.3 (arbeidstre + full historikk), `npm audit`, `pip-audit`, manuelle mønstersøk, gjennomgang av workflows og historikk.
**Regel:** Kun rapportering — ingen endringer er utført.

---

## 0. Kartlegging: hva repoet består av

| Del | Innhold |
|---|---|
| Node.js-pakke | `package.json` (privat, `engines >=20`), `index.js` (pipeline-modell), `test/pipeline.test.js`. Ingen workspaces — én enkelt pakke i rot. |
| Python-prototype | `generate_midi.py` (frittstående MIDI-verktøy), pytest-suite i `tests/`, avhengigheter i `requirements-dev.txt` (mido, pytest). |
| CI/CD | `.github/workflows/ci-cd.yml` (lint, tester, deploy-plassholder) og `shared-ci-cd.yml` (gjenbrukbar mal for andre repo via `workflow_call`). CodeQL kjører via repoets «default setup», ikke i workflow. |
| Deploy | **Ingen reell deploy finnes.** `deploy:staging` er en echo-plassholder. Ingen hosting, ingen server, ingen klient-app. |
| Dokumentasjon | README, CLAUDE.md, CONTRIBUTING.md, SECURITY.md, LICENSE (MIT). |

Konsekvens for auditen: punktene **2 (klient/server-lekkasje)**, **3 (endepunkter)** og **4 (database)** er **ikke anvendbare** — det finnes ingen klientkomponenter, ingen API-ruter/webhooks/CORS-konfigurasjon, ingen Supabase eller annen database, og ingen SQL i repoet. Dette er verifisert ved gjennomgang av samtlige filer, ikke antatt. Punktene må tas opp igjen når `core/` og `website/` bygges (MVP 0.2+).

---

## 1. Funn, sortert etter alvorlighet

### KRITISK

Ingen kritiske funn.

### HØY

#### H1. GitHub Actions er ute av drift for hele organisasjonen — all sikkerhetsskanning og CI-gating er reelt avskrudd

- **Sted:** Org-nivå (GitHub-kontoen `Livsmestring`), ikke en fil i repoet.
- **Observasjon:** Alle Actions-kjøringer siden 5. juli feiler ~3 sekunder etter start, uten logger (HTTP 404 ved nedlasting). Dette rammer CI-pipelinen, CodeQL default setup **og** Copilot-review. Copilot-boten har selv bekreftet årsaken i PR #11: *«The job was not started because the account is locked due to a billing issue.»* Samme pipeline var grønn t.o.m. 4. juli.
- **Hvorfor det er et problem:** Så lenge kontoen er låst, kjøres verken tester, lint eller CodeQL-sikkerhetsskanning. Endringer kan merges uten noen automatisk verifikasjon, og nye sårbarheter vil ikke bli oppdaget. Et rødt-på-alt CI lærer også teamet å ignorere sjekker.
- **Foreslått fiks:** Org-admin må løse betalingsproblemet: GitHub → organisasjonen `Livsmestring` → *Settings → Billing and plans*. Deretter re-kjør sjekkene på åpne PR-er og verifiser at CodeQL default setup produserer resultater igjen.

### MIDDELS

#### M1. `shared-ci-cd.yml` mangler `permissions`-blokk — GITHUB_TOKEN arver standardrettigheter

- **Sted:** `.github/workflows/shared-ci-cd.yml` (hele filen; jobber defineres fra linje 25 uten `permissions`).
- **Hvorfor det er et problem:** Uten eksplisitt `permissions` får `GITHUB_TOKEN` organisasjonens/repoets standard, som kan være lese- **og skrive**tilgang til innhold. Malen kjører vilkårlige kommandoer (se M2) med dette tokenet i miljøet — et kompromittert bygg kan da pushe kode. Hoved-workflowen `ci-cd.yml` gjør dette riktig (`permissions: contents: read` på linje 12); malen gjør det ikke.
- **Foreslått fiks:** Legg til `permissions: contents: read` på toppnivå i `shared-ci-cd.yml`.

#### M2. `shared-ci-cd.yml` kjører rå input-strenger som shell-kommandoer

- **Sted:** `.github/workflows/shared-ci-cd.yml:44`, `:47`, `:51` (`run: ${{ inputs.build-command }}` osv.).
- **Hvorfor det er et problem:** Inputs fra kallende workflow interpoleres direkte inn i `run:`. For en gjenbrukbar mal er dette delvis by design, men det betyr at ethvert repo som kaller malen — og enhver som kan endre det kallende repoets workflow — kan kjøre vilkårlige kommandoer med malens token og secrets (`API_KEY` sendes også inn, linje 21–23). Tilliten er udokumentert.
- **Foreslått fiks:** Dokumentér i malen at den kun skal kalles fra betrodde repo i egen org; vurder å begrense inputs til et sett forhåndsdefinerte kommandoer (f.eks. en `enum`-aktig sjekk i et første steg), og send ikke `API_KEY` inn før den faktisk brukes (se L2).

#### M3. Sårbar transitiv npm-avhengighet: `brace-expansion` 1.1.15 (DoS)

- **Sted:** `package-lock.json:244` (`node_modules/brace-expansion`, transitiv under `eslint` → `minimatch`).
- **Observasjon:** `npm audit`: 1 sårbarhet, alvorlighet **high** — «DoS via exponential-time expansion» + «unbounded expansion length causing OOM». Fix er tilgjengelig.
- **Hvorfor det er et problem:** DoS i mønsterekspansjon. Kontekst demper: pakken er **kun dev-avhengighet** (`dev: true`) og brukes bare av ESLint i CI — den skipes ikke til noen produksjon (som ikke finnes ennå). Derfor middels, ikke høy.
- **Foreslått fiks:** `npm audit fix` (oppdaterer transitivt innenfor semver) og commit oppdatert `package-lock.json`. Dependabot vil også foreslå dette når org-kontoen låses opp.

#### M4. Sårbar Python-avhengighet: `pytest` 8.4.2 (PYSEC-2026-1845)

- **Sted:** `requirements-dev.txt:3` (`pytest>=8,<9` løser til 8.4.2).
- **Observasjon:** `pip-audit`: 1 kjent sårbarhet, fiks i **9.0.3**. Dagens pin `<9` blokkerer fiksen.
- **Hvorfor det er et problem:** Kjent sårbarhet i testrammeverket som kjøres i CI. Kun dev/test-kontekst (ingen produksjonskjøring), derfor middels.
- **Foreslått fiks:** Endre pin til `pytest>=9.0.3,<10` og verifiser at suiten passerer (pytest 9 har få brytende endringer for en suite av denne størrelsen).

### LAV

#### L1. Actions refereres med tag, ikke commit-SHA

- **Sted:** `.github/workflows/ci-cd.yml:22, 36, 39, 55, 58, 76, 79, 105` og `.github/workflows/shared-ci-cd.yml:32, 35` (alle `uses: actions/...@v4`/`@v5`).
- **Hvorfor det er et problem:** Tags kan flyttes; ved kompromittering av en action-utgiver kan `@v4` plutselig peke på ondsinnet kode (jf. tj-actions-hendelsen 2025). SHA-pinning gjør forsyningskjeden deterministisk.
- **Foreslått fiks:** Pin til full commit-SHA med tag som kommentar, f.eks. `uses: actions/checkout@<sha> # v4.x.y`. Dependabot (allerede konfigurert for `github-actions`) holder SHA-er oppdatert.

#### L2. `API_KEY`-secret deklarert men aldri brukt

- **Sted:** `.github/workflows/shared-ci-cd.yml:21–23`.
- **Hvorfor det er et problem:** En secret som aksepteres uten å brukes utvider angrepsflaten unødig (den ligger tilgjengelig for alle steg, inkludert de vilkårlige kommandoene i M2) og inviterer til udokumentert bruk.
- **Foreslått fiks:** Fjern deklarasjonen til den faktisk trengs, eller send den kun inn i det spesifikke steget som skal bruke den via `env:`.

#### L3. Deploy-jobben trigges også av nattlig cron

- **Sted:** `.github/workflows/ci-cd.yml:4–5` (schedule) sammen med `:101` (`if: github.ref == 'refs/heads/main'`).
- **Hvorfor det er et problem:** Ved `schedule`-kjøringer er ref `main`, så deploy-steget kjører hver natt — ikke bare ved push. I dag er det en harmløs echo-plassholder, men når ekte deploy kobles på blir dette en utilsiktet nattlig deploy.
- **Foreslått fiks:** Utvid betingelsen: `if: github.event_name == 'push' && github.ref == 'refs/heads/main'`. Bør gjøres **før** reell deploy innføres.

#### L4 (informasjon). Død betingelseslogikk i den delte malen

- **Sted:** `.github/workflows/shared-ci-cd.yml:43` og `:50` (`if: ${{ inputs.build-command }}`).
- **Hvorfor det nevnes:** Inputs har defaults, så betingelsene er alltid sanne — «valgfri» build/deploy kan i praksis ikke skrus av. Ikke en sårbarhet i seg selv, men det svekker antakelsen om at deploy-steget kan deaktiveres av kallende repo, som har sikkerhetsimplikasjoner den dagen deploy-kommandoen gjør noe reelt.
- **Foreslått fiks:** Fjern defaults og la kallende repo eksplisitt oppgi kommandoer, eller sammenlign mot tom streng.

---

## 2–4. Klient/server, endepunkter, database

**Ikke anvendbart i dag** — verifisert, ikke antatt:

- Ingen klient-/serverkode eksisterer (ingen Next.js, ingen komponenter, ingen bundling). Ingen miljøvariabler brukes i koden i det hele tatt (`process.env`/`os.environ` forekommer ikke).
- Ingen route handlers, API-ruter, webhooks eller CORS-konfigurasjon finnes.
- Ingen Supabase, ingen database, ingen SQL (rå eller ORM).

**Anbefaling for MVP 0.2+:** Når `core/`/`website/` bygges, gjenta denne auditen med fokus på disse tre punktene, og etabler RLS-policyer og auth-sjekker som del av første migrering — ikke i etterkant. Gitt målgruppen (mindreårige) bør datamodellene GDPR-vurderes før første persondata lagres (jf. prinsippene i SECURITY.md).

---

## 5. Hemmeligheter — rent

- **gitleaks** på arbeidstreet: 0 funn. På full historikk (17 commits, 78,7 kB): **0 funn**.
- Manuelle søk etter `sk-`, `sbp_`, `whsec_`, `eyJ…`, `-----BEGIN` i arbeidstre og full historikk: ingen reelle treff. (Ett falskt positiv: strengen `microtask-1.2.3` i `package-lock.json:1023` matcher `sk-1` — en npm-pakke-URL, ingen hemmelighet.)
- **Ingen `.env`-filer** er noen gang committet, heller ikke i historikken.

## 7. Git-hygiene — rent

- Ingen filer som matcher `.gitignore`-mønstre (`*.mid`, `__pycache__`, `node_modules/`, `.DS_Store`, `.env*`) finnes i historikken.
- Eneste slettede fil i historikken er `architecture.md` (dokumentasjon, ikke sensitiv).

---

## Oppsummering

| Alvorlighet | Antall | Funn |
|---|---|---|
| Kritisk | 0 | — |
| Høy | 1 | H1: Org-konto låst — CI og all sikkerhetsskanning ute av drift |
| Middels | 4 | M1 manglende permissions i delt mal · M2 rå kommando-inputs · M3 brace-expansion (npm, dev) · M4 pytest (pip, dev) |
| Lav | 4 | L1 tag- i stedet for SHA-pinning · L2 ubrukt API_KEY-secret · L3 deploy på cron · L4 død betingelseslogikk |

Repoet er i god sikkerhetsmessig stand for sitt nåværende innhold: ingen hemmeligheter i tre eller historikk, ren git-hygiene, minst-privilegium-token i hoved-workflowen, og ingen eksponerte flater (ingen server, API eller database ennå). Det viktigste enkelttiltaket er **å låse opp org-kontoen (H1)** — uten det er alle andre vernemekanismer (CI, CodeQL, Dependabot-oppdateringer, Copilot-review) i praksis avskrudd.

*Merknad utenfor sikkerhetsomfang: motstriden mellom README («alle rettigheter forbeholdes») og LICENSE (MIT) er et juridisk, ikke teknisk, funn — allerede rapportert i hovedauditen som B3.*
