# -*- coding: utf-8 -*-
"""Inline SVG diagrams for ERP case studies (themed via CSS variables)."""


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


