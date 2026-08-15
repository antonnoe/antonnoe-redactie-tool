#!/usr/bin/env python3
"""wrap.py — legt de review-laag over een BESTAANDE HTML-dossierpagina.

Voor rijke, zelf-opgemaakte pagina's (WordPress-export, een .if-dossier-wrapper
met eigen <style>) die je NIET uit markdown bouwt. De opmaak blijft intact;
de tool voegt alleen de klik-/opmerking-/rollen-laag toe.

Gebruik:  python3 wrap.py mijn-dossier.html          (leest ./config.json)
          python3 wrap.py mijn-dossier.html mijn.json
Resultaat: index.html

Geen dependencies nodig (geen markdown).
"""
import io, os, sys, json

ROOT = os.path.dirname(os.path.abspath(__file__))


def laad_config(pad):
    cfg = json.load(io.open(pad, encoding="utf-8")) if os.path.exists(pad) else {}
    cfg.setdefault("titel", "Dossier")
    cfg.setdefault("mail", "")
    cfg.setdefault("project_sleutel", "dossier")
    cfg.setdefault("opslag_sleutel", "review-" + cfg["project_sleutel"] + "-v1")
    cfg.setdefault("supabase", {})
    cfg["supabase"].setdefault("url", "")
    cfg["supabase"].setdefault("anon_key", "")
    cfg["supabase"].setdefault("tabel", "redactie_opmerkingen")
    return cfg


def main():
    if len(sys.argv) < 2:
        sys.exit("Gebruik: python3 wrap.py <dossier.html> [config.json]")
    content_pad = sys.argv[1]
    cfg_pad = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "config.json")
    cfg = laad_config(cfg_pad)

    inhoud = io.open(content_pad, encoding="utf-8").read()
    tpl = io.open(os.path.join(ROOT, "wrap-template.html"), encoding="utf-8").read()

    vervang = {
        "{{TITEL}}": cfg["titel"],
        "{{INHOUD}}": inhoud,
        "{{MAIL}}": cfg["mail"],
        "{{OPSLAG_SLEUTEL}}": cfg["opslag_sleutel"],
        "{{PROJECT_SLEUTEL}}": cfg["project_sleutel"],
        "{{SUPABASE_URL}}": cfg["supabase"]["url"],
        "{{SUPABASE_ANON_KEY}}": cfg["supabase"]["anon_key"],
        "{{SUPABASE_TABEL}}": cfg["supabase"]["tabel"],
    }
    for k, v in vervang.items():
        tpl = tpl.replace(k, v)

    dest = os.path.join(ROOT, "index.html")
    io.open(dest, "w", encoding="utf-8").write(tpl)
    sync = "aan" if cfg["supabase"]["url"] and cfg["supabase"]["anon_key"] else "uit (lokaal)"
    print("OK: index.html — bestaande pagina omhuld (" + str(len(tpl)) + " bytes), Supabase-sync: " + sync)


if __name__ == "__main__":
    main()
