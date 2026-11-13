# Portfolio pages: how to edit

The Portfolio tab on the home page links to two branch pages:

| URL | Built from |
|---|---|
| `/data-science/` | `tools/data-science-cards.html` (the six original cards, unchanged) |
| `/cybersecurity/` | `tools/cybersecurity-projects.yml` |
| `/cybersecurity/<slug>/` | one S.T.A.R. page per project in the same YAML file |

## Change text or add a project

1. Edit `tools/cybersecurity-projects.yml` (or `tools/data-science-cards.html`).
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

The branch cards on the home page (`index.html`, Portfolio section) show "6 projects" and "13 projects".
Update those numbers by hand when you add or remove projects.
