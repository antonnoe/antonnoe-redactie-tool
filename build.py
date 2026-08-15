#!/usr/bin/env python3
"""Redactie-tool — bouwt een aanklikbaar review-exemplaar (index.html) uit een
map met markdown-hoofdstukken + template.html + config.json.

Gebruik:  python3 build.py            (leest ./config.json)
          python3 build.py mijn.json  (andere config)

Vereist:  pip install markdown
"""
import re, glob, os, sys, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))


def laad_config(pad):
    cfg = json.load(open(pad, encoding="utf-8"))
    cfg.setdefault("titel", "Naamloos project")
    cfg.setdefault("mail", "")
    cfg.setdefault("content_dir", "content")
    cfg.setdefault("intro_html", "<h1>Review-exemplaar</h1>")
    cfg.setdefault("citaat_marker", "BRON")
    cfg.setdefault("citaat_label", "Brontekst, letterlijk overgenomen")
    cfg.setdefault("open_punt_marker", "OPEN")
    cfg.setdefault("open_punt_tekst", "Nog open. Aanvulling of bronverwijzing welkom.")
    cfg.setdefault("project_sleutel", "project")
    cfg.setdefault("opslag_sleutel", "review-" + cfg["project_sleutel"] + "-v1")
    cfg.setdefault("supabase", {})
    cfg["supabase"].setdefault("url", "")
    cfg["supabase"].setdefault("anon_key", "")
    cfg["supabase"].setdefault("tabel", "redactie_opmerkingen")
    cfg.setdefault("galerij", None)
    return cfg


def slug(tekst):
    s = tekst.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "sectie"


def hoofdstuk_html(pad, cfg):
    import markdown
    t = open(pad, encoding="utf-8").read()
    m = re.search(r"^#\s+(.+)$", t, re.M)
    titel = m.group(1).strip() if m else os.path.basename(pad)
    t = re.sub(r"^#\s+.+$", "", t, count=1, flags=re.M)

    # Open-punt-markering:  [OPEN: vrije toelichting]
    marker = re.escape(cfg["open_punt_marker"])
    def vraagblok(mm):
        binnen = mm.group(1).strip(" :—-").strip()
        binnen = binnen.replace("<", "&lt;")
        staart = " <em>(" + binnen + ")</em>" if binnen else ""
        return ('\n<div class="vraag"><span class="vraaglabel">Open punt</span>'
                + cfg["open_punt_tekst"] + staart + "</div>\n")
    t = re.sub(r"\[" + marker + r"([^\]]*)\]", vraagblok, t)

    body = markdown.markdown(t, extensions=["tables"])

    # inline-markers (optioneel): SVG-fragment en HTML-fragment uit /assets/
    body = re.sub(r"<!--\s*SVG-INLINE:\s*([^>]+?)\s*-->", lambda mm: _inline_asset(mm, cfg, "svg"), body)
    body = re.sub(r"<!--\s*HTML-INLINE:\s*([^>]+?)\s*-->", lambda mm: _inline_asset(mm, cfg, "html"), body)

    # citaatkaart:  <!-- BRON --> voor een blockquote markeert die als brontekst
    cm = re.escape(cfg["citaat_marker"])
    patroon = r"(<!--\s*" + cm + r"\s*-->\s*)?<blockquote>(.*?)</blockquote>(\s*<!--\s*/?" + cm + r"\s*-->)?"
    def kaart(mm):
        is_bron = mm.group(1) or mm.group(3) or ("<!-- " + cfg["citaat_marker"] + " -->") in mm.group(2)
        if is_bron:
            return ('<figure class="bron"><figcaption>' + html.escape(cfg["citaat_label"])
                    + '</figcaption><blockquote>' + mm.group(2) + "</blockquote></figure>")
        return "<blockquote>" + mm.group(2) + "</blockquote>"
    body = re.sub(patroon, kaart, body, flags=re.S)
    body = body.replace("<!-- " + cfg["citaat_marker"] + " -->", "").replace("<!-- /" + cfg["citaat_marker"] + " -->", "")

    body = body.replace("<table>", '<div class="tabelwrap"><table>').replace("</table>", "</table></div>")
    return slug(titel), titel, body


def _inline_asset(mm, cfg, soort):
    naam = mm.group(1).strip()
    pad = os.path.join(ROOT, "assets", naam)
    if not os.path.exists(pad):
        return '<div class="notitie">[' + soort + '-fragment ontbreekt: ' + html.escape(naam) + "]</div>"
    inhoud = open(pad, encoding="utf-8").read()
    if soort == "svg":
        inhoud = re.sub(r"<\?xml.*?\?>", "", inhoud, flags=re.S)
        return '<figure class="schema">' + inhoud + "</figure>"
    return inhoud


def galerij_html(cfg):
    g = cfg.get("galerij")
    if not g or not g.get("items"):
        return ""
    kaarten = []
    for it in g["items"]:
        kaarten.append('<figure class="galerijkaart"><img loading="lazy" src="'
                       + html.escape(it.get("src", "")) + '" alt="' + html.escape(it.get("alt", ""))
                       + '"><figcaption>' + html.escape(it.get("caption", "")) + "</figcaption></figure>")
    return ('<section id="galerij"><p class="eyebrow">' + html.escape(g.get("eyebrow", "Beeld"))
            + '</p><h1>' + html.escape(g.get("titel", "Beeld")) + "</h1>"
            + ("<p>" + html.escape(g["intro"]) + "</p>" if g.get("intro") else "")
            + '<div class="galerij">' + "".join(kaarten) + "</div></section>")


def main():
    cfg_pad = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "config.json")
    cfg = laad_config(cfg_pad)

    paden = sorted(glob.glob(os.path.join(ROOT, cfg["content_dir"], "*.md")))
    if not paden:
        sys.exit("Geen markdown-hoofdstukken gevonden in " + cfg["content_dir"] + "/")

    secties, nav = [], []
    for p in paden:
        sid, titel, body = hoofdstuk_html(p, cfg)
        secties.append('<section id="' + sid + '"><h1>' + html.escape(titel) + "</h1>" + body + "</section>")
        nav.append('<a href="#' + sid + '">' + html.escape(titel) + "</a>")
    if cfg.get("galerij") and cfg["galerij"].get("items"):
        nav.append('<a href="#galerij"><span>✦</span>' + html.escape(cfg["galerij"].get("titel", "Beeld")) + "</a>")

    tpl = open(os.path.join(ROOT, "template.html"), encoding="utf-8").read()
    vervang = {
        "{{TITEL}}": cfg["titel"],
        "{{INTRO}}": cfg["intro_html"],
        "{{NAV}}": "".join(nav),
        "{{INHOUD}}": "".join(secties),
        "{{GALERIJ}}": galerij_html(cfg),
        "{{MAIL}}": cfg["mail"],
        "{{OPSLAG_SLEUTEL}}": cfg["opslag_sleutel"],
        "{{PROJECT_SLEUTEL}}": cfg["project_sleutel"],
        "{{SUPABASE_URL}}": cfg["supabase"]["url"],
        "{{SUPABASE_ANON_KEY}}": cfg["supabase"]["anon_key"],
        "{{SUPABASE_TABEL}}": cfg["supabase"]["tabel"],
    }
    for k, v in vervang.items():
        tpl = tpl.replace(k, v)

    uit = os.path.join(ROOT, "index.html")
    open(uit, "w", encoding="utf-8").write(tpl)
    sync = "aan" if cfg["supabase"]["url"] and cfg["supabase"]["anon_key"] else "uit (lokaal)"
    print("OK: index.html — " + str(len(secties)) + " hoofdstukken, "
          + str(len(uit)) + " bytes-pad, Supabase-sync: " + sync)


if __name__ == "__main__":
    main()
