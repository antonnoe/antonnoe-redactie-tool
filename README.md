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
| `config.json` | Projectinstellingen. |
| `supabase.sql` | Eenmalige tabel + RLS-policy voor centrale opslag (optioneel). |
| `content/` | Je hoofdstukken in markdown. |
| `assets/` | (optioneel) SVG-/HTML-fragmenten voor de inline-markers. |

De tool is voortgekomen uit het redactie-exemplaar van een boekdossier en is
losgemaakt van die specifieke inhoud, zodat hij op elk tekstproject past.
