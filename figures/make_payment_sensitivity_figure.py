"""Break-even draw vs. average PWYW payment, at a $5 gift shop spend per added local.

Reproduces sensitivity table 8 of capabilities/economic-research/model.xlsx on a
finer payment grid. Standard library only. Run:
    python3 figures/make_payment_sensitivity_figure.py

Outputs (next to this script): payment-sensitivity.svg and payment-sensitivity-data.csv

Formulas are the spec's closed forms (spec.md, "Analysis logic"). Inputs are the
model's base inputs; items marked PLACEHOLDER are not yet backed by verified sources.
"""
import csv
import math
import os

TOTAL_DAILY_VISITORS = 5000
LOCALS_INIT = 0.075
AUDIO_PRICE = 7.0
RATE_INIT = 0.10
RATE_PWYW = 0.20                    # PLACEHOLDER
HEADSET = 1.0
CAMPAIGN_DAYS = 90
SATURATION = 10_000                 # PLACEHOLDER
FEE_KEEP = 1.0
SPILLOVER = 0.0                     # PLACEHOLDER
GIFT_SHOP = 5.0                     # the author's base case
BASE_AVG_PAY = 3.747                # model's campaign-average payment (60% ratio, fade) - PLACEHOLDER

MARKETING = [5000, 10000, 15000, 20000]
EMPHASIS = 10000                    # the model's base marketing spend
PAYMENTS = [i * 0.25 for i in range(0, 41)]   # $0 to $10

locals_base = TOTAL_DAILY_VISITORS * LOCALS_INIT


def parts(m):
    aware = 1 - math.exp(-m / SATURATION)
    return locals_base * aware


def required_rise(m, p):
    la = parts(m)
    existing = la * (FEE_KEEP * (RATE_PWYW * p - RATE_INIT * AUDIO_PRICE)
                     - HEADSET * (RATE_PWYW - RATE_INIT) + RATE_PWYW * SPILLOVER)
    per_added = RATE_PWYW * (FEE_KEEP * p - HEADSET) + GIFT_SHOP
    return (m / CAMPAIGN_DAYS - existing) / per_added / locals_base


def zero_crossing(m):
    """Payment at which no added locals are needed (existing-local effect covers marketing)."""
    la = parts(m)
    k = m / CAMPAIGN_DAYS / la
    return (k + FEE_KEEP * RATE_INIT * AUDIO_PRICE + HEADSET * (RATE_PWYW - RATE_INIT) - RATE_PWYW * SPILLOVER) / (FEE_KEEP * RATE_PWYW)


here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "payment-sensitivity-data.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["avg_payment_usd"] + [f"rise_needed_marketing_{m}_usd" for m in MARKETING])
    for p in PAYMENTS:
        w.writerow([f"{p:.2f}"] + [f"{required_rise(m, p):.4f}" for m in MARKETING])

# --- chart -------------------------------------------------------------------
W, H = 960, 600
ML, MR, MT, MB = 78, 40, 116, 104
PW, PH = W - ML - MR, H - MT - MB
YMAX, XMAX = 0.32, 10.0
INK, INK2, GRID, GRAY, ACCENT = "#1a1a1a", "#52514e", "#dcdcd8", "#77767a", "#2a78d6"
FONT = "Times New Roman, Times, serif"


def X(p): return ML + PW * p / XMAX
def Y(v): return MT + PH * (1 - v / YMAX)


o = []
a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d" font-family="{FONT}">')
a('<title id="t">Rise in local visitors needed to break even, by average pay-what-you-want payment</title>')
a('<desc id="d">Line chart at a $5 gift shop spend per added local. The required rise in local visitors falls as the average '
  'payment rises, and reaches zero between about $6 and $7.50 depending on marketing spend.</desc>')
a(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
a(f'<text x="{ML}" y="34" font-size="22" font-weight="bold" fill="{INK}">Higher average payments sharply cut the local draw PWYW needs</text>')
a(f'<text x="{ML}" y="58" font-size="15" fill="{INK2}">Rise in today\'s local visitors needed to break even, by average PWYW payment, at a $5 gift shop spend per added local.</text>')
# legend
a(f'<text x="{ML}" y="86" font-size="14" fill="{INK2}">Marketing spend:</text>')
x = ML + 128
for m in MARKETING:
    col, sw = (ACCENT, 3.5) if m == EMPHASIS else (GRAY, 2)
    a(f'<line x1="{x}" y1="82" x2="{x+26}" y2="82" stroke="{col}" stroke-width="{sw}"/>')
    a(f'<text x="{x+32}" y="86" font-size="14" fill="{INK2}">${m:,}</text>')
    x += 32 + 9 * len(f"${m:,}") + 22
# grid + axes
for i in range(0, 7):
    v = i * 0.05
    a(f'<line x1="{ML}" y1="{Y(v):.1f}" x2="{ML+PW}" y2="{Y(v):.1f}" stroke="{GRID if i else INK2}" stroke-width="1"/>')
    a(f'<text x="{ML-10}" y="{Y(v)+5:.1f}" font-size="14" text-anchor="end" fill="{INK2}">{v:.0%}</text>')
a(f'<text transform="translate(20,{MT+PH/2}) rotate(-90)" font-size="15" text-anchor="middle" fill="{INK2}">Rise in local visitors needed</text>')
for p in range(0, 11, 2):
    a(f'<line x1="{X(p):.1f}" y1="{MT+PH}" x2="{X(p):.1f}" y2="{MT+PH+5}" stroke="{INK2}"/>')
    a(f'<text x="{X(p):.1f}" y="{MT+PH+22}" font-size="14" text-anchor="middle" fill="{INK2}">${p}</text>')
a(f'<text x="{ML+PW/2}" y="{MT+PH+46}" font-size="15" text-anchor="middle" fill="{INK2}">Average payment per aware local audio-tour user (campaign average)</text>')

# reference guides: model base payment and today's price
for p, text, anchor, dx in ((BASE_AVG_PAY, "Model base payment $3.75 (placeholder)", "end", -8), (AUDIO_PRICE, "Today's price $7", "start", 8)):
    a(f'<line x1="{X(p):.1f}" y1="{MT}" x2="{X(p):.1f}" y2="{MT+PH}" stroke="{INK2}" stroke-width="1" stroke-dasharray="4 4"/>')
    a(f'<text x="{X(p)+dx:.1f}" y="{MT+16}" font-size="14" text-anchor="{anchor}" fill="{INK}">{text}</text>')

# lines (stop at the zero crossing), gray first, emphasis last
order = [m for m in MARKETING if m != EMPHASIS] + [EMPHASIS]
for m in order:
    z = zero_crossing(m)
    pts = [(p, required_rise(m, p)) for p in PAYMENTS if p < z]
    pts.append((z, 0.0))
    col, sw = (ACCENT, 3.5) if m == EMPHASIS else (GRAY, 2)
    a(f'<polyline points="{" ".join(f"{X(p):.1f},{Y(v):.1f}" for p, v in pts)}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>')
    a(f'<circle cx="{X(z):.1f}" cy="{Y(0):.1f}" r="6" fill="#ffffff" stroke="{col}" stroke-width="2.5">'
      f'<title>${m:,} marketing: no added locals needed once the average payment reaches ${z:.2f}</title></circle>')
    # direct label at the left end, above the line
    v0 = required_rise(m, 0.0)
    colt = ACCENT if m == EMPHASIS else INK2
    wt = "bold" if m == EMPHASIS else "normal"
    a(f'<text x="{X(0.15):.1f}" y="{Y(v0)-10:.1f}" font-size="14" font-weight="{wt}" fill="{colt}">${m:,}</text>')
    # hover points
    for p in (0, 2, 4, 6):
        v = required_rise(m, p)
        if v >= 0:
            a(f'<circle cx="{X(p):.1f}" cy="{Y(v):.1f}" r="4" fill="{col}" stroke="#ffffff" stroke-width="2">'
              f'<title>${m:,} marketing, ${p} average payment: {v:.1%} rise needed</title></circle>')
# annotation for the rings
a(f'<text x="{X(7.7):.1f}" y="{Y(0.085):.1f}" font-size="14" fill="{INK}">Open circle: past this payment,</text>')
a(f'<text x="{X(7.7):.1f}" y="{Y(0.085)+18:.1f}" font-size="14" fill="{INK}">PWYW pays for itself with no</text>')
a(f'<text x="{X(7.7):.1f}" y="{Y(0.085)+36:.1f}" font-size="14" fill="{INK}">added locals at all.</text>')
# footnote
a(f'<text x="{ML}" y="{H-36}" font-size="12.5" fill="{INK2}">Assumes 20% of aware locals take the tour, a $1 headset per user, no card fee to the museum, and a $5 net gift shop spend per added local only.</text>')
a(f'<text x="{ML}" y="{H-18}" font-size="12.5" fill="{INK2}">Take-up and marketing response are placeholder assumptions. Payments above $7 mean locals pay more than today\'s price. Source: author\'s model.</text>')
a('</svg>')

with open(os.path.join(here, "payment-sensitivity.svg"), "w") as f:
    f.write("\n".join(o))
print("wrote payment-sensitivity.svg and payment-sensitivity-data.csv")
for m in MARKETING:
    print(f"${m:,}: $0 -> {required_rise(m, 0):.4f}, $3.75 -> {required_rise(m, 3.75):.4f}, zero at ${zero_crossing(m):.2f}")
