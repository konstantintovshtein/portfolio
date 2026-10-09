"""Generate the eight portfolio HTML pages from one shared head, header and footer.

Usage (from the repo root): npm run build:html
                        or: python tools/build_pages.py

Edit page content in this file, never in the generated .html files: the next build overwrites them.
"""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent

# Formspree form ID (the part after /f/ in your Formspree endpoint).
# Until it is set, the form shows a "not connected yet" message instead of sending.
FORMSPREE_ID = "YOUR_FORM_ID"

# Drop your résumé at this path and rebuild: "Download résumé" buttons appear automatically.
RESUME = "assets/Konstantin-Tovshtein-Resume.pdf"
HAS_RESUME = (ROOT / RESUME).exists()

NAV = [
    ("home", "./index.html", "Home"),
    ("about", "./about.html", "About"),
    ("experience", "./experience.html", "Experience"),
    ("projects", "./projects.html", "Projects"),
    ("contact", "./index.html#contact", "Contact"),
]

LINKEDIN = "https://www.linkedin.com/in/konstantin-tovshtein-0b1a21221/"
GITHUB = "https://github.com/konstantintovshtein?tab=repositories"
CORESHARE_REPO = "https://github.com/konstantintovshtein/coreshare"
CORESHARE_TEAM_REPO = "https://github.com/borodooovitsyn/coreshare"
TEAM_BADGE = '<span class="badge"><svg aria-hidden="true" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>Team project</span>'
TABLEAU_BEEDIE = "https://public.tableau.com/app/profile/konstantin.tovshtein/viz/BusinessAnalyticsHackathon/Dashboard"
ONE_PAY_SITE = "https://onepayltd.kz/ru"


def ext_links(links, indent, cls="btn btn--med btn--theme-inv"):
    return "".join(
        f'\n{indent}<a href="{url}" class="{cls}" target="_blank" rel="noopener noreferrer">{label}</a>'
        for label, url in links
    )


def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <meta name="theme-color" content="#09090b" />
    <meta name="color-scheme" content="dark" />
    <title>{title}</title>
    <meta name="description" content="{desc}" />

    <link
      rel="preload"
      href="./assets/fonts/kt-sans-latin-var.woff2"
      as="font"
      type="font/woff2"
      crossorigin
    />
    <link rel="stylesheet" href="css/style.css" />
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>
"""


def header(active):
    def cur(key):
        return ' aria-current="page"' if key == active else ""

    desktop = "\n".join(
        f'            <li class="header__link-wrapper">\n'
        f'              <a href="{href}" class="header__link"{cur(key)}>{label}</a>\n'
        f"            </li>"
        for key, href, label in NAV
    )
    mobile = "\n".join(
        f'            <li class="header__sm-menu-link">\n'
        f'              <a href="{href}"{cur(key)}>{label}</a>\n'
        f"            </li>"
        for key, href, label in NAV
    )
    return f"""    <header class="header">
      <div class="header__content">
        <a href="./index.html" class="header__logo-container">
          <div class="header__logo-img-cont">
            <img
              src="./assets/png/konstantin-tovshtein.webp"
              width="320"
              height="320"
              alt=""
              class="header__logo-img"
            />
          </div>
          <span class="header__logo-sub">Konstantin Tovshtein</span>
        </a>
        <div class="header__main">
          <nav class="header__nav" aria-label="Main">
            <ul class="header__links">
{desktop}
            </ul>
          </nav>
          <button
            type="button"
            class="header__main-ham-menu-cont"
            aria-label="Open menu"
            aria-expanded="false"
            aria-controls="mobile-menu"
          >
            <img
              src="./assets/svg/ham-menu.svg"
              alt=""
              class="header__main-ham-menu"
            />
            <img
              src="./assets/svg/ham-menu-close.svg"
              alt=""
              class="header__main-ham-menu-close d-none"
            />
          </button>
        </div>
      </div>
      <div class="header__sm-menu" id="mobile-menu">
        <nav class="header__sm-menu-content" aria-label="Main">
          <ul class="header__sm-menu-links">
{mobile}
          </ul>
        </nav>
      </div>
    </header>
"""


FOOTER = f"""    <footer class="main-footer">
      <div class="main-container">
        <div class="main-footer__upper">
          <div class="main-footer__row main-footer__row-1">
            <h2 class="heading heading-sm main-footer__heading-sm">Social</h2>
            <div class="main-footer__social-cont">
              <a class="main-footer__social" href="{LINKEDIN}" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn profile">
                <img class="main-footer__icon" src="./assets/png/linkedin-ico.png" alt="" width="24" height="24" />
              </a>
              <a class="main-footer__social" href="{GITHUB}" target="_blank" rel="noopener noreferrer" aria-label="GitHub repositories">
                <img class="main-footer__icon" src="./assets/png/github-ico.png" alt="" width="24" height="24" />
              </a>
            </div>
          </div>
          <div class="main-footer__row main-footer__row-2">
            <h2 class="heading heading-sm">Konstantin Tovshtein</h2>
            <p class="main-footer__short-desc">
              BBA student at Simon Fraser University studying Management Information Systems and Accounting, with a minor in Computer Science. Based in Vancouver, BC.
            </p>
          </div>
        </div>
      </div>
    </footer>

    <script src="./assets/vendor/lenis/lenis.min.js"></script>
    <script src="./index.js"></script>
  </body>
</html>
"""


def chips(items, indent="              "):
    inner = "\n".join(f'{indent}  <div class="skills__skill">{i}</div>' for i in items)
    return f'{indent}<div class="skills">\n{inner}\n{indent}</div>'


def page(name, title, desc, active, body):
    main = f'    <main id="main" tabindex="-1">\n{body}    </main>\n'
    html = head(title, desc) + header(active) + main + FOOTER
    (ROOT / name).write_text(html, encoding="utf-8", newline="\n")
    print("wrote", name)


def page_hero(title, sub):
    return f"""    <section class="page-hero">
      <div class="main-container">
        <h1 class="heading-primary">{title}</h1>
        <p class="page-hero__sub">{sub}</p>
      </div>
    </section>
"""


# ---------------------------------------------------------------- content

ROLES = [
    {
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
        "org": "Repatt AI",
        "role": "Database Automation and Sales Outreach",
        "meta": "AI startup &middot; Lead generation",
        "points": [
            "Wrote <strong>Python</strong> scripts that extracted business data from Google Maps into Excel spreadsheets.",
            "Turned that data into customer leads and ran business sales outreach.",
        ],
        "tools": ["Python", "Excel", "Automation"],
        "case": None,
    },
    {
        "org": "Crowe MacKay",
        "role": "Accounting Assistant",
        "meta": "Public accounting",
        "points": [
            "Reviewed corporate financial ledgers.",
            "Compiled financial information for management using the firm&rsquo;s accounting tools.",
            "Completed <strong>10% more</strong> work than my assigned target.",
        ],
        "tools": ["Excel", "QuickBooks", "Financial reporting"],
        "case": None,
    },
    {
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

PROJECTS = [
    {
        "eyebrow": "Hackathon &middot; StormHacks 2026",
        "title": "CoreShare: GPU sharing marketplace",
        "team": True,
        "desc": "Our team built a marketplace that rents idle GPUs to people who need compute, with owners paid in SOL per minute of measured usage. My part: full-stack work on the web and desktop apps, plus the Solana wallet sign-in and Devnet payouts.",
        "tools": ["Next.js", "Electron", "FastAPI", "Python", "Docker", "Solana"],
        "case": "./stormhacks-gpu.html",
        "links": [("Team repo on GitHub", CORESHARE_TEAM_REPO)],
        "featured": True,
    },
    {
        "eyebrow": "Hackathon &middot; Beedie Business Analytics",
        "team": True,
        "links": [("View Tableau dashboard", TABLEAU_BEEDIE)],
        "title": "Business analytics hackathon",
        "desc": "Our team cleaned dense datasets and presented our data models in Tableau.",
        "tools": ["Tableau", "Data cleaning", "Data modelling"],
        "case": None,
    },
    {
        "eyebrow": "Business case &middot; Course project",
        "title": "Aegis Atmosphere market expansion",
        "desc": "A research report and presentation on expanding hospital-grade air purification into Iran and Vietnam. I structured the presentation with the PACADI case framework.",
        "tools": ["Market research", "PACADI", "PowerPoint"],
        "case": None,
    },
    {
        "eyebrow": "Database design &middot; Course project",
        "title": "TEMU database model",
        "desc": "A relational database model of an e-commerce marketplace. I wrote the SQL queries with help from GitHub Copilot.",
        "tools": ["SQL", "Database design", "GitHub Copilot"],
        "case": None,
    },
]


def project_card(p, heading="h3"):
    cls = "card card--featured" if p.get("featured") else "card"
    btns = ""
    if p["case"]:
        btns += f'\n                <a href="{p["case"]}" class="btn btn--med btn--theme">Case Study</a>'
    btns += ext_links(p.get("links", []), "                ")
    action = (
        f'\n              <div class="card__actions">{btns}\n              </div>'
        if btns
        else "\n              <!-- TODO: add a GitHub / Devpost / demo link here when available -->"
    )
    return f"""            <article class="{cls}">
              <div class="card__top">
                <p class="card__eyebrow">{p["eyebrow"]}</p>{TEAM_BADGE if p.get("team") else ""}
              </div>
              <{heading} class="card__title">{p["title"]}</{heading}>
              <p class="card__desc">{p["desc"]}</p>
{chips(p["tools"])}{action}
            </article>"""


# ---------------------------------------------------------------- index

RESUME_BUTTON = (
    f'\n          <a href="./{RESUME}" class="btn btn--theme-inv" download>Download Résumé</a>'
    if HAS_RESUME
    else ""
)

hero_socials = f"""      <div class="home-hero__socials">
        <div class="home-hero__social">
          <a href="{LINKEDIN}" class="home-hero__social-icon-link" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn profile">
            <img src="./assets/png/linkedin-ico.png" alt="" width="26" height="26" class="home-hero__social-icon" />
          </a>
        </div>
        <div class="home-hero__social">
          <a href="{GITHUB}" class="home-hero__social-icon-link home-hero__social-icon-link--bd-none" target="_blank" rel="noopener noreferrer" aria-label="GitHub repositories">
            <img src="./assets/png/github-ico.png" alt="" width="26" height="26" class="home-hero__social-icon" />
          </a>
        </div>
      </div>
"""

contact = f"""    <section id="contact" class="contact sec-pad" aria-labelledby="contact-title">
      <div class="main-container">
        <h2 class="heading heading-sec heading-sec__mb-med" id="contact-title">
          <span class="heading-sec__main heading-sec__main--lt">Contact</span>
          <span class="heading-sec__sub heading-sec__sub--lt">
            Open to roles, contracts, or conversations about interesting work.
          </span>
        </h2>
        <div class="contact__form-container">
          <form
            action="https://formspree.io/f/{FORMSPREE_ID}"
            method="POST"
            class="contact__form"
            data-contact-form
          >
            <div class="contact__form-field">
              <label class="contact__form-label" for="name">Name</label>
              <input
                required
                placeholder="Enter Your Name"
                type="text"
                autocomplete="name"
                class="contact__form-input"
                name="name"
                id="name"
              />
            </div>
            <div class="contact__form-field">
              <label class="contact__form-label" for="email">Email</label>
              <input
                required
                placeholder="Enter Your Email"
                type="email"
                autocomplete="email"
                class="contact__form-input"
                name="email"
                id="email"
              />
            </div>
            <div class="contact__form-field">
              <label class="contact__form-label" for="message">Message</label>
              <textarea
                data-lenis-prevent
                required
                cols="30"
                rows="10"
                class="contact__form-input"
                placeholder="Enter Your Message"
                name="message"
                id="message"
              ></textarea>
            </div>
            <input type="text" name="_gotcha" class="contact__honeypot" tabindex="-1" autocomplete="off" aria-hidden="true" />
            <div class="contact__actions">
              <p class="contact__status" role="status" data-contact-status></p>
              <button type="submit" class="btn btn--theme contact__btn">Send Message</button>
            </div>
          </form>
          <p class="contact__alt">
            Prefer LinkedIn?
            <a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">Message me there</a>.
          </p>
        </div>
      </div>
    </section>
"""

featured_roles = [ROLES[0], ROLES[1], ROLES[4]]
role_cards = "\n".join(
    f"""            <article class="card">
              <p class="card__eyebrow">{r["org"]}</p>
              <h3 class="card__title">{r["role"]}</h3>
              <p class="card__desc">{r["points"][-1] if r["org"] == "Jetlink Solutions" else r["points"][0]}</p>
              <div class="card__actions">
                <a href="{r["case"]}" class="text-link">Read the case study &rarr;</a>
              </div>
            </article>"""
    for r in featured_roles
)

index_body = f"""    <section class="home-hero">
      <div class="home-hero__content">
        <span class="home-hero__eyebrow">MIS &middot; Accounting &middot; Computer Science</span>
        <h1 class="heading-primary">Hey, I'm <span class="heading-primary__name">Konstantin Tovshtein</span></h1>
        <div class="home-hero__info">
          <p class="text-primary">
            A fourth-year BBA student at Simon Fraser University. I work where finance meets information systems: dashboards, databases, compliance and the code that ties them together. Next stop, a career in fintech.
          </p>
        </div>
        <div class="home-hero__cta">
          <a href="./experience.html" class="btn btn--theme">View Experience</a>
          <a href="./projects.html" class="btn btn--theme-inv">See Projects</a>{RESUME_BUTTON}
        </div>
      </div>
{hero_socials}      <div class="home-hero__mouse-scroll-cont">
        <div class="mouse"></div>
      </div>
    </section>
    <section class="sec-pad" aria-labelledby="glance-title">
      <div class="main-container">
        <div class="section-head">
          <div>
            <h2 class="section-head__title" id="glance-title">At a glance</h2>
            <p class="section-head__sub">A few numbers from the work so far.</p>
          </div>
          <a href="./about.html" class="text-link">More about me &rarr;</a>
        </div>
        <div class="stats">
          <div class="stats__item">
            <span class="stats__value">25<span>%</span></span>
            <span class="stats__label">Lower system costs after my ProxySmart dashboard at Jetlink Solutions</span>
          </div>
          <div class="stats__item">
            <span class="stats__value">10<span>%</span></span>
            <span class="stats__label">Above my assigned workload at Crowe MacKay</span>
          </div>
          <div class="stats__item">
            <span class="stats__value">5</span>
            <span class="stats__label">Roles across fintech, accounting, AI and events</span>
          </div>
          <div class="stats__item">
            <span class="stats__value">2</span>
            <span class="stats__label">Hackathons, including a full-stack build at Stormhacks 2026</span>
          </div>
        </div>
      </div>
    </section>
    <section class="sec-pad sec-alt" aria-labelledby="featured-title">
      <div class="main-container">
        <div class="section-head">
          <div>
            <h2 class="section-head__title" id="featured-title">Featured project</h2>
            <p class="section-head__sub">The most recent thing I built.</p>
          </div>
          <a href="./projects.html" class="text-link">All projects &rarr;</a>
        </div>
{project_card(PROJECTS[0])}
      </div>
    </section>
    <section class="sec-pad" aria-labelledby="roles-title">
      <div class="main-container">
        <div class="section-head">
          <div>
            <h2 class="section-head__title" id="roles-title">Selected experience</h2>
            <p class="section-head__sub">Payments compliance, data and a company I co-founded.</p>
          </div>
          <a href="./experience.html" class="text-link">Full experience &rarr;</a>
        </div>
        <div class="card-grid card-grid--3">
{role_cards}
        </div>
      </div>
    </section>
{contact}"""

page(
    "index.html",
    "Konstantin Tovshtein",
    "Portfolio of Konstantin Tovshtein, a BBA student at Simon Fraser University in Management Information Systems and Accounting, aiming for fintech and information systems.",
    "home",
    index_body,
)

# ---------------------------------------------------------------- experience


def timeline_item(r):
    points = "\n".join(f"              <li>{p}</li>" for p in r["points"])
    btns = ""
    if r["case"]:
        btns += f'\n              <a href="{r["case"]}" class="btn btn--med btn--theme-inv">Case Study</a>'
    btns += ext_links(r.get("links", []), "              ")
    action = f'\n            <div class="timeline__actions">{btns}\n            </div>' if btns else ""
    return f"""          <article class="timeline__item">
            <!-- TODO: add dates for this role -->
            <p class="timeline__org">{r["org"]}</p>
            <h2 class="timeline__role">{r["role"]}</h2>
            <p class="timeline__meta">{r["meta"]}</p>
            <ul class="timeline__points">
{points}
            </ul>
{chips(r["tools"], "            ")}{action}
          </article>"""


exp_body = (
    page_hero(
        "Experience",
        "Payments compliance, data analysis, accounting and a company I co-founded.",
    )
    + f"""    <section class="sec-pad">
      <div class="main-container">
        <div class="timeline">
{chr(10).join(timeline_item(r) for r in ROLES)}
        </div>
      </div>
    </section>
"""
)
page(
    "experience.html",
    "Experience | Konstantin Tovshtein",
    "Work experience of Konstantin Tovshtein: One Pay Ltd, Jetlink Solutions, Repatt AI, Crowe MacKay and Medusa Events.",
    "experience",
    exp_body,
)

# ---------------------------------------------------------------- projects

proj_body = (
    page_hero(
        "Projects",
        "Hackathons and course projects, from a GPU sharing app to market expansion research.",
    )
    + f"""    <section class="sec-pad">
      <div class="main-container">
        <div class="card-grid">
{chr(10).join(project_card(p, "h2") for p in PROJECTS)}
        </div>
      </div>
    </section>
"""
)
page(
    "projects.html",
    "Projects | Konstantin Tovshtein",
    "Projects by Konstantin Tovshtein, including a GPU sharing platform built at Stormhacks 2026 and the Beedie Business Analytics Hackathon.",
    "projects",
    proj_body,
)

# ---------------------------------------------------------------- about

SKILLS = [
    ("Languages and frameworks", ["Python", "C", "Go", "Rust", "Next.js", "SQL"]),
    ("Data and BI", ["PostgreSQL", "MySQL", "Power BI", "Tableau", "Excel"]),
    ("Cloud and workflow", ["Microsoft Azure", "GitHub", "Linear", "Jira", "Asana"]),
    ("AI", ["Prompt engineering", "Anthropic AI coursework", "Gemini", "GitHub Copilot"]),
    ("Design", ["Figma", "Canva"]),
    ("Accounting", ["QuickBooks", "Financial ledgers", "PCI DSS"]),
]
skill_groups = "\n".join(
    f"""          <div class="skill-group">
            <h3 class="skill-group__title">{title}</h3>
{chips(items, "            ")}
          </div>"""
    for title, items in SKILLS
)

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
interest_cards = "\n".join(
    f"""          <article class="card">
            <h3 class="card__title">{t}</h3>
            <p class="card__desc">{d}</p>
          </article>"""
    for t, d in INTERESTS
)

about_body = (
    page_hero(
        "About",
        "Business student, part-time developer, full-time tinkerer.",
    )
    + f"""    <section class="sec-pad">
      <div class="main-container about-page__grid">
        <div>
          <h2 class="section-head__title">My story</h2>
          <p class="about-page__para">
            I'm <strong>Konstantin Tovshtein</strong>, a fourth-year Business Administration student at <strong>Simon Fraser University</strong> in Burnaby. I concentrate in <strong>Management Information Systems</strong> and <strong>Accounting</strong>, with a minor in <strong>Computer Science</strong>.
          </p>
          <p class="about-page__para">
            My work sits between finance and engineering. I review ledgers, build dashboards, write SQL and Python, and I have helped get payment software ready for PCI DSS. I want to build a career in <strong>fintech and information systems</strong>, where both sides matter.
          </p>
          <p class="about-page__para">
            Most of what I know came from doing it. I co-founded an events company with three partners, built a monitoring dashboard that helped cut system costs by 25%, automated lead generation with Python, and built the Solana payments for CoreShare, a GPU sharing marketplace our team made at StormHacks 2026.
          </p>
          <div class="about-page__actions">
            <a href="./index.html#contact" class="btn btn--med btn--theme">Get in touch</a>{RESUME_BUTTON.replace('btn btn--theme-inv', 'btn btn--med btn--theme-inv')}
          </div>
        </div>
        <div>
          <h2 class="section-head__title">Education</h2>
          <div class="about-page__edu-item">
            <p class="about-page__edu-school">Simon Fraser University</p>
            <p class="about-page__edu-detail">Bachelor of Business Administration, fourth year. Concentrations in Management Information Systems and Accounting. Minor in Computer Science.</p>
          </div>
          <div class="about-page__edu-item">
            <p class="about-page__edu-school">Fraser International College</p>
            <p class="about-page__edu-detail">Pathway to SFU. Mentored first-year international students as they settled into university life.</p>
          </div>
        </div>
      </div>
    </section>
    <section class="sec-pad sec-alt" aria-labelledby="skills-title">
      <div class="main-container">
        <div class="section-head">
          <div>
            <h2 class="section-head__title" id="skills-title">Skills</h2>
            <p class="section-head__sub">Tools I use at work, in class and on my own projects.</p>
          </div>
        </div>
        <div class="skill-groups">
{skill_groups}
        </div>
        <p class="callout">
          <strong>Currently learning:</strong> agentic harnesses, the tooling that lets AI models plan and act across multi-step tasks. I also understand core data structures and have written custom sorting implementations in C.
        </p>
      </div>
    </section>
    <section class="sec-pad" aria-labelledby="beyond-title">
      <div class="main-container">
        <div class="section-head">
          <div>
            <h2 class="section-head__title" id="beyond-title">Beyond work</h2>
            <p class="section-head__sub">What I do when I'm not at a keyboard.</p>
          </div>
        </div>
        <div class="card-grid">
{interest_cards}
        </div>
      </div>
    </section>
"""
)
page(
    "about.html",
    "About | Konstantin Tovshtein",
    "About Konstantin Tovshtein: education at Simon Fraser University, technical skills and interests.",
    "about",
    about_body,
)

# ---------------------------------------------------------------- case studies


def case_study(name, title, sub, sections, tools, back, desc, image=None, links=(), team=False):
    secs = "\n".join(
        f"""            <div class="project-details__desc">
              <h2 class="project-details__content-title">{h}</h2>
{chr(10).join(f'              <p class="project-details__desc-para">{p}</p>' for p in paras)}
            </div>"""
        for h, paras in sections
    )
    back_href, back_label = back
    if image:
        src, alt, caption = image
        showcase = f"""          <figure class="project-details__showcase-img-cont">
            <img src="{src}" alt="{alt}" class="project-details__showcase-img" width="2505" height="1282" />
            <figcaption class="project-details__caption">{caption}</figcaption>
          </figure>"""
    else:
        showcase = "          <!-- TODO: add a real screenshot or photo here (project-details__showcase-img) -->"
    ext = ext_links(links, "              ", "btn btn--med btn--theme-inv project-details__links-btn")
    body = f"""    <section class="project-cs-hero">
      <div class="project-cs-hero__content">{('<div class="project-cs-hero__badge">' + TEAM_BADGE + '</div>') if team else ""}
        <h1 class="heading-primary">{title}</h1>
        <div class="project-cs-hero__info">
          <p class="text-primary">{sub}</p>
        </div>
      </div>
    </section>
    <section class="project-details">
      <div class="main-container">
        <div class="project-details__content">
{showcase}
          <div class="project-details__content-main">
{secs}
            <div class="project-details__tools-used">
              <h2 class="project-details__content-title">Tools Used</h2>
{chips(tools)}
            </div>
            <div class="project-details__links">
              <a href="{back_href}" class="btn btn--med btn--theme project-details__links-btn">{back_label}</a>{ext}
            </div>
          </div>
        </div>
      </div>
    </section>
"""
    page(name, f"{title.replace(' &mdash; ', ' | ')} | Konstantin Tovshtein", desc, "experience" if "experience" in back_href else "projects", body)


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
    ("./experience.html", "All Experience"),
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
    ("./projects.html", "All Projects"),
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
    ("./experience.html", "All Experience"),
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
    ("./experience.html", "All Experience"),
    "Case study: ProxySmart, a proxy infrastructure dashboard by Konstantin Tovshtein that helped Jetlink Solutions cut system costs by 25%.",
    image=(
        "./assets/jpeg/jetlink-proxysmart-dashboard.webp",
        "ProxySmart dashboard for JetLink Canada showing 1 of 1 servers online, 39 devices, 24 working, 15 idle, 0 errors and 24 ports",
        "ProxySmart, the dashboard I built for JetLink Canada: servers, devices and their working, idle and error status at a glance.",
    ),
)
