"""Export processed results to docs/data for the static site."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

def main() -> None:
    src = Path("data/processed")
    dst = Path("docs/data")
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.glob("*.json"):
        shutil.copy(f, dst / f.name)
    # Also copy events for the explorer
    events = Path("data/events.csv")
    if events.exists():
        shutil.copy(events, dst / "events.csv")
    print("Exported to docs/data/")

if __name__ == "__main__":
    main()
