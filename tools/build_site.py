"""Build the static portfolio site from the Notion Markdown export.

Usage (from the repo root):
    python tools/build_site.py                      # export at ../Notion_Portfolio
    python tools/build_site.py --export "D:/path/to/export"

Writes index.html, projects/*.html and assets/img/*. It never touches
assets/css, assets/js, assets/fonts, 404.html, README.md or CLAUDE.md.
Needs Python 3.9+ and Pillow (pip install pillow).
"""
import os, re, glob, html, hashlib, argparse, urllib.parse
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
ap = argparse.ArgumentParser()
ap.add_argument('--export', default=os.path.join(OUT, '..', 'Notion_Portfolio'),
                help='Folder that contains the unzipped Notion export')
ARGS = ap.parse_args()
SRC = os.path.abspath(ARGS.export)
_roots = [d for d in glob.glob(os.path.join(SRC, 'John Novoa*')) if os.path.isdir(d)]
if not _roots:
    raise SystemExit(f'No Notion export found in {SRC} (expected a folder named "John Novoa ...")')
ROOT = _roots[0]
PROJ_DIR = [d for d in glob.glob(os.path.join(ROOT, 'Open boxes for details*')) if os.path.isdir(d)][0]
SUB_DIR = os.path.join(PROJ_DIR, 'Additional Engineering Projects', 'Complementary Design Work')
SITE_URL = 'https://johnnovoa.github.io/portfolio/'
EMAIL = 'johnenovoap@gmail.com'
LINKEDIN = 'https://www.linkedin.com/in/john-novoa'

TYPO_FIXES = {'desing': 'design'}


def esc(s):
    return html.escape(s, quote=True)


def fix(s):
    for a, b in TYPO_FIXES.items():
        s = s.replace(a, b)
    return s.strip()


def inline(s):
    s = esc(fix(s))
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def split_year(title):
    m = re.match(r'^(.*?)\s*\((\d{4})\)?\s*$', title)
    return (m.group(1), m.group(2)) if m else (title, '')


def parse_page(md_path):
    lines = open(md_path, encoding='utf-8').read().splitlines()
    base = os.path.relpath(os.path.dirname(md_path), SRC)
    page = {'title': fix(lines[0].lstrip('# ')), 'props': {}, 'images': [], 'groups': []}
    i = 1
    while i < len(lines):
        m = re.match(r'^(Industry|Key skills|Description|Order): ?(.*)$', lines[i])
        if m:
            page['props'][m.group(1)] = m.group(2).strip()
        elif lines[i].strip():
            break
        i += 1
    in_aside, group = False, None
    while i < len(lines):
        ln = lines[i].rstrip()
        im = re.match(r'^!\[(.*?)\]\((.+?)\)$', ln)
        if im:
            rel = os.path.normpath(os.path.join(base, urllib.parse.unquote(im.group(2))))
            cap = fix(im.group(1))
            page['images'].append({'rel': rel, 'caption': cap})
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and fix(lines[j]) == cap:
                i = j
        elif ln.startswith('<aside'):
            in_aside = True
        elif ln.startswith('</aside'):
            in_aside, group = False, None
        elif in_aside:
            hm = re.match(r'^\S*\s*\*\*(.+?):?\*\*\s*$', ln)
            if hm and not ln.startswith('-'):
                group = {'title': hm.group(1).rstrip(':'), 'items': []}
                page['groups'].append(group)
            elif ln.startswith('- '):
                if group is None:
                    group = {'title': '', 'items': []}
                    page['groups'].append(group)
                group['items'].append(ln[2:])
        i += 1
    return page


# ---------------------------------------------------------------- data
projects = []
for md in glob.glob(os.path.join(PROJ_DIR, '*.md')):
    p = parse_page(md)
    p['order'] = int(p['props'].get('Order', 99))
    p['name'], p['year'] = split_year(p['title'])
    p['slug'] = slug(p['name'])
    projects.append(p)
projects.sort(key=lambda p: p['order'])

subprojects = []
for md in glob.glob(os.path.join(SUB_DIR, '*.md')):
    p = parse_page(md)
    p['order'] = int(p['props'].get('Order', 99))
    p['name'], p['year'] = split_year(p['title'])
    p['slug'] = slug(p['name'])
    subprojects.append(p)
subprojects.sort(key=lambda p: p['order'])

main_md = open(glob.glob(os.path.join(SRC, 'John Novoa*.md'))[0], encoding='utf-8').read()
INTRO = [l for l in main_md.splitlines() if l.startswith('Senior Mechanical Engineer')][0]
PHOTO = os.path.relpath(glob.glob(os.path.join(ROOT, '954ccd86*.png'))[0], SRC)

experience = [
    ('2026-Present', 'Robot.com', 'Senior Mechanical Engineer'),
    ('2024-2025', 'Grupo Abstract', 'CAD/CAM Applications Engineer'),
    ('2023-2024', 'Perdomo Business Group', 'Product Design Engineer'),
    ('2022-2023', 'Idascol', 'Senior Mechanical Designer'),
    ('2021-2022', 'voestalpine High Performance Metals Colombia', 'Production Planning Engineer'),
    ('2019-2021', 'Matrix Telcom', 'CNC Programmer and Operator'),
]
education = [
    ('2025-2026', 'Universidad Distrital Francisco José de Caldas',
     'Specialization in Engineering Project Management (postgraduate degree)'),
    ('2012-2019', 'Universidad Distrital Francisco José de Caldas', 'B.E. Mechanical Engineering'),
]
certifications = [
    ('2025', 'CSWP-Simulation'),
    ('2025', 'ENOVIA Collaborative Industry Innovator Associate'),
    ('2024', 'CSWE, Certified SOLIDWORKS Expert'),
    ('2024', 'SolidCAM Technician Associate'),
    ('2020', 'CSWP'),
    ('2020', 'CSWP Advanced: Mold Making, Surfacing, Drawing Tools, Weldments, Sheet Metal'),
]
skills = [
    ('CAD & Design', 'SOLIDWORKS (CSWE), Solid Edge, AutoCAD. DFM, parametric modeling, assemblies, drawings.'),
    ('CAE & Simulation', 'ANSYS, SOLIDWORKS Simulation (CSWP-Simulation)'),
    ('CAM & Manufacturing', 'SolidCAM, Mastercam'),
    ('PLM & Collaboration', '3DEXPERIENCE, SOLIDWORKS PDM'),
    ('CAD Automation', 'Python, SOLIDWORKS API'),
    ('Project Management', 'Engineering Project Management specialization, agile and hybrid methods'),
    ('Languages', 'Spanish (native), English (EF SET 62/100, C1)'),
]

# ---------------------------------------------------------------- images
IMG_CACHE = {}
PHOTO_CACHE = {}
BASE_CACHE = {}


def base_image(rel):
    """Open an export image, flatten transparency onto white (except the portrait), cap at 1600 px."""
    if rel in BASE_CACHE:
        return BASE_CACHE[rel]
    im = Image.open(os.path.join(SRC, rel))
    if '954ccd86' in rel:
        im = im.convert('RGBA')
        im.thumbnail((480, 480), Image.LANCZOS)
    else:
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA')
            bg = Image.new('RGB', im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[3])
            im = bg
        else:
            im = im.convert('RGB')
        im.thumbnail((1600, 1600), Image.LANCZOS)
    BASE_CACHE[rel] = im
    return im


def ratio(rel):
    im = base_image(rel)
    return im.width / im.height


def is_photo(rel):
    """True when the image corners are not white (a photo, not a render on white)."""
    if rel in PHOTO_CACHE:
        return PHOTO_CACHE[rel]
    im = base_image(rel).convert('RGB')
    w, h = im.size
    pts = [(2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3), (w // 2, 2), (w // 2, h - 3)]
    dark = sum(1 for x, y in pts if min(im.getpixel((x, y))) < 225)
    PHOTO_CACHE[rel] = dark >= 3
    return PHOTO_CACHE[rel]


def asset(rel, kind='full'):
    """Write an image into assets/img and return (path_from_root, w, h)."""
    key = (rel, kind)
    if key in IMG_CACHE:
        return IMG_CACHE[key]
    im = base_image(rel).copy()
    limit = {'full': 1600, 'thumb': 760}[kind]
    im.thumbnail((limit, limit), Image.LANCZOS)
    stem = hashlib.md5(rel.replace(os.sep, '/').encode()).hexdigest()[:10]
    name = stem + ('' if kind == 'full' else '-sm') + '.webp'
    path = f'assets/img/{name}'
    im.save(os.path.join(OUT, path), 'WEBP', quality=84, method=6)
    IMG_CACHE[key] = (path, im.width, im.height)
    return IMG_CACHE[key]


def img_tag(rel, prefix, alt, kind='full', cls='', eager=False, sizes=None):
    path, w, h = asset(rel, kind)
    extra = '' if eager else ' loading="lazy"'
    srcset = ''
    if kind == 'full' and w > 760:
        tp, tw, _ = asset(rel, 'thumb')
        srcset = f' srcset="{prefix}{tp} {tw}w, {prefix}{path} {w}w" sizes="{sizes or "(max-width: 760px) 100vw, 60vw"}"'
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="{prefix}{path}"{srcset} width="{w}" height="{h}" alt="{esc(alt)}" decoding="async"{extra}>'


# ---------------------------------------------------------------- shared chrome
def head(title, desc, prefix, canonical, og_img):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0E1B2E">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{prefix}assets/fonts/archivo-wdth.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{prefix}assets/css/site.css">
</head>
'''


def nav(prefix, home):
    h = '' if home else f'{prefix}index.html'
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="nav">
  <div class="wrap nav-in">
    <a class="mark" href="{prefix}index.html" aria-label="John Novoa, home"><span class="mark-box">JN</span><span class="mark-name">John Novoa</span></a>
    <nav aria-label="Main">
      <a href="{h}#work">Work</a>
      <a href="{h}#about">About</a>
      <a class="nav-cta" href="mailto:{EMAIL}">Email me</a>
    </nav>
  </div>
</header>
'''


def contact_band():
    return f'''<section class="contact" id="contact" aria-labelledby="contact-h">
  <div class="wrap contact-in">
    <div>
      <h2 id="contact-h">Let's work together</h2>
      <p>Email is the fastest way to reach me. I reply in English or Spanish.</p>
    </div>
    <div class="contact-actions">
      <a class="btn btn-dark" href="mailto:{EMAIL}">Email me</a>
      <button class="btn btn-line copy" type="button" data-copy="{EMAIL}">Copy email</button>
      <a class="btn btn-line" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
    </div>
    <p class="contact-mail">{EMAIL}</p>
  </div>
</section>
'''


def foot(prefix):
    return f'''<footer class="foot">
  <div class="wrap foot-in">
    <span>John Novoa, Senior Mechanical Engineer</span>
    <span>Updated November 2026</span>
  </div>
</footer>
<dialog class="lightbox" aria-label="Enlarged image">
  <button class="lb-close" type="button" aria-label="Close">Close</button>
  <img alt="">
  <p class="lb-cap"></p>
</dialog>
<script src="{prefix}assets/js/site.js" defer></script>
</body>
</html>
'''


def chips(s):
    return ''.join(f'<li>{esc(x.strip())}</li>' for x in s.split(',') if x.strip())


def impact_items(p, n=2):
    for g in p['groups']:
        if 'Impact' in g['title']:
            return g['items'][:n]
    return []


# ---------------------------------------------------------------- home
def home():
    pre = ''
    hero_imgs = [
        ('Humanoid Robot Dual-Arm Redesign (2026)/2_dual_arm_robot.png', 'Design', 'Dual-arm humanoid robot, CAD model', 'hc-a'),
        ('Removable Pizza Carrier for a Delivery Robot (2026/Removable_Pizza_Carrier_-_Pizza_carrier_mounted_on_the_delivery_robot.jpg',
         'Build', 'Pizza carrier on a delivery robot', 'hc-b'),
        ('Humanoid Robot Dual-Arm Redesign (2026)/5_chest_frame_stress.png', 'Validate', 'Chest frame stress analysis', 'hc-c'),
    ]
    base = os.path.relpath(PROJ_DIR, SRC)
    collage = ''
    for i, (r, label, alt, cls) in enumerate(hero_imgs):
        rel = os.path.normpath(os.path.join(base, r))
        collage += (f'<figure class="hc {cls}" data-enter style="--d:{i}">'
                    f'{img_tag(rel, pre, alt, "thumb" if cls != "hc-c" else "full", eager=True)}'
                    f'<figcaption><span class="tag">{label}</span>{esc(alt)}</figcaption></figure>')

    featured_slugs = [p['slug'] for p in projects if p['images']][:4]
    feat = ''
    for k, p in enumerate([p for p in projects if p['slug'] in featured_slugs]):
        first = p['images'][0]
        bullets = ''.join(f'<li>{inline(x)}</li>' for x in impact_items(p))
        feat += f'''
    <article class="feature{' flip' if k % 2 else ''}">
      <a class="feature-media{' cover' if is_photo(first['rel']) else ''}" href="projects/{p['slug']}.html" tabindex="-1" aria-hidden="true">
        {img_tag(first['rel'], pre, first['caption'], 'full', sizes='(max-width: 900px) 100vw, 55vw')}
      </a>
      <div class="feature-text">
        <p class="meta"><span class="year">{p['year']}</span>{esc(p['props'].get('Industry', ''))}</p>
        <h3><a href="projects/{p['slug']}.html">{esc(p['name'])}</a></h3>
        <p class="feature-desc">{inline(p['props'].get('Description', ''))}</p>
        {f'<ul class="ticks">{bullets}</ul>' if bullets else ''}
        <a class="more" href="projects/{p['slug']}.html">Read the case study<span class="sr"> about {esc(p['name'])}</span></a>
      </div>
    </article>'''

    cards = ''
    for p in projects:
        if p['slug'] in featured_slugs:
            continue
        if p['images']:
            thumb = img_tag(p['images'][0]['rel'], pre, '', 'thumb')
        else:
            thumb = '<span class="thumb-code" aria-hidden="true"><span>SOLIDWORKS API</span><span>Python</span><span>Batch runs</span></span>'
        cards += f'''
      <li class="card">
        <a href="projects/{p['slug']}.html">
          <span class="card-thumb{' cover' if p['images'] and is_photo(p['images'][0]['rel']) else ''}">{thumb}</span>
          <span class="card-body">
            <span class="meta">{f'<span class="year">{p["year"]}</span>' if p['year'] else ''}{esc(p['props'].get('Industry', ''))}</span>
            <span class="card-title">{esc(p['name'])}</span>
            <span class="card-desc">{inline(p['props'].get('Description', ''))}</span>
          </span>
        </a>
      </li>'''

    timeline = ''.join(f'<li><span class="when">{esc(d)}</span><span><strong>{esc(a)}</strong>{esc(b)}</span></li>'
                       for d, a, b in experience)
    edu = ''.join(f'<li><span class="when">{esc(d)}</span><span><strong>{esc(b)}</strong>{esc(a)}</span></li>'
                  for d, a, b in education)
    certs = ''.join(f'<li><span class="when">{y}</span><span>{esc(c)}</span></li>' for y, c in certifications)
    sk = ''.join(f'<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in skills)
    processes = ['Injection molding', 'CNC machining', 'Sheet metal', 'Welding', 'Casting', '3D printing']

    desc = ('John Novoa, Senior Mechanical Engineer in Colombia. Robots, electrical safety products, '
            'injection molds and industrial parts, designed for manufacturing and checked with FEA.')
    og = 'assets/img/og.jpg'
    page = head('John Novoa | Senior Mechanical Engineer', desc, pre, SITE_URL, og)
    page += '<body class="home">\n' + nav(pre, True)
    page += f'''<main id="main">
<section class="hero" aria-labelledby="hero-h">
  <div class="wrap hero-in">
    <div class="hero-text" data-enter style="--d:0">
      <p class="kicker">Senior Mechanical Engineer in Colombia</p>
      <h1 id="hero-h">John Novoa</h1>
      <p class="hero-lead">I design robots, tools and molds around the process that will make them: CNC machining, sheet metal, casting, injection molding or 3D printing.</p>
      <div class="hero-actions">
        <a class="btn btn-yellow" href="#work">See my projects</a>
        <a class="btn btn-ghost" href="mailto:{EMAIL}">Email me</a>
      </div>
      <ul class="hero-facts">
        <li><strong>7 years</strong> in mechanical design</li>
        <li><strong>CSWE</strong> Certified SOLIDWORKS Expert</li>
        <li><strong>FEA</strong> SOLIDWORKS Simulation and ANSYS</li>
      </ul>
    </div>
    <div class="hero-collage">{collage}</div>
  </div>
  <div class="process-strip"><div class="wrap"><span class="ps-label">Designed for</span><ul>{''.join(f'<li>{x}</li>' for x in processes)}</ul></div></div>
</section>

<section class="work" id="work" aria-labelledby="work-h">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="work-h">Selected work</h2>
      <p>Robots, electrical safety products, plastic parts and molds. Most recent first.</p>
    </div>
    {feat}
  </div>
</section>

<section class="more-work" aria-labelledby="more-h">
  <div class="wrap">
    <h2 id="more-h" class="sec-title">More projects</h2>
    <ul class="cards">{cards}
    </ul>
  </div>
</section>

<section class="about" id="about" aria-labelledby="about-h">
  <div class="wrap">
    <div class="about-top">
      {img_tag(PHOTO, pre, 'Portrait of John Novoa', 'full', cls='portrait')}
      <div>
        <h2 id="about-h" class="sec-title">About</h2>
        <p class="about-lead">{inline(INTRO)}</p>
      </div>
    </div>
    <div class="about-grid">
      <div class="col">
        <h3>Experience</h3>
        <ol class="tl">{timeline}</ol>
      </div>
      <div class="col">
        <h3>Education</h3>
        <ol class="tl">{edu}</ol>
        <h3>Certifications</h3>
        <ul class="tl certs">{certs}</ul>
      </div>
      <div class="col">
        <h3>Tools</h3>
        <dl class="skills">{sk}</dl>
      </div>
    </div>
  </div>
</section>
</main>
'''
    page += contact_band() + foot(pre)
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page)


# ---------------------------------------------------------------- project pages
def figure(img, pre, kind='full'):
    cap = img['caption']
    wide = ' wide' if ratio(img['rel']) > 1.45 else ''
    return (f'<figure class="shot{wide}"><button class="zoom" type="button" aria-label="Enlarge image: {esc(cap)}">'
            f'{img_tag(img["rel"], pre, cap, kind)}</button><figcaption>{esc(cap)}</figcaption></figure>')


def groups_html(groups):
    out = ''
    for g in groups:
        items = ''.join(f'<li>{inline(x)}</li>' for x in g['items'])
        if 'Impact' in g['title']:
            out += f'<section class="impact"><h2>{esc(g["title"])}</h2><ul class="ticks">{items}</ul></section>'
        elif g['title']:
            out += f'<section class="block"><h2>{esc(g["title"])}</h2><ul class="dots">{items}</ul></section>'
        else:
            out += f'<ul class="dots">{items}</ul>'
    return out


def project_page(p, idx):
    pre = '../'
    imgs = p['images']
    hero = imgs[0] if imgs else None
    rest = imgs[1:]
    prev_p = projects[idx - 1] if idx > 0 else None
    next_p = projects[idx + 1] if idx + 1 < len(projects) else None
    hero_html = ''
    if hero:
        hero_html = f'<figure class="p-hero-img"><button class="zoom" type="button" aria-label="Enlarge image: {esc(hero["caption"])}">{img_tag(hero["rel"], pre, hero["caption"], "full", eager=True, sizes="(max-width: 900px) 100vw, 50vw")}</button><figcaption>{esc(hero["caption"])}</figcaption></figure>'
    gallery = ''
    if rest:
        gallery = '<section class="gallery" aria-label="Images"><div class="shots">' + ''.join(figure(i, pre) for i in rest) + '</div></section>'
    subs = ''
    if p['name'] == 'Additional Engineering Projects':
        for s in subprojects:
            sfigs = ''.join(figure(i, pre, 'full') for i in s['images'])
            subs += f'''
    <section class="sub" id="{s['slug']}">
      <div class="sub-head">
        <h2>{esc(s['name'])}{f' <span class="year">{s["year"]}</span>' if s['year'] else ''}</h2>
        <p>{inline(s['props'].get('Description', ''))}</p>
        {groups_html(s['groups'])}
      </div>
      <div class="shots small">{sfigs}</div>
    </section>'''
    pager = '<nav class="pager" aria-label="More projects">'
    pager += (f'<a class="pg prev" href="{prev_p["slug"]}.html"><span>Previous</span>{esc(prev_p["name"])}</a>' if prev_p else '<span></span>')
    pager += (f'<a class="pg next" href="{next_p["slug"]}.html"><span>Next</span>{esc(next_p["name"])}</a>' if next_p else '<span></span>')
    pager += '</nav>'

    desc = p['props'].get('Description', '')
    og = asset(hero['rel'], 'full')[0] if hero else 'assets/img/og.jpg'
    page = head(f'{p["name"]} | John Novoa', desc, pre, f'{SITE_URL}projects/{p["slug"]}.html', og)
    page += '<body class="project">\n' + nav(pre, False)
    page += f'''<main id="main">
<article>
  <header class="p-head{' no-img' if not hero else ''}">
    <div class="wrap p-head-in">
      <div class="p-head-text">
        <a class="back" href="../index.html#work">All projects</a>
        <p class="meta">{f'<span class="year">{p["year"]}</span>' if p['year'] else ''}{esc(p['props'].get('Industry', ''))}</p>
        <h1>{esc(p['name'])}</h1>
        <p class="p-lead">{inline(desc)}</p>
        <ul class="chips" aria-label="Key skills">{chips(p['props'].get('Key skills', ''))}</ul>
      </div>
      {hero_html}
    </div>
  </header>
  <div class="wrap p-body">
    {groups_html(p['groups']) if p['groups'] else ''}
    {gallery}
    {subs}
    {pager}
  </div>
</article>
</main>
'''
    page += contact_band() + foot(pre)
    open(os.path.join(OUT, 'projects', f'{p["slug"]}.html'), 'w', encoding='utf-8').write(page)


# ---------------------------------------------------------------- run
import shutil
for d in ['assets/img', 'projects']:
    full = os.path.join(OUT, d)
    if os.path.isdir(full):
        shutil.rmtree(full)
    os.makedirs(full)
# social preview from the cover collage
col = [k for k in (os.path.relpath(f, SRC) for f in glob.glob(os.path.join(PROJ_DIR, '**', '*Cover_collage*'), recursive=True))][0]
im = base_image(col).copy()
w, h = im.size
th = int(w * 630 / 1200)
im = im.crop((0, (h - th) // 2, w, (h - th) // 2 + th)).resize((1200, 630), Image.LANCZOS)
im.save(os.path.join(OUT, 'assets/img/og.jpg'), 'JPEG', quality=85)

home()
for i, p in enumerate(projects):
    project_page(p, i)
if not os.path.exists(os.path.join(OUT, '.nojekyll')):
    open(os.path.join(OUT, '.nojekyll'), 'w').write('')
print(f'Built {1 + len(projects)} pages and {len(IMG_CACHE)} images into {OUT}')
