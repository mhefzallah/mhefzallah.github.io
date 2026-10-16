# -*- coding: utf-8 -*-
"""Build the static portfolio: index.html + work/<slug>.html.

Design: "Vision 2030" — emerald + gold, Alexandria headings, IBM Plex Sans Arabic text.
Run:  python3 tools/build.py
"""
import os
from html import escape
from urllib.parse import quote

from content import SITE, EMAIL, WHATSAPP, LINKEDIN, GITHUB, PROJECTS, ARCHIVE
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
    ("17", "Odoo client projects in the last 21 months", "مشروع Odoo لعملاء خلال آخر ٢١ شهرًا"),
    ("1,900+", "commits across 347 working days", "commit على مدار ٣٤٧ يوم عمل"),
    ("120+", "modules delivered — built or integrated", "موديول تم تسليمه — تطويرًا أو تكاملًا"),
    ("11 → 19", "every Odoo version from 11 to 19", "كل إصدارات Odoo من ١١ إلى ١٩"),
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


def masthead(prefix, home):
    h = "" if home else prefix + "index.html"
    return f'''
<body>
  <a class="skip" href="#main">{T("Skip to content", "انتقل إلى المحتوى")}</a>
  <header class="masthead">
    <div class="wrap masthead__row">
      <a class="brand" href="{prefix}index.html" aria-label="Mohammed Hefzallah — home">
        <span class="brand__mark" aria-hidden="true">M<b>H</b></span>
        <span class="brand__text"><strong>{T("Mohammed Hefzallah", "محمد حفظ الله")}</strong><small>{T("Odoo ERP · Fullstack", "Odoo ERP · ويب متكامل")}</small></span>
      </a>
      <nav class="nav" aria-label="Main">
        <a href="{h}#work">{T("Work", "الأعمال")}</a>
        <a href="{h}#services">{T("Services", "الخدمات")}</a>
        <a href="{h}#experience">{T("Experience", "الخبرة")}</a>
        <a href="{h}#contact">{T("Contact", "تواصل")}</a>
      </nav>
      <div class="tools">
        <button class="lang" type="button" data-lang-toggle aria-label="Switch language">{T("العربية", "English")}</button>
        <a class="btn btn--gold btn--sm" href="{CALL}" target="_blank" rel="noopener">{T("Book a call", "احجز مكالمة")}</a>
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

def home():
    pre = ""
    counts = {k: sum(k in p["kinds"] for p in PROJECTS) for k in KIND_LABEL}
    filters = [("all", ("All", "الكل"), len(PROJECTS))] + [(k, KIND_LABEL[k], counts[k]) for k in ("erp", "web", "mobile")]
    chips = "".join(
        f'<button type="button" class="chip{" is-on" if k == "all" else ""}" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{T(*lab)} <sup>{n}</sup></button>'
        for k, lab, n in filters)

    cards = "".join(f'''
        <article class="card{" card--wide" if i == 1 else ""} reveal" data-kinds="{" ".join(p["kinds"])}">
          <a class="card__link" href="work/{p["slug"]}.html">
            {cover(pre, p)}
            <div class="card__body">
              <div class="card__tags">{kinds_label(p)}<span class="card__year">{p["year"]}</span></div>
              <h3 class="card__title">{T(*p["title"])}</h3>
              <p class="card__out">{T(*p["outcome"])}</p>
              <span class="card__more">{T("View case study", "عرض دراسة الحالة")} {ICON["arrow"]}</span>
            </div>
          </a>
        </article>''' for i, p in enumerate(PROJECTS, 1))

    rows = "".join(f'''
            <tr data-kinds="{'erp' if t == 'Odoo' else 'web'}"><td class="num">{y}</td><td><b>{T(*name)}</b></td><td>{T(*sector)}</td><td><span class="tag tag--soft">{t}</span></td><td class="muted" dir="ltr">{stack}</td></tr>'''
                   for y, t, name, sector, stack in ARCHIVE)

    stats = "".join(f'<div class="stat reveal"><dt dir="ltr">{v}</dt><dd>{T(en, ar)}</dd></div>' for v, en, ar in STATS)

    exp = exp_rows()

    body = f'''
  <main id="main">
    <section class="hero">
      <div class="wrap hero__grid">
        <div class="hero__text">
          <p class="badge"><span class="dot" aria-hidden="true"></span>{T("Available for new projects", "متاح لمشاريع جديدة")}</p>
          <h1 class="display">{T("I build the systems businesses <em>run on.</em>", "أبني الأنظمة التي <em>تُدار بها</em> الأعمال.")}</h1>
          <p class="lede">{T("Odoo ERP developer and fullstack engineer for companies in Saudi Arabia, the UAE and Egypt — from payroll that follows Saudi Labor Law and ZATCA e-invoicing to web platforms that take live payments.",
                             "مطوّر أنظمة Odoo ERP ومهندس ويب متكامل لشركات في السعودية والإمارات ومصر — من رواتب متوافقة مع نظام العمل السعودي وفوترة ZATCA، إلى منصّات ويب تستقبل مدفوعات حقيقية.")}</p>
          <div class="actions">
            <a class="btn btn--primary" href="{CALL}" target="_blank" rel="noopener">{T("Book a 30-min call", "احجز مكالمة ٣٠ دقيقة")} {ICON["arrow"]}</a>
            <a class="btn btn--outline" href="#work">{T("View my work", "شاهد أعمالي")}</a>
          </div>
          <ul class="hero__points">
            <li>{ICON["check"]}{T("Odoo Certified Professional", "معتمد من Odoo")}</li>
            <li>{ICON["check"]}{T("Odoo 11 → 19, Community &amp; Enterprise", "Odoo من ١١ إلى ١٩، Community وEnterprise")}</li>
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
            <span>{T("Odoo Developer at AZM Squad", "مطوّر Odoo في AZM Squad")}</span>
          </figcaption>
          <div class="portrait__float" aria-hidden="true"><b dir="ltr">63</b><span>{T("modules moved to v19, zero data loss", "موديول تمت ترقيتها لـ v19 دون فقدان بيانات")}</span></div>
        </figure>
      </div>
      <div class="wrap">
        <dl class="stats">{stats}</dl>
      </div>
    </section>

    <section class="strip" aria-label="Sectors and integrations">
      <div class="wrap strip__row">
        <p class="strip__label">{T("Sectors I’ve worked in", "قطاعات عملت فيها")}</p>
        <ul class="strip__list">
          <li>{T("Government", "الحكومة")}</li><li>{T("Oil &amp; Gas", "النفط والغاز")}</li><li>{T("Construction", "المقاولات")}</li>
          <li>{T("Automotive", "السيارات")}</li><li>{T("Retail &amp; POS", "التجزئة")}</li><li>{T("Logistics", "اللوجستيات")}</li>
          <li>{T("Tourism", "السياحة")}</li><li>{T("Education", "التعليم")}</li><li>{T("Consulting", "الاستشارات")}</li>
        </ul>
      </div>
    </section>

    <section class="section" id="work">
      <div class="wrap">
        {section_head("01", "Selected work", "أبرز الأعمال", ("Case studies from ERP and web projects — with screenshots, decisions and results.", "دراسات حالة من مشاريع ERP والويب — بالصور والقرارات والنتائج."), f'<div class="filters" role="group" aria-label="Filter">{chips}</div>')}
        <div class="cards">{cards}
        </div>
        <details class="archive reveal">
          <summary><span>{T("More modules &amp; tools", "موديولات وأدوات إضافية")}</span><span class="archive__count" dir="ltr">{len(ARCHIVE)}</span><span class="archive__icon" aria-hidden="true">+</span></summary>
          <div class="table-wrap">
            <table>
              <thead><tr><th>{T("Year", "السنة")}</th><th>{T("Module", "الموديول")}</th><th>{T("Sector", "القطاع")}</th><th>{T("Type", "النوع")}</th><th>{T("Built with", "التقنيات")}</th></tr></thead>
              <tbody>{rows}
              </tbody>
            </table>
          </div>
          <p class="note">{T("Client ERPs are private, so modules are listed by sector rather than by client name.", "أنظمة العملاء سرّية، لذلك تُذكر الموديولات حسب القطاع لا باسم العميل.")}</p>
        </details>
      </div>
    </section>

    <section class="section section--dark" id="services">
      {PATTERN}
      <div class="wrap">
        {section_head("02", "How I can help", "كيف أساعدك", ("Every engagement starts with a free 30-minute call.", "كل تعاون يبدأ بمكالمة مجانية مدتها ٣٠ دقيقة."))}
        <div class="services">
          <article class="service reveal">
            <span class="service__icon">{ICON["erp"]}</span>
            <h3>{T("Odoo implementation &amp; custom modules", "تطبيق Odoo وموديولات مخصّصة")}</h3>
            <p>{T("Saudi HR &amp; payroll, ZATCA e-invoicing, POS, approvals, inventory and integrations — scoped, estimated and delivered in weekly sprints.", "الموارد البشرية والرواتب السعودية، فوترة ZATCA، نقاط البيع، الموافقات، المخزون والتكاملات — بنطاق وتقدير واضحين وتسليم في سبرنتات أسبوعية.")}</p>
            <span class="service__how">{T("Fixed-scope project", "مشروع بنطاق محدّد")}</span>
          </article>
          <article class="service reveal">
            <span class="service__icon">{ICON["upgrade"]}</span>
            <h3>{T("Upgrades, audits &amp; support", "الترقيات والمراجعة والدعم")}</h3>
            <p>{T("Version upgrades up to Odoo 19, performance and code audits, and a monthly retainer for fixes and enhancements.", "ترقية الإصدارات حتى Odoo 19، مراجعة الأداء والكود، وعقد دعم شهري للإصلاحات والتحسينات.")}</p>
            <span class="service__how">{T("Audit · monthly retainer", "مراجعة · عقد شهري")}</span>
          </article>
          <article class="service reveal">
            <span class="service__icon">{ICON["web"]}</span>
            <h3>{T("Web platforms &amp; mobile apps", "منصّات ويب وتطبيقات جوال")}</h3>
            <p>{T("Arabic-first websites, booking and customer portals, dashboards and mobile apps — connected to your ERP when needed.", "مواقع عربية أولًا، منصّات حجز وبوابات عملاء، لوحات تحكم وتطبيقات جوال — مربوطة بنظام ERP عند الحاجة.")}</p>
            <span class="service__how">{T("Fixed-scope project", "مشروع بنطاق محدّد")}</span>
          </article>
        </div>
        <ol class="process">
          <li class="reveal"><span class="process__n" dir="ltr">01</span><b>{T("Discovery call", "مكالمة تعارف")}</b><span>{T("30 minutes, free.", "٣٠ دقيقة مجانًا.")}</span></li>
          <li class="reveal"><span class="process__n" dir="ltr">02</span><b>{T("Scope &amp; quote", "النطاق والتسعير")}</b><span>{T("Written scope within 48 hours.", "نطاق مكتوب خلال ٤٨ ساعة.")}</span></li>
          <li class="reveal"><span class="process__n" dir="ltr">03</span><b>{T("Build in sprints", "التنفيذ على مراحل")}</b><span>{T("Weekly demos on staging.", "عرض أسبوعي على بيئة تجريبية.")}</span></li>
          <li class="reveal"><span class="process__n" dir="ltr">04</span><b>{T("Launch &amp; train", "الإطلاق والتدريب")}</b><span>{T("Go-live, training and support.", "التشغيل والتدريب والدعم.")}</span></li>
        </ol>
      </div>
    </section>

    <section class="section" id="expertise">
      <div class="wrap">
        {section_head("03", "What I work with", "ما أعمل به")}
        <div class="skills">
          <div class="skill reveal">
            <h3>{T("Odoo &amp; ERP", "Odoo وأنظمة ERP")}</h3>
            <ul class="pills">
              <li>Odoo 11 – 19</li><li>Python ORM</li><li>OWL</li><li>QWeb</li><li>PostgreSQL</li><li>Odoo.sh</li>
              <li>{T("Accounting", "المحاسبة")}</li><li>ZATCA</li><li>{T("HR &amp; Payroll", "الموارد البشرية والرواتب")}</li><li>POS</li><li>{T("Inventory &amp; WMS", "المخزون والمستودعات")}</li><li>{T("Approvals", "الموافقات")}</li><li>{T("Migrations", "الترقيات")}</li>
            </ul>
          </div>
          <div class="skill reveal">
            <h3>{T("Web &amp; mobile", "الويب والجوال")}</h3>
            <ul class="pills">
              <li>React</li><li>Next.js</li><li>TypeScript</li><li>JavaScript</li><li>Tailwind CSS</li><li>Django REST</li><li>PHP</li>
              <li>MySQL</li><li>Supabase</li><li>REST APIs</li><li>JWT</li><li>PWA</li><li>Capacitor</li><li>{T("Arabic RTL", "واجهات RTL")}</li>
            </ul>
          </div>
          <div class="skill reveal">
            <h3>{T("Integrations", "التكاملات")}</h3>
            <ul class="pills">
              <li>ZATCA</li><li>PayTabs</li><li>Telr</li><li>Neoleap</li><li>SMSA Express</li><li>OneStock</li><li>Salla</li><li>Google Drive</li><li>OneDrive</li><li>Gemini AI</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--soft" id="experience">
      <div class="wrap">
        {section_head("04", "Experience", "الخبرة", None, f'<a class="btn btn--outline btn--sm" href="{CV_REQ}" target="_blank" rel="noopener">{T("Request full CV", "اطلب السيرة الذاتية")}</a>')}
        <ol class="timeline">{exp}</ol>
        <div class="creds">
          <div class="cred reveal"><span class="cred__icon">{ICON["check"]}</span><b>{T("B.Sc. Computer Science", "بكالوريوس علوم الحاسب")}</b><span>{T("New Cairo Academy · 2024", "أكاديمية القاهرة الجديدة · ٢٠٢٤")}</span></div>
          <div class="cred reveal"><span class="cred__icon">{ICON["check"]}</span><b>{T("Odoo Certified Professional", "شهادة Odoo المعتمدة")}</b><span>{T("Functional v15 · Odoo S.A. · 2024", "وظيفية الإصدار 15 · Odoo S.A. · ٢٠٢٤")}</span></div>
          <div class="cred reveal"><span class="cred__icon">{ICON["check"]}</span><b>{T("Languages", "اللغات")}</b><span>{T("Arabic (native) · English (professional)", "العربية (الأم) · الإنجليزية (مهنية)")}</span></div>
        </div>
      </div>
    </section>
  </main>'''
    title = "Mohammed Hefzallah — Odoo ERP & Fullstack Engineer"
    desc = "Odoo ERP developer and fullstack engineer building ERP systems and web platforms for companies in Saudi Arabia, the UAE and Egypt."
    return head(title, desc, "", "") + masthead("", True) + body + footer("")


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
    return head(title, p["outcome"][0], f'work/{p["slug"]}.html', pre, og=f'assets/og/{p["slug"]}.jpg') + masthead(pre, False) + body + footer(pre)


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
