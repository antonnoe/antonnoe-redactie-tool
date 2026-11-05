# CLAUDE.md

Repo: antonnoe-redactie-tool

## Wat dit is
Een lichtgewicht review-laag voor lange teksten. Hoofdstukken in markdown of een bestaande HTML-pagina worden omgezet naar één statische index.html waarin een reviewer per alinea, lijst, tabel of citaatkaart een opmerking kan achterlaten, zonder account. Bron: README.md.

## Live adres
Niet in de repo vastgelegd. De map docs/ (met .nojekyll) bevat een gebouwd voorbeeld, wat op GitHub Pages wijst, maar het adres staat nergens.

## Opbouw
- build.py: bouwt index.html uit template.html, config.json en content/*.md (markdown-modus).
- wrap.py en wrap-template.html: leggen de review-laag over een bestaande HTML-pagina (wrap-modus).
- template.html: de shell met CSS en het klik-, opmerking- en synchronisatiemechanisme.
- slot.html: optioneel, vergrendelt een gebouwde pagina met een wachtwoord (AES-256 in de browser).
- config.json, config-if.json en config.example.json: projectinstellingen.
- supabase.sql: tabel redactie_opmerkingen met row-level security (optioneel).
- content/: hoofdstukken in markdown (01-inleiding.md, 02-tweede-hoofdstuk.md).
- docs/: index.html en .nojekyll, een gebouwd exemplaar.
- voorbeeld-if.html: voorbeeldpagina voor de wrap-modus.
- index.html (de uitvoer) staat in .gitignore.

## Techniek
Python 3 met alleen het pakket markdown voor build.py. wrap.py heeft geen afhankelijkheden. Het resultaat is volledig statisch en draait zonder backend.

## Externe diensten en namen van omgevingsvariabelen
- Supabase, optioneel, voor centrale opslag van opmerkingen. Geen omgevingsvariabelen: de koppeling staat in config.json onder "supabase" met de velden url, anon_key en tabel.
- Google Fonts (Poppins en Mulish) in de gebouwde pagina.
- Overige velden in config.json: titel, mail, content_dir, intro_html, citaat_marker, citaat_label, open_punt_marker, open_punt_tekst, project_sleutel, opslag_sleutel, galerij.
- Een lokale config.local.json staat in .gitignore voor echte sleutels.

## Hoe het live gaat
Lokaal draaien: python3 build.py (of python3 wrap.py pagina.html config.json), dat schrijft index.html. De gebouwde pagina wordt daarna zelf geplaatst bij een statische host (README noemt Vercel, Netlify of een servermap). Er is geen workflow of vercel.json in de repo.

## Regels en besluiten
Bron: README.md.
- Reviewers hebben geen account nodig en kunnen niets teruglezen of wissen; opslag in Supabase is append-only met row-level security.
- Vier rollen: auteur, redactie, eindredacteur en beeldredactie; auteur en eindredacteur mogen opmerkingen afvinken, beeldredactie mag beelden toevoegen.
- Een broncitaat markeer je met de opmerking BRON vóór een blockquote; een open punt schrijf je inline als [OPEN: toelichting].
- Wachtwoordslot is één gedeeld wachtwoord; kwijt betekent opnieuw bouwen.

Laatst nagelopen: 5 november 2026
