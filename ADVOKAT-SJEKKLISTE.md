# ✅ ADVOKAT-SJEKKLISTE – HAR JEG SPURT OM ALT?

Bruk denne listen under og etter advokat-møtet for å sikre at du har dekket alt.

---

## 📋 FØR MØTET (Forberedelse)

- [ ] Lastet ned alle 6 juridiske dokumenter
- [ ] Lest ADVOKAT-PAKKE.md (forståelse av hva som skal diskuteres)
- [ ] Skrevet email til advokat med møte-forespørsel
- [ ] Avtalt møtetidspunkt (helst 2-3 timer)
- [ ] Sendt dokumenter til advokat dagen før møtet
- [ ] Laget liste over kritiske spørsmål (fra ADVOKAT-PAKKE.md)

---

## 🎯 UNDER MØTET – GDPR & PERSONVERN

**DATAINNSAMLING:**
- [ ] Advokat bekrefter: Navn, epost, aldersgruppe, profil-bilde = OK å samle
- [ ] Advokat sier: Lovlig datainnsamlings-grunnlag er **[samtykke/kontraktsmessig/annet]**
- [ ] Advokat bekrefter: Vi kan lagre bruker-historier og progresjon
- [ ] **Handling:** Notér hvilke grunnlag advokaten anbefaler

**FORELDRE-SAMTYKKE:**
- [ ] Advokat sier: Vi trenger foreldre-godkjenning for brukere under **[13/16/18]** år
- [ ] Advokat forklarer: Hvordan implementerer vi det? (Digitalt? Papir?)
- [ ] Advokat sier: Hvor lenge lagrer vi samtykke-dokumenter? (**[1/3/5]** år)
- [ ] **Handling:** Få konkret prosedyre for foreldre-godkjenning

**DATABEHANDLERE:**
- [ ] Advokat bekrefter: Supabase + AWS = OK som databehandlere
- [ ] Advokat sier: DPA (Data Processing Agreement) må inneholde **[liste av krav]**
- [ ] Advokat sjekker: Allerede på plass med Supabase? (Ja/nei → handling)
- [ ] **Handling:** Få DPA-mal eller instruks for å få på plass

**SLETTING & PRIVATHET:**
- [ ] Advokat sier: Bruker kan be om sletting innen **[30/60/90]** dager
- [ ] Advokat sier: Vi må slette data UNNTATT **[logg/backup/annet]**
- [ ] Advokat bekrefter: Retten til dataportabilitet (Art. 20 GDPR)
- [ ] **Handling:** Implementer sletting-prosess teknisk

**DATALEKKASJE:**
- [ ] Advokat sier: Hvis data lekker, må vi varsle innen **72 timer**
- [ ] Advokat sier: Varsle **[bruker/Datatilsynet/begge]** først
- [ ] Advokat sier: Kontakt Datatilsynet på: **[epost/telefon]**
- [ ] **Handling:** Lag incident response-plan for datalekkasje

---

## 🎯 UNDER MØTET – BARNEVERNSLOVEN

**ANSVAR SOM PLATTFORM:**
- [ ] Advokat sier: Vi har juridisk ansvar for bruker-sikkerhet
- [ ] Advokat sier: Vi MÅ moderere innhold (ikke valgfritt)
- [ ] Advokat sier: Vi MÅ rapportere tegn på misbruk
- [ ] **Handling:** Dokumenter ansvar i intern policy

**RAPPORTERINGSPLIKT:**
- [ ] Advokat sier: Tegn på **[misbruk/neglekt/vold/seksuelt overgrep]** = rapporter
- [ ] Advokat sier: Rapporter til **[lokal barnevernstjeneste/Politiet/begge]**
- [ ] Advokat sier: Tidsramme: **[umiddelbar/samme dag/innen 24 timer]**
- [ ] Advokat sier: Rapporter selv om usikker (ikke nødvendig sikkerhet)
- [ ] **Handling:** Lag checklist for når vi rapporterer

**MODERASJONS-ANSVAR:**
- [ ] Advokat bekrefter: Vi kan fjerne hatefullt/seksuelt/voldelig innhold
- [ ] Advokat sier: Vi kan suspend/block brukere som bryter regler
- [ ] Advokat sier: Vi MÅ dokumentere alle moderasjons-beslutninger
- [ ] Advokat sier: Oppbevare logg i **[1/2/5]** år (juridisk krav)
- [ ] **Handling:** Sett opp dokumentering-system (spreadsheet/database)

**ANSVAR VIS-À-VIS BARN:**
- [ ] Advokat sier: Vi må beskytte barn fra grooming/seksuell kontakt
- [ ] Advokat sier: Private meldinger mellom brukere – må vi moderere? (Ja/nei)
- [ ] Advokat sier: Hvis barn blir misbrukt på plattformen, ansvar er **[oss/bruker/begge]**
- [ ] **Handling:** Implementer tekniske sikkerhetstiltak basert på råd

---

## 🎯 UNDER MØTET – FORBRUKERLOVEN & BETALING

**BRUKERBETALINGER:**
- [ ] Advokat sier: Abonnement – bruker kan kansellere når som helst? (Ja/nei)
- [ ] Advokat sier: Returrett – bruker kan få pengene tilbake innen **14** dager
- [ ] Advokat sier: Unntakelser fra returrett? (Digitalt innhold → **[ja/nei]**)
- [ ] Advokat sier: Hva hvis bruker er under 18 år? (Trenger foreldre-godkjenning?)
- [ ] **Handling:** Oppdater betalings-vilkår

**BRUKSVILKÅR:**
- [ ] Advokat godkjenner: Innhold i bruksvilkårene (punkt 1-8)
- [ ] Advokat sier: Ansvarsbegrensning ("As-Is") = juridisk OK? (Ja/nei)
- [ ] Advokat sier: Vi kan unngå ansvar for **[indirekte skader/brukeres data/annet]**?
- [ ] Advokat sier: Må vi ha disclaimer om ikke-tilgjengelighet? (Ja/nei)
- [ ] **Handling:** Revider bruksvilkårene basert på tilbakemeldinger

**FAKTURAER & SKATT:**
- [ ] Advokat sier: Hva skal stå på faktura? (Org.nr, adresse, MVA?)
- [ ] Advokat sier: Vi er **[momsplikt/momsfritt]** (avklart?)
- [ ] Advokat sier: Kontakt: **[Skatteetaten/Revisor]** for skattekonfig
- [ ] **Handling:** Sett opp fakturering riktig

---

## 🎯 UNDER MØTET – PARTNER-AVTALE

**PARTNER-VILKÅR:**
- [ ] Advokat godkjenner: Provisjon-modell (15-25%)
- [ ] Advokat sier: Kan partner markedsføre fritt? (Regler? Godkjenning?)
- [ ] Advokat sier: Kan vi kansellere partner-avtale? (Tidsramme: **30** dager?)
- [ ] Advokat sier: Hva hvis partner bryter reglene? (Suspension? Block?)
- [ ] **Handling:** Revider partner-avtale basert på råd

**IP-RETTIGHETER:**
- [ ] Advokat bekrefter: Partner kan IKKE bruke MURMUROS-logo uten godkjenning
- [ ] Advokat bekrefter: Partner eier IKKE opphavsretten til markedsføring-materiale
- [ ] Advokat sier: Hva ved oppsigelse? (Partner sletter alt brukt materiale?)
- [ ] **Handling:** Legg inn IP-klausul i partner-avtale

**ANSVAR:**
- [ ] Advokat sier: Hvem er ansvarlig hvis partner gjør noe ulovlig?
- [ ] Advokat sier: Kan vi holdes ansvarlig for partner-markedsføring? (Ja/nei)
- [ ] Advokat sier: Disclaimer i partner-avtale? (Ja/nei)
- [ ] **Handling:** Legg inn ansvarsbegrensning

---

## 🎯 UNDER MØTET – FORSIKRING & RISK

**ANSVARSFORSIKRING:**
- [ ] Advokat anbefaler: Vi burde ha ansvarsforsikring? (Ja/nei)
- [ ] Advokat sier: Type: **[Profesjonell ansvarsforsikring/Cyberliaility/begge]**
- [ ] Advokat sier: Minimums-dekning: **[1/5/10]** millioner NOK
- [ ] Advokat sier: Kontakt forsikringsmegler: **[navn/telefon]**
- [ ] **Handling:** Kartlegg forsikringsalternativer

**JURIDISK DEKNING:**
- [ ] Advokat sier: Hvis bruker suer oss, hvem dekker juridiske kostnadier?
- [ ] Advokat sier: Vi trenger **[rettshjelpsforsikring/annet]**? (Ja/nei)
- [ ] **Handling:** Undersøk rettshjelpsforsikring

---

## 🎯 ETTER MØTET – HANDLING

**DOKUMENTER TIL REVISJON:**
- [ ] Advokat sender: Revidert personvernvedtekt
- [ ] Advokat sender: Revidert bruksvilkår
- [ ] Advokat sender: Revidert partner-avtale
- [ ] Advokat sender: DPA-mal (for Supabase/AWS)
- [ ] Advokat sender: Barnevernspolicy feedback
- [ ] Advokat sender: Invoicing/møte-oppsummering

**DIN HANDLING:**
- [ ] Implementer alle advokat-tilbakemeldinger
- [ ] Oppdater MURMUROS-Intern-Barnevernspolicy.docx basert på krav
- [ ] Oppdater MURMUROS-Moderasjons-rutiner.docx (rapporteringsplikt osv.)
- [ ] Lag DPA (eller få Supabase til å undertegne advokat sin mal)
- [ ] Sett opp dokumentering-system (logg av moderasjons-beslutninger)
- [ ] Kontakt forsikringsmegler (hvis anbefalt)
- [ ] **Tegn advokat-avtale** (få kvittering)

**ENDELIG SJEKK:**
- [ ] Alle 6 dokumenter er nå juridisk godkjent
- [ ] Du vet eksakt hvem du rapporterer til (barnevernstjeneste/politiet)
- [ ] Du vet hvordan du dokumenterer allt (logg-system)
- [ ] Du har forsikring på plass (eller bekreftet at det ikke er nødvendig)
- [ ] Du er klar for moderator-team (jur. grunnlag solid)

---

## 💬 SPØRSMÅL TIL NOTERE HVIS DU IKKE FORSTÅR SVARET

(Spør advokaten igjen eller søk på internett)

- [ ] Spørsmål 1: ___________________________________________________________
- [ ] Spørsmål 2: ___________________________________________________________
- [ ] Spørsmål 3: ___________________________________________________________

---

## 📅 TIDSPLAN ETTER MØTET

| Aktivitet | Frist | Status |
|-----------|-------|--------|
| Advokat sender reviderte dokumenter | Uke 2 | ☐ |
| Du implementerer tilbakemeldinger | Uke 3 | ☐ |
| Advokat godkjenner sluttversjon | Uke 3 | ☐ |
| Tegn advokat-avtale + betaling | Uke 3 | ☐ |
| **Juridisk grunnlag = KLAR** | **Uke 4** | ☐ |

---

**Versjon:** 1.0
**Dato:** September 2026
**Status:** Klar for bruk under advokat-møte
