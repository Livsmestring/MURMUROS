# 📋 ADVOKAT-PAKKE – MURMUROS

**Formål:** Juridisk gjennomgang av en ungdomsempowerment-plattform

**Status:** MVP 0.1 – Klar for juridisk validering før launch

---

## 🎯 MØTE-AGENDA (2-3 timer)

### DEL 1: KONTEKST (15 min)
- Hva er MURMUROS? (livsmestring-plattform for ungdom)
- Brukergruppe: Hovedsakelig 13-18 år (noen yngre, noen eldre)
- Teknologi: Web-plattform (Supabase backend, React frontend)
- Forretningsmodell: 
  - Abonnement for brukere
  - Lisenser til skoler/organisasjoner
  - Partner-provisjon (affiliate/reseller)

### DEL 2: JURIDISKE KRAV (60 min)

**PRIORITET 1: GDPR & PERSONVERN**
- Brukerne er barn/ungdom → Spesielle krav
- Samler: Navn, epost, aldersgruppe, profilbilde, brukerhistorie
- Databehandlere: Supabase (database), AWS (backup)
- Spørsmål for advokat:
  - ✓ Hva er lovlig datainnsamlings-grunnlag? (Samtykke? Kontraktsmessig?)
  - ✓ Når trenger vi foreldre-samtykke? (Under 13? 16? 18?)
  - ✓ Hva skal DPA (Data Processing Agreement) inneholde?
  - ✓ Hvor lenge kan vi lagre data?
  - ✓ Hva hvis bruker vil slette alt (retten til å bli glemt)?

**PRIORITET 2: BARNEVERNSLOVEN**
- Plattformen tjener barn → Lovpliktig ansvar
- Vi skal ha moderasjon av innhold
- Tegn på misbruk → Rapportering til barnevernstjenesten
- Spørsmål for advokat:
  - ✓ Hva er vår juridiske ansvar som plattform-eier?
  - ✓ Når må vi rapportere til barnevernstjenesten? (Hvilke tegn?)
  - ✓ Hvordan dokumenterer vi at vi fulgte reglene?
  - ✓ Hva hvis et barn misbrukes på plattformen – hva er vår ansvar?
  - ✓ Trenger vi særskilt forsikring (ansvarsforsikring)?

**PRIORITET 3: FORBRUKERLOVEN & E-HANDEL**
- Vi tar betaling fra brukere (abonnement)
- Vi selger til skoler/organisasjoner
- Spørsmål for advokat:
  - ✓ Hvilke opplysninger må på faktura?
  - ✓ Hva er returretten? (14 dager? Annet?)
  - ✓ Hvordan håndteres refusjon?
  - ✓ Hva skal bruksvilkårene dekke konkret?
  - ✓ Hva om brukeren er under 18 år – trenger vi foreldre-godkjenning for betaling?

**PRIORITET 4: INNHOLDSANSVAR & OPPHAVSRETT**
- Brukere laster opp historier, kunstneri, musikk
- Vi modererer innholdet
- Spørsmål for advokat:
  - ✓ Hvem eier opphavsretten? (Bruker? Vi? Begge?)
  - ✓ Kan vi bruke bruker-innhold for markedsføring? (Krav om samtykke?)
  - ✓ Hva hvis bruker laster opp opphavsrettsbeskyttet musikk?
  - ✓ Hva hvis innholdet er hatefullt eller seksuelt?

---

## 📄 DOKUMENTER SOM MÅ GJENNOMGÅS

### Offentlige dokumenter (bruker-facing):
1. ✅ **MURMUROS-Personvernvedtekt.docx** 
   - Status: MAL, trenger tilpasning + godkjenning
   - Advokat skal: Validere GDPR-compliance, sjekke foreldre-samtykke-regler

2. ✅ **MURMUROS-Bruksvilkar.docx**
   - Status: MAL, trenger tilpasning + godkjenning
   - Advokat skal: Sikre juridisk dekning, returrett, ansvarsbegrensning

3. ✅ **MURMUROS-Partner-avtale.docx**
   - Status: MAL, trenger tilpasning + godkjenning
   - Advokat skal: Validere provisjon-modell, IP-rettigheter, avslutningsbetingelser

### Private dokumenter (intern bruk):
4. ✅ **MURMUROS-Intern-Barnevernspolicy.docx**
   - Status: GUIDE, trenger juridisk validering
   - Advokat skal: Sikre at policy oppfyller barnevernsloven-krav

5. ✅ **MURMUROS-Moderasjons-rutiner.docx**
   - Status: GUIDE, trenger juridisk review
   - Advokat skal: Validere rapporteringsplikt, dokumentering

6. ✅ **MURMUROS-Incident-Response-Plan.docx**
   - Status: GUIDE, trenger juridisk review
   - Advokat skal: Sikre at prosedyrer er juridisk korrekte

---

## ⚠️ KRITISKE SPØRSMÅL

**Databehandling:**
- [ ] DPA (Data Processing Agreement) – hva må stå i den?
- [ ] Datatilbaketrekking – hvordan implementerer vi det teknisk + juridisk?
- [ ] Datalekkasje – meldingsplikt innen 72 timer. Hvem skal vi varsle?

**Barn & Ungdom:**
- [ ] Alder-grense for platform? (13+? 16+? 18+?)
- [ ] Når trenger vi foreldre-samtykke? (Hva sier lov?)
- [ ] Profil-synlighet – hvem kan se hvem?
- [ ] Private meldinger mellom brukere – må vi moderere dem?

**Moderasjon & Rapportering:**
- [ ] Hvilke tegn på misbruk krever rapportering til barnevernstjenesten?
- [ ] Tidsramme for rapportering? (Umiddelbar? Innen 24 timer?)
- [ ] Hvem skal rapportere? (Alle ansatte? Bare leder?)
- [ ] Dokumentering – hva skal vi lagre og hvor lenge?

**Betalinger & Forbrukerloven:**
- [ ] Kan vi ta betaling fra brukere under 18 år? (Krav om foreldre-godkjenning?)
- [ ] Hva om bruker "ångrer" og vil tilbake? (14-dagers returrett?)
- [ ] Abonnement – kan bruker kansellere når som helst?
- [ ] Prislisting – hva må vi vise? (Skatt? Valutakurs?)

**Ansvar & Forsikring:**
- [ ] Hva er vår juridiske ansvar hvis noe går galt?
- [ ] Disclaimer/ansvarsbegrensning – hva kan vi skrive?
- [ ] Trenger vi ansvarsforsikring? (Type, dekning?)

---

## 📊 TIDSPLAN

| Fase | Hva | Frist |
|------|-----|-------|
| **Møte** | Advokat-konsultasjon (2-3 timer) | 1 uke |
| **Review** | Advokat gjennomgår dokumenter | +1 uke |
| **Revideringer** | Du implementerer tilbakemeldinger | +1 uke |
| **Godkjenning** | Advokat godkjenner alle dokumenter | +1 uke |
| **KLAR FOR LAUNCH** | Juridisk fundament på plass | Uke 4 |

**Total tidsramme: 3-4 uker**

---

## 💼 ADVOKAT-VALG

**Du trenger en advokat som:**
- ✓ Spesialiserer seg i GDPR/personvern
- ✓ Har erfaring med barnevernsloven
- ✓ Forståelse for tech/platform-modeller
- ✓ Kjennskap til norsk forbrukerrett

**Anbefalt søk:**
- Advokatsamfunnet.no (søk på "GDPR barnevernsloven")
- Teknologi-rettet advokatkontorer (ofte mer tech-vennlig)
- Sjekk referanser fra andre ungdomsplattformer

**Kostnadsestimat:**
- Initial konsultasjon: 3-5 timer → ~15.000-25.000 NOK
- Dokumentgjennomgang: ~10.000-20.000 NOK
- Revideringer og godkjenning: ~10.000-20.000 NOK
- **Total: ~35.000-65.000 NOK** (prisgunstig investering for juridisk trygghet)

---

## 📧 EMAIL-TEMPLATE TIL ADVOKAT

```
Emne: Juridisk gjennomgang – MURMUROS ungdomsplattform

Hei [Advokat-navn],

Vi utvikler MURMUROS, en norskspråklig ungdomsempowerment-plattform som 
kombinerer storytelling, musikk og teknologi for personlig vekst.

Vi trenger juridisk gjennomgang av:
1. Personvernpolicy (GDPR)
2. Bruksvilkår (inkl. betaling, forbrukerloven)
3. Partner-avtale (affiliate/reseller-modell)
4. Barnevernsloven-compliance (moderasjon, rapportering)

Brukergruppe: Ungdom 13-18 år
Databehandlere: Supabase, AWS
Forretningsmodell: Abonnement + partner-provisjon

Vedlagt: Dokumenter som skal gjennomgås

Kan du tilby en initial konsultasjon på 2-3 timer?

Takk,
[Ditt navn]
```

---

## ✅ ETTER ADVOKAT-MØTET

**Når advokaten er ferdig, skal du ha:**
- ☐ Godkjente juridiske dokumenter (personvernvedtekt, bruksvilkår, partner-avtale)
- ☐ DPA (Data Processing Agreement) klar for Supabase/AWS
- ☐ Klar forståelse av rapporteringsplikt til barnevernstjenesten
- ☐ Barnevernspolicy validert
- ☐ Juridisk akseptabel moderasjons-prosess
- ☐ Ansvarsforsikring rekomendert (ja/nei)

**Neste steg:** Moderator-team og teknisk oppsett (barnevernspolicy + moderasjons-panel)

---

**Versjon:** 1.0
**Dato:** September 2026
**Status:** Klar for advokat-presentasjon
