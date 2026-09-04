---
type: spec
capability: marginal-analysis
engagement: perfect-competition
date: 2026-08-23
status: draft            # draft | built | audited
built_with: ""           # fill in when the model is actually built
source: "Shidler README.md — 'the scenario — all assumptions in one place'; case-perfect-competition-stage2.html"
---

# Marginal Analysis — Perfect Competition (Garden) — model specification

## Purpose
Choose how many of 64 beds to plant in tomatoes, carrots, and mesclun, and how many
temporary workers to hire, to maximize season profit. The farm is a price taker:
per-bed revenue is fixed and outside its control, so the only lever is quantity, and
the only thing that makes quantity interesting is that labor hours per bed rise as
each crop is scaled up.

## Objective function
Maximize

    PROFIT = SUM_c [ PRICE_c x q_c ]
           - SUM_c [ FERT_c x q_c ]
           - LABOR_CASH_COST(N_TEMP)
           - FIXED_COSTS

This is a maximization of profit, not a minimization of marginal cost. Marginal cost
is an input to the decision rule below, never the objective.

## Decision variables
| Name | Domain | Meaning |
|---|---|---|
| `Q_TOM` | integer, 0..20 | beds planted in tomatoes |
| `Q_CAR` | integer, 0..20 | beds planted in carrots |
| `Q_MES` | integer, 0..30 | beds planted in mesclun |
| `N_TEMP` | integer, 0..4 | temporary workers hired |

`N_TEMP` is a decision, not a given. Choosing it is the second half of the marginal
analysis and it is where most of the money moves — see Conventions, "Labor costing".

## Constraints
    BEDS_USED     = Q_TOM + Q_CAR + Q_MES <= TOTAL_BEDS
    CAP_TOM       Q_TOM <= MAXBED_TOM
    CAP_CAR       Q_CAR <= MAXBED_CAR
    CAP_MES       Q_MES <= MAXBED_MES
    LABOR         LABOR_HRS_TOM(Q_TOM) + LABOR_HRS_CAR(Q_CAR) + LABOR_HRS_MES(Q_MES)
                    <= LABOR_SUPPLY(N_TEMP)
    integrality and non-negativity on all four decision variables

The per-crop caps sum to 70 against 64 beds, so `BEDS_USED` binds whenever all three
crops are attractive. Beds may be left fallow; the constraint is `<=`, not `=`.

## The perfect-competition assumption, and what it actually buys us
The farm cannot move price, so `PRICE_c` is exogenous and marginal revenue equals
price for every bed. The decision rule follows directly:

    plant bed q of crop c while  MARGINAL_CONTRIB_c(q) = PRICE_c - MC_c(q) > 0

subject to the constraints above. Where a constraint binds, the crop stops short of
`MC_c = PRICE_c` and the binding constraint carries a positive shadow price.

This gives the model its sharpest acceptance test: for any crop that ends below its
bed cap and with slack in the bed and labor constraints, `MC_c` must sit just below
`PRICE_c` at the last bed planted and above it at the next. See Validation rules.

## Inputs — the named contract
All values from the case scenario table. Nothing here is inferred.

### Scenario-wide
| Name | Value | Unit | Source |
|---|---|---|---|
| `WEEKS` | 36 | weeks per season | Case scenario, header line |
| `FIXED_COSTS` | 20000 | USD per season | Case scenario, header line |
| `TOTAL_BEDS` | 64 | beds (16 beds x 4 plots) | Case scenario, header line |
| `FARMER_SALARY` | 50000 | USD per season | Case scenario, header line |
| `FARMER_FIELD_HRS` | 720 | hours per season | Case scenario, header line |
| `TEMP_MAX` | 4 | workers | Case scenario, header line |
| `TEMP_COST` | 25000 | USD per worker per season | Case scenario, header line |
| `TEMP_HRS` | 1440 | hours per worker per season | Case scenario, header line |

`FARMER_RATE` and `TEMP_RATE` are not entered here. They are computed rates — see
Calculation logic — and are never typed in as the rounded $34.72 / $17.36 the case
displays. See Conventions, "Rates are ratios, not decimals."

### Per crop
| Name | Tomatoes | Carrots | Mesclun | Unit | Source |
|---|---|---|---|---|---|
| `MAXBED_c` | 20 | 20 | 30 | beds | Case scenario, crop table |
| `PRICE_c` | 8800 | 2094 | 2700 | USD per bed | Case scenario, crop table |
| `HRS_WK_BED_c` | 5/2 | 5/6 | 5/4 | hours per week per bed | Case scenario, crop table |
| `FERT_c` | 880 | 440 | 880 | USD per bed | Case scenario, crop table |
| `DIM_c` | 10.00% | 2.50% | 1.25% | per additional bed | Case scenario, crop table |

`PRICE_c` is revenue per bed — the case has already collapsed price per unit and yield
per bed into one figure, so yield is not separately modeled and per-bed revenue does
not decline with scale. Every nonlinearity in this model lives in labor.

`HRS_WK_BED_CAR` is entered as `5/6`, the ratio the case's displayed `0.833` rounds.
See Conventions, "Rates are ratios, not decimals" — the same rule applies to every
derived or truncated-looking figure in this contract, not only this one.

## Structure
| Sheet | Purpose |
|---|---|
| `Inputs` | The named contract above, one named range per row. No formulas. |
| `Labor` | Per crop, one row per bed 1..MAXBED_c: marginal hours, cumulative hours, marginal cost, marginal contribution. |
| `Optimize` | Decision variables, constraints, objective. The cell Solver drives. |
| `P&L` | Cash profit and loss at the chosen mix. Reconciles to `Optimize`. |
| `Checks` | Every validation rule below, one row each, pass/fail. |

## Calculation logic
In named-range notation. `c` ranges over the three crops; `q` is a bed index.

Computed rates — formulas, never re-typed as their rounded decimals:

    FARMER_RATE = FARMER_SALARY / FARMER_FIELD_HRS   ( = 50000/1440, not 34.72 )
    TEMP_RATE   = TEMP_COST / TEMP_HRS               ( = 25000/1440, not 17.36 )

Season hours for a single bed of crop c, before diminishing returns:

    SEASON_HRS_PER_BED_c = HRS_WK_BED_c x WEEKS

Diminishing returns compound on the whole crop, not incrementally per added bed: every
one of the q beds planted of crop c is charged the same `(1 + DIM_c)^q` multiplier, so
planting one more bed of a crop already at scale raises the labor bill on beds already
in the ground, not just on the new one.

    LABOR_HRS_c(q) = SEASON_HRS_PER_BED_c x q x (1 + DIM_c)^q

    MARGINAL_LABOR_HRS_c(q) = LABOR_HRS_c(q) - LABOR_HRS_c(q-1)
                             = SEASON_HRS_PER_BED_c x (1 + DIM_c)^(q-1) x (1 + q x DIM_c)

Marginal cost of the q-th bed, and its contribution:

    MC_c(q) = MARGINAL_LABOR_HRS_c(q) x MARGINAL_WAGE + FERT_c

    MARGINAL_CONTRIB_c(q) = PRICE_c - MC_c(q)

Labor supply and cash cost:

    LABOR_SUPPLY(N_TEMP)    = FARMER_FIELD_HRS + N_TEMP x TEMP_HRS
    LABOR_CASH_COST(N_TEMP) = FARMER_SALARY + N_TEMP x TEMP_COST
    LABOR_SLACK             = LABOR_SUPPLY(N_TEMP) - SUM_c LABOR_HRS_c(Q_c)

## Conventions

**Labor costing — the one that decides the answer.** The farmer's salary is paid in
full whatever is planted, so her 720 field hours are sunk within the season and carry
no marginal cost. Temporary workers are the marginal source of labor, so
`MARGINAL_WAGE = TEMP_RATE` (computed as `TEMP_COST / TEMP_HRS`, ≈ $17.36/hr — see
"Rates are ratios, not decimals" below) for the `MC_c(q)` calculation above. The
farmer's computed `FARMER_RATE` is reported for reference and is never charged against
a bed; doing so would double-count a fixed salary.

**Temps are lumpy, and this is not a rounding detail.** A temp is $25,000 for 1,440
hours, hired whole. Labor cash cost is therefore a step function, and within a step the
cash cost of one more hour is zero while the cash cost of the hour that forces a new
hire is $25,000. Pricing marginal labor at the smooth `TEMP_RATE` is a modeling
convenience that is correct for ranking beds and wrong for the hiring decision. The
model must therefore solve over `N_TEMP` explicitly — evaluate the optimal bed mix at
each `N_TEMP` in 0..4 and take the best profit — rather than optimizing beds at a fixed
wage and reading off the temp count afterwards. A scoping check while writing this spec,
run against the labor formula below, confirmed the sweep is not busywork: profit peaks
at `N_TEMP = 3` (beds 10/19/28, profit ≈ $16,586), and hiring a fourth temp *reduces*
profit to ≈ $12,720 — a swing of roughly $3,866 — while also changing the bed mix. A
model that assumes four temps and optimizes beds against a flat wage gets both the
hiring call and the mix wrong.

**Diminishing returns compound on the whole crop, not incrementally per bed.** This
reverses what an earlier draft of this spec specified, on direct evidence, and the
correction matters enough to record why. That draft read `DIM_c` as "each additional
bed needs `DIM_c` more hours than the previous bed" and used it to justify the reading
on the grounds that tomatoes then stopped at 18 beds — matching the engagement brief's
hypothesis — with total labor demand landing 16 hours over supply. Checked directly
against the case's own labor formula, `LABOR_HRS_c(q) = SEASON_HRS_PER_BED_c x q x
(1 + DIM_c)^q`, neither fact holds: under that formula tomatoes stop at 10 beds on an
unconstrained `MC = PRICE` test, not 18, and a mix of 18/20/30 needs about 11,950 labor
hours, nearly double the supply, not 16 hours over it. The per-bed reading's supporting
arithmetic belonged to the per-bed formula alone; it was not independent evidence, and
should not have been read as corroboration. The case's formula is adopted instead on a
harder test: at `q = 10` tomato beds it gives 2,334.37 hours, matching the published
check figure exactly, where the per-bed series gives 1,434.37 — a difference too large
to be rounding, and the check figure is the authority here, not the more natural-sounding
English reading. **Recommendation: build the model on `LABOR_HRS_c(q) = SEASON_HRS_PER_BED_c
x q x (1 + DIM_c)^q`**, per Calculation logic above, and treat this paragraph, not the
one it replaces, as the citable rationale.

**Costing order.** Fertilizer is a pure per-bed variable cost, charged in full to every
bed planted. `FIXED_COSTS` and `FARMER_SALARY` are period costs, subtracted once at the
bottom of the P&L and never allocated to a crop or a bed. No crop is charged a share of
overhead, so per-crop figures are contributions, not profits, and must be labeled as
such.

**Rates are ratios, not decimals.** Every figure the case displays as a rounded decimal
is entered as the ratio it comes from, computed by formula: `HRS_WK_BED_CAR = 5/6`
(never `0.833`), `FARMER_RATE = FARMER_SALARY / FARMER_FIELD_HRS` (never `34.72`),
`TEMP_RATE = TEMP_COST / TEMP_HRS` (never `17.36`). A rounded literal entered instead of
the ratio is a bug, not a simplification — a sibling workbook in this cohort stored the
rounded rates directly and came out $13.16 high on a $42,762 profit; its own check row
caught the drift, and the fix was exactly this rule. No intermediate rounding anywhere
in the workbook: rounding happens at presentation only, to whole dollars and one decimal
place on hours.

**Boundaries.** Bed counts are whole beds; partial beds do not exist. Beds may be left
fallow. `N_TEMP` is whole workers, capped at 4. A crop may be planted in zero beds.

## Validation rules
The finished model must satisfy all of these, each as a visible pass/fail row on
`Checks`.

1. `BEDS_USED <= 64` and each `Q_c <= MAXBED_c`.
2. `LABOR_SLACK >= 0` at the chosen `N_TEMP`.
3. `LABOR_SLACK < TEMP_HRS` — otherwise a temp is being paid for nothing and `N_TEMP`
   is not optimal.
4. **Price-taker test.** For any crop that ends strictly below its cap while both
   `BEDS_USED < 64` and `LABOR_SLACK > 0`, `MC_c(Q_c) < PRICE_c <= MC_c(Q_c + 1)`.
   A crop that fails this and is not at a binding constraint is mis-solved.
5. **Constraint attribution.** Every crop stopped below its cap is traceable to a named
   binding constraint. No crop stops for an unexplained reason.
6. **Hand calculation.** Tomatoes at `q = 10`: `LABOR_HRS_TOM(10) = 2,334.37` hours,
   `MARGINAL_LABOR_HRS_TOM(10) = 424.43` hours, `MC_TOM(10) ≈ 8,248.59`. Computed by hand
   off the spec, this and two other bed counts must match the model to the dollar.
7. **Cash reconciliation.** `PROFIT` on `Optimize` equals `PROFIT` on the `P&L` sheet
   built from actual cash outlays (`FIXED_COSTS` + `FARMER_SALARY` + `N_TEMP` x
   `TEMP_COST` + fertilizer). This is the check that catches the smooth-wage error
   described in Conventions.
8. **Hiring sweep.** Profit is evaluated at every `N_TEMP` in 0..4 and the reported
   answer is the maximum. The full sweep is visible, not just the winner.
9. Every calculated cell contains a formula. No hardcoded numbers outside `Inputs`.
10. No error values anywhere in the workbook.

## Outputs
| Name | Meaning |
|---|---|
| `Q_TOM`, `Q_CAR`, `Q_MES` | Beds planted per crop |
| `N_TEMP` | Temporary workers hired |
| `BEDS_FALLOW` | `TOTAL_BEDS - BEDS_USED` |
| `LABOR_HRS_USED`, `LABOR_SLACK` | Hours consumed and idle |
| `REVENUE`, `FERT_COST`, `LABOR_CASH_COST`, `FIXED_COSTS` | P&L lines |
| `PROFIT` | Season profit |
| `MC_c` at last bed, `MARGINAL_CONTRIB_c` at last bed | Per crop, for the price-taker test |
| `BINDING_c` | Which constraint stopped each crop |
| `PROFIT_BY_NTEMP` | Profit at each `N_TEMP` in 0..4 — the hiring sweep |
| `BED_SHADOW_PRICE` | Contribution gained from one more bed, when beds bind |

## Open decisions
None blocking. `MARGINAL_WAGE` is `TEMP_RATE`, computed as a ratio, with the farmer's
hours sunk; `DIM_c` compounds on the whole crop via `LABOR_HRS_c(q) = SEASON_HRS_PER_BED_c
x q x (1 + DIM_c)^q`; and every rate the case displays rounded is entered as its exact
ratio. All three were revised from an earlier draft after being checked against the
case's own numbers — see Conventions.

## Audit findings
Added AFTER the build. For each check: what you checked, what you found, what you did
about it.
