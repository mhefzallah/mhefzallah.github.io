# -*- coding: utf-8 -*-
"""Build the static portfolio: index.html + work/<slug>.html.

Run:  python3 tools/build.py
"""
import os
from html import escape
from urllib.parse import quote

from content import (SITE, EMAIL, WHATSAPP, LINKEDIN, GITHUB, PROJECTS, ARCHIVE)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AR_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


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

# ----------------------------------------------------------------------------
# Diagrams (inline SVG, themed through CSS variables)
# ----------------------------------------------------------------------------

def diagram(name):
    if name == "migration":
        steps = [("01", "Audit", "مراجعة", "63 modules"), ("02", "Rewrite", "إعادة كتابة", "ORM · XML · OWL"),
                 ("03", "Validate", "تحقق", "Odoo.sh staging"), ("04", "Release", "إطلاق", "Zero data loss")]
        cells = []
        for i, (n, en, ar, sub) in enumerate(steps):
            x = 40 + i * 190
            cells.append(f'''
      <g transform="translate({x} 150)">
        <rect width="160" height="120" class="d-box{' d-box--accent' if i == 3 else ''}"/>
        <text x="14" y="26" class="d-mono">{n}</text>
        <text x="14" y="70" class="d-title"><tspan lang="en">{en}</tspan><tspan lang="ar">{ar}</tspan></text>
        <text x="14" y="98" class="d-mono">{sub}</text>
      </g>''')
            if i < 3:
                cells.append(f'<path d="M{x + 166} 210 h18" class="d-line" marker-end="url(#arr)"/>')
        mods = ["POS", "ZATCA", "Telr", "HR", "Website", "Inventory", "Accounting", "Reports"]
        chips = "".join(
            f'<g transform="translate({40 + i * 95} 330)"><rect width="85" height="30" class="d-chip"/><text x="42.5" y="20" text-anchor="middle" class="d-mono">{m}</text></g>'
            for i, m in enumerate(mods))
        return f'''<svg class="diagram" viewBox="0 0 800 400" role="img" aria-label="Migration process: audit, rewrite, validate, release">
      <defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="d-arrow"/></marker></defs>
      <text x="40" y="70" class="d-big">v17</text>
      <path d="M150 58 h110" class="d-line" marker-end="url(#arr)"/>
      <text x="280" y="70" class="d-big d-accent">v19</text>
      <text x="40" y="110" class="d-mono">FIG. — MIGRATION PIPELINE</text>
      {''.join(cells)}
      {chips}
    </svg>'''
    if name == "erp":
        mods = [("HR & Payroll", "الموارد البشرية", -90), ("Accounting · ZATCA", "المحاسبة · ZATCA", -30),
                ("POS & Retail", "نقاط البيع", 30), ("Inventory · WMS", "المخزون", 90),
                ("Fleet · Automotive", "السيارات", 150), ("Approvals · Purchase", "الموافقات", 210)]
        import math
        cx, cy = 400, 235
        nodes = []
        for en, ar, deg in mods:
            a = math.radians(deg)
            x, y = cx + 175 * math.cos(a), cy + 120 * math.sin(a)
            nodes.append(f'<path d="M{cx} {cy} L{x:.0f} {y:.0f}" class="d-line d-line--thin"/>')
            nodes.append(f'<g transform="translate({x - 80:.0f} {y - 17:.0f})"><rect width="160" height="34" class="d-chip d-chip--solid"/>'
                         f'<text x="80" y="22" text-anchor="middle" class="d-small"><tspan lang="en">{en}</tspan><tspan lang="ar">{ar}</tspan></text></g>')
        ints = ["SMSA", "OneStock", "Neoleap", "Telr", "PayTabs", "Google Drive", "REST · JWT", "ZATCA"]
        ring = "".join(
            f'<text x="{cx + 340 * math.cos(math.radians(-67.5 + i * 45)):.0f}" y="{cy + 200 * math.sin(math.radians(-67.5 + i * 45)) + 4:.0f}" text-anchor="middle" class="d-mono">{n}</text>'
            for i, n in enumerate(ints))
        return f'''<svg class="diagram" viewBox="0 0 800 470" role="img" aria-label="Odoo core with HR, accounting, POS, inventory, automotive and approvals modules, plus integrations">
      <ellipse cx="{cx}" cy="{cy}" rx="340" ry="200" class="d-ring"/>
      {''.join(nodes)}
      <circle cx="{cx}" cy="{cy}" r="46" class="d-core"/>
      <text x="{cx}" y="{cy + 8}" text-anchor="middle" class="d-core-t">odoo</text>
      {ring}
      <text x="24" y="28" class="d-mono">FIG. — MODULES &amp; INTEGRATIONS</text>
    </svg>'''
    return ""


# ----------------------------------------------------------------------------
# Shared chrome
# ----------------------------------------------------------------------------

def head(title_en, desc, path, prefix):
    url = SITE + "/" + path
    return f'''<!doctype html>
<html lang="en" dir="ltr" data-lang="en" data-theme="paper">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title_en)}</title>
  <meta name="description" content="{escape(desc)}">
  <meta name="theme-color" content="#F3EFE6">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="en" href="{url}?lang=en">
  <link rel="alternate" hreflang="ar" href="{url}?lang=ar">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(title_en)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/img/og.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..600&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+Arabic:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&family=Noto+Naskh+Arabic:wght@500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}assets/style.css">
  <script>
    (function () {{
      var r = document.documentElement, q = new URLSearchParams(location.search), s = {{}};
      try {{ s.l = localStorage.getItem('lang'); s.t = localStorage.getItem('theme'); }} catch (e) {{}}
      var l = q.get('lang') || s.l || ((navigator.language || '').slice(0, 2) === 'ar' ? 'ar' : 'en');
      if (l !== 'ar' && l !== 'en') l = 'en';
      var t = s.t || (matchMedia('(prefers-color-scheme: dark)').matches ? 'ink' : 'paper');
      r.lang = l; r.dir = l === 'ar' ? 'rtl' : 'ltr'; r.dataset.lang = l; r.dataset.theme = t;
      r.classList.add('js');
    }})();
  </script>
</head>'''


def masthead(prefix, home):
    h = "" if home else prefix
    return f'''
<body>
  <a class="skip" href="#main">{T("Skip to content", "انتقل إلى المحتوى")}</a>
  <header class="masthead">
    <div class="wrap masthead__row">
      <a class="mark" href="{prefix}index.html" aria-label="Mohammed Abdullah — home">
        <span class="mark__mono">M<i>.</i>A</span>
        <span class="mark__name">{T("Mohammed Abdullah", "محمد عبدالله")}</span>
      </a>
      <nav class="nav" aria-label="Main">
        <a href="{h}#work">{T("Work", "الأعمال")}</a>
        <a href="{h}#services">{T("Services", "الخدمات")}</a>
        <a href="{h}#experience">{T("Experience", "الخبرة")}</a>
        <a href="{h}#contact">{T("Contact", "تواصل")}</a>
        <span class="nav__bar" aria-hidden="true"></span>
      </nav>
      <div class="tools">
        <span class="clock" title="Cairo time"><span class="clock__dot" aria-hidden="true"></span><span data-clock>--:--</span> {T("Cairo", "القاهرة")}</span>
        <button class="icon-btn" type="button" data-theme-toggle aria-label="Toggle dark mode">
          <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M12 3.5a8.5 8.5 0 0 1 0 17z" fill="currentColor"/></svg>
        </button>
        <button class="lang" type="button" data-lang-toggle aria-label="Switch language">{T("عربي", "English")}</button>
      </div>
    </div>
  </header>'''


def footer(prefix):
    return f'''
  <footer class="footer">
    <div class="wrap footer__grid">
      <div>
        <p class="footer__big">{T("Have a system to build — or fix?", "عندك نظام تريد بناءه — أو إصلاحه؟")}</p>
        <a class="btn btn--ink" href="{CALL}" target="_blank" rel="noopener">{T("Book a 30-min call", "احجز مكالمة ٣٠ دقيقة")}<span class="arrow" aria-hidden="true">→</span></a>
      </div>
      <ul class="footer__links">
        <li><a href="{CALL}" target="_blank" rel="noopener">WhatsApp</a></li>
        <li><a href="{MAIL}">{T("Email", "البريد")}</a></li>
        <li><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></li>
        <li><a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a></li>
        <li><a href="{CV_REQ}" target="_blank" rel="noopener">{T("Request my CV", "اطلب السيرة الذاتية")}</a></li>
      </ul>
    </div>
    <div class="wrap footer__base">
      <p>© <span data-year>2026</span> {T("Mohammed Abdullah", "محمد عبدالله")} · {T("2026 Edition", "إصدار ٢٠٢٦")}</p>
      <p class="colophon">{T("Set in Fraunces &amp; IBM Plex. Built with plain HTML, CSS and a little JavaScript.", "بخطوط Fraunces وIBM Plex. مبني بـ HTML وCSS وقليل من JavaScript.")}</p>
      <p><a class="u" href="#main">{T("Back to top", "للأعلى")} ↑</a></p>
    </div>
  </footer>
  <div class="lightbox" data-lightbox hidden>
    <button class="lightbox__close" type="button" aria-label="Close">×</button>
    <button class="lightbox__nav lightbox__prev" type="button" aria-label="Previous">←</button>
    <figure><img alt=""><figcaption></figcaption></figure>
    <button class="lightbox__nav lightbox__next" type="button" aria-label="Next">→</button>
  </div>
  <script src="{prefix}assets/main.js" defer></script>
</body>
</html>
'''


def img(prefix, name, alt, cls="", lazy=True, w=1440, h=900):
    if name.endswith("mobile"):
        w, h = 390, 844
    return (f'<img class="{cls}" src="{prefix}assets/work/{name}.webp" width="{w}" height="{h}" alt="{escape(alt)}"'
            f'{" loading=\"lazy\" decoding=\"async\"" if lazy else ""}>')


def cover(prefix, p, lazy=True):
    if p.get("diagram"):
        return f'<div class="cover cover--diagram">{diagram(p["diagram"])}</div>'
    return f'<div class="cover">{img(prefix, p["cover"], p["title"][0], lazy=lazy)}</div>'


def kinds_attr(p):
    return " ".join(p["kinds"])


def kinds_label(p):
    return " · ".join(T(*KIND_LABEL[k]) for k in p["kinds"])


# ----------------------------------------------------------------------------
# Home page
# ----------------------------------------------------------------------------

def home():
    pre = ""
    counts = {k: sum(k in p["kinds"] for p in PROJECTS) for k in KIND_LABEL}
    filters = [("all", ("All", "الكل"), len(PROJECTS))] + [(k, KIND_LABEL[k], counts[k]) for k in ("web", "erp", "mobile")]
    chips = "".join(
        f'<button type="button" class="chip{" is-on" if k == "all" else ""}" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{T(*lab)}<sup>{n}</sup></button>'
        for k, lab, n in filters)

    cards = []
    for i, p in enumerate(PROJECTS, 1):
        big = " card--wide" if i in (1, 2) else ""
        cards.append(f'''
        <article class="card{big} reveal" data-kinds="{kinds_attr(p)}">
          <a class="card__link" href="work/{p["slug"]}.html">
            {cover(pre, p)}
            <div class="card__meta"><span class="num">N° {i:02d}</span><span>{kinds_label(p)}</span><span>{p["year"]}</span></div>
            <h3 class="card__title">{T(*p["title"])}</h3>
            <p class="card__out">{T(*p["outcome"])}</p>
            <span class="card__more">{T("Read case study", "اقرأ دراسة الحالة")} <span class="arrow" aria-hidden="true">→</span></span>
          </a>
        </article>''')

    rows = "".join(f'''
          <tr data-kinds="{'erp' if t == 'Odoo' else 'web'}"><td class="mono">{y}</td><td>{T(*name)}</td><td class="muted">{T(*sector)}</td><td class="mono tag">{t}</td><td class="mono muted">{stack}</td></tr>'''
                   for y, t, name, sector, stack in ARCHIVE)

    body = f'''
  <main id="main">
    <section class="hero wrap">
      <div class="hero__top">
        <p class="status"><span class="dot" aria-hidden="true"></span>{T("Available for new projects", "متاح لمشاريع جديدة")}</p>
        <p class="status status--muted">{T("Remote · KSA · UAE · Europe", "عن بُعد · السعودية · الإمارات · أوروبا")}</p>
      </div>
      <div class="hero__grid">
        <div class="hero__text">
          <h1 class="display">{T("I build the systems businesses <em>run&nbsp;on.</em>", "أبني الأنظمة التي <em>تُدار بها</em> الأعمال.")}</h1>
          <p class="lede">{T("Odoo ERP developer and fullstack engineer. For four years I’ve designed, migrated and shipped ERP systems and web platforms for companies in Saudi Arabia, the UAE and Egypt — from payroll that follows Saudi Labor Law to booking sites that take live payments.",
                             "مطوّر Odoo ERP ومهندس ويب متكامل. على مدار أربع سنوات صمّمتُ وطوّرتُ وأطلقتُ أنظمة ERP ومنصّات ويب لشركات في السعودية والإمارات ومصر — من رواتب متوافقة مع نظام العمل السعودي، إلى مواقع حجز تستقبل مدفوعات حقيقية.")}</p>
          <div class="actions">
            <a class="btn btn--ink" href="{CALL}" target="_blank" rel="noopener">{T("Book a 30-min call", "احجز مكالمة ٣٠ دقيقة")}<span class="arrow" aria-hidden="true">→</span></a>
            <a class="btn btn--line" href="#work">{T("See the work", "شاهد الأعمال")}</a>
          </div>
        </div>
        <figure class="portrait">
          <div class="portrait__frame"><img src="assets/img/portrait.webp" width="900" height="803" alt="Mohammed Abdullah" fetchpriority="high"></div>
          <figcaption><span>{T("Mohammed Abdullah", "محمد عبدالله")}</span><span>{T("Cairo, Egypt", "القاهرة، مصر")}</span></figcaption>
        </figure>
      </div>

      <dl class="ledger">
        <div><dt>{T("Now", "حاليًا")}</dt><dd>{T("Odoo Developer at AZM Squad", "مطوّر Odoo في AZM Squad")}</dd></div>
        <div><dt>{T("Certified", "معتمد")}</dt><dd>{T("Odoo Certified Professional (v15)", "شهادة Odoo المعتمدة (الإصدار 15)")}</dd></div>
        <div><dt>{T("Clients in", "عملاء في")}</dt><dd>{T("Saudi Arabia · UAE · Egypt", "السعودية · الإمارات · مصر")}</dd></div>
        <div><dt>{T("Sectors", "القطاعات")}</dt><dd>{T("Government, oil &amp; gas, construction, automotive, retail, logistics, tourism, education", "الحكومة، النفط والغاز، المقاولات، السيارات، التجزئة، اللوجستيات، السياحة، التعليم")}</dd></div>
      </dl>

      <dl class="stats">
        <div><dt>4<span class="plus">+</span></dt><dd>{T("years building ERP &amp; web products", "سنوات في بناء أنظمة ERP ومنتجات ويب")}</dd></div>
        <div><dt>9</dt><dd>{T("enterprise Odoo.sh environments delivered", "بيئات Odoo.sh مؤسسية تم تسليمها")}</dd></div>
        <div><dt>63</dt><dd>{T("modules migrated v17 → v19, zero data loss", "موديول نُقلت من v17 إلى v19 دون فقدان بيانات")}</dd></div>
        <div><dt>500<span class="plus">+</span></dt><dd>{T("shipments a day through systems I built", "شحنة يوميًا عبر أنظمة من تطويري")}</dd></div>
      </dl>
    </section>

    <section class="section wrap" id="work">
      <header class="section__head">
        <p class="eyebrow">N° 01</p>
        <h2 class="title">{T("Selected work", "أبرز الأعمال")}</h2>
        <div class="filters" role="group" aria-label="Filter projects">{chips}</div>
      </header>
      <div class="cards" data-cards>{''.join(cards)}
      </div>

      <details class="archive reveal">
        <summary><span>{T("Full archive", "الأرشيف الكامل")}</span><span class="mono muted">{T(f"{len(ARCHIVE)} more modules &amp; tools", f"{len(ARCHIVE)} موديولًا وأداة إضافية".translate(AR_DIGITS))}</span><span class="archive__icon" aria-hidden="true">+</span></summary>
        <div class="table-wrap">
          <table>
            <thead><tr><th>{T("Year", "السنة")}</th><th>{T("Project", "المشروع")}</th><th>{T("Sector", "القطاع")}</th><th>{T("Type", "النوع")}</th><th>{T("Built with", "التقنيات")}</th></tr></thead>
            <tbody>{rows}
            </tbody>
          </table>
        </div>
        <p class="note">{T("Client ERPs are private, so modules are listed by sector rather than by name.", "أنظمة ERP الخاصة بالعملاء سرّية، لذلك تُذكر الموديولات حسب القطاع لا باسم العميل.")}</p>
      </details>
    </section>

    <section class="section section--ink" id="services">
      <div class="wrap">
        <header class="section__head">
          <p class="eyebrow">N° 02</p>
          <h2 class="title">{T("How I can help", "كيف أساعدك")}</h2>
          <p class="section__note">{T("Three ways to work together. Every engagement starts with a free 30-minute call.", "ثلاث طرق للعمل معًا. وكل تعاون يبدأ بمكالمة مجانية مدتها ٣٠ دقيقة.")}</p>
        </header>
        <div class="offers">
          <article class="offer reveal">
            <p class="offer__n">A</p>
            <h3>{T("Odoo implementation &amp; custom modules", "تطبيق Odoo وموديولات مخصّصة")}</h3>
            <p>{T("New modules, Saudi HR &amp; payroll, ZATCA, POS, approvals and integrations — scoped, estimated and delivered in weekly sprints.", "موديولات جديدة، موارد بشرية ورواتب سعودية، ZATCA، نقاط بيع، موافقات وتكاملات — بنطاق وتقدير واضحين وتسليم في سبرنتات أسبوعية.")}</p>
            <p class="offer__how mono">{T("Fixed-scope project", "مشروع بنطاق محدّد")}</p>
          </article>
          <article class="offer reveal">
            <p class="offer__n">B</p>
            <h3>{T("Upgrades, audits &amp; support", "الترقيات والمراجعة والدعم")}</h3>
            <p>{T("Version upgrades up to v19, performance and code audits, and an ongoing retainer for fixes and enhancements.", "ترقية الإصدارات حتى v19، مراجعة الأداء والكود، وعقد دعم شهري للإصلاحات والتحسينات.")}</p>
            <p class="offer__how mono">{T("Audit · monthly retainer", "مراجعة · عقد شهري")}</p>
          </article>
          <article class="offer reveal">
            <p class="offer__n">C</p>
            <h3>{T("Web platforms &amp; mobile apps", "منصّات ويب وتطبيقات جوال")}</h3>
            <p>{T("Arabic-first websites, booking and portal platforms, dashboards and PWAs/mobile apps — connected to your ERP when needed.", "مواقع عربية أولًا، منصّات حجز وبوابات، لوحات تحكم وتطبيقات جوال — مربوطة بنظام ERP عند الحاجة.")}</p>
            <p class="offer__how mono">{T("Fixed-scope project", "مشروع بنطاق محدّد")}</p>
          </article>
        </div>
        <ol class="process">
          <li class="reveal"><span class="mono">01</span><b>{T("Discovery call", "مكالمة تعارف")}</b><span>{T("30 minutes, free. We map the problem.", "٣٠ دقيقة مجانًا. نحدّد المشكلة.")}</span></li>
          <li class="reveal"><span class="mono">02</span><b>{T("Scope &amp; quote", "النطاق والتسعير")}</b><span>{T("A written scope and estimate within 48 hours.", "نطاق مكتوب وتقدير خلال ٤٨ ساعة.")}</span></li>
          <li class="reveal"><span class="mono">03</span><b>{T("Build in sprints", "البناء على مراحل")}</b><span>{T("Weekly demos on a staging environment.", "عرض أسبوعي على بيئة تجريبية.")}</span></li>
          <li class="reveal"><span class="mono">04</span><b>{T("Launch &amp; train", "الإطلاق والتدريب")}</b><span>{T("Go-live, user training and support.", "التشغيل الفعلي وتدريب المستخدمين والدعم.")}</span></li>
        </ol>
      </div>
    </section>

    <section class="section wrap" id="expertise">
      <header class="section__head">
        <p class="eyebrow">N° 03</p>
        <h2 class="title">{T("What I work with", "ما أعمل به")}</h2>
      </header>
      <div class="columns">
        <div class="col reveal">
          <h3 class="col__title">{T("Odoo &amp; ERP", "Odoo وأنظمة ERP")}</h3>
          <ul class="list">
            <li>{T("Custom modules — Python ORM, OWL, QWeb", "موديولات مخصّصة — Python ORM وOWL وQWeb")}</li>
            <li>{T("Version migrations, v11 through v19", "ترقية الإصدارات من v11 حتى v19")}</li>
            <li>{T("Accounting &amp; ZATCA e-invoicing, Phase 1 &amp; 2", "المحاسبة والفوترة الإلكترونية ZATCA، المرحلة ١ و٢")}</li>
            <li>{T("HR &amp; payroll for Saudi Labor Law", "الموارد البشرية والرواتب وفق نظام العمل السعودي")}</li>
            <li>{T("POS, inventory, WMS &amp; manufacturing", "نقاط البيع والمخزون والمستودعات والتصنيع")}</li>
            <li>{T("Odoo.sh staging, CI/CD &amp; automated backups", "Odoo.sh والنشر المستمر والنسخ الاحتياطي التلقائي")}</li>
          </ul>
        </div>
        <div class="col reveal">
          <h3 class="col__title">{T("Fullstack web &amp; mobile", "الويب المتكامل والجوال")}</h3>
          <ul class="list">
            <li>React · Next.js · TypeScript · Tailwind</li>
            <li>Django REST · PHP REST APIs · JWT</li>
            <li>PostgreSQL · MySQL · Supabase</li>
            <li>{T("Arabic-first RTL interfaces", "واجهات عربية أولًا بدعم RTL")}</li>
            <li>{T("PWAs and Android / iOS apps with Capacitor", "تطبيقات PWA وAndroid وiOS عبر Capacitor")}</li>
            <li>{T("Headless CMS (Sanity), performance &amp; SEO", "أنظمة محتوى Headless (Sanity)، الأداء وSEO")}</li>
          </ul>
        </div>
        <div class="col col--aside reveal">
          <h3 class="col__title">{T("Integrations", "التكاملات")}</h3>
          <p class="chips-text">ZATCA · PayTabs · Telr · Neoleap · SMSA Express · OneStock · Salla · Google Drive · OneDrive · Gemini AI</p>
          <h3 class="col__title">{T("Languages", "اللغات")}</h3>
          <p class="chips-text">{T("Arabic (native) · English (professional)", "العربية (الأم) · الإنجليزية (مهنية)")}</p>
        </div>
      </div>
    </section>

    <section class="section wrap" id="experience">
      <header class="section__head">
        <p class="eyebrow">N° 04</p>
        <h2 class="title">{T("Experience", "الخبرة")}</h2>
        <p class="section__note"><a class="u" href="{CV_REQ}" target="_blank" rel="noopener">{T("Request my full CV", "اطلب السيرة الذاتية كاملة")} ↗</a></p>
      </header>
      <ol class="timeline">
        {exp_rows()}
      </ol>
      <div class="creds reveal">
        <p><b>{T("B.Sc. Computer Science", "بكالوريوس علوم الحاسب")}</b>{T("New Cairo Academy, 2024", "أكاديمية القاهرة الجديدة، ٢٠٢٤")}</p>
        <p><b>{T("Odoo Certified Professional", "شهادة Odoo المعتمدة")}</b>{T("Functional, v15 — Odoo S.A., 2024", "وظيفية، الإصدار 15 — Odoo S.A.، ٢٠٢٤")}</p>
        <p><b>{T("Mentoring", "الإرشاد")}</b>{T("Mentored 5 junior developers; wrote the team’s Odoo 17 module standards", "إرشاد ٥ مطوّرين مبتدئين؛ وكتابة معايير موديولات Odoo 17 للفريق")}</p>
      </div>
    </section>

    <section class="contact" id="contact">
      <div class="wrap">
        <p class="eyebrow">N° 05</p>
        <h2 class="contact__title">{T("Let’s talk about <em>your</em> system.", "لنتحدث عن <em>نظامك</em>.")}</h2>
        <p class="contact__lede">{T("Tell me what you’re trying to fix or build. I reply within one working day, and my hours overlap fully with Saudi business hours.", "أخبرني بما تريد إصلاحه أو بناءه. أردّ خلال يوم عمل واحد، وساعات عملي متوافقة بالكامل مع ساعات العمل في السعودية.")}</p>
        <div class="contact__actions">
          <a class="btn btn--paper" href="{CALL}" target="_blank" rel="noopener">{T("Book a 30-min call on WhatsApp", "احجز مكالمة ٣٠ دقيقة عبر واتساب")}<span class="arrow" aria-hidden="true">→</span></a>
          <a class="btn btn--ghost" href="{MAIL}">{T("Send a project brief", "أرسل وصف المشروع")}</a>
        </div>
        <div class="contact__links">
          <button class="big-link" type="button" data-copy="{EMAIL}"><span class="big-link__label">{T("Email — click to copy", "البريد — اضغط للنسخ")}</span><span class="big-link__value" dir="ltr">{EMAIL}</span><span class="copied" aria-live="polite"></span></button>
          <a class="big-link" href="{CALL}" target="_blank" rel="noopener"><span class="big-link__label">WhatsApp</span><span class="big-link__value" dir="ltr">+20 155 446 3171</span></a>
          <a class="big-link" href="{LINKEDIN}" target="_blank" rel="noopener"><span class="big-link__label">LinkedIn</span><span class="big-link__value" dir="ltr">in/mohamed-hefzallah</span></a>
          <a class="big-link" href="{GITHUB}" target="_blank" rel="noopener"><span class="big-link__label">GitHub</span><span class="big-link__value" dir="ltr">@mhefzallah</span></a>
        </div>
      </div>
    </section>
  </main>'''
    title = "Mohammed Abdullah — Odoo ERP & Fullstack Engineer"
    desc = "Odoo ERP developer and fullstack engineer building ERP systems and web platforms for companies in Saudi Arabia, the UAE and Egypt."
    return head(title, desc, "", "") + masthead("", True) + body + footer("")


def exp_rows():
    rows = [
        (("2025 — now", "٢٠٢٥ — الآن"), ("Odoo Developer", "مطوّر Odoo"), "AZM Squad", ("Government ERP serving 1,000+ users across 10+ departments", "نظام ERP حكومي يخدم أكثر من ١٠٠٠ مستخدم في أكثر من ١٠ إدارات"), ("Saudi Arabia · remote", "السعودية · عن بُعد")),
        (("2025 — now", "٢٠٢٥ — الآن"), ("Independent ERP &amp; Fullstack Consultant", "مستشار ERP ومطوّر ويب مستقل"), ("Self-employed", "عمل حر"), ("Odoo migrations, Saudi HR &amp; payroll, delivery operations, booking platforms and learning apps", "ترقيات Odoo، موارد بشرية ورواتب سعودية، عمليات توصيل، منصّات حجز وتطبيقات تعليمية"), ("KSA · UAE · Egypt", "السعودية · الإمارات · مصر")),
        (("2022 — 2025", "٢٠٢٢ — ٢٠٢٥"), ("Odoo Developer", "مطوّر Odoo"), "Algoriza", ("10+ modules for Saudi logistics &amp; e-commerce", "أكثر من ١٠ موديولات للوجستيات والتجارة الإلكترونية في السعودية"), ("Remote", "عن بُعد")),
        (("2022", "٢٠٢٢"), ("Junior Odoo Developer", "مطوّر Odoo مبتدئ"), "Algoriza", ("5 modules shipped to production as an intern", "٥ موديولات على الإنتاج خلال فترة التدريب"), ("Remote", "عن بُعد")),
    ]
    out = []
    for when, role, org, note, where in rows:
        org_html = T(*org) if isinstance(org, tuple) else org
        out.append(f'<li class="reveal"><span class="when">{T(*when)}</span><span class="what"><b>{T(*role)}</b> {org_html}<small>{T(*note)}</small></span><span class="where">{T(*where)}</span></li>')
    return "\n        ".join(out)


# ----------------------------------------------------------------------------
# Case-study pages
# ----------------------------------------------------------------------------

def case(i, p):
    pre = "../"
    nxt = PROJECTS[i % len(PROJECTS)]
    did = "".join(f'<li class="reveal"><span class="mono">{n:02d}</span><div><h4>{T(en_h, ar_h)}</h4><p>{T(en, ar)}</p></div></li>'
                  for n, (en_h, ar_h, en, ar) in enumerate(p["did"], 1))
    decisions = ""
    if p["decisions"]:
        decisions = f'''
        <section class="block reveal">
          <h2 class="block__h">{T("Key decisions", "قرارات أساسية")}</h2>
          <ul class="decisions">{''.join(f"<li>{T(*d)}</li>" for d in p["decisions"])}</ul>
        </section>'''
    results = ""
    if p["results"]:
        results = f'''
        <section class="block reveal">
          <h2 class="block__h">{T("Results", "النتائج")}</h2>
          <dl class="results">{''.join(f'<div><dt>{v}</dt><dd>{T(en, ar)}</dd></div>' for v, en, ar in p["results"])}</dl>
        </section>'''
    gallery = ""
    if p["gallery"] or p["mobile"]:
        figs = "".join(
            f'<figure class="fig reveal"><button type="button" class="fig__btn" data-zoom aria-label="Enlarge">{img(pre, name, en)}</button>'
            f'<figcaption><span class="mono">Fig. {n}</span> {T(en, ar)}</figcaption></figure>'
            for n, (name, en, ar) in enumerate([g for g in p["gallery"] if g[0] != p.get("cover") or len(p["gallery"]) == 1], 1))
        phones = ""
        if p["mobile"]:
            phones = '<div class="phones reveal">' + "".join(
                f'<figure class="phone"><button type="button" class="fig__btn" data-zoom aria-label="Enlarge">{img(pre, m, "Mobile view")}</button></figure>'
                for m in p["mobile"]) + f'<p class="mono muted">{T("On mobile", "على الجوال")}</p></div>'
        gallery = f'''
        <section class="block">
          <h2 class="block__h reveal">{T("Gallery", "معرض الصور")}</h2>
          <div class="gallery">{figs}</div>
          {phones}
        </section>'''
    elif p.get("diagram"):
        gallery = f'''
        <section class="block reveal">
          <p class="note">{T("Screens from client ERPs are confidential, so this case study uses diagrams and numbers instead of screenshots.", "شاشات أنظمة ERP الخاصة بالعملاء سرّية، لذا تعتمد دراسة الحالة هذه على المخططات والأرقام بدل الصور.")}</p>
        </section>'''
    links = "".join(f'<a href="{u}" target="_blank" rel="noopener">{t} ↗</a>' for t, u in p["links"])
    links_row = f'<div><dt>{T("Live", "الرابط")}</dt><dd class="links">{links}</dd></div>' if links else ""

    body = f'''
  <main id="main" class="casepage">
    <div class="wrap">
      <a class="back u" href="../index.html#work">← {T("All work", "كل الأعمال")}</a>
      <header class="case-head">
        <p class="strip mono"><span>{kinds_label(p)}</span><span>{T(*p["sector"])}</span><span>{p["year"]}</span></p>
        <h1 class="case-title">{T(*p["title"])}</h1>
        <p class="case-out">{T(*p["outcome"])}</p>
      </header>
      <div class="case-hero reveal">{cover(pre, p, lazy=False)}</div>

      <div class="case-grid">
        <aside class="case-meta">
          <dl>
            <div><dt>{T("Role", "الدور")}</dt><dd>{T(*p["role"])}</dd></div>
            <div><dt>{T("Year", "السنة")}</dt><dd>{p["year"]}</dd></div>
            <div><dt>{T("Built with", "التقنيات")}</dt><dd class="mono stack">{p["stack"]}</dd></div>
            {links_row}
          </dl>
          <a class="btn btn--ink btn--block" href="{CALL}" target="_blank" rel="noopener">{T("Need something similar?", "تحتاج شيئًا مشابهًا؟")}<span class="arrow" aria-hidden="true">→</span></a>
        </aside>
        <div class="case-body">
          <section class="block reveal">
            <h2 class="block__h">{T("Context", "السياق")}</h2>
            {''.join(f'<p class="prose">{T(*c)}</p>' for c in p["context"])}
          </section>
          <section class="block">
            <h2 class="block__h reveal">{T("What I built", "ما الذي بنيته")}</h2>
            <ol class="did">{did}</ol>
          </section>
          {decisions}
          {results}
        </div>
      </div>
      {gallery}

      <a class="next reveal" href="{nxt['slug']}.html">
        <span class="mono muted">{T("Next case study", "دراسة الحالة التالية")}</span>
        <span class="next__title">{T(*nxt["title"])} <span class="arrow" aria-hidden="true">→</span></span>
      </a>
    </div>
  </main>'''
    title = f'{p["title"][0]} — Mohammed Abdullah'
    return head(title, p["outcome"][0], f'work/{p["slug"]}.html', pre) + masthead(pre, False) + body + footer(pre)


def main():
    os.makedirs(os.path.join(ROOT, "work"), exist_ok=True)
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(home())
    for i, p in enumerate(PROJECTS, 1):
        with open(os.path.join(ROOT, "work", p["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(case(i, p))
    print("built index.html +", len(PROJECTS), "case studies")


if __name__ == "__main__":
    main()
