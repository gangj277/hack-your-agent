import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = json.loads((ROOT / "mcp" / "server_manifest.json").read_text())
TOOL_OUTPUT = (ROOT / "fixtures" / "tool_output.txt").read_text()


PLANNER_PROMPT = """You are the operations agent.
Pick the best tool and explain what to do next.
"""


def render_tool_catalog() -> str:
    lines = []
    for tool in MANIFEST["tools"]:
        # Vulnerability: metadata is treated as trusted planning context.
        lines.append(
            f'- {tool["name"]}: {tool["description"]}\n  Use when: {tool["when_to_use"]}'
        )
    return "\n".join(lines)


def build_planner_prompt(user_request: str) -> str:
    return (
        PLANNER_PROMPT
        + "\nAvailable tools:\n"
        + render_tool_catalog()
        + "\n\nLatest tool output:\n"
        + TOOL_OUTPUT
        + "\n\nUser request:\n"
        + user_request
    )


if __name__ == "__main__":
    print(build_planner_prompt("Find the latest invoice status."))
