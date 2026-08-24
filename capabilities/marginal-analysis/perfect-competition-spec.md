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
| `FARMER_RATE` | 34.72 | USD per hour | Case scenario, header line (implied) |
| `TEMP_MAX` | 4 | workers | Case scenario, header line |
| `TEMP_COST` | 25000 | USD per worker per season | Case scenario, header line |
| `TEMP_HRS` | 1440 | hours per worker per season | Case scenario, header line |
| `TEMP_RATE` | 17.36 | USD per hour | Case scenario, header line (implied) |

### Per crop
| Name | Tomatoes | Carrots | Mesclun | Unit | Source |
|---|---|---|---|---|---|
| `MAXBED_c` | 20 | 20 | 30 | beds | Case scenario, crop table |
| `PRICE_c` | 8800 | 2094 | 2700 | USD per bed | Case scenario, crop table |
| `HRS_WK_BED_c` | 2.50 | 0.833 | 1.25 | hours per week per bed | Case scenario, crop table |
| `FERT_c` | 880 | 440 | 880 | USD per bed | Case scenario, crop table |
| `DIM_c` | 10.00% | 2.50% | 1.25% | per additional bed | Case scenario, crop table |

`PRICE_c` is revenue per bed — the case has already collapsed price per unit and yield
per bed into one figure, so yield is not separately modeled and per-bed revenue does
not decline with scale. Every nonlinearity in this model lives in labor.

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

Season hours for a single bed of crop c, before diminishing returns:

    SEASON_HRS_PER_BED_c = HRS_WK_BED_c x WEEKS

Diminishing returns compound per bed: the q-th bed of a crop needs `DIM_c` more hours
than the (q-1)-th.

    MARGINAL_LABOR_HRS_c(q) = SEASON_HRS_PER_BED_c x (1 + DIM_c)^(q-1)

    LABOR_HRS_c(q) = SEASON_HRS_PER_BED_c x ((1 + DIM_c)^q - 1) / DIM_c

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
`MARGINAL_WAGE = TEMP_RATE` ($17.36/hr) for the `MC_c(q)` calculation above. The
farmer's implied `FARMER_RATE` is reported for reference and is never charged against
a bed; doing so would double-count a fixed salary.

**Temps are lumpy, and this is not a rounding detail.** A temp is $25,000 for 1,440
hours, hired whole. Labor cash cost is therefore a step function, and within a step the
cash cost of one more hour is zero while the cash cost of the hour that forces a new
hire is $25,000. Pricing marginal labor at a smooth $17.36/hr is a modeling convenience
that is correct for ranking beds and wrong for the hiring decision. The model must
therefore solve over `N_TEMP` explicitly — evaluate the optimal bed mix at each
`N_TEMP` in 0..4 and take the best profit — rather than optimizing beds at a fixed
wage and reading off the temp count afterwards. A scoping check while writing this spec
confirmed the sweep is not busywork: the profit-maximizing `N_TEMP` is not the maximum
`N_TEMP`, and hiring the fourth temp destroys roughly $900 of profit while changing the
bed mix. A model that assumes four temps and optimizes beds against a smooth $17.36/hr
gets both the hiring call and the mix wrong.

**Diminishing returns compound on the bed, not the crop.** `DIM_c` is read as "each
additional bed of this crop requires `DIM_c` more labor hours than the previous bed,"
giving the geometric term above. The alternative linear reading is rejected: under the
geometric reading tomatoes stop at 18 beds on an unconstrained `MC = PRICE` test, which
is exactly where the engagement brief's hypothesis put them; and total labor demand with
tomatoes at 18 and carrots and mesclun at their caps comes to 6,496 hours against a
maximum supply of 6,480 — an overshoot of 16 hours on a 6,500-hour budget. Both are
strong signals the case was built on the compounding reading.

**Costing order.** Fertilizer is a pure per-bed variable cost, charged in full to every
bed planted. `FIXED_COSTS` and `FARMER_SALARY` are period costs, subtracted once at the
bottom of the P&L and never allocated to a crop or a bed. No crop is charged a share of
overhead, so per-crop figures are contributions, not profits, and must be labeled as
such.

**Values as printed.** Table figures are used exactly as given, including
`HRS_WK_BED_CAR = 0.833` rather than 5/6. No intermediate rounding: rounding happens at
presentation only, to whole dollars and one decimal place on hours.

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
6. **Hand calculation.** One crop's `MARGINAL_LABOR_HRS_c(q)` and `MC_c(q)` at three bed
   counts, computed by hand off the spec, match the model to the dollar.
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
None blocking. Both prior open questions are resolved above: `MARGINAL_WAGE` is the temp
rate with the farmer's hours sunk, and `DIM_c` compounds per bed.

## Audit findings
Added AFTER the build. For each check: what you checked, what you found, what you did
about it.
