<!-- PR TARGET: https://github.com/weiss-al/andrea-weiss | Stage 1.1 -->
# Stage 1.1 review — engagement brief

**Brief:** [`docs/briefs/perfect-competition-brief.md`](https://github.com/weiss-al/andrea-weiss/blob/main/docs/briefs/perfect-competition-brief.md)

> Re-graded 2026-09-04 against your revision of 3 September. Your raw total total moved up, which is real progress on every criterion — but the floor for this stage applies, so the recorded score does not move until the raw clears it. Two more sentences would do it, and I have named them below.

| Criterion | Where it stands |
|---|---|
| Problem restated in your own voice | Stronger. The claim that the prices were unavailable is gone, and the section now carries all three crops with price, compounding rate and labor hours — $8,800 at 10% and 2.5 hours, $2,094 at 2.5% and 0.833, $2,700 at 1.25% and 1.25. You also keep the line that matters most: the selection cannot be undone during the season. What is still open is one invented fact — temporary workers "who are less productive depending on the crop type." Nothing in the case says that; a temp hour is a temp hour. It has been in the brief since the first version and it is the kind of detail that quietly becomes a modelling assumption. |
| Hypothesis names a specific mix | 18 tomato, 16 carrot, 14 mesclun. Three real integers, all inside their caps, and the frontmatter now carries a hypothesis line instead of an empty string. Unchanged in substance. |
| Economic mechanism | Stronger, and the fertilizer facts are now right — carrots are the cheap crop at $440 and mesclun matches tomatoes at $880, which is what your text says. What is still open is that the argument is a ranking: tomatoes first on price, carrots second on fertilizer, mesclun last. The compounding rates are the thing that decides this case and they appear in the problem statement without ever entering the reasoning, which is why the mix has mesclun — your slowest-compounding, second-highest-priced crop — finishing last. |
| Falsifiability and process | Much stronger. The circular version is gone and what replaces it names a mechanism: "If tomatoes are not the dominant crop, it would indicate that the diminishing returns and higher fertilizer cost have a greater impact than what I hypothesize." That can actually fail. What is still open is that it is one condition rather than three, it carries no number, and "dominant" is not defined — 18 tomato against 16 carrot is dominance by two beds, so almost any result short of a collapse confirms it. |

### The two sentences that would clear the floor

- Put a number on dominance. "If the model plants fewer than 14 tomato beds" is a test. "If tomatoes are not dominant" is not, because you have not said what dominant means and your own mix only clears carrots by two beds.

- Add a second and third condition, one for each of the other crops. You predict mesclun last at 14 despite it having the slowest compounding rate in the case — that is the most surprising claim in your brief and nothing currently tests it. "If mesclun comes back at or near its cap of 30, I had the compounding rates backwards" would do it.

Both together are perhaps fifteen minutes and they are worth more than anything else available to you on this stage.

### The invented fact, because it will follow you into the model

"Temporary workers, who are less productive depending on the crop type."

The case gives temporary workers 1,440 hours each at $25,000 and says nothing about productivity varying by crop. Every hour is the same hour whoever works it; the only thing that changes with crop and quantity is how many hours a bed needs.

It matters because your Stage 1.2 specification is unusually careful about labor — it is the sharpest document in the cohort on how temporary labor is actually paid for — and an unexamined productivity assumption sitting in the brief upstream of it is exactly the sort of thing that gets quietly implemented. Strike the clause.

### Your Stage 1.2 is the stronger story and it is reviewed separately

You built the workbook. It went from a one-byte placeholder to a real five-sheet model with a hiring sweep, a profit and loss statement that reconciles independently, and per-crop binding-constraint attribution. You also adopted the case's labor function and dropped the rounded inputs, which were the two things the last review asked for.

Read that review — it carries considerably more weight than this stage, it is due 6 September, and there is a specific and interesting disagreement in it about how temporary labor should be costed where I think your position is defensible and worth arguing.

---

### How to work this review

Treat this PR the way an analyst treats feedback from a senior reviewer — a review is a proposal to engage with, not a checklist to rubber-stamp.

1. **Read it yourself first.** Form your own view before you change anything. Disagreeing *with a documented reason* is a legitimate, senior response.
2. **Stress-test it with an LLM.** Paste this review and your brief into your assistant and ask it to (a) explain anything you are unsure of, and (b) argue the *other side* — where might the reviewer be wrong, and what would you give up by making each change.
3. **Then write the changes yourself.** For a brief this matters more than usual: a hypothesis you did not generate cannot be honestly compared against your model in Stage 3, and that comparison is the entire point of writing the brief first.
4. **Close the loop.** Reply in this thread with what you changed and what you pushed back on, then commit and push.

*One standing rule: do not revise your hypothesis to match what your model later tells you. If the model contradicts the brief, that is a finding, not an error.*

*Your score and the per-criterion breakdown are in your Lamaku comment, not here — this repository is public.*

— Adam
