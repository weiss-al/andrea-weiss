---
type: spec
capability: economic-research
engagement: research-paper
date: 2026-10-05
status: draft            # draft | built | audited
built_with: "Claude Code (Sonnet 5.5), openpyxl, from this file; model.xlsx recalculated with the Python `formulas` engine and cross-checked against an independent Python calculation. Not yet opened in Excel."
source: "Individual Research Paper page (Kumu)"
---

# Pay What You Want Analysis Specification

## Purpose
Determine whether a pay-what-you-want (PWYW) audio tour for local visitors to a museum would be profitable. The museum is free to enter. Tourists keep paying $7 for the audio tour; locals pay what they choose. A marketing campaign draws additional local visitors, and the model weighs the new revenue (audio tour payments and gift shop spend) against the revenue lost from existing locals who stop paying $7, the added costs, and the campaign spend.

The model must answer, for a 90-day campaign: how many added local visitors per day PWYW needs to break even (the headline output), and how that requirement changes with marketing spend and gift shop spend. It also reports net profit, the gift shop spend at which the program breaks even, and the average PWYW payment at which it breaks even.

The conclusion is drawn by comparing the required draw with what a campaign of that size could plausibly achieve, so the paper does not depend on a verified estimate of how many locals marketing attracts.

## Inputs — the named contract
| Name | Value | Unit | Source |
|---|---|---|---|
| `Total_Daily_Visitors` | 5000 | people/day | Assumed |
| `Percentage_Locals_Init` | 7.5% (range 5–10%) | share of visitors | Assumed (author) |
| `Total_Daily_AudioTour` | 250 | people/day | Assumed. Includes locals who take the tour today |
| `AudioTour_Price` | 7 | $ | Given. Paid by tourists; paid by locals before PWYW. Replaces `Audio_Tour_Cost` in the earlier draft, which named a price, not a cost |
| `Local_AudioTour_Rate_Init` | 10% | share of locals | Author |
| `Local_AudioTour_Rate_PWYW` | 20% (range 10–50%) | share of locals | PLACEHOLDER. Author expects take-up to rise under PWYW; to be replaced by researched value |
| `PWYW_Suggested_Price` | 7 | $ | Recommended price shown to locals |
| `PWYW_Payment_Ratio` | 60% (test 40–80%) | average payment ÷ suggested price | PLACEHOLDER. Day-1 mean over all aware local audio-tour users, including those who pay $0 |
| `Payment_Fade_Total` | 15% | decline in average payment | PLACEHOLDER. Fall from day 1 to the last campaign day |
| `Fade_Timescale_Days` | 30 | days | PLACEHOLDER. Speed of the fade; the decline slows over time |
| `GiftShop_Net_Spend_Local` | 5 (test $0–$15, base cases $5 and $10) | $ per new local visitor | Author. Net contribution, not gross sales. Break-even value is an output |
| `GiftShop_Spillover` | 0 | $ per existing local taking the PWYW tour | PLACEHOLDER. Extra net spend by an existing local after a PWYW tour. 0 is conservative; to be researched |
| `Marketing_Spend` | variable, $0–$20,000 | $ | Given. One-time cost of the campaign |
| `Locals_Share_Ceiling` | 12.5% (test 7.5–20%) | share of visitors | PLACEHOLDER. Highest local share of daily visitors the campaign can reach. Equal to `Percentage_Locals_Init` means no draw |
| `Marketing_Saturation_Spend` | 10,000 | $ | PLACEHOLDER. Spend at which about 63% of the achievable lift is reached |
| `Campaign_Days` | 90 | days | Author (3-month campaign) |
| `Headset_Cost` | 1 | $ per audio-tour user | Given |
| `Device_Capacity` | 500 | audio-tour users/day | Given. Extra devices needed above this |
| `Device_Block_Size` | 25 | guests/day of capacity | Given |
| `Device_Block_Cost` | 5000 | $ per block | Given |
| `Device_Amort_Days` | 365 | days | Author (1-year amortization) |
| `Card_Fee_Rate` | 2.8% | share of payment | Author. Credit card processing fee on local audio-tour payments |
| `Card_Fee_Museum_Share` | 0% | share of the fee | Author. The fee is charged to the customer, so the museum bears none. Set above 0 to test otherwise |

Derived inputs:

- `Total_Daily_Tourists = Total_Daily_Visitors × (1 − Percentage_Locals_Init)`
- `Total_Daily_Locals = Total_Daily_Visitors × Percentage_Locals_Init`
- `AudioLocal_Base = Total_Daily_Locals × Local_AudioTour_Rate_Init`
- `AudioTourist_Base = Total_Daily_AudioTour − AudioLocal_Base`
- `Fee_Keep = 1 − Card_Fee_Rate × Card_Fee_Museum_Share`
- `Average_PWYW_Start = PWYW_Suggested_Price × PWYW_Payment_Ratio`
- `Fade_Multiplier`: the campaign average of the fading payment as a share of day 1 (formula below)
- `Average_PWYW = Average_PWYW_Start × Fade_Multiplier`
- `Awareness = 1 − EXP(−Marketing_Spend / Marketing_Saturation_Spend)`. This is 0 at $0 marketing and also the share of existing locals who know PWYW exists.
- `Percentage_Locals_Final = Percentage_Locals_Init + (Locals_Share_Ceiling − Percentage_Locals_Init) × Awareness`

Items marked PLACEHOLDER are not backed by verified research. Results that depend on them are not findings. Sources are identified here but are not added until verified.

## Structure
Tabs in `model.xlsx`:

- **Model:** inputs, derived inputs, a baseline vs. campaign daily view, campaign results, and checks.
- **Sensitivity:** tables 1–5 show net profit over the campaign; tables 6–8 show the break-even draw.
  1. Marketing spend × gift shop spend per new local.
  2. Campaign-average payment × local audio-tour take-up.
  3. Marketing spend × local traffic ceiling (the lowest ceiling equals the initial share: no draw).
  4. Local traffic ceiling × gift shop spend.
  5. Four paired take-up and payment scenarios, because take-up and payment move together (more people take it when it asks for less). The pairs are placeholders that illustrate the trade-off.
  6. Break-even added locals per day, by marketing spend × gift shop spend.
  7. The same break-even as a percentage rise in today's local visitors.
  8. Break-even rise in local visitors by campaign-average payment ($0–$10) × marketing spend, at the base gift shop spend. Negative values mean the program pays for itself with no added locals.

  Tables 6–8 are closed-form and do not use the Engine. They are the main figure candidates.
- **Engine:** one row per sensitivity scenario, so every table cell is traceable.
- **Lists:** dropdown values.

Factors assessed by sensitivity: average PWYW amount, increased local visitor traffic, amount invested in marketing, and average visitor gift shop spend. The sensitivity ranges for traffic and gift shop spend run down to zero on purpose, because no verified evidence supports either value.

## Analysis logic
In named notation. All quantities are for an average campaign day unless stated.

```
Fade_Shape             = (1 − (Fade_Timescale_Days / Campaign_Days) × (1 − EXP(−Campaign_Days / Fade_Timescale_Days)))
                         / (1 − EXP(−Campaign_Days / Fade_Timescale_Days))
Fade_Multiplier        = 1 − Payment_Fade_Total × Fade_Shape

Locals_Campaign        = Total_Daily_Tourists × Percentage_Locals_Final / (1 − Percentage_Locals_Final)
Added_Locals           = Locals_Campaign − Total_Daily_Locals
Locals_Unaware         = Total_Daily_Locals × (1 − Awareness)
Locals_Aware           = Locals_Campaign − Locals_Unaware       (includes all added locals)
AudioLocal_Campaign    = Locals_Unaware × Local_AudioTour_Rate_Init + Locals_Aware × Local_AudioTour_Rate_PWYW
AudioTotal_Campaign    = AudioTourist_Base + AudioLocal_Campaign

Audio_Revenue_Change   = Fee_Keep × ( Locals_Unaware × Local_AudioTour_Rate_Init × AudioTour_Price
                         + Locals_Aware × Local_AudioTour_Rate_PWYW × Average_PWYW
                         − AudioLocal_Base × AudioTour_Price )
Headset_Cost_Change    = (AudioTotal_Campaign − Total_Daily_AudioTour) × Headset_Cost
Device_Blocks          = MAX(0, ROUNDUP((AudioTotal_Campaign − Device_Capacity) / Device_Block_Size, 0))
Device_Cost_Per_Day    = Device_Blocks × Device_Block_Cost / Device_Amort_Days
GiftShop_Change        = Added_Locals × GiftShop_Net_Spend_Local
                         + Total_Daily_Locals × Awareness × Local_AudioTour_Rate_PWYW × GiftShop_Spillover

Daily_Contribution     = Audio_Revenue_Change − Headset_Cost_Change − Device_Cost_Per_Day + GiftShop_Change
Net_Profit             = Daily_Contribution × Campaign_Days − Marketing_Spend

Existing_Local_Effect  = Total_Daily_Locals × Awareness × ( Fee_Keep × (Local_AudioTour_Rate_PWYW × Average_PWYW
                           − Local_AudioTour_Rate_Init × AudioTour_Price)
                           − Headset_Cost × (Local_AudioTour_Rate_PWYW − Local_AudioTour_Rate_Init)
                           + Local_AudioTour_Rate_PWYW × GiftShop_Spillover )
Per_Added_Local        = Local_AudioTour_Rate_PWYW × (Fee_Keep × Average_PWYW − Headset_Cost) + GiftShop_Net_Spend_Local
Breakeven_Added_Locals = (Marketing_Spend / Campaign_Days − Existing_Local_Effect) / Per_Added_Local
                         (no break-even if Per_Added_Local ≤ 0)
Required_Rise          = Breakeven_Added_Locals / Total_Daily_Locals
Net_Profit_Audio_Only  = Net_Profit − GiftShop_Change × Campaign_Days
ROI                    = Net_Profit / Marketing_Spend

Breakeven_GiftShop     = GiftShop_Net_Spend_Local − Net_Profit / (Added_Locals × Campaign_Days)
Breakeven_Average_PWYW = Average_PWYW − Net_Profit / (Locals_Aware × Local_AudioTour_Rate_PWYW × Fee_Keep × Campaign_Days)
```

Concepts the model uses (author to confirm which the paper cites by name): marginal cost (the $1 headset); price discrimination between tourists and locals; cannibalization (existing locals moving from $7 to PWYW); diminishing returns to marketing; a lumpy capacity cost (device blocks); complementary spending in the gift shop; and the social obligation to pay that sets the average PWYW payment.

Each sensitivity table is a figure candidate. The paper should cite the figure the argument uses, not all of them.

## Conventions
- Model basis is the average day of the campaign, multiplied by `Campaign_Days`. The lift in local visitors is held at `Percentage_Locals_Final` for every campaign day. No ramp-up or fade.
- The model covers only the 90-day campaign, by design, to test the program's utility in isolation. Anything after day 90 is ignored.
- Locals are identified by a Hawaii ID. Checking IDs costs the museum nothing, and companions of locals do not get PWYW. No tourists get PWYW.
- Locals do not come today because the museum does not appeal to them. Marketing alone, without PWYW, would draw no additional visitors. So all added locals are attributed to PWYW together with the locally targeted campaign, and no marketing-only comparison is modeled.
- Locals may pay as little as $0. `Average_PWYW` is the mean over all aware local audio-tour users, including those who pay $0.
- The card fee (2.8%) is charged to the customer, so it is not a museum cost unless `Card_Fee_Museum_Share` is raised. It applies to local audio-tour payments only. Tourist payments are unchanged.
- Gift shop spend per local visitor is a sensitivity variable, not a point estimate. The model counts it for added locals only, because existing locals' purchases already occur. A separate `GiftShop_Spillover` (0 by default) covers any extra spend by existing locals.
- `Percentage_Locals_Final` is the local share of all visitors. Tourist numbers do not change, so added locals are in addition to the 5,000 baseline.
- Nothing changes without marketing. Locals who have not heard of PWYW (the share `1 − Awareness`) behave as they do today: `Local_AudioTour_Rate_Init` take the tour and pay $7. Locals who have heard of it, including every added local, take the tour at `Local_AudioTour_Rate_PWYW` and pay `Average_PWYW`. The lost $7 from aware existing locals is counted.
- `Average_PWYW` is the mean over all aware local audio-tour users, including those who pay $0. Each of them still costs `Headset_Cost`. The Sensitivity table of average payment includes a $0 row.
- Tourists always pay `AudioTour_Price`.
- The average payment fades over the campaign as `1 − EXP(−t / Fade_Timescale_Days)`, scaled so the total decline is reached on the last day. The model uses the campaign average. Fade applies to payments only. Take-up and visit volume do not fade.
- Take-up and payment are not independent. Sensitivity table 5 pairs them. No functional form between them is assumed.
- Gift shop spend is a net contribution. Only incremental spend is counted: all of a new local's spend, and the spillover for existing locals. Baseline gift shop sales are not modeled.
- Device cost is charged only for the campaign's share of the amortization period (`Campaign_Days / Device_Amort_Days`).
- Marketing is a one-time cost charged in full to the campaign.
- Museum admission is free, so there is no admission revenue.
- Citation style: APA with footnote citations. Page limit of four pages of body text, not counting title page, figures, bibliography, appendix. Double-spaced, 12-point Times New Roman, one-inch margins.
- Sources can be identified but should not be added before being verified.

## Validation rules
Model:
- Baseline audio-tour revenue equals `Total_Daily_AudioTour × AudioTour_Price` ($1,750).
- Baseline audio-tour users equal `AudioLocal_Base + AudioTourist_Base`.
- `Percentage_Locals_Final` is at least `Percentage_Locals_Init` and below 100%.
- Net profit at `Breakeven_GiftShop` is zero.
- The Engine base scenario equals the Model tab's net profit, and the Engine's $0-marketing scenario equals $0.
- `Fade_Multiplier` is above 0 and at most 100%.
- Daily contribution equals the existing-local effect plus added locals × the per-local contribution, when no extra devices are needed.
- Net profit at the break-even draw is zero (Engine test scenario), when no extra devices are needed.
- No error cells. Every calculated cell contains a formula.
- Hand check: at `Marketing_Spend` = 0, net profit is exactly $0 whatever the other inputs, because no local is aware of PWYW and no one is added.
- Break-even identities: net profit is zero at `Breakeven_GiftShop` and at `Breakeven_Average_PWYW`.

Paper:
- At least one labeled figure the text actually uses.
- The recommendation is defended against its strongest objection.
- No repository URL or identifying information on body pages.
- Every placeholder in the model is replaced by a verified, cited value, or the paper states that it is an assumption.

## Outputs
Model outputs, by name: `Breakeven_Added_Locals`, `Required_Rise`, the ratio of assumed to required draw, `Existing_Local_Effect`, `Net_Profit`, `ROI`, `Breakeven_GiftShop`, `Breakeven_Average_PWYW`, `Net_Profit_Audio_Only`, the gift shop share of campaign contribution, and the eight sensitivity tables.

Files: `capabilities/economic-research/model.xlsx`; the finished paper at `analysis/research-paper.pdf`; figures in `figures/` (`break-even-draw.svg` and `payment-sensitivity.svg`, each with its data table and the script that reproduces it from the spec's formulas; equivalent charts sit beside tables 7 and 8 in `model.xlsx`); the closing reflection in `prompt-log.md`.

## Audit findings
Added AFTER the paper is drafted. For each check: what you checked, what you found, what you did about it.
