"""Optional LLM-assisted departure_type classifier. Labels always reviewable."""
from __future__ import annotations

import os
from typing import Optional


def classify_departure(text: str) -> Optional[str]:
    """Return one of: forced/scandal | voluntary/unplanned | planned succession | death/health | other
    Requires ANTHROPIC_API_KEY. Never used silently; results go to CSV for manual review.
    """
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        return None
    # Placeholder: real call would use anthropic.Anthropic().messages.create(...)
    # Prompt would include few-shot examples and require structured output.
    return "other"  # stub
