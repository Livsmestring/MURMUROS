# Bidra til MURMUROS

Takk for at du vil bidra til MURMUROS! Dette dokumentet beskriver hvordan du kommer i gang og hva vi forventer av bidrag.

## Kom i gang

Du trenger:

- **Node.js 20+** (LTS)
- **Python 3.11+**

```bash
git clone https://github.com/Livsmestring/MURMUROS.git
cd MURMUROS

# Node-avhengigheter
npm ci

# Python-avhengigheter (for generate_midi.py og testene)
pip install -r requirements-dev.txt
```

## Arbeidsflyt

1. Opprett en egen gren (branch) fra `main` — commit aldri direkte til `main`.
2. Hold endringene små og fokuserte: én ting per pull request.
3. Åpne en pull request mot `main` med en tydelig beskrivelse av hva og hvorfor.
4. CI må være grønn før merge.

## Kjør sjekkene lokalt

Kjør de samme sjekkene som CI før du pusher:

```bash
npm test                 # JavaScript-tester
npm run lint             # ESLint
python -m pytest -q      # Python-tester
```

## Språk og stil

- Innhold og dokumentasjon skrives på **norsk**.
- Kode-identifikatorer og commit-meldinger kan være på engelsk.
- Alt vi bygger skal kunne knyttes til ett eller flere steg i MURMUROS-modellen (se README).

## Trygghet og personvern

MURMUROS lages for ungdom. Derfor gjelder alltid:

- **Aldri** legg ekte persondata (historier, navn, kontaktinfo) i repoet — heller ikke i testdata. Bruk alltid fiktive eksempler.
- **Aldri** legg hemmeligheter (API-nøkler, passord, tokens) i repoet. Bruk GitHub Secrets.

Se også [SECURITY.md](SECURITY.md) for hvordan du rapporterer sikkerhetsproblemer.

## Lisens for bidrag

MURMUROS er lisensiert i to deler, og bidrag følger den delen de hører til:

- **Kode** (`core/`, `index.js`, `schemas/`, `test/`, `tests/`, `.github/` med
  flere) lisensieres under **MIT** — se [LICENSE](LICENSE).
- **Innhold** (norsk narrativ- og kurstekst, arketypeinnholdet i
  `archetypes/`, pedagogisk materiale, grafikk og lyd) er
  **© DevByNorth, alle rettigheter forbeholdes** — se
  [LICENSE-CONTENT](LICENSE-CONTENT).

Når du åpner en pull request, bekrefter du at du har rett til å bidra med
innholdet, og at bidraget kan brukes i MURMUROS på vilkårene over. Bidra
aldri med materiale du ikke har rettigheter til — det gjelder også tekst,
bilder, lyd og musikk hentet fra andre kilder.
