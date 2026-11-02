"""Generate the portfolio's HTML pages from one shared head, header and footer.

Usage (from the repo root): npm run build:html
                        or: python tools/build_pages.py

Edit page content in this file, never in the generated .html files: the next build overwrites them.
"""
import sys
from datetime import date
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent

# Formspree form ID (the part after /f/ in your Formspree endpoint).
# Until it is set, the form shows a "not connected yet" message instead of sending.
FORMSPREE_ID = "YOUR_FORM_ID"

# Drop your résumé at this path and rebuild: a "Résumé" nav link and intro button appear automatically.
RESUME = "assets/Konstantin-Tovshtein-Resume.pdf"
HAS_RESUME = (ROOT / RESUME).exists()

# Link previews (LinkedIn, Slack, iMessage) need absolute addresses.
SITE_URL = "https://konstantintovshtein.github.io/portfolio/"
# 1200x630 card shown with every shared link. Edit tools/share-card.html and re-render it
# (instructions at the top of that file); the copy there must stay factual.
SHARE_IMAGE = "assets/png/share-card.png"
SHARE_IMAGE_ALT = (
    "Konstantin Tovshtein, BBA student at Simon Fraser University in MIS and Accounting. "
    "25% lower system costs after his ProxySmart dashboard at Jetlink Solutions; "
    "10% above his assigned workload at Crowe MacKay."
)

NAV = [
    ("home", "./index.html", "Home"),
    ("projects", "./projects.html", "Projects"),
    *([("resume", f"./{RESUME}", "Résumé")] if HAS_RESUME else []),
    ("contact", "./index.html#contact", "Contact"),
]

LINKEDIN = "https://www.linkedin.com/in/konstantin-tovshtein-0b1a21221/"
GITHUB = "https://github.com/konstantintovshtein?tab=repositories"
CORESHARE_REPO = "https://github.com/konstantintovshtein/coreshare"
CORESHARE_TEAM_REPO = "https://github.com/borodooovitsyn/coreshare"
TEAM_BADGE = '<span class="badge"><svg aria-hidden="true" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>Team project</span>'
RESUME_ICON = '<svg class="pill__icon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M6 2.75h8.5L19 7.25v14H6z"/><path d="M14 2.75v5h5M9 12.5h6M9 16h6"/></svg>'

# Brand marks drawn in the text colour, so they stay sharp at any size. Paths: Simple Icons (CC0).
SOCIAL_ICONS = {
    "linkedin": (
        "2 2 20 20",
        "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.064 2.064 0 1 1 0-4.128 2.064 2.064 0 0 1 0 4.128zM7.119 20.452H3.555V9h3.564z",
    ),
    "github": (
        "0 0 24 24",
        "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12",
    ),
}


def social_icon(name, cls, size):
    box, path = SOCIAL_ICONS[name]
    return (
        f'<svg class="{cls}" viewBox="{box}" width="{size}" height="{size}" fill="currentColor"'
        f' aria-hidden="true" focusable="false"><path d="{path}"/></svg>'
    )


TABLEAU_BEEDIE = "https://public.tableau.com/app/profile/konstantin.tovshtein/viz/BusinessAnalyticsHackathon/Dashboard"
ONE_PAY_SITE = "https://onepayltd.kz/ru"
PROXYSMART_IMG = "./assets/jpeg/jetlink-proxysmart-dashboard.webp"


def ext_links(links, indent, cls="text-link"):
    return "".join(
        f'\n{indent}<a href="{url}" class="{cls}" target="_blank" rel="noopener noreferrer">{label}</a>'
        for label, url in links
    )


def srcset(src):
    # Smaller copies sit next to the original as name-800.webp etc.; list the ones that exist.
    stem = src.removesuffix(".webp")
    widths = [w for w in (800, 1280, 1920) if (ROOT / f"{stem}-{w}.webp").exists()]
    return ", ".join([f"{stem}-{w}.webp {w}w" for w in widths] + [f"{src} 2505w"])


def head(name, title, desc, cls):
    url = SITE_URL if name == "index.html" else SITE_URL + name
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#05070c" />
    <meta name="color-scheme" content="dark" />
    <title>{title}</title>
    <meta name="description" content="{desc}" />
    <link rel="canonical" href="{url}" />

    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Konstantin Tovshtein" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{SITE_URL}{SHARE_IMAGE}" />
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="{SHARE_IMAGE_ALT}" />
    <meta name="twitter:card" content="summary_large_image" />

    <link rel="icon" href="./assets/png/favicon-32.png" sizes="32x32" type="image/png" />
    <link rel="icon" href="./assets/svg/favicon.svg" type="image/svg+xml" />
    <link rel="apple-touch-icon" href="./assets/png/apple-touch-icon.png" />

    <link
      rel="preload"
      href="./assets/fonts/kt-sans-latin-var.woff2"
      as="font"
      type="font/woff2"
      crossorigin
    />
    <script>document.documentElement.classList.add('js')</script>
    <link rel="stylesheet" href="css/style.css" />
  </head>
  <body class="{cls}">
    <a class="skip-link" href="#main">Skip to content</a>
    <div class="page-bg" aria-hidden="true"><canvas class="page-bg__streaks"></canvas></div>
"""


def header(active):
    def cur(key):
        return ' aria-current="page"' if key == active else ""

    links = "\n".join(
        f'          <li><a href="{href}" class="nav__link"{cur(key)}>{label}</a></li>'
        for key, href, label in NAV
    )
    return f"""    <header class="nav">
      <div class="nav__inner">
        <a href="./index.html" class="nav__logo">Konstantin Tovshtein</a>
        <nav aria-label="Main">
          <ul class="nav__links">
{links}
          </ul>
        </nav>
      </div>
    </header>
"""


FOOTER = f"""    <footer class="footer">
      <p>&copy; {date.today().year} Konstantin Tovshtein</p>
    </footer>

    <script src="./assets/vendor/lenis/lenis.min.js"></script>
    <script src="./index.js"></script>
  </body>
</html>
"""


def tags(items, indent):
    inner = "\n".join(f'{indent}  <li class="tag">{i}</li>' for i in items)
    return f'{indent}<ul class="tags">\n{inner}\n{indent}</ul>'


def page(name, title, desc, active, cls, body):
    main = f'    <main id="main" tabindex="-1">\n{body}    </main>\n'
    html = head(name, title, desc, cls) + header(active) + main + FOOTER
    (ROOT / name).write_text(html, encoding="utf-8", newline="\n")
    print("wrote", name)


def section(key, title, inner, extra=""):
    return f"""    <section class="section reveal" id="{key}" aria-labelledby="{key}-title">
      <div class="container">
        <h2 class="section-title" id="{key}-title" data-type>{title}</h2>
{inner}{extra}
      </div>
    </section>
"""


# ---------------------------------------------------------------- content

ROLES = [
    {
        "mark": "OP",
        "org": "One Pay Ltd",
        "role": "Compliance and Engineering Support",
        "meta": "Payment processing &middot; PCI DSS and Visa certification",
        "points": [
            "Gathered and organized the legal documentation the company needed to pass <strong>PCI DSS</strong> and <strong>Visa certification</strong>.",
            "Helped optimize the company&rsquo;s <strong>Rust</strong>-based payment software so it adhered to PCI DSS requirements.",
        ],
        "tools": ["Rust", "PCI DSS", "Visa certification", "GitHub"],
        "case": "./one-pay.html",
        "links": [("One Pay website", ONE_PAY_SITE)],
    },
    {
        "mark": "JS",
        "org": "Jetlink Solutions",
        "role": "Technical Support Specialist and Data Analyst",
        "meta": "IT support &middot; Data analysis",
        "points": [
            "Resolved hardware and software issues for staff quickly so work kept moving.",
            "Built <strong>ProxySmart</strong>, a custom dashboard that tracks the company&rsquo;s proxy servers, devices and ports, refreshing every 15 minutes.",
            "The dashboard helped management cut system costs by <strong>25%</strong>.",
        ],
        "tools": ["ProxySmart", "Dashboard design", "Data analysis", "Technical support"],
        "case": "./jetlink.html",
    },
    {
        "mark": "RA",
        "org": "Repatt AI",
        "role": "Database Automation and Sales Outreach",
        "meta": "AI startup &middot; Lead generation",
        "points": [
            "Wrote <strong>Python</strong> scripts that extracted business data from Google Maps into Excel spreadsheets.",
            "Turned that data into customer leads and ran business sales outreach.",
        ],
        "tools": ["Python", "Excel", "Automation"],
    },
    {
        "mark": "CM",
        "org": "Crowe MacKay",
        "role": "Accounting Assistant",
        "meta": "Public accounting",
        "points": [
            "Reviewed corporate financial ledgers.",
            "Compiled financial information for management using the firm&rsquo;s accounting tools.",
            "Completed <strong>10% more</strong> work than my assigned target.",
        ],
        "tools": ["Excel", "QuickBooks", "Financial reporting"],
    },
    {
        "mark": "ME",
        "org": "Medusa Events",
        "role": "Co-Founder",
        "meta": "Nightlife and themed social events &middot; Vancouver",
        "points": [
            "Co-founded the company with three equal partners and run it alongside my studies.",
            "Write marketing copy and design promotional graphics in <strong>Canva</strong> and <strong>Figma</strong>.",
            "Use generative AI tools like <strong>Higgsfield</strong> and <strong>Gemini</strong> for event marketing.",
            "Handle vendor negotiations, venue logistics and the revenue distribution framework between partners.",
        ],
        "tools": ["Canva", "Figma", "Higgsfield", "Gemini", "Asana", "Excel"],
        "case": "./medusa-events.html",
    },
]

EDUCATION = [
    {
        "mark": "SFU",
        "org": "Simon Fraser University",
        "role": "Bachelor of Business Administration",
        "meta": "Fourth year &middot; Burnaby, BC",
        "points": [
            "Concentrations in <strong>Management Information Systems</strong> and <strong>Accounting</strong>, with a minor in <strong>Computer Science</strong>.",
        ],
    },
    {
        "mark": "FIC",
        "org": "Fraser International College",
        "role": "Pathway to Simon Fraser University",
        "points": [
            "Mentored first-year international students as they settled into university life.",
        ],
    },
]

CATEGORIES = [
    ("hackathons", "Hackathons"),
    ("work", "Work"),
    ("course", "Course projects"),
]

PROJECTS = [
    {
        "category": "hackathons",
        "featured": True,
        "eyebrow": "Hackathon &middot; StormHacks 2026",
        "title": "CoreShare: GPU sharing marketplace",
        "team": True,
        "desc": "Our team built a marketplace that rents idle GPUs to people who need compute, with owners paid in SOL per minute of measured usage. My part: full-stack work on the web and desktop apps, plus the Solana wallet sign-in and Devnet payouts.",
        "tools": ["Next.js", "Electron", "FastAPI", "Python", "Docker", "Solana"],
        "case": "./stormhacks-gpu.html",
    },
    {
        "category": "work",
        "featured": True,
        "eyebrow": "Work &middot; Jetlink Solutions",
        "title": "ProxySmart dashboard",
        "desc": "A custom dashboard that tracks JetLink Canada&rsquo;s proxy servers, devices and ports, refreshing every 15 minutes. It helped management cut system costs by 25%.",
        "tools": ["Dashboard design", "Data analysis"],
        "case": "./jetlink.html",
        "image": PROXYSMART_IMG,
    },
    {
        "category": "hackathons",
        "featured": True,
        "eyebrow": "Hackathon &middot; Beedie Business Analytics",
        "title": "Business analytics hackathon",
        "team": True,
        "desc": "Our team cleaned dense datasets and presented our data models in Tableau.",
        "tools": ["Tableau", "Data cleaning", "Data modelling"],
        "link": TABLEAU_BEEDIE,
    },
    {
        "category": "course",
        "eyebrow": "Business case &middot; Course project",
        "title": "Aegis Atmosphere market expansion",
        "desc": "A research report and presentation on expanding hospital-grade air purification into Iran and Vietnam. I structured the presentation with the PACADI case framework.",
        "tools": ["Market research", "PACADI", "PowerPoint"],
    },
    {
        "category": "course",
        "eyebrow": "Database design &middot; Course project",
        "title": "TEMU database model",
        "desc": "A relational database model of an e-commerce marketplace. I wrote the SQL queries with help from GitHub Copilot.",
        "tools": ["SQL", "Database design", "GitHub Copilot"],
    },
]

SKILLS = [
    ("Languages and frameworks", ["Python", "C", "Go", "Rust", "Next.js", "SQL"]),
    ("Data and BI", ["PostgreSQL", "MySQL", "Power BI", "Tableau", "Excel"]),
    ("Cloud and workflow", ["Microsoft Azure", "GitHub", "Linear", "Jira", "Asana"]),
    ("AI", ["Prompt engineering", "Anthropic AI coursework", "Gemini", "GitHub Copilot"]),
    ("Design", ["Figma", "Canva"]),
    ("Accounting", ["QuickBooks", "Financial ledgers", "PCI DSS"]),
]

INTERESTS = [
    (
        "On two wheels and four",
        "I ride a red 2024 Honda CBR500 and drive a 2009 BMW 7 Series. I do my own maintenance and performance tuning, and I research protective gear and engine hardware upgrades.",
    ),
    (
        "Games and mods",
        "I organize casual Dota 2 tournaments for friends in Vancouver and tinker with Minecraft modding in NeoForge.",
    ),
    (
        "In the kitchen",
        "I cook at home: Eggs Benedict, traditional Russian solyanka and Ragu alla Bolognese. I brew masala chai and mix a decent Aperol Spritz.",
    ),
    (
        "Houseplants",
        "I grow houseplants at home, including a Foxtail Fern.",
    ),
]


def project_card(p):
    # The whole card is one link: to its case study, else to its external page, else no link.
    if p.get("case"):
        tag, attrs = "a", f' href="{p["case"]}"'
    elif p.get("link"):
        tag, attrs = "a", f' href="{p["link"]}" target="_blank" rel="noopener noreferrer"'
    else:
        tag, attrs = "article", ""
    media = (
        f"""
              <div class="project-card__media">
                <img src="{p["image"]}" srcset="{srcset(p["image"])}" sizes="(min-width: 768px) 720px, 92vw" alt="" width="2505" height="1282" loading="lazy" decoding="async" />
              </div>"""
        if p.get("image")
        else ""
    )
    return f"""            <{tag} class="project-card"{attrs}>{media}
              <div class="project-card__top">
                <span class="label">{p["eyebrow"]}</span>{TEAM_BADGE if p.get("team") else ""}
              </div>
              <h3 class="project-card__title">{p["title"]}</h3>
              <p class="project-card__desc">{p["desc"]}</p>
{tags(p["tools"], "              ")}
            </{tag}>"""


def entry(r):
    points = "".join(f"\n              <li>{p}</li>" for p in r["points"])
    meta = f'\n                <p class="entry__meta">{r["meta"]}</p>' if r.get("meta") else ""
    skills = (
        f'\n            <p class="entry__skills">{" &middot; ".join(r["tools"])}</p>' if r.get("tools") else ""
    )
    links = ""
    if r.get("case"):
        links += f'\n              <a href="{r["case"]}" class="text-link">Read the case study &rarr;</a>'
    links += ext_links(r.get("links", []), "              ")
    links_block = f'\n            <div class="entry__links">{links}\n            </div>' if links else ""
    return f"""          <article class="entry">
            <div class="entry__head">
              <span class="entry__logo" aria-hidden="true">{r["mark"]}</span>
              <div>
                <h3 class="entry__role">{r["role"]}</h3>
                <p class="entry__org">{r["org"]}</p>{meta}
              </div>
            </div>
            <ul class="entry__points">{points}
            </ul>{skills}{links_block}
          </article>"""


# ---------------------------------------------------------------- index

resume_pill = (
    f'\n            <a href="./{RESUME}" class="pill">{RESUME_ICON}Résumé (PDF)</a>' if HAS_RESUME else ""
)

hero = """    <section class="hero" id="hero">
      <div class="hero__content">
        <h1 class="hero__name">Konstantin Tovshtein</h1>
        <p class="hero__sub">BBA Student at SFU &middot; MIS, Accounting, Computer Science</p>
      </div>
      <a href="#intro" class="hero__arrow" aria-label="Scroll to introduction"><span class="hero__arrow-icon"></span></a>
    </section>
"""

intro = f"""    <section class="section reveal" id="intro" aria-label="Introduction">
      <div class="container">
        <div class="panel intro">
          <div class="intro__text">
            <p class="intro__lead">A fourth-year BBA student at Simon Fraser University. I work where finance meets information systems: dashboards, databases, compliance and the code that ties them together. Next stop, a career in fintech.</p>
            <div class="pills">{resume_pill}
              <a href="{GITHUB}" class="pill" target="_blank" rel="noopener noreferrer">{social_icon("github", "pill__icon", 18)}GitHub</a>
              <a href="{LINKEDIN}" class="pill" target="_blank" rel="noopener noreferrer">{social_icon("linkedin", "pill__icon", 18)}LinkedIn</a>
            </div>
          </div>
          <img class="intro__photo" src="./assets/png/konstantin-tovshtein.webp" width="320" height="320" alt="Konstantin Tovshtein" />
        </div>
      </div>
    </section>
"""

featured = section(
    "featured",
    "Featured Projects",
    f"""        <div class="project-list">
{chr(10).join(project_card(p) for p in PROJECTS if p.get("featured"))}
        </div>""",
    '\n        <p class="see-all"><a href="./projects.html" class="text-link">See all projects &rarr;</a></p>',
)

experience = section(
    "experience",
    "Experience",
    f"""        <div class="entries">
{chr(10).join(entry(r) for r in ROLES)}
        </div>""",
)

education = section(
    "education",
    "Education",
    f"""        <div class="entries">
{chr(10).join(entry(r) for r in EDUCATION)}
        </div>""",
)

skill_groups = "\n".join(
    f"""          <div class="skill-group">
            <h3 class="skill-group__title">{title}</h3>
{tags(items, "            ")}
          </div>"""
    for title, items in SKILLS
)
skills = section(
    "skills",
    "Skills",
    f"""        <div class="skill-groups">
{skill_groups}
        </div>
        <p class="note">
          <strong>Currently learning:</strong> agentic harnesses, the tooling that lets AI models plan and act across multi-step tasks. I also understand core data structures and have written custom sorting implementations in C.
        </p>""",
)

interest_cards = "\n".join(
    f"""          <article class="mini">
            <h3 class="mini__title">{t}</h3>
            <p class="mini__desc">{d}</p>
          </article>"""
    for t, d in INTERESTS
)
beyond = section(
    "beyond",
    "Beyond work",
    f"""        <div class="mini-grid">
{interest_cards}
        </div>""",
)

contact = f"""    <section class="section reveal" id="contact" aria-labelledby="contact-title">
      <div class="container">
        <div class="contact__head">
          <h2 class="section-title" id="contact-title" data-type>Contact</h2>
          <div class="pills">
            <a href="{LINKEDIN}" class="pill pill--icon" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn profile">{social_icon("linkedin", "pill__icon", 18)}</a>
            <a href="{GITHUB}" class="pill pill--icon" target="_blank" rel="noopener noreferrer" aria-label="GitHub repositories">{social_icon("github", "pill__icon", 18)}</a>
          </div>
        </div>
        <p class="contact__intro">Open to roles, contracts, or conversations about interesting work.</p>
        <form
          action="https://formspree.io/f/{FORMSPREE_ID}"
          method="POST"
          class="contact__form"
          data-contact-form
        >
          <div class="field">
            <label class="field__label" for="name">Name</label>
            <input required type="text" autocomplete="name" class="field__input" name="name" id="name" />
          </div>
          <div class="field">
            <label class="field__label" for="email">Email</label>
            <input required type="email" autocomplete="email" class="field__input" name="email" id="email" />
          </div>
          <div class="field">
            <label class="field__label" for="message">Message</label>
            <textarea data-lenis-prevent required rows="6" class="field__input" name="message" id="message"></textarea>
          </div>
          <input type="text" name="_gotcha" class="contact__honeypot" tabindex="-1" autocomplete="off" aria-hidden="true" />
          <div class="contact__actions">
            <button type="submit" class="btn">Send</button>
            <p class="contact__status" role="status" data-contact-status></p>
          </div>
        </form>
        <p class="contact__alt">
          Prefer LinkedIn?
          <a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">Message me there</a>.
        </p>
      </div>
    </section>
"""

page(
    "index.html",
    "Konstantin Tovshtein",
    "Portfolio of Konstantin Tovshtein, a BBA student at Simon Fraser University in Management Information Systems and Accounting, aiming for fintech and information systems.",
    "home",
    "page-home",
    hero + intro + featured + experience + education + skills + beyond + contact,
)

# ---------------------------------------------------------------- projects

chips = "\n".join(
    f'            <li><a href="#{key}" class="pill">{label}</a></li>' for key, label in CATEGORIES
)
categories = "\n".join(
    f"""    <section class="category reveal" id="{key}" aria-labelledby="{key}-title">
      <div class="container container--wide">
        <h2 class="category__title" id="{key}-title">{label}</h2>
        <div class="project-grid">
{chr(10).join(project_card(p) for p in PROJECTS if p["category"] == key)}
        </div>
      </div>
    </section>"""
    for key, label in CATEGORIES
)
proj_body = f"""    <section class="page-head">
      <div class="container container--wide">
        <h1 class="page-title" data-scramble>Projects</h1>
        <div class="panel projects-intro">
          <p class="projects-intro__text">Hackathons, work and course projects, from a GPU sharing app to market expansion research.</p>
          <ul class="pills">
{chips}
          </ul>
        </div>
      </div>
    </section>
{categories}
"""
page(
    "projects.html",
    "Projects | Konstantin Tovshtein",
    "Projects by Konstantin Tovshtein, including a GPU sharing platform built at StormHacks 2026 and the Beedie Business Analytics Hackathon.",
    "projects",
    "page-projects",
    proj_body,
)

# ---------------------------------------------------------------- case studies

TO_PROJECTS = ("./projects.html", "Back to Projects")
TO_EXPERIENCE = ("./index.html#experience", "Back to Experience")


def case_study(name, title, sub, sections, tools, back, desc, image=None, links=(), team=False):
    secs = "\n".join(
        f"""          <section class="case__section">
            <h2>{h}</h2>
{chr(10).join(f'            <p>{p}</p>' for p in paras)}
          </section>"""
        for h, paras in sections
    )
    back_href, back_label = back
    if image:
        src, alt, caption = image
        showcase = f"""          <figure class="case__figure">
            <img src="{src}" srcset="{srcset(src)}" sizes="(min-width: 768px) 656px, 88vw" alt="{alt}" width="2505" height="1282" decoding="async" />
            <figcaption>{caption}</figcaption>
          </figure>"""
    else:
        showcase = "          <!-- TODO: add a real screenshot or photo here (case__figure) -->"
    meta = ""
    if links or team:
        meta = f"""
          <div class="case__meta">
            <div class="case__links">{ext_links(links, "              ")}
            </div>{TEAM_BADGE if team else ""}
          </div>"""
    body = f"""    <div class="case-page">
      <div class="container">
        <article class="case">
          <p class="case__back"><a href="{back_href}">&larr; {back_label}</a></p>
          <h1 class="case__title">{title}</h1>
          <p class="case__desc">{sub}</p>{meta}
{showcase}
{secs}
          <section class="case__section">
            <h2>Tools used</h2>
{tags(tools, "            ")}
          </section>
        </article>
      </div>
    </div>
"""
    active = "projects" if back == TO_PROJECTS else None
    page(name, f"{title.replace(' &mdash; ', ' | ')} | Konstantin Tovshtein", desc, active, "page-case", body)


case_study(
    "medusa-events.html",
    "Co-Founder &mdash; Medusa Events",
    "Nightlife and themed social events in Vancouver, run by four equal partners with no external funding.",
    [
        (
            "Overview",
            [
                "Medusa Events is a Vancouver company that organizes nightlife and themed social events. I co-founded it with three other partners. We set it up as an equal shareholding arrangement from the start, so every operational and financial decision needs clear processes and agreement across all four of us. There is no single person in charge, so the systems we put in place have to hold things together without constant oversight.",
                "My work covers vendor negotiations, venue logistics and the revenue distribution framework that decides how earnings are split across equal partnership stakes. I also led the effort to source event materials from local small businesses instead of large suppliers, which lowered costs and cut post-event waste.",
            ],
        ),
        (
            "Marketing",
            [
                "I write the marketing copy and design the promotional graphics for our events in Canva and Figma. For campaigns I use generative AI tools like Higgsfield and Gemini to produce event visuals and promotional content.",
                "Running a company this way taught me more about operational structure, teamwork and financial transparency than most coursework does.",
            ],
        ),
    ],
    ["Canva", "Figma", "Higgsfield", "Gemini", "Asana", "Excel", "QuickBooks"],
    TO_EXPERIENCE,
    "How Konstantin Tovshtein co-founded and runs Medusa Events, a nightlife and themed events company in Vancouver.",
)

case_study(
    "stormhacks-gpu.html",
    "CoreShare &mdash; StormHacks 2026",
    "A team hackathon project: a marketplace that rents idle GPUs to people who need compute, with owners paid in SOL per minute of measured usage.",
    [
        (
            "Overview",
            [
                "CoreShare lets GPU owners share spare capacity and earn SOL for every minute their hardware is actually used. Renters submit batch jobs without needing a cloud account or a credit card. It is a team project: we built it from scratch together at StormHacks 2026. It runs on the Solana Devnet, so no real funds are involved.",
            ],
        ),
        (
            "How it works",
            [
                "A renter submits a batch job, which is split into chunks. Idle providers claim chunks in parallel, so more machines mean faster completion. Each chunk runs in a locked-down Docker container with no network access, a read-only filesystem, and VRAM and compute caps enforced through NVIDIA MPS.",
                "The worker streams GPU utilization from nvidia-smi into a TimescaleDB table, which rolls usage up per minute for dashboards and payouts. Settlement then sends SOL to each provider in batches, designed to be idempotent and crash-safe so a retry never pays anyone twice.",
                "The product has four parts. A Next.js web app handles renting, wallet login, live jobs and earnings. An Electron desktop app gives providers a GPU share slider and bundles the Python worker. A FastAPI backend runs auth, device pairing, the job queue and metering. The Solana layer handles Devnet escrow and per-minute settlement.",
            ],
        ),
        (
            "My role on the team",
            [
                "The system above is the whole team's work. My share was full-stack development across the web app and the desktop app. I implemented Solana wallet authentication, so users sign in with their wallet instead of a password, and the payouts to providers on Devnet.",
            ],
        ),
    ],
    ["Next.js", "Tailwind", "Electron", "FastAPI", "Python", "PostgreSQL", "TimescaleDB", "Docker", "NVIDIA MPS", "Solana"],
    TO_PROJECTS,
    "Case study: CoreShare, a GPU sharing marketplace with Solana wallet sign-in and Devnet payouts, built at StormHacks 2026.",
    links=[("Team repo on GitHub", CORESHARE_TEAM_REPO), ("My fork", CORESHARE_REPO)],
    team=True,
)

case_study(
    "one-pay.html",
    "Compliance &mdash; One Pay Ltd",
    "Helping a payment processing company prepare for PCI DSS and Visa certification.",
    [
        (
            "Overview",
            [
                "One Pay Ltd is a payment processing company. Before a processor can handle card payments, it has to meet the Payment Card Industry Data Security Standard (PCI DSS) and pass card network certification such as Visa's.",
            ],
        ),
        (
            "What I did",
            [
                "I gathered and organized the legal documentation the company needed to pass PCI DSS and Visa certification.",
                "I also helped optimize the company's payment software, built in Rust, so that it adhered to PCI DSS requirements. The role put me right where finance, regulation and engineering meet, which is the space I want to work in.",
            ],
        ),
    ],
    ["Rust", "PCI DSS", "Visa certification", "GitHub"],
    TO_EXPERIENCE,
    "Case study: Konstantin Tovshtein's compliance work at One Pay Ltd for PCI DSS and Visa certification.",
    links=[("One Pay website", ONE_PAY_SITE)],
)

case_study(
    "jetlink.html",
    "Data Analyst &mdash; Jetlink Solutions",
    "Fixing problems day to day, then building ProxySmart, the monitoring dashboard that helped cut system costs by 25%.",
    [
        (
            "Overview",
            [
                "At Jetlink Solutions I worked as a technical support specialist and data analyst. Day to day I handled hardware and software issues and resolved them promptly so the team could keep working.",
            ],
        ),
        (
            "The dashboard",
            [
                "I built ProxySmart, a custom dashboard for tracking the performance of JetLink Canada's proxy infrastructure. It shows how many servers are online, how many devices are working, idle or in an error state, and how many ports are in use.",
                "Data refreshes automatically every 15 minutes, with options to refresh on demand and clear expired port entries.",
                "Using the dashboard, management cut system costs by 25%.",
            ],
        ),
    ],
    ["ProxySmart", "Dashboard design", "Data analysis", "Technical support"],
    TO_EXPERIENCE,
    "Case study: ProxySmart, a proxy infrastructure dashboard by Konstantin Tovshtein that helped Jetlink Solutions cut system costs by 25%.",
    image=(
        PROXYSMART_IMG,
        "ProxySmart dashboard for JetLink Canada showing 1 of 1 servers online, 39 devices, 24 working, 15 idle, 0 errors and 24 ports",
        "ProxySmart, the dashboard I built for JetLink Canada: servers, devices and their working, idle and error status at a glance.",
    ),
)
