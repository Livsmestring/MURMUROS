# MurMur Task Block

Standardmal for alle oppdrag som sendes til Claude Code.
Plassering i repo: `docs/prompts/murmur-task-block.md`

---

## Hvorfor malen finnes

Claude Code er sterk på utførelse og svak på å vite når noe er ferdig.
Malen flytter «ferdig» fra magefølelse til noe som kan sjekkes, og
plasserer beslutningene hos deg i stedet for hos modellen.

Fire faste deler, alltid i samme rekkefølge:

| Del | Formål | Hva som går galt uten den |
|---|---|---|
| KONTEKST | Hvor er vi, hva finnes fra før | Modellen gjetter på filstruktur og navn |
| OPPDRAG | Hva som skal skje, i nummererte steg | Arbeidet blir usammenhengende |
| AKSEPTKRITERIER | Hvordan du vet det er ferdig | Halvferdig output som ser ferdig ut |
| PORTER | Hvor den skal stoppe og spørre | Modellen tar beslutninger som er dine |

---

## Malen

```
# OPPDRAG: <kort tittel>

## KONTEKST
<Hvor i MurMur-porteføljen hører dette hjemme.>
<Hvilket repo, hvilken branch, hvilke filer som allerede finnes.>
<Hva som er forsøkt før, hvis relevant.>
<Hva jeg IKKE vet — si det eksplisitt, så slipper modellen å gjette.>

## OPPDRAG
1. <Første steg — konkret handling, ikke mål.>
2. <Andre steg.>
   a. <Delsteg når rekkefølgen betyr noe.>
3. <Siste steg — vanligvis dokumentasjon eller oppsummering.>

## AKSEPTKRITERIER
- <Noe som kan verifiseres — fil finnes, test passerer, kommando gir 0.>
- <Ett kriterium per linje.>
- <Ta med minst ett negativt kriterium: hva som IKKE skal ha skjedd.>

## PORTER
- Stopp etter steg <N> og vent på godkjenning
- Kjør på ETT tilfelle først, vis resultat, vent på «kjør resten»
- Ved tvil om <navn/sti/valg>: spør, ikke gjett
- Ikke commit til main uten at akseptkriteriene er verifisert
```

---

## Regler som gjelder alle oppdrag

**Skriv negative kriterier.** «Ingen repo er slettet» fanger feil som
positive kriterier aldri fanger.

**Én port per beslutning som koster penger eller er irreversibel.**
Arkivering, deploy, sletting, secret-rotasjon, DNS. Aldri automatisk.

**Si hva du ikke vet.** Setningen «jeg vet ikke de eksakte repo-navnene»
er mer verdt enn tre avsnitt med kontekst. Den forhindrer den vanligste
feilen: at modellen finner på et plausibelt navn.

**Batch-oppdrag kjøres alltid 1 → vis → resten.** Gjelder alt som
gjentas over flere repoer, filer eller kunder.

**Ikke be om «produksjonsklar kode» i oppdraget.** Skriv heller
akseptkriteriet som gjør den produksjonsklar: tester passerer, ingen
`TODO` igjen, typesjekk grønn.

---

## Varianter

### Kodeoppdrag
Legg til under AKSEPTKRITERIER:
```
- `npm run typecheck` gir exit 0
- `npm test` passerer, ingen skipped
- Ingen nye ESLint-warnings
- Ingen hardkodede secrets eller URL-er
```

### Arkitekturoppdrag
Bytt ut OPPDRAG med:
```
1. Les <filer> og oppsummer nåværende struktur. STOPP.
2. Foreslå 3-5 alternativer med fordeler, ulemper, kompleksitet,
   ytelse, skalerbarhet og vedlikeholdbarhet. STOPP.
3. Implementer valgt alternativ etter min beslutning.
```

### Opprydding / migrering
Legg alltid til under PORTER:
```
- Ingen destruktive kommandoer uten eksplisitt godkjenning per tilfelle
- Vis dry-run før faktisk kjøring
```

---

## Bruk

1. Kopier malen.
2. Fyll ut de fire delene. Bruk 5 minutter — det sparer en time.
3. Lim inn i Claude Code.
4. Svar på portene. Ikke la modellen passere dem selv.
