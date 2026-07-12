#!/usr/bin/env python3
"""
Strip test runner.

Six independent API calls. Three prompt variants x two model generations.
No agent harness, no tool loop, no conversation state. The whole point of the
experiment is to measure the effect of scaffolding, so the runner must not add any.

Each cell is:
    system  = prompts/{variant}.md, verbatim
    user    = design.md, verbatim
    nothing else

Usage:
    export ANTHROPIC_API_KEY=...
    python run.py --old <model-string> --new <model-string> --max-tokens 32000

On Windows PowerShell, use `python run.py` — `./run.py` does not invoke Python.

Verify the model strings against your own API access before running. Hold the
capability tier roughly constant and vary the generation, or you will be measuring
model size rather than model generation.

Any run that stops because it hit the output ceiling is VOID. The script fails hard
rather than writing a truncated run, because a truncated output drops elements
silently, which is indistinguishable from the contract failing, and would manufacture
a false positive for our own hypothesis.
"""

import argparse
import hashlib
import json
import os
import pathlib
import sys
import time

try:
    from anthropic import Anthropic
except ImportError:
    sys.exit("pip install anthropic")

ROOT = pathlib.Path(__file__).parent
VARIANTS = ["A-full", "B-contract", "C-minimal"]


def load_dotenv() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    load_dotenv()
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY not set. Export it or put it in .env (gitignored).")

    ap = argparse.ArgumentParser()
    ap.add_argument("--old", required=True, help="prior-generation model string")
    ap.add_argument("--new", required=True, help="current-generation model string")
    ap.add_argument("--max-tokens", type=int, default=32000)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument(
        "--thinking-budget",
        type=int,
        default=0,
        help="extended thinking budget tokens, 0 to disable. Cannot be equalised "
             "across generations; whatever you use is recorded and reported as an "
             "uncontrolled variable.",
    )
    args = ap.parse_args()

    design_path = ROOT / "design.md"
    if not design_path.exists():
        sys.exit("design.md not found. Run ./fetch-design.sh first.")

    design = design_path.read_text()
    design_hash = sha256(design_path)

    runs_dir = ROOT / "runs"
    runs_dir.mkdir(exist_ok=True)

    client = Anthropic()
    models = {"old": args.old, "new": args.new}

    manifest = {
        "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "design_sha256": design_hash,
        "yardstick_tag": "yardstick-v1.0.0",
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
        "thinking_budget": args.thinking_budget,
        "models": models,
        "runs": [],
    }

    print(f"design.md sha256: {design_hash}")
    print(f"max_tokens={args.max_tokens} temperature={args.temperature}\n")

    truncated = []

    for gen, model in models.items():
        for variant in VARIANTS:
            prompt_path = ROOT / "prompts" / f"{variant}.md"
            system = prompt_path.read_text()
            cell = f"{variant}-{gen}"

            print(f"  {cell:22s} {model} ... ", end="", flush=True)

            kwargs = dict(
                model=model,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                system=system,
                messages=[{"role": "user", "content": design}],
            )
            if args.thinking_budget:
                # extended thinking requires temperature=1 on current APIs
                kwargs["thinking"] = {
                    "type": "enabled",
                    "budget_tokens": args.thinking_budget,
                }
                kwargs["temperature"] = 1.0

            t0 = time.time()
            resp = client.messages.create(**kwargs)
            elapsed = round(time.time() - t0, 1)

            text = "".join(
                b.text for b in resp.content if getattr(b, "type", None) == "text"
            )

            out_tokens = resp.usage.output_tokens
            stop = resp.stop_reason
            hit_ceiling = stop == "max_tokens"

            (runs_dir / f"{cell}.md").write_text(text)

            manifest["runs"].append(
                {
                    "cell": cell,
                    "variant": variant,
                    "generation": gen,
                    "model": model,
                    "prompt_sha256": sha256(prompt_path),
                    "stop_reason": stop,
                    "input_tokens": resp.usage.input_tokens,
                    "output_tokens": out_tokens,
                    "max_tokens": args.max_tokens,
                    "headroom": args.max_tokens - out_tokens,
                    "truncated": hit_ceiling,
                    "seconds": elapsed,
                }
            )

            flag = "  <-- TRUNCATED" if hit_ceiling else ""
            print(f"{out_tokens:>6} tok  stop={stop}  {elapsed}s{flag}")

            if hit_ceiling:
                truncated.append(cell)

    (runs_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))

    print()
    if truncated:
        print("VOID. These runs hit the output ceiling:")
        for c in truncated:
            print(f"  {c}")
        print(
            "\nA truncated run drops elements silently. Scoring it would hand us our own\n"
            "hypothesis for free. Raise --max-tokens and re-run ALL SIX arms, not just\n"
            "the truncated ones. Do not score anything in runs/."
        )
        return 1

    # headroom warning: near-ceiling is not proof of truncation but it is a smell
    tight = [
        r["cell"] for r in manifest["runs"] if r["headroom"] < 0.1 * args.max_tokens
    ]
    if tight:
        print("WARNING: under 10% headroom on:", ", ".join(tight))
        print("Consider raising --max-tokens and re-running all six.\n")

    print("All six runs complete, none truncated.")
    print("Raw output in runs/. Commit before scoring:\n")
    print('  git add runs/ && git commit -m "six raw runs, pre-scoring"')
    return 0


if __name__ == "__main__":
    sys.exit(main())
