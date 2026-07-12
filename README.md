# Scaffolding inversion experiment

Testing whether prompt scaffolding that helped older models now degrades newer ones,
and whether the common fix (delete the scaffolding) quietly costs you coverage.

## Hypothesis

Prompt text splits into two kinds.

- Procedure: numbered steps, "think step by step", instructions on how to reason.
- Contract: what "done" means, what cannot be silently skipped.

Claim: procedure has become dead weight on newer models and degrades their output.
Contract is load-bearing on every model, and stripping it causes silent coverage loss,
meaning elements vanish from the threat model without the output ever saying so.

## Design

Three prompt variants x two models = six runs. One design document, unchanged, for all six.

| Variant | Procedure | Contract | Output schema |
|---------|-----------|----------|---------------|
| A-full  | yes       | yes      | yes           |
| B-contract | no     | yes      | yes           |
| C-minimal  | no     | no       | yes           |

The output schema is held constant across all three. Vary it and you measure format
divergence instead of coverage.

Predicted result, stated so it can be wrong:

- A on the newer model underperforms B on the newer model (procedure hurts).
- A on the older model holds up better than A on the newer one (procedure used to help).
- C loses elements relative to B, and does not acknowledge losing them (contract is
  load-bearing). This is the interesting half. If C is fine, the hypothesis is dead and
  we say so.

## Files

- `fetch-design.sh` — pulls the substrate. Run this first. Writes `design.provenance.txt`
  (fetch timestamp) beside `design.md`; only `design.md` is hashed for reproducibility.
- `prompts/A-full.md` — the original prompt, unmodified.
- `prompts/B-contract.md` — procedure removed, contract kept.
- `prompts/C-minimal.md` — both removed.
- `truth/elements.md` — ground truth. Fill in by hand before any run.
- `TASK.md` — human checklist. Work top to bottom.
- `RUN-PROMPT.md` — paste into Claude Code to orchestrate the runs and scoring.
- `runs/` — raw model output, one file per cell. Never edited.

## The substrate

Apache Guacamole manual, four chapters fetched whole (v2 substrate). Apache License 2.0.
Fetched verbatim, never authored by us: if we wrote the design doc, we would be choosing
which elements are buried, and we already have a prediction about what happens to buried
elements. Publish the sha256 that `fetch-design.sh` prints.

**Committed substrate SHA256:** `d816f70ea3a2698e007293d13aab91c9b73563ab1bd62ed22ab0e64833716ab5`

Clone, run `./fetch-design.sh`, and the hash must match. Fetch timestamp lives in
`design.provenance.txt`, not in `design.md`.

Chapters: `guacamole-architecture`, `configuring-guacamole`, `jdbc-auth`, `reverse-proxy`.
Roughly 32,000 words. The architecture chapter alone was too small (~700 words, no data
stores) and would have produced a ceiling effect; v2 widens the grid so data stores,
secrets at rest, and multiple trust boundaries can actually be lost.

**Scoping rule:** all chapters fetched whole; no sections removed. Real design docs are
mostly install and configuration reference. A model that cannot find the design inside
the noise is telling you something true. Cherry-picking sentences out of the config
chapter would not be defensible.

Composition is lopsided: `configuring-guacamole` ~57%, `jdbc-auth` ~33%, `reverse-proxy`
~7%, `guacamole-architecture` ~3%. Most bulk is protocol-parameter reference and JDBC
install walkthroughs. Expect some models to threat-model operational steps rather than
the system architecture.

Chosen because elements are threaded through prose (nothing is enumerated), it has
genuinely rich trust boundaries (browser, Java web app, plaintext TCP hop to guacd,
dynamically loaded protocol plugins, JDBC auth store, reverse proxy), and it has no
canonical published threat model that a model could recall instead of deriving.
Buried signals (`guacd-ssl`, unencrypted webapp-to-guacd hop, port 4822) appear rarely
in the text; omissions there are meaningful.

Known contamination, stated up front: there is well-known 2020 vulnerability research on
Guacamole's RDP plugin. That is memory-corruption bug hunting, not a DFD-level threat
model, so it should not hand a model the element list. Flag it in the write-up anyway.

## Order of operations

1. `./fetch-design.sh`. Record the hash.
2. Fill in `truth/elements.md` by hand. Do not skip this and do not delegate it.
3. Only now open the prompt variants.
4. Run the six cells. Save raw output before analysing anything. Set a generous max
   output limit. Record output token counts for all six runs. Check every run for a
   truncated final table row; any truncated run is void and gets re-run, not scored.
   Truncation masquerades as silent coverage loss and would manufacture a false positive.
5. Score blind: one fixed scorer, fresh context, one output at a time, not told which
   variant or model produced it.

## Confounds we cannot remove

- The two models expose reasoning depth differently, so effort and thinking settings
  cannot be made identical across models. Record what was used. Report it as uncontrolled.
- One run per cell means variance is unmeasured. Differences of one or two elements are
  noise, not findings. Say so.
- The scorer is itself a model. Fix it across all six outputs so at least the error is
  constant.
- Output truncation: with a large input and a per-element threat table, a model that hits
  its output ceiling drops elements silently. Mitigate by generous max output, recording
  output token counts, and voiding any run with a truncated final row.
- Substrate dilution: install and JDBC walkthroughs are operational, not architectural.
  Models may produce filler threats against SQL grants or driver placement rather than
  system design. Score against ground truth elements, not against every sentence in the doc.

## How this experiment fails

If arm C keeps full coverage on the newer model, the silent-coverage-loss claim is dead
and the finding collapses into the same de-scaffolding take everyone already has.
That outcome gets published too.
