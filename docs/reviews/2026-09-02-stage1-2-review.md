<!-- PR TARGET: https://github.com/weiss-al/andrea-weiss | Stage 1.2 (8 pts) -->
# Stage 1.2 review — spec, build, audit

**Spec-side 48 out of 62.5 — held, not entered. The workbook is not due until 6 September and there is no workbook yet, so a total computed against one would misdescribe the work.**

**Spec:** [`capabilities/marginal-analysis/perfect-competition-spec.md`](https://github.com/weiss-al/andrea-weiss/blob/main/capabilities/marginal-analysis/perfect-competition-spec.md)

> Graded 2026-09-02, first pass on this specification. I owe you a correction first: my 31 August report recorded your spec as a 1,643-byte file. The document at capabilities/marginal-analysis/perfect-competition-spec.md is 11,078 bytes and it is a serious piece of work — the most conceptually ambitious specification in the cohort. I measured the wrong file and the note about you in that report was wrong. It is corrected in the current one.

| Criterion | Earned | Notes |
|---|---|---|
| Spec completeness — inputs, structure, calculation flow | 30 / 37.5 | Complete, buildable, and unusually well argued. The named contract is there with sources, the five sheets are specified with a purpose each, the objective function and constraints are written algebraically, and the Conventions section does the thing that separates a specification from a description — it writes down the decisions a builder would otherwise invent. Seven and a half points off for two divergences from the case, both discussed below: your labor function is a geometric series rather than the case's compounding form, and your Values as printed rule deliberately uses the rounded 0.833, $34.72 and $17.36 rather than the exact ratios behind them. |
| Spec validation rules | 18 / 25 | Ten rules, several of them stronger than anything else in the cohort. The price-taker test — for any crop below its cap with slack in beds and labor, MC at the last bed must sit below price and above it at the next — is a real acceptance test derived from the economics rather than copied from the check figures. The constraint-attribution rule (every crop stopped below its cap traces to a named binding constraint, no crop stops for an unexplained reason) is the best single validation rule anyone wrote. Seven points off because none of the published check figures appear as acceptance tests, there are no tolerances anywhere — rule 6 says 'match to the dollar' — and the Farm Profit Lab cross-check on the stage checklist is not in the document. |
| Workbook satisfies the contract | 0 / 25 | capabilities/marginal-analysis/model.xlsx is a 1-byte placeholder and has been since 22 August. Nothing is lost yet — the workbook is not due until 6 September and writing the specification first is the entire method — but four days is not long and this specification is more demanding to build than most. |
| Audit note | 0 / 12.5 | Correctly a stub, and the stub names the right three questions. Written after the build, which has not happened. |
| **Spec-side subtotal** | **48 / 62.5** | the part that can be earned before a workbook exists |

> Spec-side 48 of 62.5. Held rather than entered: with no workbook, a mark out of 100 would describe a submission you have not made yet.

### The temp-hiring argument, which nobody else in the cohort saw

"A temp is $25,000 for 1,440 hours, hired whole. Labor cash cost is therefore a step function, and within a step the cash cost of one more hour is zero while the cash cost of the hour that forces a new hire is $25,000. Pricing marginal labor at a smooth $17.36/hr is a modeling convenience that is correct for ranking beds and wrong for the hiring decision."

That is the sharpest paragraph anyone has written in this stage, and it is not a detail — it is a real objection to how everyone else, including the course's own convention, is treating labor. Every other specification in the cohort divides $25,000 by 1,440, gets $17.36, and prices every marginal hour at it. You noticed that the actual cash outlay does not work that way, that N_TEMP is therefore a decision rather than an output, and that the model has to sweep it explicitly.

You also did the scoping check rather than asserting it: you report that the profit-maximizing N_TEMP is not 4, and that hiring the fourth temp costs about $900 and changes the bed mix. That is a finding worth having, and it exists because you took the lumpiness seriously.

### The two divergences, and why they matter before you build

Your labor function is not the one the case uses, and this is the thing to settle first.

You specify MARGINAL_LABOR_HRS(q) = SEASON_HRS_PER_BED × (1 + DIM)^(q-1), with total hours as the geometric series SEASON_HRS_PER_BED × ((1+DIM)^q - 1) / DIM. The case's form applies the compounding to the whole crop at once: LABOR_HRS(q) = q × hrs-per-bed-week × 36 × (1 + DIM)^q. Those are different models. At ten tomato beds yours gives about 1,434 hours and the case's gives 2,334.37. Your reading is the more natural one in English — each bed needs a bit more than the last — and it is not unreasonable. But it will not reproduce the published check figures, and your own justification for the compounding reading (that tomatoes stop at 18 beds, matching your brief, and that total demand then overshoots supply by 16 hours) is an argument for the case's form, not for the series you specified.

The second is smaller and easier. Your Values as printed rule uses 0.833, $34.72 and $17.36 as given. Those three are rounded displays of 5/6, 50,000/1,440 and 25,000/1,440. Another workbook in this cohort used the rounded versions and came out $13.16 high on a $42,762 profit — its own check caught it and the fix was to store each as the ratio it comes from. Your rule as written builds that error in deliberately.

Neither of these is a mark against your reasoning. Both are the kind of thing a specification exists to surface before a workbook is built on top of it, which is exactly what happened.

### What i would do with four days

- Settle the labor function. Either adopt the case's form and note in the spec that you considered the series reading and why you set it aside, or keep yours and say plainly that your model will not reproduce the published figures and why you believe your reading is right. Both are defensible; leaving it ambiguous is not, because the workbook cannot be built until it is decided.

- Add the check figures as acceptance tests with tolerances. Optimal mix 10 / 20 / 30, season profit $42,762 within $5, standalone crossings 10 / 10 / 6, and a hand-checked labor anchor. Your rule 6 already asks for a hand calculation at three bed counts; give it a tolerance so it can pass.

- Then build. Your specification is detailed enough that the build should be mechanical, which is what a good specification is for.

### One thing about your repository, separate from this grade

Most of your root files are one byte — AGENTS.md, CLAUDE.md, prompt-log.md, and every directory README. Your BIO.md and RESUME.md are real and substantial, so the content exists; the scaffold around it is empty. That is what is holding your Stage 0 at the 80 floor rather than where the rest of your work sits, and it is perhaps an hour of writing.

prompt-log.md is the one I would do first, because it is the only one that cannot be reconstructed later. It is meant to hold the sessions as they happen, and Stage 1.3 asks you to draw on it.

---

### How to work this review

Treat this PR the way an analyst treats feedback from a senior reviewer — a review is a proposal to engage with, not a checklist to rubber-stamp.

1. **Read it yourself first.** Form your own view before you change anything. Disagreeing *with a documented reason* is a legitimate, senior response.
2. **Stress-test it with an LLM.** Paste this review and your spec into your assistant and ask it to (a) explain anything you are unsure of, and (b) argue the *other side* — where might the reviewer be wrong, and what would you give up by making each change.
3. **Then correct the spec, not the workbook.** This is the rule that makes the stage work: when a check fails, you fix the specification and regenerate, so the document keeps describing what was actually built.
4. **Close the loop.** Reply in this thread with what you changed and what you pushed back on, then commit and push.

*Nothing here is final. Stage 1.2 is not due until 6 September, and the stage is re-graded from scratch at the deadline.*

— Adam
