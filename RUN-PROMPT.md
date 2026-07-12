# Claude Code prompt: scaffolding inversion experiment

Paste this into Claude Code in a clean directory. Put your design document and the
three prompt variants in place first (see "What you supply" below).

---

I'm testing whether prompt scaffolding that helped older models now hurts newer ones,
because I'm about to publish the claim and I don't want to publish a guess. The result
needs to survive someone else re-running it.

## The hypothesis

Prompt text splits into two kinds. Procedure (numbered steps, "think step by step",
instructions on how to reason) and contract (what "done" means, what cannot be silently
skipped). The claim is that procedure has become dead weight on newer models and actively
degrades their output, while contract is load-bearing on every model and stripping it
causes silent coverage loss.

## What you supply

- `design.md` — the system design document being threat modelled. One document, used
  unchanged for every run.
- `prompts/A-full.md` — original prompt: procedure and contract both present.
- `prompts/B-contract.md` — procedure removed, contract kept.
- `prompts/C-minimal.md` — procedure and contract both removed. Goal and output format only.

## Constraints

The design is 3 prompt variants x 2 models = 6 runs. Same design document, same output
format, one run per cell. Save every raw output to `runs/{variant}-{model}.md` before any
analysis touches it.

Ground truth must exist before the runs. Read `design.md` and enumerate every element
(external entities, processes, data stores, data flows) and every trust boundary into
`truth/elements.md`. Do this first, in its own step, before you read any of the prompt
variants or generate any threat model. If you build the element list after seeing the
outputs, the scoring is circular and the experiment is worthless.

Scoring must be blind and consistent. Use a single fresh-context subagent as the scorer
for all 6 outputs. It sees `truth/elements.md` and one output at a time. It must not know
which variant or model produced the output, and must not see the other outputs. For each
run it reports:

- Elements from ground truth with at least one threat against them (coverage count).
- Elements with zero threats, and whether the output explicitly acknowledged the omission
  or just dropped it. This distinction is the whole experiment. A missing element that the
  output flags as deliberately out of scope is not the same failure as one that vanished.
- Total threat count, and the count at each severity.
- Threats that restate a STRIDE category rather than describe an attack (filler count).
- Threats that reference no specific component or flow from the design (generic count).

Report the results as a single table, one row per run, plus a short answer to: did removing
procedure change coverage, and did removing the contract cause unacknowledged omissions.

## Confounds to state, not hide

The two models expose reasoning depth differently, so effort/thinking settings cannot be
made identical across models. Record exactly what you used for each model and note it as an
uncontrolled variable in the write-up. One run per cell means variance is unmeasured, so do
not report small differences as findings. If two cells differ by one or two elements, say
that is within noise and not a result.

If the outcome contradicts the hypothesis, say so plainly in the write-up. A clean negative
is worth more to me than a confirmation I have to defend later.

Lead with the outcome when you report back.
