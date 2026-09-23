const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell, WidthType, BorderStyle } = require('docx');
const fs = require('fs');

// Utility functions
const normal = (text, options = {}) => new TextRun({
  text,
  size: options.size || 22,
  font: 'Calibri',
  ...options
});

const heading = (text, level = 1) => new Paragraph({
  text: new TextRun({
    text,
    bold: true,
    size: 24 + (3 - level) * 4,
    font: 'Calibri'
  }),
  heading: level === 1 ? HeadingLevel.HEADING_1 : level === 2 ? HeadingLevel.HEADING_2 : HeadingLevel.HEADING_3,
  spacing: { before: 240, after: 120 }
});

const section = (title) => new Paragraph({
  text: new TextRun({
    text: title,
    bold: true,
    size: 24,
    font: 'Calibri'
  }),
  spacing: { before: 200, after: 100 }
});

// === 1. INTERN BARNEVERNSPOLICY ===
const safeguardingPolicy = new Document({
  sections: [{
    properties: {},
    children: [
      heading('INTERN BARNEVERNSPOLICY – MURMUROS', 1),
      new Paragraph({
        text: new TextRun({
          text: 'Versjon 1.0 | Gjelder fra September 2026 | Kun for internt bruk',
          italic: true,
          size: 20
        }),
        spacing: { after: 240 }
      }),

      section('1. FORMÅL'),
      new Paragraph({ text: normal('MURMUROS har en absolutt nulltoleranse for misbruk av ungdommer. Denne policyen sikrer at vi:') }),
      new Paragraph({ text: normal('✓ Beskytter ungdommer fra skade, misbruk og utnytting'), spacing: { before: 100 } }),
      new Paragraph({ text: normal('✓ Etablerer klare rutiner for håndtering av bekymringsverdig adferd') }),
      new Paragraph({ text: normal('✓ Dokumenterer hendelser for juridisk dekning') }),
      new Paragraph({ text: normal('✓ Følger barnevernsloven og andre relevante lover'), spacing: { after: 200 } }),

      section('2. ANSVAR OG ROLLER'),
      new Paragraph({ text: normal('**Platform-leder:** Overordnet ansvar for barnevernspolicy, årlig audit, trening av team') }),
      new Paragraph({ text: normal('**Innholdsmoderatorar:** Daglig gjennomgang, rapportering, blokkering av brukere') }),
      new Paragraph({ text: normal('**Teknisk team:** Sikkerhet, logging, og rapporteringsverktøy') }),
      new Paragraph({ text: normal('**Alle ansatte:** Obligatorisk barnevernstrening når de starter'), spacing: { after: 200 } }),

      section('3. RISIKER OG TEGN PÅ MISBRUK'),
      new Paragraph({ text: normal('**Tegn å være obs på:**') }),
      new Paragraph({ text: normal('🚩 Voksne som kontakter ungdommer privat (\\\"grooming\\\")'), spacing: { before: 100 } }),
      new Paragraph({ text: normal('🚩 Seksuelt innhold eller anmodning om bilder') }),
      new Paragraph({ text: normal('🚩 Trakassering, mobbing, eller truende atferd') }),
      new Paragraph({ text: normal('🚩 Selvskadingsforsøk eller selvmordtanker nevnt offentlig') }),
      new Paragraph({ text: normal('🚩 Innhold som antyder misbruk, overgrep eller vold') }),
      new Paragraph({ text: normal('🚩 Innhold som promoterer selvskade, spiseforstyrrelser, eller rusmisbruk'), spacing: { after: 200 } }),

      section('4. MODERASJONSREGLER'),
      new Paragraph({ text: normal('**Automatisk blokkering (AI/filtre):**') }),
      new Paragraph({ text: normal('- Ord som antyder seksuelt innhold med mindreårige'), spacing: { before: 100 } }),
      new Paragraph({ text: normal('- Bildekontroll: nakenhet, vold, selvskade') }),
      new Paragraph({ text: normal('- Anmodninger om persondata (telefonnummer, adresse, sosiale medier-kontoer)') }),
      new Paragraph({ text: normal('- Lenker til eksterne chat-tjenester eller \\\"møt meg IRL\\\"') }),

      new Paragraph({ text: normal('**Manuell moderasjon (daglig gjennomgang):**'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('- Gjennomgå rapporterte innhold') }),
      new Paragraph({ text: normal('- Vurder kontekst (humor vs. seriøs fare)') }),
      new Paragraph({ text: normal('- Dokumenter beslutning og handling') }),
      new Paragraph({ text: normal('- Kontakt bruker hvis det er forvirrende'), spacing: { after: 200 } }),

      section('5. HANDLINGSREGLER VED BEKYMRING'),
      new Paragraph({ text: normal('**Steg 1: Dokumenter (umiddelbar)') }),
      new Paragraph({ text: normal('- Ta screenshot/logg av problematisk innhold'), spacing: { before: 100 } }),
      new Paragraph({ text: normal('- Notér dato, tid, bruker-ID, hva som ble sagt') }),
      new Paragraph({ text: normal('- Lagre i sikker mappe (ikke på chat)') }),

      new Paragraph({ text: normal('**Steg 2: Moderasjon (samme dag)'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('- Fjern problematisk innhold') }),
      new Paragraph({ text: normal('- Send varsling til bruker: \\\"Ditt innhold bryter reglene fordi..., derfor fjernet vi det.\\\"') }),
      new Paragraph({ text: normal('- Hvis alvorlig: Suspend eller block bruker') }),

      new Paragraph({ text: normal('**Steg 3: Eskalering (hvis relevant)'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('- Hvis tegn på SEKSUELLE OVERGREP → Ring Barnevernstjenesten SAMME DAG') }),
      new Paragraph({ text: normal('- Hvis tegn på MISHANDLING → Ring Barnevernstjenesten') }),
      new Paragraph({ text: normal('- Hvis tegn på SELVSKADE/SELVMORD → Ring Helsehjelp 116 117 eller 112') }),
      new Paragraph({ text: normal('- Dokumenter alt (tidspunkt, hvem du ringte, hva som ble sagt)'), spacing: { after: 200 } }),

      section('6. KONTAKT TIL MYNDIGHETER'),
      new Paragraph({ text: normal('**Barnevernstjenesten (kommunal):**'), spacing: { before: 100 } }),
      new Paragraph({ text: normal('- Mishandling, neglekt, seksuell misbruk') }),
      new Paragraph({ text: normal('- Søk på Google: \\\"barnevernstjenesten [din kommune]\\\"') }),

      new Paragraph({ text: normal('**Helsehjelp (Telefonisk rådgivning):**'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('- Nummer: 116 117 (24/7)') }),
      new Paragraph({ text: normal('- For selvskade, selvmordstanker, psykisk krise') }),

      new Paragraph({ text: normal('**Politiet (alvorlig fare):**'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('- Nummer: 112 (nødsituasjon)') }),
      new Paragraph({ text: normal('- Eller: Politiet.no (anmeldelse online)'), spacing: { after: 200 } }),

      section('7. PRIVACY OG DATAHÅNDTERING'),
      new Paragraph({ text: normal('**Når vi samler inn data:**') }),
      new Paragraph({ text: normal('✓ Bare hva som trengs (navn, epost, aldersgruppe)'), spacing: { before: 100 } }),
      new Paragraph({ text: normal('✓ Få samtykke fra foreldre hvis under 16 år') }),
      new Paragraph({ text: normal('✓ Krypter alle data i transit (HTTPS)') }),
      new Paragraph({ text: normal('✓ Begrenset tilgang (bare moderatorer trenger brukerhistorikk)') }),

      new Paragraph({ text: normal('**Når vi sletter data:**'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('- Bruker ber om sletting → slett innen 30 dager') }),
      new Paragraph({ text: normal('- Konto inaktiv i 2 år → vurder automatisk sletting') }),
      new Paragraph({ text: normal('- Unntak: hvis juridisk tvil eller pågående undersøkelse'), spacing: { after: 200 } }),

      section('8. ÅRLIG AUDIT OG FORBEDRING'),
      new Paragraph({ text: normal('Hvert år skal du:') }),
      new Paragraph({ text: normal('✓ Gjennomgå alle moderasjonsbeslutninger'), spacing: { before: 100 } }),
      new Paragraph({ text: normal('✓ Telle antall problematiske hendelser') }),
      new Paragraph({ text: normal('✓ Vurdere filtre og regler (fungerer de?)') }),
      new Paragraph({ text: normal('✓ Trene team på nytt') }),
      new Paragraph({ text: normal('✓ Oppdater policyen basert på erfaringer'), spacing: { after: 200 } }),

      new Paragraph({
        text: new TextRun({
          text: 'Politikk fra: September 2026 | Neste review: September 2027',
          italic: true,
          size: 20
        })
      })
    ]
  }]
});

// === 2. MODERASJONS-RUTINER (PRAKTISK GUIDE) ===
const moderationGuide = new Document({
  sections: [{
    properties: {},
    children: [
      heading('MODERASJONS-RUTINER OG SJEKKLISTER – MURMUROS', 1),
      new Paragraph({
        text: new TextRun({
          text: 'Versjon 1.0 | Praktisk guide for daglig bruk | For moderatorer og innholdssjef',
          italic: true,
          size: 20
        }),
        spacing: { after: 240 }
      }),

      section('DAGLIG MODERASJONS-SJEKKLISTE'),
      new Paragraph({ text: normal('Gjør hver dag (helst morgen):') }),
      new Paragraph({ text: normal('☐ Logg inn i moderator-panel'), spacing: { before: 100 } }),
      new Paragraph({ text: normal('☐ Gjennomgå rapporterte innhold (sorter etter prioritet)') }),
      new Paragraph({ text: normal('☐ Sjekk \\\"flagged by AI\\\" (automatisk detektert problematisk innhold)') }),
      new Paragraph({ text: normal('☐ Les kommentarer på nytt opprettet innhold') }),
      new Paragraph({ text: normal('☐ Sjekk private meldinger mellom brukere (hvis relevant)') }),
      new Paragraph({ text: normal('☐ Noter hendelser i logg-spreadsheet') }),
      new Paragraph({ text: normal('☐ Rapporter til leder hvis alvorlig'), spacing: { after: 200 } }),

      section('VURDERING: ER INNHOLDET PROBLEMATISK?'),
      new Paragraph({ text: normal('Spør deg selv:') }),

      new Paragraph({ text: normal('**1. Seksuell innhold?**'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('☐ Er det eksplisitt seksualt innhold?') }),
      new Paragraph({ text: normal('☐ Er det anmodringer om bilder eller video?') }),
      new Paragraph({ text: normal('☐ Er det forsøk på \\\"grooming\\\" (voksne som nærmer seg ungdom)?') }),
      new Paragraph({ text: normal('✓ HANDL: Fjern umiddelbart, block bruker, rapporter til barnevernstjenesten') }),

      new Paragraph({ text: normal('**2. Vold, mobbing eller trakassering?**'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('☐ Er det truende språk?') }),
      new Paragraph({ text: normal('☐ Er det mobbing av en annen bruker?') }),
      new Paragraph({ text: normal('☐ Er det hat-speech eller diskriminering?') }),
      new Paragraph({ text: normal('✓ HANDL: Fjern, advar bruker, suspend hvis gjentatt') }),

      new Paragraph({ text: normal('**3. Selvskade eller suisidtanker?**'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('☐ Nevner brukeren selvskade, selvmord, eller spiseforstyrrelser?') }),
      new Paragraph({ text: normal('☐ Er det propaganda for selvskade (\\\"pro-ana\\\" osv.)?') }),
      new Paragraph({ text: normal('✓ HANDL: Fjern innhold, varsle bruker med hjelperessurser, ring Helsehjelp 116 117') }),

      new Paragraph({ text: normal('**4. Persondata eller sikkerhet?**'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('☐ Er det deling av personlige detaljer (telefonnummer, adresse, navn på skolen)?') }),
      new Paragraph({ text: normal('☐ Er det forsøk på å møte \\\"IRL\\\" (In Real Life)?') }),
      new Paragraph({ text: normal('☐ Er det lenker til eksterne tjenester?') }),
      new Paragraph({ text: normal('✓ HANDL: Fjern, varsle bruker, blokkering hvis nødvendig') }),

      new Paragraph({ text: normal('**5. Spam eller reklame?**'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('☐ Er det kommersielt innhold?') }),
      new Paragraph({ text: normal('☐ Er det gjentatte spam-meldinger?') }),
      new Paragraph({ text: normal('✓ HANDL: Fjern, advar bruker'), spacing: { after: 200 } }),

      section('EKSEMPLER: HVA SKAL GJØRES?'),
      new Paragraph({ text: normal('**Eksempel 1: Mobbing**'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('Bruker A skriver: \\\"Du er så dum. Alle hater deg. Slutt med det du gjør.\\\"') }),
      new Paragraph({ text: normal('→ Fjern kommentaren') }),
      new Paragraph({ text: normal('→ Send varsling til bruker A: \\\"Din kommentar bryter regel om mobbing. Henspilling på vold eller trakassering er ikke tillatt.\\\"') }),
      new Paragraph({ text: normal('→ Noter i logg') }),
      new Paragraph({ text: normal('→ Hvis bruker har tidligere varsler: Suspend konto i 24 timer') }),

      new Paragraph({ text: normal('**Eksempel 2: Mulig selvskade**'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('Bruker B skriver: \\\"Jeg kan ikke holde det ut lenger. Jeg vil ikke være her.\\\"') }),
      new Paragraph({ text: normal('→ Fjern innlegget (for å ikke inspirere andre)') }),
      new Paragraph({ text: normal('→ Send privat melding til bruker B: \\\"Vi er bekymret for deg. Snakk med noen du stoler på. Her er hjelperessurser: [lenke]\\\"') }),
      new Paragraph({ text: normal('→ Ring Helsehjelp 116 117 (om du er utsatt, de gir råd)') }),
      new Paragraph({ text: normal('→ Noter i logg og varsle leder') }),

      new Paragraph({ text: normal('**Eksempel 3: Seksuell tilnærming (Grooming)**'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('Bruker C (kanskje voksken?) skriver til bruker D: \\\"Du virker interessant. Vil du chatte privat?\\\"') }),
      new Paragraph({ text: normal('→ Fjern umiddelbart') }),
      new Paragraph({ text: normal('→ Block bruker C') }),
      new Paragraph({ text: normal('→ Ring barnevernstjenesten SAMME DAG') }),
      new Paragraph({ text: normal('→ Noter navn på kommune og hvem du snakket med') }),
      new Paragraph({ text: normal('→ Varsle leder og juridisk ekspert'), spacing: { after: 200 } }),

      section('LOGG-FORMAT (BRUK SPREADSHEET)'),
      new Paragraph({ text: normal('Opprett en Google Sheets-fil med disse kolonnene:') }),
      new Paragraph({ text: normal('| Dato | Tid | Bruker-ID | Hva hendte | Alvorlighet | Handling | Moderator |'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('| 2026-09-23 | 14:35 | user_1234 | Mobbing av bruker_5678 | Medium | Fjernet kommentar, varsel | Anna |') }),
      new Paragraph({ text: normal('| 2026-09-23 | 15:10 | user_9999 | Mulig grooming | KRITISK | Fjernet, blocka, ringte barnevernstjenesten | Ole |'), spacing: { after: 200 } }),

      section('MELDINGER TIL BRUKERE'),
      new Paragraph({ text: normal('**Standardvarsel (brudd på regler):**'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('\\\"Hei [navn], ditt innhold \\\"[sitere]\\\" bryter våre regler fordi [grunnen]. Vi har fjernet det. Du kan [lenke] lese hele regelverket vårt. Hvis du mener det er en feil, kontakt oss på [epost].\\\"') }),

      new Paragraph({ text: normal('**Alvorlig varsel (trakassering/mobbing):**'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('\\\"Hei [navn], vi har oppdaget at du trakasserer andre brukere. Dette bryter våre regler og vi kan ikke tillate det. Hvis det fortsetter, blokkerer vi kontoen din. Hvis du sliter med noe, vi kan hjelpe via [ressurs].\\\"') }),

      new Paragraph({ text: normal('**Bekymringsvarsel (selvskade/selvmord):**'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('\\\"Hei [navn], vi er bekymret for deg basert på det du skrev. Du er ikke alene. Her er folk som kan hjelpe: Helsehjelp 116 117 (gratis, hele tiden), Telefonkrisen 22 59 22 00. Du betyr noe. Vi er her hvis du trenger.\\\"'), spacing: { after: 200 } }),

      section('ESKALERING TIL LEDER'),
      new Paragraph({ text: normal('Ring eller send e-post umiddelbar hvis:') }),
      new Paragraph({ text: normal('🚨 Tegn på seksuelt misbruk av mindreårig'), spacing: { before: 100 } }),
      new Paragraph({ text: normal('🚨 Selvmords-trussel') }),
      new Paragraph({ text: normal('🚨 Mishandling eller vold') }),
      new Paragraph({ text: normal('🚨 Bruker som bruker falsk identitet/predator') }),
      new Paragraph({ text: normal('🚨 Juridisk spørsmål eller potensial PR-krise'), spacing: { after: 200 } }),

      section('TRENING FOR MODERATORER'),
      new Paragraph({ text: normal('Ny moderator skal gjennom før de starter:') }),
      new Paragraph({ text: normal('1️⃣ Les intern barnevernspolicy (denne fil + MURMUROS-Barnevernspolicy.docx)'), spacing: { before: 100 } }),
      new Paragraph({ text: normal('2️⃣ Shadow en erfaren moderator i 2 dager') }),
      new Paragraph({ text: normal('3️⃣ Quiz: \\\"Hva ville du gjøre hvis...?\\\" (10 spørsmål)') }),
      new Paragraph({ text: normal('4️⃣ First review av deres beslutninger (leder godkjenner)') }),
      new Paragraph({ text: normal('5️⃣ Årlig oppdaterings-trening'), spacing: { after: 200 } }),

      new Paragraph({
        text: new TextRun({
          text: 'Sist oppdatert: September 2026 | Neste gjennomgang: Mars 2027',
          italic: true,
          size: 20
        })
      })
    ]
  }]
});

// === 3. INCIDENT RESPONSE PLAN ===
const incidentPlan = new Document({
  sections: [{
    properties: {},
    children: [
      heading('INCIDENT RESPONSE PLAN – MURMUROS', 1),
      new Paragraph({
        text: new TextRun({
          text: 'Versjon 1.0 | Hva skal vi gjøre hvis det skjer noe alvorlig?',
          italic: true,
          size: 20
        }),
        spacing: { after: 240 }
      }),

      section('ALARM-SITUASJONER OG RESPONS'),
      new Paragraph({ text: normal('**Situasjon: Bruker truet med selvmord**'), spacing: { before: 120 } }),
      new Paragraph({ text: normal('0 min: Ring Helsehjelp 116 117 (eller 112 hvis akutt)'), spacing: { before: 100 } }),
      new Paragraph({ text: normal('5 min: Varsle leder') }),
      new Paragraph({ text: normal('15 min: Dokumenter (screenshot, bruker-ID, tidspunkt)') }),
      new Paragraph({ text: normal('30 min: Send bekymringsmelding til bruker') }),
      new Paragraph({ text: normal('1 dag: Oppfølging – er de OK?') }),

      new Paragraph({ text: normal('**Situasjon: Seksuelt overgrep av barn**'), spacing: { before: 200 } }),
      new Paragraph({ text: normal('0 min: STOPP alt annet. Ring Politiet 112 eller Barnevernstjenesten'), spacing: { before: 100 } }),
      new Paragraph({ text: normal('5 min: Varsle leder og juridisk ekspert') }),
      new Paragraph({ text: normal('15 min: Block bruker(e) involvert') }),
      new Paragraph({ text: normal('30 min: Dokumenter alt (IKKE slett noe)') }),
      new Paragraph({ text: normal('1 time: Møte med leder for kriseplan') }),

      new Paragraph({ text: normal('**Situasjon: Datalekkasje (brukerdata exposed)**'), spacing: { before: 200 } }),
      new Paragraph({ text: normal('0 min: Stopp det som årsaken til lekkasjen'), spacing: { before: 100 } }),
      new Paragraph({ text: normal('5 min: Varsle IT/sikkerhet og leder') }),
      new Paragraph({ text: normal('15 min: Vurder hvor alvorlig det er') }),
      new Paragraph({ text: normal('30 min: Varsle alle berørte brukere via epost') }),
      new Paragraph({ text: normal('2 timer: Kontakt personvernombudsman@datatilsynet.no') }),
      new Paragraph({ text: normal('24 timer: Juridisk vurdering') }),

      new Paragraph({ text: normal('**Situasjon: Falsk anklage (bruker blir feilaktig blokkert)**'), spacing: { before: 200 } }),
      new Paragraph({ text: normal('30 min: Undersøk grundig'), spacing: { before: 100 } }),
      new Paragraph({ text: normal('1 time: Kontakt bruker, unnskyld hvis feil') }),
      new Paragraph({ text: normal('2 timer: Restore konto hvis det var feil') }),
      new Paragraph({ text: normal('1 dag: Vurder om moderatørens beslutning var riktig'), spacing: { after: 200 } }),

      section('KONTAKTLISTE (OPPBEVARES SIKKERT)'),
      new Paragraph({ text: normal('Leder: [navn] [tlf] [epost]'), spacing: { before: 100 } }),
      new Paragraph({ text: normal('Juridisk ekspert: [navn] [tlf] [epost]') }),
      new Paragraph({ text: normal('IT/Sikkerhet: [navn] [tlf] [epost]') }),
      new Paragraph({ text: normal('Barnevernstjenesten [din kommune]: [tlf]') }),
      new Paragraph({ text: normal('Politiet: 112 eller 02800 (non-emergency)') }),
      new Paragraph({ text: normal('Helsehjelp: 116 117') }),
      new Paragraph({ text: normal('Datatilsynet: post@datatilsynet.no eller 55 30 45 45'), spacing: { after: 200 } }),

      section('DOKUMENTERING I KRISE'),
      new Paragraph({ text: normal('✓ Hvem var involvert (bruker-ID, ikke navn hvis mulig)') }),
      new Paragraph({ text: normal('✓ Hva hendte (eksakt tidspunkt, innhold)'), spacing: { before: 100 } }),
      new Paragraph({ text: normal('✓ Hvem du ringte og når') }),
      new Paragraph({ text: normal('✓ Hva de sa') }),
      new Paragraph({ text: normal('✓ Dine handlinger (fjernet innhold, blocka bruker osv.)') }),
      new Paragraph({ text: normal('✓ Oppfølging (varslet foreldre, lege osv.)'), spacing: { after: 200 } }),

      new Paragraph({
        text: new TextRun({
          text: 'Plan fra: September 2026 | Test-øvelse anbefalt hvert halvår',
          italic: true,
          size: 20
        })
      })
    ]
  }]
});

// Save all documents
async function createDocuments() {
  try {
    const safeguardingBuffer = await Packer.toBuffer(safeguardingPolicy);
    fs.writeFileSync('MURMUROS-Intern-Barnevernspolicy.docx', safeguardingBuffer);
    console.log('✓ Intern barnevernspolicy opprettet');

    const moderationBuffer = await Packer.toBuffer(moderationGuide);
    fs.writeFileSync('MURMUROS-Moderasjons-rutiner.docx', moderationBuffer);
    console.log('✓ Moderasjons-rutiner opprettet');

    const incidentBuffer = await Packer.toBuffer(incidentPlan);
    fs.writeFileSync('MURMUROS-Incident-Response-Plan.docx', incidentBuffer);
    console.log('✓ Incident response plan opprettet');

    console.log('\n✅ Alle barnevernsdokumenter opprettet:');
    console.log('1. MURMUROS-Intern-Barnevernspolicy.docx');
    console.log('2. MURMUROS-Moderasjons-rutiner.docx');
    console.log('3. MURMUROS-Incident-Response-Plan.docx');
  } catch (error) {
    console.error('Feil ved oppretting av dokumenter:', error);
  }
}

createDocuments();
