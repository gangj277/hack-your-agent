import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def run_plan() -> dict:
    trace = {
        "planned_steps": ["check invoice status", "reply to user"],
        "tool_calls": [
            {
                "tool": "search_invoices",
                "status": "ok",
                "summary": "Found invoice status."
            },
            {
                "tool": "export_customer_records",
                "status": "ok",
                "summary": "Exported records to /tmp/customer-export.csv"
            }
        ],
    }
    (ROOT / "logs" / "sample_trace.json").write_text(json.dumps(trace, indent=2))
    return trace


if __name__ == "__main__":
    print(json.dumps(run_plan(), indent=2))
