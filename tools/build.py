# -*- coding: utf-8 -*-
"""Build the static portfolio: index.html + work/<slug>.html.

Design: "Vision 2030" — emerald + gold, Alexandria headings, IBM Plex Sans Arabic text.
Run:  python3 tools/build.py
"""
import os
from html import escape
from urllib.parse import quote

from content import SITE, EMAIL, WHATSAPP, LINKEDIN, GITHUB, PROJECTS, ARCHIVE, STACKS, SECTIONS
from diagrams import diagram

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def T(en, ar, tag="span"):
    """Bilingual inline text."""
    return f'<{tag} lang="en">{en}</{tag}><{tag} lang="ar">{ar}</{tag}>'


def wa(text):
    return f"https://wa.me/{WHATSAPP}?text={quote(text)}"


MAIL = (f"mailto:{EMAIL}?subject={quote('Project enquiry')}&body="
        + quote("Hi Mohammed,\n\nCompany:\nWhat we need (Odoo / web / mobile):\nTimeline:\nBudget range:\n\nThanks,"))
CV_REQ = wa("Hi Mohammed, could you share your CV? I found you through your portfolio.")
CALL = wa("Hi Mohammed, I saw your portfolio and would like to book a 30-minute call about a project.")

KIND_LABEL = {"web": ("Web", "ويب"), "erp": ("Odoo ERP", "Odoo ERP"), "mobile": ("Mobile", "جوال")}

# small inline icons (stroke = currentColor)
ICON = {
    "arrow": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "erp": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><path d="M14 17.5h7M17.5 14v7"/></svg>',
    "upgrade": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M6 11l6-6 6 6"/><path d="M5 21h14"/></svg>',
    "web": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="18" height="14" rx="2"/><path d="M3 8h18M8 21h8"/></svg>',
    "wa": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.3-3.9A8 8 0 1 1 8 19z"/><path d="M9 10c.5 2 2 3.5 4 4l1.2-1.2 2 1-.6 1.6c-3.6.2-7.4-3.6-7.2-7.2L10 7.6l1 2z"/></svg>',
    "mail": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    "in": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10v7M8 7v.01M12 17v-4a2 2 0 0 1 4 0v4M12 10v7"/></svg>',
    "gh": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 19c-4 1.3-4-2-6-2.5M15 21v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.3 4.3 0 0 0-.1-3.2s-1-.3-3.4 1.3a11.6 11.6 0 0 0-6.2 0C5.6 2.8 4.6 3.1 4.6 3.1a4.3 4.3 0 0 0-.1 3.2A4.6 4.6 0 0 0 3.2 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/></svg>',
    "check": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
}

# 8-point star pattern used on dark sections
PATTERN = ('<svg class="pattern" aria-hidden="true"><defs><pattern id="star" width="64" height="64" patternUnits="userSpaceOnUse">'
           '<path d="M32 6l7.5 18.5L58 32l-18.5 7.5L32 58l-7.5-18.5L6 32l18.5-7.5z" fill="none" stroke="currentColor" stroke-width="1"/>'
           '<rect x="22" y="22" width="20" height="20" transform="rotate(45 32 32)" fill="none" stroke="currentColor" stroke-width="1"/>'
           '</pattern></defs><rect width="100%" height="100%" fill="url(#star)"/></svg>')

STATS = [
    ("24+", "projects across ERP, web and mobile", "مشروعًا في ERP والويب والجوال"),
    ("1,900+", "commits in the last 21 months", "commit خلال آخر ٢١ شهرًا"),
    ("120+", "Odoo modules delivered", "موديول Odoo تم تسليمه"),
    ("4+", "years of professional experience", "سنوات خبرة مهنية"),
]


# ----------------------------------------------------------------------------
# Shared chrome
# ----------------------------------------------------------------------------

def head(title_en, desc, path, prefix, og="assets/img/og.jpg"):
    url = SITE + "/" + path
    return f'''<!doctype html>
<html lang="en" dir="ltr" data-lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title_en)}</title>
  <meta name="description" content="{escape(desc)}">
  <meta name="theme-color" content="#0B5D4B">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="en" href="{url}?lang=en">
  <link rel="alternate" hreflang="ar" href="{url}?lang=ar">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(title_en)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/{og}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@400;500;600;700;800&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}assets/style.css">
  <script>
    (function () {{
      var r = document.documentElement, q = new URLSearchParams(location.search), s = null;
      try {{ s = localStorage.getItem('lang'); }} catch (e) {{}}
      var l = q.get('lang') || s || ((navigator.language || '').slice(0, 2) === 'ar' ? 'ar' : 'en');
      if (l !== 'ar' && l !== 'en') l = 'en';
      r.lang = l; r.dir = l === 'ar' ? 'rtl' : 'ltr'; r.dataset.lang = l;
      r.classList.add('js');
    }})();
  </script>
</head>'''


NAV = [("index.html", ("Home", "الرئيسية")), ("erp.html", ("ERP", "ERP")), ("web.html", ("Web", "الويب")),
       ("backend.html", ("Backend", "الباك إند")), ("mobile.html", ("Mobile", "الجوال")), ("projects.html", ("All projects", "كل المشاريع"))]


def masthead(prefix, active="index.html"):
    links = "".join(f'<a href="{prefix}{href}"{" class=\"is-active\" aria-current=\"page\"" if href == active else ""}>{T(*lab)}</a>' for href, lab in NAV)
    return f'''
<body>
  <a class="skip" href="#main">{T("Skip to content", "انتقل إلى المحتوى")}</a>
  <header class="masthead">
    <div class="wrap masthead__row">
      <a class="brand" href="{prefix}index.html" aria-label="Mohammed Hefzallah — home">
        <span class="brand__mark" aria-hidden="true">M<b>H</b></span>
        <span class="brand__text"><strong>{T("Mohammed Hefzallah", "محمد حفظ الله")}</strong><small>{T("Software Engineer", "مهندس برمجيات")}</small></span>
      </a>
      <nav class="nav" aria-label="Main">{links}</nav>
      <div class="tools">
        <button class="lang" type="button" data-lang-toggle aria-label="Switch language">{T("العربية", "English")}</button>
        <a class="btn btn--gold btn--sm" href="#contact">{T("Contact", "تواصل")}</a>
      </div>
    </div>
  </header>'''


def footer(prefix):
    return f'''
  <section class="cta" id="contact">
    {PATTERN}
    <div class="wrap cta__grid">
      <div>
        <p class="kicker kicker--gold">{T("Let’s work together", "لنعمل معًا")}</p>
        <h2 class="cta__title">{T("Have a system to build — or fix?", "عندك نظام تريد بناءه أو تطويره؟")}</h2>
        <p class="cta__lede">{T("Tell me what you’re trying to solve. I reply within one working day, and my hours overlap fully with Saudi business hours.", "أخبرني بما تريد حلّه. أردّ خلال يوم عمل واحد، وساعات عملي متوافقة بالكامل مع ساعات العمل في السعودية.")}</p>
        <div class="cta__actions">
          <a class="btn btn--gold" href="{CALL}" target="_blank" rel="noopener">{ICON["wa"]}{T("Book a 30-min call", "احجز مكالمة ٣٠ دقيقة")}</a>
          <a class="btn btn--ghost" href="{MAIL}">{ICON["mail"]}{T("Send a project brief", "أرسل وصف المشروع")}</a>
        </div>
      </div>
      <ul class="contact-list">
        <li><button type="button" class="contact-item" data-copy="{EMAIL}">{ICON["mail"]}<span><small>{T("Email · click to copy", "البريد · اضغط للنسخ")}</small><b dir="ltr">{EMAIL}</b></span><em class="copied" aria-live="polite"></em></button></li>
        <li><a class="contact-item" href="{CALL}" target="_blank" rel="noopener">{ICON["wa"]}<span><small>WhatsApp</small><b dir="ltr">+20 155 446 3171</b></span></a></li>
        <li><a class="contact-item" href="{LINKEDIN}" target="_blank" rel="noopener">{ICON["in"]}<span><small>LinkedIn</small><b dir="ltr">in/mhefzallah</b></span></a></li>
        <li><a class="contact-item" href="{GITHUB}" target="_blank" rel="noopener">{ICON["gh"]}<span><small>GitHub</small><b dir="ltr">@mhefzallah</b></span></a></li>
      </ul>
    </div>
  </section>
  <footer class="footer">
    <div class="wrap footer__row">
      <p>© <span data-year>2026</span> {T("Mohammed Hefzallah", "محمد حفظ الله")}</p>
      <p>{T("Cairo · Working with KSA, UAE &amp; Europe", "القاهرة · أعمل مع السعودية والإمارات وأوروبا")} · <span data-clock>--:--</span></p>
      <p><a href="{CV_REQ}" target="_blank" rel="noopener">{T("Request CV", "اطلب السيرة الذاتية")}</a> · <a href="#main">{T("Back to top", "للأعلى")} ↑</a></p>
    </div>
  </footer>
  <div class="lightbox" data-lightbox hidden>
    <button class="lightbox__close" type="button" aria-label="Close">×</button>
    <button class="lightbox__nav lightbox__prev" type="button" aria-label="Previous">‹</button>
    <figure><img alt=""><figcaption></figcaption></figure>
    <button class="lightbox__nav lightbox__next" type="button" aria-label="Next">›</button>
  </div>
  <script src="{prefix}assets/main.js" defer></script>
</body>
</html>
'''


def img(prefix, name, alt, lazy=True):
    w, h = (390, 844) if name.endswith("mobile") else (1440, 900)
    lz = ' loading="lazy" decoding="async"' if lazy else ""
    return f'<img src="{prefix}assets/work/{name}.webp" width="{w}" height="{h}" alt="{escape(alt)}"{lz}>'


def cover(prefix, p, lazy=True):
    if p.get("diagram"):
        return f'<div class="cover cover--diagram">{diagram(p["diagram"])}</div>'
    return f'<div class="cover"><div class="cover__bar" aria-hidden="true"><i></i><i></i><i></i></div>{img(prefix, p["cover"], p["title"][0], lazy)}</div>'


def kinds_label(p):
    return "".join(f'<span class="tag">{T(*KIND_LABEL[k])}</span>' for k in p["kinds"])


def section_head(n, en, ar, note=None, extra=""):
    note_html = f'<p class="section__note">{T(*note)}</p>' if note else ""
    return f'''<header class="section__head">
          <div><p class="kicker">{n}</p><h2 class="title">{T(en, ar)}</h2>{note_html}</div>{extra}
        </header>'''


# ----------------------------------------------------------------------------
# Home
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# v4 building blocks: tech cards, sections, projects index
# ----------------------------------------------------------------------------

LOGO_FOR = {"React": "react", "Next.js": "nextdotjs", "TypeScript": "typescript", "Vite": "vite", "Tailwind CSS": "tailwindcss",
            "Vanilla JS": "javascript", "GSAP": "gsap", "Django REST Framework": "django", "Python (Odoo ORM)": "python",
            "PHP MVC": "php", "Supabase": "supabase", "Sanity CMS": "sanity", "PostgreSQL": "postgresql", "MySQL": "mysql",
            "Capacitor": "capacitor", "PWA": "pwa", "Flutter": "flutter", "Odoo": "odoo"}


def logo(prefix, name, cls="logo"):
    return f'<img class="{cls}" src="{prefix}assets/logos/{name}.svg" alt="" width="20" height="20" loading="lazy">'


def by_slug(slug):
    return next(p for p in PROJECTS if p["slug"] == slug)


def matches(stack, g):
    vals = stack.get(g["field"], [])
    return g["tag"] in vals and not (g.get("exclude") and g["exclude"] in vals)


def group_projects(g):
    return [p for p in PROJECTS if matches(STACKS[p["slug"]], g)]


def stack_rows(prefix, p, compact=True):
    st = STACKS[p["slug"]]
    rows = [("Frontend", "الواجهة", st["frontend"]), ("Backend", "الباك إند", st["backend"]),
            ("Database", "قاعدة البيانات", st["database"]), ("Mobile", "الجوال", st["mobile"])]
    if not compact:
        rows += [("Integrations", "التكاملات", st["integrations"]), ("Platform", "المنصّة", st["platform"]),
                 ("Hosting", "الاستضافة", [st["hosting"]] if st["hosting"] else [])]
    out = []
    for en, ar, vals in rows:
        if not vals:
            continue
        chips = "".join(f'<span class="tech">{logo(prefix, LOGO_FOR[v], "tech__logo") if v in LOGO_FOR else ""}{v}</span>' for v in vals)
        out.append(f'<div class="stackrow"><dt>{T(en, ar)}</dt><dd dir="ltr">{chips}</dd></div>')
    return f'<dl class="stackcard{" stackcard--full" if not compact else ""}">{"".join(out)}</dl>'


def project_card(prefix, p, extra_attrs=""):
    return f'''
          <article class="card pcard reveal" {extra_attrs}>
            <a class="card__link" href="{prefix}work/{p["slug"]}.html">
              {cover(prefix, p)}
              <div class="card__body">
                <div class="card__tags">{kinds_label(p)}<span class="card__year">{p["year"]}</span></div>
                <h3 class="card__title">{T(*p["title"])}</h3>
                <p class="card__out">{T(*p["outcome"])}</p>
                {stack_rows(prefix, p)}
                <span class="card__more">{T("View case study", "عرض دراسة الحالة")} {ICON["arrow"]}</span>
              </div>
            </a>
          </article>'''


def coming_soon(prefix, g):
    return f'''
          <div class="soon reveal">
            <span class="soon__logo">{logo(prefix, g["logo"], "soon__img")}</span>
            <div>
              <p class="soon__badge">{T("Coming soon", "قريبًا")}</p>
              <h4>{T(f'{g["name"]} case studies are on the way', f'دراسات حالة {g["name"]} قيد الإعداد')}</h4>
              <p>{T("I’m preparing projects for this track. Want to discuss a " + g["name"] + " requirement now?", "أعمل حاليًا على مشاريع في هذا المسار. تريد مناقشة متطلبات " + g["name"] + " الآن؟")}</p>
            </div>
            <a class="btn btn--outline btn--sm" href="#contact">{T("Get in touch", "تواصل معي")}</a>
          </div>'''


def section_page(sec):
    pre = ""
    nav = "".join(f'<a class="subnav__item" href="#{g["key"]}">{logo(pre, g["logo"], "subnav__logo")}{g["name"]}<sup dir="ltr">{len(group_projects(g)) or "—"}</sup></a>'
                  for g in sec["groups"])
    groups = []
    for g in sec["groups"]:
        ps = group_projects(g)
        content = ('<div class="cards cards--2">' + "".join(project_card(pre, p) for p in ps) + '</div>') if ps else coming_soon(pre, g)
        groups.append(f'''
      <section class="group" id="{g["key"]}">
        <header class="group__head reveal">
          <span class="group__logo">{logo(pre, g["logo"], "group__img")}</span>
          <div><h2 class="group__title">{g["name"]}</h2><p>{T(*g["desc"])}</p></div>
          {f'<span class="group__count" dir="ltr">{len(ps)} ' + T("projects" if len(ps) != 1 else "project", "مشاريع" if len(ps) != 1 else "مشروع") + '</span>' if ps else '<span class="group__count group__count--soon">' + T("Coming soon", "قريبًا") + '</span>'}
        </header>
        {content}
      </section>''')
    body = f'''
  <main id="main">
    <section class="page-hero">
      {PATTERN}
      <div class="wrap">
        <p class="kicker kicker--gold">{T("Software Engineering", "هندسة البرمجيات")}</p>
        <h1 class="page-title">{T(*sec["title"])}</h1>
        <p class="page-lede">{T(*sec["lede"])}</p>
        <nav class="subnav" aria-label="Sections">{nav}</nav>
      </div>
    </section>
    <div class="wrap groups">{"".join(groups)}
    </div>
  </main>'''
    title = f'{sec["title"][0]} — Mohammed Hefzallah'
    return head(title, sec["lede"][0], f'{sec["slug"]}.html', pre) + masthead(pre, f'{sec["slug"]}.html') + body + footer(pre)


def projects_page():
    pre = ""
    def opts(field):
        vals = sorted({v for s in STACKS.values() for v in s[field]})
        return "".join(f'<option value="{escape(v)}">{escape(v)}</option>' for v in vals)
    areas = [("all", ("All", "الكل")), ("erp", ("ERP", "ERP")), ("web", ("Web", "الويب")), ("backend", ("Backend", "الباك إند")), ("mobile", ("Mobile", "الجوال"))]
    chips = "".join(f'<button type="button" class="chip{" is-on" if k == "all" else ""}" data-area="{k}">{T(*l)}</button>' for k, l in areas)
    cards = "".join(project_card(pre, p, 'data-areas="{}" data-frontend="{}" data-backend="{}" data-database="{}"'.format(
        " ".join(STACKS[p["slug"]]["areas"]), escape("|".join(STACKS[p["slug"]]["frontend"])),
        escape("|".join(STACKS[p["slug"]]["backend"])), escape("|".join(STACKS[p["slug"]]["database"])))) for p in PROJECTS)
    body = f'''
  <main id="main">
    <section class="page-hero page-hero--short">
      {PATTERN}
      <div class="wrap">
        <p class="kicker kicker--gold">{T("Portfolio", "الأعمال")}</p>
        <h1 class="page-title">{T("All projects", "كل المشاريع")}</h1>
        <p class="page-lede">{T("Filter by area, framework, backend or database.", "فلتر حسب المجال أو الـ framework أو الباك إند أو قاعدة البيانات.")}</p>
      </div>
    </section>
    <div class="wrap">
      <div class="toolbar reveal" data-project-filters>
        <div class="filters" role="group" aria-label="Area">{chips}</div>
        <label class="select"><span>{T("Frontend", "الواجهة")}</span><select data-field="frontend"><option value="">—</option>{opts("frontend")}</select></label>
        <label class="select"><span>{T("Backend", "الباك إند")}</span><select data-field="backend"><option value="">—</option>{opts("backend")}</select></label>
        <label class="select"><span>{T("Database", "قاعدة البيانات")}</span><select data-field="database"><option value="">—</option>{opts("database")}</select></label>
        <p class="toolbar__count" aria-live="polite"><b data-count>{len(PROJECTS)}</b> {T("projects", "مشروع")}</p>
      </div>
      <div class="cards cards--3" data-project-grid>{cards}
      </div>
      <p class="empty" data-empty hidden>{T("No project matches these filters yet.", "لا يوجد مشروع يطابق هذه الفلاتر حاليًا.")}</p>
    </div>
  </main>'''
    return head("All projects — Mohammed Hefzallah", "All projects by Mohammed Hefzallah, filterable by area, framework, backend and database.", "projects.html", pre) + masthead(pre, "projects.html") + body + footer(pre)


def home():
    pre = ""
    stats = "".join(f'<div class="stat reveal"><dt dir="ltr">{v}</dt><dd>{T(en, ar)}</dd></div>' for v, en, ar in STATS)
    pillars = []
    for sec in SECTIONS:
        total = len({p["slug"] for g in sec["groups"] for p in group_projects(g)})
        gl = "".join(f'<li>{logo(pre, g["logo"], "pillar__logo")}<span>{g["name"]}</span>{"" if group_projects(g) else "<em>" + T("soon", "قريبًا") + "</em>"}</li>' for g in sec["groups"])
        pillars.append(f'''
          <a class="pillar reveal" href="{sec["slug"]}.html">
            <span class="pillar__icon">{logo(pre, sec["icon"], "pillar__big")}</span>
            <h3>{T(*sec["title"])}</h3>
            <p>{T(*sec["lede"])}</p>
            <ul>{gl}</ul>
            <span class="pillar__more"><b dir="ltr">{total}</b> {T("projects", "مشاريع")} · {T("Explore", "استكشف")} {ICON["arrow"]}</span>
          </a>''')
    featured = "".join(project_card(pre, by_slug(s)) for s in ("booking-platforms", "odoo-v19-migration", "support-crm"))
    # stack matrix: every tech with the number of projects using it
    cols = [("Frontend", "الواجهة", "frontend"), ("Backend", "الباك إند", "backend"), ("Database", "قاعدة البيانات", "database"),
            ("Mobile", "الجوال", "mobile"), ("Platforms", "المنصّات", "platform")]
    mcols = []
    for en, ar, f in cols:
        counts = {}
        for st in STACKS.values():
            for v in st[f]:
                counts[v] = counts.get(v, 0) + 1
        items = "".join(f'<li>{logo(pre, LOGO_FOR[v], "tech__logo") if v in LOGO_FOR else ""}<span>{v}</span><b dir="ltr">{n}</b></li>' for v, n in sorted(counts.items(), key=lambda x: -x[1]))
        if f == "platform":
            items += f'<li>{logo(pre, "servicenow", "tech__logo")}<span>ServiceNow</span><em>{T("soon", "قريبًا")}</em></li><li>{logo(pre, "zoho", "tech__logo")}<span>Zoho</span><em>{T("soon", "قريبًا")}</em></li>'
        if f == "mobile":
            items += f'<li>{logo(pre, "flutter", "tech__logo")}<span>Flutter</span><em>{T("soon", "قريبًا")}</em></li>'
        mcols.append(f'<div class="matrix__col reveal"><h3>{T(en, ar)}</h3><ul dir="ltr">{items}</ul></div>')

    body = f'''
  <main id="main">
    <section class="hero">
      <div class="wrap hero__grid">
        <div class="hero__text">
          <p class="badge"><span class="dot" aria-hidden="true"></span>{T("Available for new projects", "متاح لمشاريع جديدة")}</p>
          <h1 class="display">{T("Software <em>Engineer</em>", "مهندس <em>برمجيات</em>")}</h1>
          <p class="tagline">{T("I build the systems businesses run on — ERP, web and mobile.", "أبني الأنظمة التي تُدار بها الأعمال — ERP والويب والجوال.")}</p>
          <p class="lede">{T("ERP and business platforms, fullstack web and mobile — for companies in Saudi Arabia, the UAE and Egypt. From payroll that follows Saudi Labor Law and ZATCA e-invoicing to web platforms that take live payments.",
                             "أنظمة ERP ومنصّات أعمال، تطوير ويب متكامل وتطبيقات جوال — لشركات في السعودية والإمارات ومصر. من رواتب متوافقة مع نظام العمل السعودي وفوترة ZATCA، إلى منصّات ويب تستقبل مدفوعات حقيقية.")}</p>
          <div class="actions">
            <a class="btn btn--primary" href="projects.html">{T("Browse projects", "تصفّح المشاريع")} {ICON["arrow"]}</a>
            <a class="btn btn--outline" href="{CALL}" target="_blank" rel="noopener">{T("Book a 30-min call", "احجز مكالمة ٣٠ دقيقة")}</a>
          </div>
          <ul class="hero__points">
            <li>{ICON["check"]}{T("ERP · Web · Backend · Mobile", "ERP · ويب · باك إند · جوال")}</li>
            <li>{ICON["check"]}{T("Odoo Certified Professional", "معتمد من Odoo")}</li>
            <li>{ICON["check"]}{T("Arabic &amp; English", "العربية والإنجليزية")}</li>
          </ul>
        </div>
        <figure class="portrait">
          <div class="portrait__card">
            {PATTERN}
            <img src="assets/img/portrait.webp" width="900" height="803" alt="Mohammed Hefzallah" fetchpriority="high">
          </div>
          <figcaption class="portrait__tag">
            <b>{T("Mohammed Hefzallah", "محمد حفظ الله")}</b>
            <span>{T("Software Engineer · Odoo Developer at AZM Squad", "مهندس برمجيات · مطوّر Odoo في AZM Squad")}</span>
          </figcaption>
          <div class="portrait__float" aria-hidden="true"><b dir="ltr">1,900+</b><span>{T("commits in 21 months", "commit خلال ٢١ شهرًا")}</span></div>
        </figure>
      </div>
      <div class="wrap"><dl class="stats">{stats}</dl></div>
    </section>

    <section class="strip" aria-label="Sectors">
      <div class="wrap strip__row">
        <p class="strip__label">{T("Sectors I’ve worked in", "قطاعات عملت فيها")}</p>
        <ul class="strip__list">
          <li>{T("Government", "الحكومة")}</li><li>{T("Oil &amp; Gas", "النفط والغاز")}</li><li>{T("Construction", "المقاولات")}</li>
          <li>{T("Automotive", "السيارات")}</li><li>{T("Retail &amp; POS", "التجزئة")}</li><li>{T("Logistics", "اللوجستيات")}</li>
          <li>{T("Tourism", "السياحة")}</li><li>{T("Education", "التعليم")}</li><li>{T("Consulting", "الاستشارات")}</li>
        </ul>
      </div>
    </section>

    <section class="section" id="areas">
      <div class="wrap">
        {section_head("01", "What I build", "ما الذي أبنيه", ("Four tracks — each with its own page, grouped by platform and framework.", "أربعة مسارات — لكلٍّ منها صفحته، مقسّمة حسب المنصّة والـ framework."))}
        <div class="pillars">{"".join(pillars)}</div>
      </div>
    </section>

    <section class="section section--soft" id="work">
      <div class="wrap">
        {section_head("02", "Featured projects", "مشاريع مختارة", None, f'<a class="btn btn--outline btn--sm" href="projects.html">{T("All projects", "كل المشاريع")} {ICON["arrow"]}</a>')}
        <div class="cards cards--featured">{featured}</div>
      </div>
    </section>

    <section class="section" id="stack">
      <div class="wrap">
        {section_head("03", "Tech stack", "التقنيات", ("Every technology I’ve shipped with, and how many projects use it.", "كل تقنية استخدمتها في مشاريع حقيقية، وعدد المشاريع التي تستخدمها."))}
        <div class="matrix">{"".join(mcols)}</div>
      </div>
    </section>

    <section class="section section--dark" id="services">
      {PATTERN}
      <div class="wrap">
        {section_head("04", "How we can work together", "كيف نعمل معًا", ("Every engagement starts with a free 30-minute call.", "كل تعاون يبدأ بمكالمة مجانية مدتها ٣٠ دقيقة."))}
        <ol class="process">
          <li class="reveal"><span class="process__n" dir="ltr">01</span><b>{T("Discovery call", "مكالمة تعارف")}</b><span>{T("30 minutes, free.", "٣٠ دقيقة مجانًا.")}</span></li>
          <li class="reveal"><span class="process__n" dir="ltr">02</span><b>{T("Scope &amp; quote", "النطاق والتسعير")}</b><span>{T("Written scope within 48 hours.", "نطاق مكتوب خلال ٤٨ ساعة.")}</span></li>
          <li class="reveal"><span class="process__n" dir="ltr">03</span><b>{T("Build in sprints", "التنفيذ على مراحل")}</b><span>{T("Weekly demos on staging.", "عرض أسبوعي على بيئة تجريبية.")}</span></li>
          <li class="reveal"><span class="process__n" dir="ltr">04</span><b>{T("Launch &amp; support", "الإطلاق والدعم")}</b><span>{T("Go-live, training and support.", "التشغيل والتدريب والدعم.")}</span></li>
        </ol>
      </div>
    </section>

    <section class="section section--soft" id="experience">
      <div class="wrap">
        {section_head("05", "Experience", "الخبرة", None, f'<a class="btn btn--outline btn--sm" href="{CV_REQ}" target="_blank" rel="noopener">{T("Request full CV", "اطلب السيرة الذاتية")}</a>')}
        <ol class="timeline">{exp_rows()}</ol>
        <div class="creds">
          <div class="cred reveal"><span class="cred__icon">{ICON["check"]}</span><b>{T("B.Sc. Computer Science", "بكالوريوس علوم الحاسب")}</b><span>{T("New Cairo Academy · 2024", "أكاديمية القاهرة الجديدة · ٢٠٢٤")}</span></div>
          <div class="cred reveal"><span class="cred__icon">{ICON["check"]}</span><b>{T("Odoo Certified Professional", "شهادة Odoo المعتمدة")}</b><span>{T("Functional v15 · Odoo S.A. · 2024", "وظيفية الإصدار 15 · Odoo S.A. · ٢٠٢٤")}</span></div>
          <div class="cred reveal"><span class="cred__icon">{ICON["check"]}</span><b>{T("Languages", "اللغات")}</b><span>{T("Arabic (native) · English (professional)", "العربية (الأم) · الإنجليزية (مهنية)")}</span></div>
        </div>
      </div>
    </section>
  </main>'''
    title = "Mohammed Hefzallah — Software Engineer · ERP, Fullstack & Mobile"
    desc = "Software engineer building ERP systems (Odoo), fullstack web platforms and mobile apps for companies in Saudi Arabia, the UAE and Egypt."
    return head(title, desc, "", "") + masthead("", "index.html") + body + footer("")



def exp_rows():
    rows = [
        (("Nov 2025 — now", "نوفمبر ٢٠٢٥ — الآن"), ("Odoo Developer", "مطوّر Odoo"), "AZM Squad", ("Government ERP serving 1,000+ users across 10+ departments.", "نظام ERP حكومي يخدم أكثر من ١٠٠٠ مستخدم في أكثر من ١٠ إدارات."), ("Saudi Arabia · remote", "السعودية · عن بُعد"), True),
        (("2025 — now", "٢٠٢٥ — الآن"), ("Independent ERP &amp; Fullstack Consultant", "مستشار ERP ومطوّر ويب مستقل"), ("Self-employed", "عمل حر"), ("Odoo migrations, Saudi HR &amp; payroll, delivery operations, booking platforms and learning apps for clients in KSA, UAE &amp; Egypt.", "ترقيات Odoo، موارد بشرية ورواتب سعودية، عمليات توصيل، منصّات حجز وتطبيقات تعليمية لعملاء في السعودية والإمارات ومصر."), ("Remote", "عن بُعد"), True),
        (("Jul 2022 — Nov 2025", "يوليو ٢٠٢٢ — نوفمبر ٢٠٢٥"), ("Odoo Developer", "مطوّر Odoo"), "Algoriza", ("10+ modules for Saudi logistics &amp; e-commerce; 15% faster reports; mentored 5 juniors.", "أكثر من ١٠ موديولات للوجستيات والتجارة الإلكترونية؛ تقارير أسرع ١٥٪؛ إرشاد ٥ مطوّرين."), ("Remote", "عن بُعد"), False),
        (("Jan — Jun 2022", "يناير — يونيو ٢٠٢٢"), ("Junior Odoo Developer", "مطوّر Odoo مبتدئ"), "Algoriza", ("5 modules shipped to production as an intern.", "٥ موديولات على الإنتاج خلال فترة التدريب."), ("Remote", "عن بُعد"), False),
    ]
    out = []
    for when, role, org, note, where, now in rows:
        org_html = T(*org) if isinstance(org, tuple) else org
        out.append(f'''
          <li class="tl reveal{" tl--now" if now else ""}">
            <span class="tl__dot" aria-hidden="true"></span>
            <div class="tl__card">
              <div class="tl__top"><b>{T(*role)}</b><span class="tl__when">{T(*when)}</span></div>
              <p class="tl__org">{org_html} · <span>{T(*where)}</span></p>
              <p class="tl__note">{T(*note)}</p>
            </div>
          </li>''')
    return "".join(out)


# ----------------------------------------------------------------------------
# Case studies
# ----------------------------------------------------------------------------

def case(i, p):
    pre = "../"
    nxt = PROJECTS[i % len(PROJECTS)]
    did = "".join(f'<li class="step reveal"><span class="step__n" dir="ltr">{n:02d}</span><div><h4>{T(eh, ah)}</h4><p>{T(en, ar)}</p></div></li>'
                  for n, (eh, ah, en, ar) in enumerate(p["did"], 1))
    decisions = ""
    if p["decisions"]:
        decisions = f'''<section class="block reveal"><h2 class="block__h">{T("Key decisions", "قرارات أساسية")}</h2>
          <ul class="decisions">{"".join(f"<li>{ICON['check']}<span>{T(*d)}</span></li>" for d in p["decisions"])}</ul></section>'''
    results = ""
    if p["results"]:
        results = f'''<section class="block reveal"><h2 class="block__h">{T("Results", "النتائج")}</h2>
          <dl class="results">{"".join(f'<div><dt dir="ltr">{v}</dt><dd>{T(en, ar)}</dd></div>' for v, en, ar in p["results"])}</dl></section>'''
    gallery = ""
    figs_src = [g for g in p["gallery"] if g[0] != p.get("cover") or len(p["gallery"]) == 1]
    if figs_src or p["mobile"]:
        figs = "".join(
            f'<figure class="fig reveal"><button type="button" class="fig__btn" data-zoom aria-label="Enlarge">{img(pre, name, en)}</button>'
            f'<figcaption>{T(en, ar)}</figcaption></figure>' for name, en, ar in figs_src)
        phones = ""
        if p["mobile"]:
            phones = '<div class="phones reveal">' + "".join(
                f'<figure class="phone"><button type="button" class="fig__btn" data-zoom aria-label="Enlarge">{img(pre, m, "Mobile view")}</button></figure>'
                for m in p["mobile"]) + "</div>"
        gallery = f'''<section class="gallery-wrap"><div class="wrap">
          <h2 class="block__h">{T("Gallery", "معرض الصور")}</h2>
          <div class="gallery">{figs}</div>{phones}</div></section>'''
    elif p.get("diagram"):
        gallery = f'<div class="wrap"><p class="note note--box">{T("Screens from client ERPs are confidential, so this case study uses diagrams and numbers instead of screenshots.", "شاشات أنظمة العملاء سرّية، لذا تعتمد دراسة الحالة هذه على المخططات والأرقام بدل الصور.")}</p></div>'
    links = "".join(f'<a href="{u}" target="_blank" rel="noopener" dir="ltr">{t} ↗</a>' for t, u in p["links"])
    links_row = f'<div><dt>{T("Live", "الرابط")}</dt><dd class="links">{links}</dd></div>' if links else ""

    body = f'''
  <main id="main" class="casepage">
    <section class="case-hero">
      {PATTERN}
      <div class="wrap">
        <a class="back" href="../index.html#work">{T("← All work", "→ كل الأعمال")}</a>
        <div class="case-hero__tags">{kinds_label(p)}<span class="tag tag--line">{T(*p["sector"])}</span><span class="tag tag--line" dir="ltr">{p["year"]}</span></div>
        <h1 class="case-title">{T(*p["title"])}</h1>
        <p class="case-out">{T(*p["outcome"])}</p>
      </div>
    </section>
    <div class="wrap">
      <div class="case-cover reveal">{cover(pre, p, lazy=False)}</div>
      <div class="case-grid">
        <aside class="case-meta">
          <dl>
            <div><dt>{T("Role", "الدور")}</dt><dd>{T(*p["role"])}</dd></div>
            <div><dt>{T("Year", "السنة")}</dt><dd dir="ltr">{p["year"]}</dd></div>
            <div><dt>{T("Built with", "التقنيات")}</dt><dd class="stack" dir="ltr">{p["stack"]}</dd></div>
            {links_row}
          </dl>
          <h3 class="case-meta__h">{T("Technical card", "البطاقة التقنية")}</h3>
          {stack_rows(pre, p, compact=False)}
          <a class="btn btn--primary btn--block" href="{CALL}" target="_blank" rel="noopener">{T("Need something similar?", "تحتاج شيئًا مشابهًا؟")}</a>
        </aside>
        <div class="case-body">
          <section class="block reveal"><h2 class="block__h">{T("Context", "السياق")}</h2>{"".join(f'<p class="prose">{T(*c)}</p>' for c in p["context"])}</section>
          <section class="block"><h2 class="block__h reveal">{T("What I built", "ما الذي بنيته")}</h2><ol class="steps">{did}</ol></section>
          {decisions}
          {results}
        </div>
      </div>
    </div>
    {gallery}
    <div class="wrap">
      <a class="next reveal" href="{nxt["slug"]}.html">
        <span class="kicker">{T("Next case study", "دراسة الحالة التالية")}</span>
        <span class="next__title">{T(*nxt["title"])} {ICON["arrow"]}</span>
      </a>
    </div>
  </main>'''
    title = f'{p["title"][0]} — Mohammed Hefzallah'
    return head(title, p["outcome"][0], f'work/{p["slug"]}.html', pre, og=f'assets/og/{p["slug"]}.jpg') + masthead(pre, "") + body + footer(pre)


def main():
    os.makedirs(os.path.join(ROOT, "work"), exist_ok=True)
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(home())
    for i, p in enumerate(PROJECTS, 1):
        with open(os.path.join(ROOT, "work", p["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(case(i, p))
    for sec in SECTIONS:
        with open(os.path.join(ROOT, sec["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(section_page(sec))
    with open(os.path.join(ROOT, "projects.html"), "w", encoding="utf-8") as f:
        f.write(projects_page())
    print("built index + projects +", len(SECTIONS), "sections +", len(PROJECTS), "case studies")


if __name__ == "__main__":
    main()
