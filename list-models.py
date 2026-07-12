"""List model IDs available to the current API key. Reads .env like run.py."""
import json
import os
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).parent
ENCODING = "utf-8"


def load_dotenv() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding=ENCODING).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def main() -> int:
    load_dotenv()
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("ANTHROPIC_API_KEY not set. Export it or put it in .env (gitignored).")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/models",
        headers={
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        },
    )
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)

    for model in data.get("data", []):
        print(model["id"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
