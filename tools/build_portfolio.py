"""Build the portfolio branch pages of pulemolise.net.

Generates:
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


# --------------------------------------------------------------- data science
def build_data_science():
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


def build_cyber_index(data):
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
    build_data_science()
    build_cyber_index(data)
    for i, p in enumerate(projects):
        build_project(p, projects[i - 1] if i else None, projects[i + 1] if i + 1 < len(projects) else None)
    print(f"Built data-science/, cybersecurity/ and {len(projects)} project pages.")


if __name__ == "__main__":
    main()
