# Redactie-tool

Een lichtgewicht **review-laag voor lange teksten**. Je zet je hoofdstukken als
markdown neer, draait één buildscript, en krijgt één statische `index.html`
waarin een reviewer op **elke alinea, lijst, tabel of citaatkaart** kan klikken
om een opmerking achter te laten — zonder account, zonder inloggen, zonder app.

Bedoeld voor het moment vóór publicatie: een domeinexpert, klant of eindredacteur
leest mee en becommentarieert, en jij krijgt alle opmerkingen terug — per
hoofdstuk gegroepeerd, met verwijzing naar de exacte passage.

## Waarom deze en niet Google Docs / een proofing-SaaS

- **Nul drempel voor de reviewer.** Eén link openen en klikken. Geen account,
  geen uitnodiging, geen software.
- **Jij bezit de data.** Alles blijft lokaal (localStorage) óf gaat naar je
  eigen Supabase-tabel — append-only, met row-level security, de reviewer kan
  niets teruglezen of wissen. Geen SaaS-lock-in, geen per-seat-kosten.
- **Gemaakt voor redactionele content.** Hoofdstukken, letterlijk overgenomen
  broncitaten (eigen kaart), en „open punten” (claims die nog nagekeken moeten
  worden) zijn eersteklas concepten — geen generieke website-markup.
- **Volledig statisch.** Host het overal (Vercel, Netlify, een map op een
  server). Geen backend nodig.

## Snelstart

```bash
pip install markdown
python3 build.py           # leest config.json + content/*.md -> index.html
# open index.html in de browser
```

## Zo werkt het

- **Hoofdstukken**: elk `.md`-bestand in `content/` (alfabetisch gesorteerd,
  vandaar `01-...`, `02-...`) wordt één sectie. De eerste `# Kop` is de titel.
- **Broncitaat** (eigen kaart): zet `<!-- BRON -->` vóór een blockquote.
- **Open punt**: schrijf inline `[OPEN: korte toelichting]`.
- **Beeld/schema inline** (optioneel): `<!-- SVG-INLINE: naam.svg -->` of
  `<!-- HTML-INLINE: fragment.html -->`, gelezen uit `assets/`.
- **Opmerkingen terug**: knop onderaan mailt of downloadt alle opmerkingen;
  vul je Supabase in `config.json` in en ze synchroniseren ook live.

## Achter een gesloten deur (wachtwoord)

Wil je dat alleen de reviewer erbij kan? Vergrendel de gebouwde pagina:

1. Open `slot.html` in je browser (dubbelklik — het werkt lokaal, offline).
2. Kies de gebouwde `index.html`, geef een wachtwoord, klik **Vergrendelen**.
3. Je krijgt een nieuwe, versleutelde `index.html` terug. Díe zet je online.
4. De reviewer opent de link, typt het wachtwoord, en de pagina ontsleutelt in
   zijn eigen browser. Eén invoerveld, verder niets.

Dit is een **echte** deur, geen sier-slot: de hele pagina is AES-256-versleuteld
(sleutel via PBKDF2, 210.000 iteraties). Zonder het juiste wachtwoord staat er
geen leesbare tekst in de broncode — anders dan bij een naïeve
"typ-het-wachtwoord"-check, waar de inhoud gewoon in de HTML zit.

Eerlijk over de grenzen:

- Het is **één gedeeld wachtwoord**. Prima voor één of enkele vertrouwde
  reviewers. Wil je per persoon toegang geven of intrekken, dan heb je een
  backend nodig — dat valt buiten deze gratis, statische opzet.
- Het wachtwoord is de énige sleutel; kwijt = opnieuw bouwen. Deel het via een
  ander kanaal dan de link zelf.
- Alles gebeurt in de browser (`slot.html` uploadt niets).

Nóg strenger en zonder wachtwoord kan ook via de hosting (bijv. Cloudflare
Access, of de wachtwoordbeveiliging van Vercel/Netlify) — maar dat is
host-afhankelijk en soms betaald. De ingebouwde deur hierboven is gratis en
overal inzetbaar.

## Configuratie

Alles staat in `config.json` (zie `config.example.json`): titel, e-mailadres
waar opmerkingen heen gaan, labels, opslagsleutel en de optionele
Supabase-koppeling. Voor centrale opslag draai je eenmalig `supabase.sql` in je
Supabase-project.

## Bestanden

| Bestand | Rol |
|---|---|
| `template.html` | De shell: alle CSS + het klik-/opmerking-/sync-mechanisme. Placeholders `{{...}}`. |
| `build.py` | Bouwt `index.html` uit `template.html` + `config.json` + `content/*.md`. |
| `slot.html` | Optioneel: vergrendelt de gebouwde pagina met een wachtwoord (AES-256, in de browser). |
| `config.json` | Projectinstellingen. |
| `supabase.sql` | Eenmalige tabel + RLS-policy voor centrale opslag (optioneel). |
| `content/` | Je hoofdstukken in markdown. |
| `assets/` | (optioneel) SVG-/HTML-fragmenten voor de inline-markers. |

De tool is voortgekomen uit het redactie-exemplaar van een boekdossier en is
losgemaakt van die specifieke inhoud, zodat hij op elk tekstproject past.
