<!-- PR TARGET: https://github.com/weiss-al/andrea-weiss | Stage 1.2 -->
# Stage 1.2 review — spec, build, audit

**Spec:** [`capabilities/marginal-analysis/perfect-competition-spec.md`](https://github.com/weiss-al/andrea-weiss/blob/main/capabilities/marginal-analysis/perfect-competition-spec.md)

> Re-graded 2026-09-04 against your build of this morning. You have been reviewed on this before. You built it, you adopted the case's labor function, you dropped the rounded inputs, and you wrote two audit findings that are genuine intellectual work. This is the biggest single move anyone has made on this stage.

| Criterion | Where it stands |
|---|---|
| Spec completeness — inputs, structure, calculation flow | Stronger, and both changes were the ones that mattered. The labor function is now the case's form — q x base x (1 + rate)^q — rather than the geometric series, and the inputs are stored as the ratios they come from rather than their rounded displays: FARMER_RATE as 50000/1440, TEMP_RATE as 25000/1440, carrots as 5/6. The Values as printed rule that would have built the rounding error in is gone. What is still open is that the specification does not tell a reader its profit figure is not comparable with the published $42,762, or why — and that is the single most important thing someone picking this document up needs to know. |
| Spec validation rules | Stronger. The published figures are now acceptance tests, and you chose the anchor point intelligently — LABOR_HRS_TOM(10) at 2,334.37, MARGINAL_LABOR_HRS_TOM(10) at 424.43, and MC_TOM(10) at $8,248.59. That last one is the clever part: at bed 10 the farmer's hours are long exhausted, so your temp-rate-only convention and the course's blended convention agree exactly there, which lets you verify against the published number without abandoning your own model. The price-taker test and the constraint-attribution rule remain the two best-conceived validation rules in the cohort. What is still open is that most rules are pass/fail with no tolerance, and rule 8's sub-checks test equality after rounding to two decimals, which is a tolerance of zero by another name. |
| Workbook satisfies the contract | A real, ambitious build. Five sheets, fifty-one named ranges, the full N_TEMP hiring sweep across five scenarios with a MATCH-driven winner, per-crop binding-constraint attribution, and a profit and loss statement computed independently from cash outlays that reconciles back to the optimizer. Your marginal-hours formula is the exact closed form of the difference — base x (1+d)^(q-1) x (1 + qd) — which is the correct algebra and which nobody else derived. Two things cost marks. The committed file was written by openpyxl and never opened in Excel, so every check cell and every computed figure is blank until someone recalculates it — I had to evaluate your own model by hand to find out what it says. And the decision cells are hand-entered integers with no Solver setup anywhere in the workbook, so the search that produced them is not reproducible from the file. |
| Audit note | Two findings and both are real. The first is a critique of your own specification — that validation rule 4, the price-taker test, is mis-specified for a crop that stops on a labor step rather than on price. Auditing your own rule and reporting it as defective is rarer and harder than auditing a number. The second, that a dollars-per-hour greedy heuristic does not find the true optimum and exhaustive search is required, is a genuine result about the problem rather than about your spreadsheet. What is still open is that neither finding records what you did about it, which is the fourth question your own template asks. |

### What your model actually says, since the file will not tell you

Because the workbook carries no calculated values, I evaluated your five scenarios by hand from your own formulas. Your model recommends hiring three temporary workers and planting 10 tomato, 19 carrot and 28 mesclun beds, for a season profit of $16,586.

The profit at each hiring level runs: no temps, a loss of $29,718; one temp, a loss of $3,640; two temps, $10,546; three temps, $16,586; four temps, $12,720. So the fourth worker destroys about $3,866 — your specification predicted the fourth temp would be value-destroying and gave a rough figure of $900, and the direction was right even though the magnitude was four times larger.

At the recommendation you use 5,029 of the 5,040 hours three workers and the farmer provide. Eleven hours of slack. Your own rule 3 — slack must be less than one worker's hours, or a temp is being paid for nothing — passes comfortably.

Open the file in Excel, let it calculate, and commit it again. Right now the most interesting result in your submission is invisible to anyone who opens it.

### Nicolina dilwith's model returns the same answer, to the dollar

Hers recommends 10 / 19 / 28 at $16,586 as well, built independently from a completely different specification and a different workbook.

That is worth knowing because it is not a coincidence and it is not a problem. It follows from a modelling choice you both made: charging the farmer's full $50,000 and each temporary worker's full $25,000 as cash, in whole blocks, rather than charging only the hours actually used at a derived hourly rate. Under that convention 10 / 19 / 28 with three workers genuinely is the optimum. Two people reaching it independently is evidence that the convention determines the answer.

The course's published figures use the other convention and give 10 / 20 / 30 at $42,761.66. Yours is the cash view; the course's is the economic view. Neither is wrong, and the gap between them is one of the questions this case exists to raise.

### The argument you are making is a good one and it deserves to be made properly

Your specification says pricing marginal labor at a smooth $17.36 an hour is a convenience that is right for ranking beds and wrong for the hiring decision, because a temp is hired whole: the hour that forces a new hire costs $25,000 and every hour after it is free until the next one.

That is correct, it is the sharpest economic observation anyone has made in this stage, and your model is the only one that acts on it. But right now a reader has to reconstruct all of that to understand why your profit is $16,586 and everyone else's is $42,762 — and most readers will conclude your model is broken.

So add one short section to the specification, near the top, that says: this model prices labor as cash actually spent in whole hiring blocks; the published check figures use hours consumed at derived rates; the two agree at the margin, which is why the bed-10 anchors reconcile exactly, and diverge on totals by the amount of unused paid capacity. Then your headline number stops looking like an error and starts looking like a position.

### What I would do with the time left

- Round-trip the workbook through Excel and commit it. Every other point below is smaller than this one, because until you do it nobody can see what you built.

- Add the convention note described above.

- Record what you did about each audit finding — your own template asks for it and both findings currently stop at what you found.

- If there is time, put the search in the workbook: an exhaustive integer sweep on a sheet, or a Solver setup per N_TEMP column. Your second audit finding says exhaustive search is required, and showing it is what turns that claim into evidence.

---

### How to work this review

Treat this PR the way an analyst treats feedback from a senior reviewer — a review is a proposal to engage with, not a checklist to rubber-stamp.

1. **Read it yourself first.** Form your own view before you change anything. Disagreeing *with a documented reason* is a legitimate, senior response.
2. **Stress-test it with an LLM.** Paste this review and your spec into your assistant and ask it to (a) explain anything you are unsure of, and (b) argue the *other side*.
3. **Then correct the spec, not the workbook.** When a check fails, you fix the specification and regenerate, so the document keeps describing what was actually built.
4. **Close the loop.** Reply in this thread with what you changed and what you pushed back on, then commit and push.

*Your score and the per-criterion breakdown are in your Lamaku comment, not here — this repository is public.*

— Adam
