# Strip test

Testing whether prompt scaffolding that helped older models now degrades newer ones, and
whether the common fix (delete the scaffolding) quietly costs you coverage.

Method: the strip test. Take a working prompt, strip a layer, strip another, see what breaks.
Predicted finding: silent coverage loss. The finding is only named as such if it shows up.

Substrate: Apache Guacamole manual v1.5.5. Guacamole is the material, not the subject.

---

## Hypothesis

Prompt text splits into two kinds.

| Kind | What it is | Claim |
|------|------------|-------|
| Procedure | Numbered steps, "think step by step", instructions on how to reason | Dead weight on newer models; may degrade output |
| Contract | Definition of done, what cannot be silently skipped | Load-bearing on every model; removing it drops elements without saying so |

## Design

Three prompt variants x two models = six runs. One design document, unchanged, for all six.

| Variant | Procedure | Contract | Output schema |
|---------|-----------|----------|---------------|
| A-full | yes | yes | yes |
| B-contract | no | yes | yes |
| C-minimal | no | no | yes |

The output schema is held constant across all three. Vary it and you measure format
divergence instead of coverage.

## Predicted outcomes, pre-registered

- A underperforms B on the newer model. Procedure hurts.
- A holds up better on the older model than on the newer one. Procedure used to help.
- C loses CORE elements relative to B, and does not acknowledge losing them. The contract
  is load-bearing. This is the interesting half.

If C-minimal holds full CORE coverage, the hypothesis is dead. That negative result gets
published. A clean negative, honestly reported, is worth more than a confirmation that has
to be defended afterwards.

---

## Substrate

Apache Guacamole manual v1.5.5, four chapters, fetched verbatim. Apache License 2.0.

- `guacamole-architecture` — the DFD spine
- `configuring-guacamole` — GUACAMOLE_HOME, guacamole.properties, user-mapping.xml, guacd
  host/port, the unencrypted-by-default web-app-to-guacd hop, connection parameters holding
  remote credentials
- `jdbc-auth` — the database: users, permissions, stored connection secrets
- `reverse-proxy` — the proxy boundary in front of the web application

`design.md`: 31,982 words, 3,284 lines.

SHA256: `d816f70ea3a2698e007293d13aab91c9b73563ab1bd62ed22ab0e64833716ab5`

Reproducibility claim: clone, run `./fetch-design.sh`, get that hash. The fetch timestamp is
written to `design.provenance.txt` (gitignored) rather than into the artifact, so `design.md`
is byte-reproducible.

Scoping rule, stated before the runs and not retro-fitted: all four chapters fetched whole.
No sections removed. Inline anchor markup stripped and CRLF normalised; no content lines
removed.

The substrate was fetched, never authored. Writing the design document ourselves would mean
choosing which elements are buried, while already holding a prediction about what happens to
buried elements.

Chosen because it is narrative rather than specification (elements are threaded through prose
and through deeply nested configuration tables, nothing is enumerated), it has genuinely rich
trust boundaries, and it has no canonical published threat model that a model could recall
instead of deriving.

---

## Ground-truth provenance

The ground-truth inventory in `truth/elements.md` was built from `design.md` by ChatGPT, an
out-of-family model relative to the model family under test. It must not be described as
hand-built.

The pre-tier inventory was subsequently read end to end by the human reviewer, Liban M, who
reviewed its inclusions, exclusions, line references, and ambiguity notes. On 12 July 2026, the
reviewer also signed off the exact row-level CORE/EXTENDED assignments after the risk-centric
tiering rule was made explicit and the servlet-container row was corrected to CORE.

The defensible publication description:

> Ground truth built by an out-of-family model, then reviewed and signed off line by line by
> a human.

The reason ground truth is not built by the model family under test: its blind spots would be
missing from both the yardstick and the outputs, every run would score full marks against a
list that already excludes the hard cases, and the experiment would return a confident null
result with no way to see the error from inside the data.

---

## Pre-registered tiering rule

Every row is frozen as one of two tiers after human Tier sign-off and before any model run.

- CORE: canonical elements that any competent threat model of this system must cover. The
  architecture spine, principal trust boundaries, authentication and configuration and
  credential stores, the browser-to-web-application path, the WebSocket and HTTP fallback
  tunnels, guacd, libguac, independently executing client plugins, the remote-target path,
  the reverse proxy, the JDBC database, and the plaintext-by-default web-application-to-guacd
  hop.
- EXTENDED: genuinely present but optional, peripheral, protocol-specific, operational, or a
  finer-grained duplicate of a CORE concept. VNC repeaters, PulseAudio, GhostScript,
  Hyper-V/VMConnect, Wake-on-LAN, recording utilities, and protocol-specific endpoints already
  represented by the canonical remote-target row.

The tiering principle is risk-centric rather than process-counting. Risk-bearing data stores,
data flows, and trust-boundary crossings are CORE; interchangeable provider, driver, or helper
processes that merely operate them are EXTENDED unless the process is itself part of the
architecture spine. Thus `user-mapping.xml` is CORE while the default XML authentication
provider is EXTENDED; the JDBC database, its credential-bearing flow, and its boundary are CORE
while the database authentication extension and JDBC driver are EXTENDED. The servlet container
(Tomcat in the documented deployment) is CORE because it hosts the web application and terminates
the proxied application path. The reverse proxy remains CORE because, when deployed, it defines
the public TLS-termination and client-network boundary.

Tiering exists to control a floor effect. The full inventory is maximalist; scoring against all
of it would let DFD granularity and peripheral detail swamp the headline metric, and would
inflate output length into the truncation confound.

The frozen pre-run yardstick contains 31 CORE rows and 108 EXTENDED rows.

---

## Scoring

The headline coverage score is calculated against CORE only. EXTENDED coverage is calculated
and reported separately as a secondary metric.

Scoring is semantic rather than string-exact. A grouped element such as "remote desktop targets
(VNC/RDP/SSH/Telnet/Kubernetes)" satisfies the canonical CORE remote-target row; the output is
not penalised for failing to enumerate each corresponding EXTENDED row. This grouped-credit
allowance applies to entity and component granularity, not to security properties.

F9 / B5 special rule: credit requires the security property, not merely the flow. An output
earns F9 or B5 only if it states that the web-application-to-guacd hop is unencrypted or
plaintext by default, or raises a threat that depends on that fact, such as interception,
tampering, or credential capture on the internal hop. Describing the hop, naming port 4822, or
listing guacd as a component does not earn credit.

The same rule applies to other security defaults and fallback modes: Kubernetes TLS disabled by
default, SSH host verification absent unless a trust anchor is configured, and JDBC
configurations that may fall back to plaintext. These properties must be stated or explicitly
used in threat reasoning; they are not inferred from generic architecture coverage.

Scoring is blind. One fixed scorer, fresh context, one output at a time. The scorer sees the
ground-truth rows and a single run, and is not told which variant or model produced it.

Per run, recorded:

- CORE elements with at least one threat against them
- CORE elements with zero threats, split into those the output explicitly flagged as out of
  scope and those that simply vanished. This distinction is the finding. An acknowledged
  omission is not a failure. An unacknowledged one is.
- Coverage broken out separately for STATED PLAINLY and BURIED rows
- EXTENDED coverage, reported separately
- Total threat count and count per severity
- Filler count: threats restating a STRIDE category rather than describing an attack
- Generic count: threats referencing no specific component or flow from the design

---

## Confounds, stated up front

- Truncation. The input is roughly 45k tokens. A model that hits its output ceiling drops
  elements silently, which is indistinguishable from the contract failing, and would
  manufacture a false positive for our own hypothesis. Output limits are held constant across
  arms, output token counts are recorded for all six runs, every run is checked for a truncated
  final row, and any truncated run is voided and re-run rather than scored.
- Effort settings cannot be equalised across models, which expose reasoning depth differently.
  Recorded per model, reported as an uncontrolled variable.
- The scorer is itself a model. Fixed across all six outputs so the error is at least constant.
- One run per cell means variance is unmeasured. Differences of one or two elements are noise,
  not findings.
- The substrate is largely installation and parameter reference rather than design. Models may
  threat-model the install instructions. Expect filler.
- Public 2020 vulnerability research exists on Guacamole's RDP plugin. That is memory-corruption
  bug hunting rather than a DFD-level threat model, so it should not hand a model the element
  list, but it is disclosed.

---

## How this experiment fails

The experiment does not get to claim silent coverage loss merely because the predicted pattern
appears. The claim fails, or the run is treated as inconclusive, under any of these conditions:

- C-minimal retains full CORE coverage. The contract-removal hypothesis is dead, and that
  negative result is published.
- The observed differences are only one or two CORE rows. With one run per cell, that is noise,
  not evidence.
- Any scored output is truncated, uses a different output limit, or ends mid-row. That run is
  void and must be repeated under the fixed limit.
- The output schema changes between arms, or effort settings are silently changed within a model.
  The comparison no longer isolates procedure versus contract.
- The scorer sees multiple outputs together, learns the model or prompt variant, or changes
  between cells. Blind scoring has failed.
- The headline result depends on EXTENDED enumeration, protocol-instance counting, or generic
  DFD granularity rather than missed CORE elements. The metric is measuring verbosity, not
  coverage.
- The yardstick or scoring rules are changed after any output is observed. A new version must be
  created and all six arms rerun.
- `design.md` cannot be reproduced at the pinned SHA256, or the four-chapter scoping rule changes.
  The runs are no longer using the same substrate.
- The result is better explained by the disclosed confounds—especially truncation, unequal effort,
  scorer error, or memorised Guacamole-specific research—than by the prompt distinction.

---

## Freeze rule

The human reviewer has signed off the exact Tier column. The tier assignments and scoring rules
are frozen before the first model run and captured by the annotated Git tag `yardstick-v1.0.0`. Any later correction requires a new yardstick
version, an explicit row-level change log, and rerunning all arms. The active yardstick is never
edited around observed outputs.

---

## Files

- `fetch-design.sh` — pulls and pins the substrate. Run first.
- `design.md` — the substrate. Fetched, never authored. Do not edit.
- `prompts/A-full.md` — the original prompt, unmodified.
- `prompts/B-contract.md` — procedure removed, contract kept.
- `prompts/C-minimal.md` — both removed.
- `truth/elements.md` — the yardstick.
- `run.py` — six independent API calls, no agent harness. Writes `runs/` and
  `runs/manifest.json`.
- `RUN-PROMPT.md` — orchestration for the six runs and the blind scoring.
- `TASK.md` — human checklist.
- `runs/` — raw model output, one file per cell. Never edited.
