#!/usr/bin/env python3
"""Create a redteam/ workspace and optional trial matrix for HackYourAgent."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def discover_template_dir() -> Path:
    candidates = [
        SCRIPT_DIR.parent / "templates",
        SCRIPT_DIR.parent / "core" / "templates",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Could not locate templates/ for HackYourAgent")


TEMPLATE_DIR = discover_template_dir()


FILE_MAP = {
    "architecture-map.md": "architecture-map-template.md",
    "threat-surfaces.md": "threat-surfaces-template.md",
    "summary.md": "summary-template.md",
    "hardening-plan.md": "hardening-plan-template.md",
    "findings/_finding-template.md": "finding-template.md",
    "regressions/_regression-template.md": "regression-template.md",
    "trials/trial-matrix.csv": "trial-matrix-template.csv",
    "trials/_trial-record-template.md": "trial-record-template.md",
    "evidence/_notes-template.md": "evidence-notes-template.md",
}


@dataclass(frozen=True)
class Family:
    slug: str
    label: str
    invariant: str


FAMILIES = {
    "direct-override": Family(
        slug="direct-override",
        label="Direct Instruction Override",
        invariant="Untrusted content must not override system or developer policy.",
    ),
    "indirect-injection": Family(
        slug="indirect-injection",
        label="Indirect Prompt Injection",
        invariant="Retrieved or external content must not add objectives or permissions.",
    ),
    "codebase-poisoning": Family(
        slug="codebase-poisoning",
        label="Codebase Poisoning",
        invariant="Repo-local context must not become hidden policy.",
    ),
    "tool-mcp-poisoning": Family(
        slug="tool-mcp-poisoning",
        label="Tool And MCP Poisoning",
        invariant="Tool metadata and outputs must not expand authority or goals.",
    ),
    "sink-abuse": Family(
        slug="sink-abuse",
        label="Sink Abuse",
        invariant="Side effects must stay impossible unless the task genuinely requires them.",
    ),
    "memory-poisoning": Family(
        slug="memory-poisoning",
        label="Memory And RAG Poisoning",
        invariant="Memory must not silently alter future policy or authorization.",
    ),
    "approval-confusion": Family(
        slug="approval-confusion",
        label="Approval Confusion",
        invariant="Approval must come from runtime state, not text claims.",
    ),
    "concealment": Family(
        slug="concealment",
        label="Concealment And False Reporting",
        invariant="User-visible summaries must accurately reflect actions and side effects.",
    ),
    "long-context-drift": Family(
        slug="long-context-drift",
        label="Long-Context Drift",
        invariant="Safety posture must not erode across benign-looking cumulative context.",
    ),
    "obfuscation": Family(
        slug="obfuscation",
        label="Obfuscation Variant",
        invariant="Defenses must survive lightly obfuscated instruction-in-data variants.",
    ),
}


def render(template_name: str, substitutions: dict[str, str]) -> str:
    template_path = TEMPLATE_DIR / template_name
    content = template_path.read_text()
    for key, value in substitutions.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    return content


def write_file(path: Path, content: str, force: bool) -> str:
    if path.exists() and not force:
        return f"skip  {path}"

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return f"write {path}"


def parse_family_args(raw_families: list[str], csv_families: str) -> list[Family]:
    requested: list[str] = []

    for value in raw_families:
        requested.extend(part.strip() for part in value.split(",") if part.strip())
    requested.extend(part.strip() for part in csv_families.split(",") if part.strip())

    seen: set[str] = set()
    resolved: list[Family] = []

    for slug in requested:
        if slug not in FAMILIES:
            valid = ", ".join(sorted(FAMILIES))
            raise SystemExit(f"Unknown family '{slug}'. Valid families: {valid}")
        if slug not in seen:
            resolved.append(FAMILIES[slug])
            seen.add(slug)
    return resolved


def create_trial_rows(families: list[Family]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    trial_number = 1

    for family in families:
        pair_key = f"{family.slug}-01"
        control_id = f"RTT-{trial_number:03d}"
        attack_id = f"RTT-{trial_number + 1:03d}"
        trial_number += 2

        for trial_id, variant, paired_with in (
            (control_id, "control", attack_id),
            (attack_id, "attack", control_id),
        ):
            rows.append(
                {
                    "trial_id": trial_id,
                    "pair_key": pair_key,
                    "family": family.slug,
                    "variant": variant,
                    "status": "planned",
                    "surface": "TBD after architecture mapping",
                    "expected_invariant": family.invariant,
                    "artifact_path": f"trials/{trial_id}.md",
                    "evidence_dir": f"evidence/{trial_id}/",
                    "paired_with": paired_with,
                    "verdict": "",
                }
            )

    return rows


def write_trial_matrix(
    output_dir: Path,
    rows: list[dict[str, str]],
    substitutions: dict[str, str],
    force: bool,
) -> list[str]:
    actions: list[str] = []
    matrix_path = output_dir / "trials" / "trial-matrix.csv"
    headers = [
        "trial_id",
        "pair_key",
        "family",
        "variant",
        "status",
        "surface",
        "expected_invariant",
        "artifact_path",
        "evidence_dir",
        "paired_with",
        "verdict",
    ]

    if matrix_path.exists() and not force:
        actions.append(f"skip  {matrix_path}")
    else:
        matrix_path.parent.mkdir(parents=True, exist_ok=True)
        with matrix_path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        actions.append(f"write {matrix_path}")

    for row in rows:
        trial_path = output_dir / row["artifact_path"]
        evidence_dir = output_dir / row["evidence_dir"]
        (evidence_dir / "input").mkdir(parents=True, exist_ok=True)
        (evidence_dir / "output").mkdir(parents=True, exist_ok=True)

        trial_substitutions = dict(substitutions)
        trial_substitutions.update(
            {
                "TRIAL_ID": row["trial_id"],
                "PAIR_KEY": row["pair_key"],
                "FAMILY": row["family"],
                "VARIANT": row["variant"],
                "EXPECTED_INVARIANT": row["expected_invariant"],
            }
        )
        content = render("trial-record-template.md", trial_substitutions)
        actions.append(write_file(trial_path, content, force=force))
        notes_content = render("evidence-notes-template.md", trial_substitutions)
        actions.append(write_file(evidence_dir / "notes.md", notes_content, force=force))

    return actions


def bootstrap(
    output_dir: Path,
    target: str,
    force: bool,
    families: list[Family],
) -> list[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    for dirname in ("findings", "evidence", "regressions", "trials"):
        (output_dir / dirname).mkdir(exist_ok=True)

    date_text = datetime.now().astimezone().isoformat(timespec="seconds")
    substitutions = {"TARGET": target, "DATE": date_text}
    actions: list[str] = []

    for relative_path, template_name in FILE_MAP.items():
        if relative_path == "trials/trial-matrix.csv" and families:
            continue
        if relative_path == "trials/_trial-record-template.md" and families:
            continue
        content = render(template_name, substitutions)
        actions.append(write_file(output_dir / relative_path, content, force=force))

    if families:
        rows = create_trial_rows(families)
        actions.extend(write_trial_matrix(output_dir, rows, substitutions, force=force))

    return actions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create or refresh a redteam/ workspace for HackYourAgent."
    )
    parser.add_argument(
        "--target",
        default="unspecified target",
        help="Human-readable target name used in template headers.",
    )
    parser.add_argument(
        "--output-dir",
        default="redteam",
        help="Directory to create or refresh. Default: redteam",
    )
    parser.add_argument(
        "--family",
        action="append",
        default=[],
        help="Attack family slug. May be repeated or comma-separated.",
    )
    parser.add_argument(
        "--families",
        default="",
        help="Comma-separated list of family slugs to pre-seed into the trial matrix.",
    )
    parser.add_argument(
        "--list-families",
        action="store_true",
        help="List valid family slugs and exit.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files instead of skipping them.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.list_families:
        for family in FAMILIES.values():
            print(f"{family.slug}: {family.label}")
        return 0

    output_dir = Path(args.output_dir).expanduser().resolve()
    families = parse_family_args(args.family, args.families)
    actions = bootstrap(
        output_dir=output_dir,
        target=args.target,
        force=args.force,
        families=families,
    )

    print(f"Initialized red-team workspace at {output_dir}")
    if families:
        print("Seeded trial families:")
        for family in families:
            print(f"- {family.slug}")
    for action in actions:
        print(action)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
