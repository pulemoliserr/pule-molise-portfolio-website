"""Build the portfolio branch pages and certifications of pulemolise.net.

Generates:
  index.html (Certifications section)  from tools/certifications.yml
  404.html, sitemap.xml, robots.txt
  data-science/index.html            from tools/data-science-cards.html
  cybersecurity/index.html           from tools/cybersecurity-projects.yml
  cybersecurity/<slug>/index.html    one S.T.A.R. page per cybersecurity project

Usage (from the repository root):
  pip install pyyaml
  python tools/build_portfolio.py
"""
import html
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
SITE = "https://pulemolise.net"
e = html.escape


def shell(depth, active, title, description, canonical, body, extra_head=""):
    """Common page layout: same sidebar, theme switcher and styles as the home page."""
    up = "../" * depth
    ds_active = ' class="active"' if active == "data-science" else ""
    cy_active = ' class="active"' if active == "cybersecurity" else ""
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{e(title)}</title>
    <meta name="description" content="{e(description)}" />
    <link rel="canonical" href="{SITE}{canonical}" />
    <meta property="og:title" content="{e(title)}" />
    <meta property="og:description" content="{e(description)}" />
    <meta property="og:url" content="{SITE}{canonical}" />{extra_head}
    <link rel="icon" type="image/png" href="{up}images/favicon.png" />
    <link rel="apple-touch-icon" href="{up}images/apple-touch-icon.png" />
    <link rel="stylesheet" href="{up}css/style.css" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />
    <link rel="stylesheet" href="{up}css/style-switcher.css" />
    <link rel="stylesheet" href="{up}css/projects.css" />
  </head>
  <body>
    <div class="main-container">
      <div class="aside">
        <div class="logo">
          <a href="{up}"><span class="logo-icon"></span></a>
        </div>
        <div class="nav-toggler"><span></span></div>
        <ul class="nav">
          <li><a href="{up}#home"><i class="fa fa-home"></i> Home</a></li>
          <li><a href="{up}#about"><i class="fa fa-user"></i> About</a></li>
          <li><a href="{up}#services"><i class="fa fa-list"></i> Services</a></li>
          <li><a href="{up}#portfolio" class="active"><i class="fa fa-briefcase"></i> Portfolio</a></li>
          <li class="sub-nav"><a href="{up}data-science/"{ds_active}>Data Science</a></li>
          <li class="sub-nav"><a href="{up}cybersecurity/"{cy_active}>Cybersecurity</a></li>
          <li><a href="{up}#certifications"><i class="fa fa-certificate"></i> Certifications</a></li>
          <li><a href="{up}#contact"><i class="fa fa-comments"></i> Contact</a></li>
        </ul>
      </div>

      <main class="page-main portfolio">
        <div class="container">
{body}
        </div>
      </main>
    </div>

    <div class="style-switcher">
      <div class="style-switcher-toggler s-icon"><i class="fas fa-cog fa-spin"></i></div>
      <div class="day-night s-icon"><i class="fas"></i></div>
      <h4>Theme Colors</h4>
      <div class="colors">
        <span class="color-1" onclick="setActiveStyle('#ec1839')"></span>
        <span class="color-2" onclick="setActiveStyle('#fa5b0f')"></span>
        <span class="color-3" onclick="setActiveStyle('#37b182')"></span>
        <span class="color-4" onclick="setActiveStyle('#1854b4')"></span>
        <span class="color-5" onclick="setActiveStyle('#f021b2')"></span>
      </div>
    </div>

    <script src="{up}js/style-switcher.js"></script>
    {'<script src="' + up + 'cybersecurity/links.js"></script>' if active == 'cybersecurity' else ''}
    <script src="{up}js/pages.js"></script>
  </body>
</html>
"""


def section_title(text):
    return f"""          <div class="row">
            <div class="section-title padd-15"><h2>{e(text)}</h2></div>
          </div>"""


def breadcrumb(depth, *crumbs):
    up = "../" * depth
    parts = [f'<a href="{up}">Home</a>', f'<a href="{up}#portfolio">Portfolio</a>']
    for label, href in crumbs:
        parts.append(f'<a href="{href}">{e(label)}</a>' if href else e(label))
    return '          <nav class="breadcrumb">' + "<span>/</span>".join(parts) + "</nav>"


# ------------------------------------------------------------- certifications
def cert_links(c, up):
    links = []
    if c.get("verify"):
        links.append(f'<a href="{c["verify"]}" target="_blank" rel="noopener"><i class="fa fa-check-circle"></i> Verify</a>')
    links.append(f'<a href="{up}certifications/files/{c["slug"]}.pdf" target="_blank" rel="noopener">'
                 '<i class="fa fa-file-pdf"></i> View certificate</a>')
    return "".join(links)


def cert_meta(c):
    parts = [c["date"]]
    if c.get("courses"):
        parts.append(f'{c["courses"]} courses')
    if c.get("number"):
        parts.append(f'Certificate no. {c["number"]}')
    return " · ".join(parts)


def build_certifications_section(certs):
    """Return the inner HTML of the home page's Certifications section."""
    out = ['            <div class="row">',
           '              <div class="section-title padd-15"><h2>Certifications</h2></div>',
           "            </div>",
           '            <div class="row">',
           f'              <p class="cert-intro padd-15">{len(certs["certifications"])} professional certificates '
           "from Google and the Corporate Finance Institute. Google certificates can be verified on Coursera.</p>",
           "            </div>"]
    for group in certs["groups"]:
        items = [c for c in certs["certifications"] if c["group"] == group]
        if not items:
            continue
        out += [f'            <h3 class="cert-group">{e(group)}</h3>', '            <div class="row">']
        for c in items:
            out.append(f"""              <div class="cert-item padd-15">
                <div class="cert-card shadow-dark">
                  <a class="cert-img" href="certifications/files/{c['slug']}.pdf" target="_blank" rel="noopener">
                    <img src="images/certifications/{c['slug']}.jpg" alt="{e(c['title'])} certificate" loading="lazy" />
                  </a>
                  <div class="cert-body">
                    <span class="cert-issuer">{e(c['issuer'])}</span>
                    <h4>{e(c['title'])}</h4>
                    <p class="cert-meta">{e(cert_meta(c))}</p>
                    <div class="cert-links">{cert_links(c, '')}</div>
                  </div>
                </div>
              </div>""")
        out.append("            </div>")
    return "\n".join(out)


def inject_certifications(certs):
    """Replace the block between the certifications markers in index.html, keeping its CRLF line endings."""
    path = ROOT / "index.html"
    raw = path.read_bytes().decode()
    start, end = "<!-- certifications:start -->", "<!-- certifications:end -->"
    assert raw.count(start) == 1 and raw.count(end) == 1, "certifications markers missing in index.html"
    a = raw.index(start) + len(start)
    b = raw.index(end)
    block = "\n" + build_certifications_section(certs) + "\n            "
    newline = "\r\n" if "\r\n" in raw else "\n"
    block = block.replace("\n", newline)
    path.write_bytes((raw[:a] + block + raw[b:]).encode())


def related_certs(certs, key, depth):
    up = "../" * depth
    items = [c for c in certs["certifications"] if c.get("related") == key]
    if not items:
        return ""
    cards = "".join(f"""
              <div class="related-cert">
                <img src="{up}images/certifications/{c['slug']}.jpg" alt="" loading="lazy" />
                <div>
                  <h4>{e(c['title'])}</h4>
                  <p>{e(c['issuer'])} · {e(c['date'])}</p>
                  <div class="cert-links">{cert_links(c, up)}</div>
                </div>
              </div>""" for c in items)
    return f"""          <div class="related-certs">
            <h3>Related certifications</h3>
            <div class="related-grid">{cards}
            </div>
            <a class="related-all" href="{up}#certifications">See all certifications <i class="fa fa-arrow-right"></i></a>
          </div>"""


# ------------------------------------------------------- 404, sitemap, robots
def build_404():
    """Custom "page not found" page. Paths are absolute because it can be served at any URL."""
    body = """          <div class="row">
            <div class="section-title padd-15"><h2>Page not found</h2></div>
          </div>
          <div class="row">
            <p class="page-intro padd-15">Sorry, this page doesn't exist or has moved. Try one of these instead:</p>
          </div>
          <div class="project-actions">
            <a class="btn" href="/"><i class="fa fa-home"></i>Home</a>
            <a class="btn btn-outline" href="/data-science/">Data Science projects</a>
            <a class="btn btn-outline" href="/cybersecurity/">Cybersecurity projects</a>
          </div>"""
    page = shell(0, "", "Page not found | Pule Molise", "This page doesn't exist.", "/404.html", body)
    # depth 0 gives relative paths; make them absolute so the page works at any URL
    for attr in ('href="', 'src="'):
        for prefix in ("css/", "js/", "images/", "data-science/", "cybersecurity/", "#"):
            page = page.replace(attr + prefix, attr + "/" + prefix)
    page = page.replace('<a href=""><span class="logo-icon">', '<a href="/"><span class="logo-icon">')
    page = page.replace('<meta name="description"', '<meta name="robots" content="noindex" />\n    <meta name="description"')
    (ROOT / "404.html").write_text(page)


def build_sitemap(projects):
    urls = ["/", "/data-science/", "/cybersecurity/"] + [f"/cybersecurity/{p['slug']}/" for p in projects]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml += [f"  <url><loc>{SITE}{u}</loc></url>" for u in urls]
    xml.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(xml) + "\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")


# --------------------------------------------------------------- data science
def build_data_science(certs):
    cards = (TOOLS / "data-science-cards.html").read_text().split("-->", 1)[1]
    cards = cards.replace('src="images/', 'src="../images/')
    body = "\n".join([
        breadcrumb(1, ("Data Science", None)),
        section_title("Data Science Projects"),
        '          <div class="row">',
        '            <p class="page-intro padd-15">Machine learning, analytics and data engineering projects. '
        'Each card opens the full project on my <a href="https://www.datascienceportfol.io/pulemoliserr" target="_blank" '
        'rel="noopener">datascienceportfol.io</a> profile.</p>',
        cards.rstrip(),
        "          </div>",
        related_certs(certs, "data-science", 1),
    ])
    page = shell(1, "data-science", "Data Science Projects | Pule Molise",
                 "Data science and machine learning projects by Pule Molise.", "/data-science/", body)
    out = ROOT / "data-science" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)


# -------------------------------------------------------------- cybersecurity
TYPE_LABEL = {"personal": "Personal project", "case-study": "Case study"}


def card(p):
    return f"""            <div class="portfolio-item padd-15" data-group="{p['group']}">
              <a href="{p['slug']}/" class="portfolio-link">
                <div class="portfolio-item-inner shadow-dark">
                  <div class="portfolio-img">
                    <img src="../images/cybersecurity/{p['slug']}.jpg" alt="{e(p['title'])}" loading="lazy" />
                  </div>
                  <div class="portfolio-info padd-15">
                    <span class="project-type {p['type']}">{TYPE_LABEL[p['type']]}</span>
                    <span class="project-category">{e(p['category'])}</span>
                    <h4>{e(p['title'])}</h4>
                    <p>{e(p['summary'])}</p>
                  </div>
                </div>
              </a>
            </div>"""


def build_cyber_index(data, certs):
    projects = data["projects"]
    used = [g for g in data["groups"] if any(p["group"] == g for p in projects)]
    filters = ['<button class="active" data-filter="all">All</button>'] + [
        f'<button data-filter="{g}">{e(data["groups"][g])}</button>' for g in used]
    n_personal = sum(p["type"] == "personal" for p in projects)
    body = "\n".join([
        breadcrumb(1, ("Cybersecurity", None)),
        section_title("Cybersecurity Projects"),
        '          <div class="row">',
        '            <p class="page-intro padd-15">Detection engineering, cloud security, incident response and GRC work. '
        'I completed the <strong>Google Cybersecurity Professional Certificate</strong> and the '
        '<strong>Google Cloud Cybersecurity Certificate</strong>. '
        f'The {n_personal} personal projects build on them; the case studies are based on the certificate\'s scenarios. '
        'Every project is written up with the S.T.A.R. method: Situation, Task, Action, Result.</p>',
        '            <div class="filters padd-15">' + "".join(filters) + "</div>",
        "\n".join(card(p) for p in projects),
        "          </div>",
        related_certs(certs, "cybersecurity", 1),
    ])
    page = shell(1, "cybersecurity", "Cybersecurity Projects | Pule Molise",
                 "Cybersecurity portfolio of Pule Molise: detection engineering, cloud security, incident response and GRC.",
                 "/cybersecurity/", body)
    (ROOT / "cybersecurity" / "index.html").write_text(page)


def star_block(letter, heading, content):
    if isinstance(content, list):
        inner = "<ul>" + "".join(f"<li>{e(x)}</li>" for x in content) + "</ul>"
    else:
        inner = f"<p>{e(content.strip())}</p>"
    return f"""            <div class="star-block">
              <div class="star-letter">{letter}</div>
              <div class="star-content"><h2>{heading}</h2>{inner}</div>
            </div>"""


def build_project(p, prev, nxt):
    links = p.get("links", {})
    actions = []
    if links.get("report"):
        actions.append(f'<a class="btn" href="../files/{links["report"]}" target="_blank" rel="noopener">'
                       '<i class="fa fa-file-pdf"></i>Read the full report</a>')
    if links.get("demo"):
        actions.append(f'<a class="btn" data-link-type="demo" data-link-key="{links["demo"]}" target="_blank" '
                       'rel="noopener"><i class="fa fa-play-circle"></i>Live demo</a>')
    if links.get("github"):
        actions.append(f'<a class="btn btn-outline" data-link-type="github" data-link-key="{links["github"]}" '
                       'target="_blank" rel="noopener"><i class="fab fa-github"></i>View code</a>')
    source = ("Personal project" if p["type"] == "personal"
              else "Case study · Google Cybersecurity Professional Certificate")
    metrics = "".join(f'<div class="metric"><div class="value">{e(v)}</div><div class="label">{e(l)}</div></div>'
                      for v, l in p["metrics"])
    nav = '          <nav class="project-nav">'
    if prev:
        nav += f'<a class="prev" href="../{prev["slug"]}/"><small>&larr; Previous</small>{e(prev["title"])}</a>'
    if nxt:
        nav += f'<a class="next" href="../{nxt["slug"]}/"><small>Next &rarr;</small>{e(nxt["title"])}</a>'
    nav += "</nav>"
    body = "\n".join([
        breadcrumb(2, ("Cybersecurity", "../"), (p["title"], None)),
        '          <header class="project-header">',
        f'            <span class="project-category">{e(p["category"])}</span>',
        f'            <h1>{e(p["title"])}</h1>',
        f'            <p class="lead">{e(p["summary"])}</p>',
        '            <div class="badges"><span class="type">' + e(source) + "</span>"
        + "".join(f"<span>{e(t)}</span>" for t in p["tools"]) + "</div>",
        '            <div class="project-actions">' + "".join(actions) + "</div>",
        "          </header>",
        f'          <div class="project-hero"><img src="../../images/cybersecurity/{p["slug"]}.jpg" alt="{e(p["title"])}" /></div>',
        f'          <div class="metrics">{metrics}</div>',
        '          <article class="star">',
        star_block("S", "Situation", p["situation"]),
        star_block("T", "Task", p["task"]),
        star_block("A", "Action", p["action"]),
        star_block("R", "Result", p["result"]),
        "          </article>",
        nav,
    ])
    og = f'\n    <meta property="og:image" content="{SITE}/images/cybersecurity/{p["slug"]}.jpg" />'
    page = shell(2, "cybersecurity", f'{p["title"]} | Pule Molise', p["summary"],
                 f'/cybersecurity/{p["slug"]}/', body, extra_head=og)
    out = ROOT / "cybersecurity" / p["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)


def main():
    data = yaml.safe_load((TOOLS / "cybersecurity-projects.yml").read_text())
    projects = data["projects"]
    slugs = [p["slug"] for p in projects]
    assert len(slugs) == len(set(slugs)), "duplicate slug"
    for p in projects:
        assert p["group"] in data["groups"], f"{p['slug']}: unknown group {p['group']}"
        for k in ("action", "result", "tools"):
            for item in p[k]:
                assert isinstance(item, str), (
                    f"{p['slug']} {k}: an item was read as {type(item).__name__}. "
                    'Put text containing ": " in double quotes.')
        for key in ("report",):
            f = p.get("links", {}).get(key)
            assert not f or (ROOT / "cybersecurity" / "files" / f).exists(), f"missing file {f}"
        assert (ROOT / "images" / "cybersecurity" / f"{p['slug']}.jpg").exists(), f"missing thumbnail for {p['slug']}"
    certs = yaml.safe_load((TOOLS / "certifications.yml").read_text())
    for c in certs["certifications"]:
        assert c["group"] in certs["groups"], f"{c['slug']}: unknown group {c['group']}"
        for f in (ROOT / "certifications" / "files" / f"{c['slug']}.pdf", ROOT / "images" / "certifications" / f"{c['slug']}.jpg"):
            assert f.exists(), f"missing {f.relative_to(ROOT)}"
    inject_certifications(certs)
    build_404()
    build_sitemap(projects)
    build_data_science(certs)
    build_cyber_index(data, certs)
    for i, p in enumerate(projects):
        build_project(p, projects[i - 1] if i else None, projects[i + 1] if i + 1 < len(projects) else None)
    print(f"Built certifications ({len(certs['certifications'])}), data-science/, cybersecurity/ "
          f"and {len(projects)} project pages.")


if __name__ == "__main__":
    main()
