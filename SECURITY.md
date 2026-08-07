# Sikkerhetspolicy

## Rapportere en sårbarhet

Ikke opprett en offentlig issue for sikkerhetsproblemer.

Bruk i stedet GitHubs private sårbarhetsrapportering: gå til **Security**-fanen i repoet og velg **"Report a vulnerability"**. Da når rapporten vedlikeholderne uten at detaljene blir offentlige.

Beskriv gjerne:

- Hva problemet er og hvor det ligger
- Hvordan det kan reproduseres
- Mulig konsekvens

Vi bekrefter mottak og følger opp så raskt vi kan.

## Støttede versjoner

Prosjektet er i tidlig utvikling (før 1.0). Kun `main`-grenen støttes med sikkerhetsoppdateringer.

## Prinsipper

MURMUROS lages for ungdom, og personvern og trygghet er kjerneverdier i prosjektet:

- Ingen ekte persondata i repoet — noensinne. Testdata skal alltid være fiktive.
- Ingen hemmeligheter (nøkler, passord, tokens) i kode eller historikk — bruk GitHub Secrets.
- Personvern (GDPR, med særlige hensyn til mindreårige) skal designes inn fra starten i alle datamodeller og funksjoner.
- CI kjører med minst mulig rettigheter (`permissions: contents: read`), og avhengigheter holdes oppdatert via Dependabot.
