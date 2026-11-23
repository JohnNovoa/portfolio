# John Novoa | Mechanical Design Portfolio

Live site: https://johnnovoa.github.io/portfolio/

Static portfolio of John Novoa, Senior Mechanical Engineer: robotics, product development, design for manufacturing, FEA and SOLIDWORKS automation.

## Structure

```
index.html            Home: hero, selected work, more projects, about, contact
projects/*.html       One case study page per project
assets/css/site.css   Styles
assets/js/site.js     Image lightbox and copy-email button
assets/img/           Project images (WebP)
assets/fonts/         Archivo variable font (SIL Open Font License)
404.html              Not-found page for GitHub Pages
tools/build_site.py   Regenerates the HTML and images from the Notion export
CLAUDE.md             Instructions for Claude Code
```

No build step for visitors and no dependencies. Open `index.html` in a browser to preview.

To regenerate after a Notion update: unzip the Notion Markdown export into `../Notion_Portfolio/` and run `python tools/build_site.py` (needs Python 3.9+ and Pillow: `pip install -r tools/requirements.txt`).

## Publishing

GitHub Pages serves the `main` branch from the root folder (Settings > Pages > Deploy from a branch > main / root).

## Content

Text and images come from the Notion portfolio. Project details stay general: product type, role, processes and results, with no internal project names, supplier names or specifications.
