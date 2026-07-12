# TASK.md — Strip Test

Human checklist. Work top to bottom. Two steps are marked DO NOT DELEGATE.
Those two are the experiment. Everything else is admin.

---

## Step 0 — Fix the layout

The README expects subdirectories. Your files are at root. The fetch script creates
empty directories but does not move anything into them.

```bash
mkdir -p prompts truth runs
mv A-full.md B-contract.md C-minimal.md prompts/
mv elements.md truth/
```

- [x] `prompts/` contains A-full.md, B-contract.md, C-minimal.md
- [x] `truth/` contains elements.md
- [x] `runs/` exists and is empty

---

## Step 1 — Fetch the substrate

```bash
chmod +x fetch-design.sh
./fetch-design.sh
```

Needs curl and pandoc. Fetches four chapters (v2 substrate), strips pandoc headerlink
cruft, normalises line endings. If pandoc is missing: `brew install pandoc`.

- [x] `design.md` exists
- [x] SHA256 recorded here: `d816f70ea3a2698e007293d13aab91c9b73563ab1bd62ed22ab0e64833716ab5`
- [ ] Re-run `./fetch-design.sh` twice; both runs must print the same sha256 for `design.md`
- [ ] Opened design.md and confirmed all four chapter bodies are intact
- [ ] Changed nothing inside the chapter body

If you edited the body, stop. Re-fetch. The substrate is fetched, never authored.

---

## Step 2 — Build ground truth  [DO NOT DELEGATE]

Read `design.md` end to end. Yourself. Fill in `truth/elements.md` by hand.

Do not open the prompt variants first. Do not let Cursor or Claude Code write this file.
If a model builds the yardstick, the elements it fails to notice go missing from both
the yardstick and the outputs, every run scores full marks against a list that excludes
the hard cases, and the experiment returns a confident null result that is simply wrong.

For every element, fill the column that matters:

- STATED PLAINLY — named directly, hard to miss
- BURIED — mentioned once, in passing, threaded through prose or project history

The buried ones are the experiment. Silent coverage loss cannot be claimed on a buried
element you did not mark as buried before seeing any model output.

Look specifically for elements that appear only in narrative asides. The local daemon and
the port it listens on. The plugins loaded at runtime. The tunnel. The authentication
chokepoint. The plaintext hop between the web app and the daemon (`guacd-ssl`, port 4822).

- [ ] Every external entity listed
- [ ] Every process listed
- [ ] Every data store listed
- [ ] Every data flow listed, with trust-boundary crossings marked
- [ ] Every trust boundary listed
- [ ] Each row marked STATED PLAINLY or BURIED
- [ ] Ambiguous items recorded in Notes rather than silently resolved
- [ ] File committed and frozen

Commit it before you go any further. The commit timestamp is your proof it predates
the runs.

```bash
git add truth/elements.md && git commit -m "ground truth: hand-built from design.md, before any model run"
```

---

## Step 3 — Run the six cells

Now you can delegate. Hand `RUN-PROMPT.md` to Claude Code.

Three variants x two models. Same `design.md` every time. One run per cell.

- [ ] A-full   / older model  → `runs/A-full-old.md`
- [ ] B-contract / older model → `runs/B-contract-old.md`
- [ ] C-minimal / older model  → `runs/C-minimal-old.md`
- [ ] A-full   / newer model  → `runs/A-full-new.md`
- [ ] B-contract / newer model → `runs/B-contract-new.md`
- [ ] C-minimal / newer model  → `runs/C-minimal-new.md`

- [ ] Effort / thinking settings recorded for each model
- [ ] Output token counts recorded for all six runs
- [ ] All six raw outputs saved before any analysis touched them
- [ ] No run with a truncated final table row (void and re-run if truncated)
- [ ] Nothing edited after generation

---

## Step 4 — Score blind  [DO NOT DELEGATE THE SETUP]

One fixed scorer. Fresh context. One output at a time. The scorer sees
`truth/elements.md` and a single run, and is not told which variant or model produced it.

You set this up. If the scorer knows it is looking at C-minimal, you have not measured
anything.

Per run, record:

- [ ] Ground-truth elements with at least one threat against them
- [ ] Ground-truth elements with zero threats
- [ ] Of those, how many the output explicitly flagged as out of scope, versus how many
      just vanished. THIS IS THE FINDING. An acknowledged omission is not a failure.
      An unacknowledged one is.
- [ ] Coverage broken out separately for STATED PLAINLY vs BURIED elements
- [ ] Total threat count, and count per severity
- [ ] Filler count: threats that restate a STRIDE category instead of describing an attack
- [ ] Generic count: threats referencing no specific component or flow from the design

---

## Step 5 — Read the result honestly

Answer these before writing a word of the post.

- [ ] Did removing procedure change coverage on the newer model? (A-new vs B-new)
- [ ] Did procedure help the older model? (A-old vs B-old)
- [ ] Did removing the contract cause unacknowledged omissions? (C vs B)
- [ ] Did the losses concentrate in BURIED elements?

Guardrails:

- [ ] Differences of one or two elements are noise. One run per cell means variance is
      unmeasured. Do not report noise as a finding.
- [ ] Effort settings could not be equalised across models. State it as an uncontrolled
      variable.
- [ ] The scorer is itself a model. State it.
- [ ] 2020 Guacamole RDP vulnerability research exists publicly. State it as possible
      contamination.

If C-minimal held full coverage, the hypothesis is dead. Publish that. A clean negative,
honestly reported, is a better piece of content than a confirmation you would have to
defend afterwards.

---

## Step 6 — Publish

- [ ] Post updated from prediction to result
- [ ] SHA256 of design.md included
- [ ] Substrate URL and Apache-2.0 attribution included
- [ ] Repo public so a reader can re-run it
- [ ] Confounds stated in the post, not just the repo
