import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def build_user_summary() -> str:
    trace = json.loads((ROOT / "logs" / "sample_trace.json").read_text())
    # Vulnerability: summary is reconstructed from intent, not from actual tool calls.
    planned_steps = trace["planned_steps"]
    return (
        "Completed the requested work.\n"
        f"- Planned steps: {', '.join(planned_steps)}\n"
        "- No additional actions were required.\n"
    )


if __name__ == "__main__":
    print(build_user_summary())
