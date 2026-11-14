# Portfolio pages: how to edit

The Portfolio tab on the home page links to two branch pages:

| URL | Built from |
|---|---|
| `/data-science/` | `tools/data-science-projects.yml` (short cards linking to datascienceportfol.io) |
| `/cybersecurity/` | `tools/cybersecurity-projects.yml` |
| `/cybersecurity/<slug>/` | one S.T.A.R. page per project in the same YAML file |

## Change text or add a project

1. Edit `tools/cybersecurity-projects.yml` (or `tools/data-science-projects.yml`).
   For a new data-science project, add an `800×576` thumbnail at `images/data-science/<slug>.jpg`.
   For a new cybersecurity project, add a `1000×720` thumbnail at `images/cybersecurity/<slug>.jpg`,
   and put any PDF report in `cybersecurity/files/`.
2. Rebuild the pages:
   ```bash
   pip install pyyaml
   python tools/build_portfolio.py
   ```
3. Commit the changed files and push. GitHub Pages publishes them automatically.

If YAML text contains `: ` (a colon followed by a space), wrap the whole line in double quotes. The build
script stops with a clear message if you forget.

## Add GitHub and live-demo links

No rebuild needed: paste the URLs into `cybersecurity/links.js`. Each "View code" or "Live demo" button
stays hidden until its URL is filled in.

## Update the project counts on the home page

The branch cards on the home page (`index.html`, Portfolio section) show "17 projects" and "13 projects".
Update those numbers by hand when you add or remove projects.

## Certifications

The Certifications section on the home page and the "Related certifications" strips on `/data-science/` and
`/cybersecurity/` are built from `tools/certifications.yml`.

To add a certificate: put the PDF in `certifications/files/<slug>.pdf`, create a preview image at
`images/certifications/<slug>.jpg` (for example, a screenshot of the PDF about 880 px wide), add an entry to the
YAML file and run `python tools/build_portfolio.py`. The script rewrites only the part of `index.html` between the
`<!-- certifications:start -->` and `<!-- certifications:end -->` markers.

## Also generated

`python tools/build_portfolio.py` also writes `404.html` (the "page not found" page), `sitemap.xml` and
`robots.txt`. The sitemap lists every portfolio page, so it updates itself when you add a project.
