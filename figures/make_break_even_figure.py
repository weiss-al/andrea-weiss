"""Break-even draw figure for the PWYW audio tour model.

Reproduces sensitivity table 7 of capabilities/economic-research/model.xlsx
(the rise in today's local visitors PWYW needs in order to break even), as a
line chart. Standard library only. Run:  python3 figures/make_break_even_figure.py

Outputs (next to this script): break-even-draw.svg and break-even-draw-data.csv

The formulas are the spec's closed forms (spec.md, "Analysis logic"). Inputs below
are the model's base inputs. Items marked PLACEHOLDER in the spec are not yet
backed by verified sources, so the figure is only as strong as those values.
"""
import csv
import math
import os

# --- base inputs (spec.md) ---------------------------------------------------
TOTAL_DAILY_VISITORS = 5000
LOCALS_INIT = 0.075                 # assumed (author), range 5-10%
AUDIO_PRICE = 7.0
RATE_INIT = 0.10                    # share of locals taking the tour today
RATE_PWYW = 0.20                    # PLACEHOLDER
SUGGESTED_PRICE = 7.0
PAYMENT_RATIO = 0.60                # PLACEHOLDER
FADE_TOTAL, FADE_TAU = 0.15, 30     # PLACEHOLDER
HEADSET = 1.0
CAMPAIGN_DAYS = 90
SATURATION = 10_000                 # PLACEHOLDER, marketing saturation spend
FEE_KEEP = 1.0                      # card fee is charged to the customer
SPILLOVER = 0.0                     # PLACEHOLDER

GIFT_SHOP = [1, 2.5, 5, 7.5, 10, 15]   # net spend per added local ($)
EMPHASIS = 5                           # the author's base case
MARKETING = list(range(1000, 20001, 500))

locals_base = TOTAL_DAILY_VISITORS * LOCALS_INIT
shape = (1 - (FADE_TAU / CAMPAIGN_DAYS) * (1 - math.exp(-CAMPAIGN_DAYS / FADE_TAU))) / (1 - math.exp(-CAMPAIGN_DAYS / FADE_TAU))
avg_pay = SUGGESTED_PRICE * PAYMENT_RATIO * (1 - FADE_TOTAL * shape)


def required_rise(m, g):
    aware = 1 - math.exp(-m / SATURATION)
    existing = locals_base * aware * (
        FEE_KEEP * (RATE_PWYW * avg_pay - RATE_INIT * AUDIO_PRICE)
        - HEADSET * (RATE_PWYW - RATE_INIT) + RATE_PWYW * SPILLOVER)
    per_added = RATE_PWYW * (FEE_KEEP * avg_pay - HEADSET) + g
    return (m / CAMPAIGN_DAYS - existing) / per_added / locals_base


data = {g: [required_rise(m, g) for m in MARKETING] for g in GIFT_SHOP}

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "break-even-draw-data.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["marketing_spend_usd"] + [f"rise_needed_gift_shop_{g:g}_usd" for g in GIFT_SHOP])
    for i, m in enumerate(MARKETING):
        w.writerow([m] + [f"{data[g][i]:.4f}" for g in GIFT_SHOP])

# --- chart -------------------------------------------------------------------
W, H = 960, 600
ML, MR, MT, MB = 78, 120, 116, 104
PW, PH = W - ML - MR, H - MT - MB
YMAX, XMAX = 0.50, 20000
INK, INK2, GRID, GRAY, ACCENT = "#1a1a1a", "#52514e", "#dcdcd8", "#77767a", "#2a78d6"
FONT = "Times New Roman, Times, serif"


def X(m): return ML + PW * m / XMAX
def Y(v): return MT + PH * (1 - v / YMAX)


o = []
a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
  f'aria-labelledby="t d" font-family="{FONT}">')
a('<title id="t">Rise in local visitors needed for pay-what-you-want to break even</title>')
a('<desc id="d">Line chart. The required rise in local visitors increases with marketing spend and falls as gift shop '
  'spend per added local rises. At $10,000 of marketing and $5 gift shop spend, a rise of about 5.9 percent is needed.</desc>')
a(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
a(f'<text x="{ML}" y="34" font-size="22" font-weight="bold" fill="{INK}">Rise in local visitors needed for pay-what-you-want to break even</text>')
a(f'<text x="{ML}" y="58" font-size="15" fill="{INK2}">Share of today\'s local visitors that must be added, by marketing spend and gift shop spend.</text>')
# grid + y axis
for i in range(0, 6):
    v = i * 0.10
    a(f'<line x1="{ML}" y1="{Y(v):.1f}" x2="{ML+PW}" y2="{Y(v):.1f}" stroke="{GRID if i else INK2}" stroke-width="1"/>')
    a(f'<text x="{ML-10}" y="{Y(v)+5:.1f}" font-size="14" text-anchor="end" fill="{INK2}">{v:.0%}</text>')
a(f'<text transform="translate(20,{MT+PH/2}) rotate(-90)" font-size="15" text-anchor="middle" fill="{INK2}">Rise in local visitors needed</text>')
# x axis
for m in (0, 5000, 10000, 15000, 20000):
    a(f'<line x1="{X(m):.1f}" y1="{MT+PH}" x2="{X(m):.1f}" y2="{MT+PH+5}" stroke="{INK2}"/>')
    a(f'<text x="{X(m):.1f}" y="{MT+PH+22}" font-size="14" text-anchor="middle" fill="{INK2}">${m:,}</text>')
a(f'<text x="{ML+PW/2}" y="{MT+PH+46}" font-size="15" text-anchor="middle" fill="{INK2}">Marketing spend over the 90-day campaign</text>')

# lines: gray context first, emphasized line last (on top)
order = [g for g in GIFT_SHOP if g != EMPHASIS] + [EMPHASIS]
dash = {1: "", 2.5: "", 7.5: "", 10: "", 15: ""}
label_y = {}
for g in order:
    pts = " ".join(f"{X(m):.1f},{Y(v):.1f}" for m, v in zip(MARKETING, data[g]))
    col, sw = (ACCENT, 3.5) if g == EMPHASIS else (GRAY, 2)
    a(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>')
    label_y[g] = Y(data[g][-1])
# direct labels, nudged so they never collide
ys = sorted(label_y.items(), key=lambda kv: kv[1])
pos, last = {}, -1e9
for g, y in ys:
    y = max(y, last + 18); pos[g] = y; last = y
for g in GIFT_SHOP:
    col = ACCENT if g == EMPHASIS else INK2
    wt = "bold" if g == EMPHASIS else "normal"
    a(f'<text x="{ML+PW+10}" y="{pos[g]+5:.1f}" font-size="15" font-weight="{wt}" fill="{col}">${g:g} per local</text>')
# markers + hover titles on the emphasized line's tick values
for g in GIFT_SHOP:
    for m in (5000, 10000, 15000, 20000):
        v = required_rise(m, g)
        col = ACCENT if g == EMPHASIS else GRAY
        a(f'<circle cx="{X(m):.1f}" cy="{Y(v):.1f}" r="4" fill="{col}" stroke="#ffffff" stroke-width="2">'
          f'<title>${m:,} marketing, ${g:g} gift shop spend: {v:.1%} rise in local visitors needed</title></circle>')
# guide line at the headline spend, with the two key values stated at the top
gx = X(10000)
a(f'<line x1="{gx:.1f}" y1="{MT}" x2="{gx:.1f}" y2="{MT+PH}" stroke="{INK2}" stroke-width="1" stroke-dasharray="4 4"/>')
a(f'<text x="{gx+8:.1f}" y="{MT+16}" font-size="15" fill="{INK}">At $10,000: a $5 gift shop spend needs a {required_rise(10000, EMPHASIS):.1%} rise;</text>')
a(f'<text x="{gx+8:.1f}" y="{MT+36}" font-size="15" fill="{INK}">a $1 spend needs {required_rise(10000, 1):.1%}.</text>')
# legend (line samples)
lx = ML
a(f'<text x="{lx}" y="86" font-size="14" fill="{INK2}">Gift shop net spend per added local:</text>')
x = lx + 250
for g in GIFT_SHOP:
    col, sw = (ACCENT, 3.5) if g == EMPHASIS else (GRAY, 2)
    a(f'<line x1="{x}" y1="82" x2="{x+26}" y2="82" stroke="{col}" stroke-width="{sw}"/>')
    a(f'<text x="{x+32}" y="86" font-size="14" fill="{INK2}">${g:g}</text>')
    x += 32 + 12 + 9 * len(f"{g:g}") + 14
# footnote
a(f'<text x="{ML}" y="{H-36}" font-size="12.5" fill="{INK2}">Assumes 20% of aware locals take the tour and pay ${avg_pay:.2f} on average, a $1 headset per user, and no card fee to the museum.</text>')
a(f'<text x="{ML}" y="{H-18}" font-size="12.5" fill="{INK2}">Take-up, payment ratio and marketing response are placeholder assumptions. Source: author\'s model.</text>')
a('</svg>')

with open(os.path.join(here, "break-even-draw.svg"), "w") as f:
    f.write("\n".join(o))
print("wrote break-even-draw.svg and break-even-draw-data.csv")
print("check: $10,000 / $5 ->", f"{required_rise(10000, 5):.4f}", "| $10,000 / $1 ->", f"{required_rise(10000, 1):.4f}",
      "| $20,000 / $15 ->", f"{required_rise(20000, 15):.4f}", "| avg payment", f"{avg_pay:.4f}")
