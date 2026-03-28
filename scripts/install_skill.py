#!/usr/bin/env python3
"""Install HackYourAgent as a native Codex or Claude Code skill."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME = "hack-your-agent"


def codex_default_dir() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    return codex_home / "skills" / SKILL_NAME


def claude_default_dir(scope: str, project_dir: str | None) -> Path:
    if scope == "user":
        return Path.home() / ".claude" / "skills" / SKILL_NAME
    base = Path(project_dir or ".").expanduser().resolve()
    return base / ".claude" / "skills" / SKILL_NAME


def reset_dir(path: Path, force: bool) -> None:
    if path.exists():
        if not force:
            raise SystemExit(f"{path} already exists. Re-run with --force to replace it.")
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_tree(src: Path, dest: Path) -> None:
    shutil.copytree(src, dest, dirs_exist_ok=True)


def rewrite_skill_text(platform: str, dest_dir: Path) -> str:
    skill_path = REPO_ROOT / "platforms" / platform / SKILL_NAME / "SKILL.md"
    text = skill_path.read_text()
    text = text.replace("../../../core/references/", "references/")
    text = text.replace("../../../core/templates/", "templates/")

    if platform == "codex":
        script_path = dest_dir / "scripts" / "init_redteam_run.py"
        text = text.replace(
            "python3 ../../../scripts/init_redteam_run.py",
            f'python3 "{script_path}"',
        )
    else:
        text = text.replace(
            "python3 ../../../scripts/init_redteam_run.py",
            'python3 "${CLAUDE_SKILL_DIR}/scripts/init_redteam_run.py"',
        )
    return text


def install_codex(dest_dir: Path, force: bool) -> Path:
    reset_dir(dest_dir, force)
    (dest_dir / "agents").mkdir(exist_ok=True)
    copy_tree(REPO_ROOT / "core" / "references", dest_dir / "references")
    copy_tree(REPO_ROOT / "core" / "templates", dest_dir / "templates")
    (dest_dir / "scripts").mkdir(exist_ok=True)
    shutil.copy2(REPO_ROOT / "scripts" / "init_redteam_run.py", dest_dir / "scripts")
    shutil.copy2(
        REPO_ROOT / "platforms" / "codex" / SKILL_NAME / "agents" / "openai.yaml",
        dest_dir / "agents",
    )
    (dest_dir / "SKILL.md").write_text(rewrite_skill_text("codex", dest_dir))
    return dest_dir


def install_claude(dest_dir: Path, force: bool) -> Path:
    reset_dir(dest_dir, force)
    copy_tree(REPO_ROOT / "core" / "references", dest_dir / "references")
    copy_tree(REPO_ROOT / "core" / "templates", dest_dir / "templates")
    (dest_dir / "scripts").mkdir(exist_ok=True)
    shutil.copy2(REPO_ROOT / "scripts" / "init_redteam_run.py", dest_dir / "scripts")
    (dest_dir / "SKILL.md").write_text(rewrite_skill_text("claude", dest_dir))
    return dest_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install HackYourAgent natively.")
    subparsers = parser.add_subparsers(dest="platform", required=True)

    codex = subparsers.add_parser("codex", help="Install for Codex.")
    codex.add_argument("--dest", help="Exact destination skill directory.")
    codex.add_argument("--force", action="store_true", help="Replace existing install.")

    claude = subparsers.add_parser("claude", help="Install for Claude Code.")
    claude.add_argument("--dest", help="Exact destination skill directory.")
    claude.add_argument(
        "--scope",
        choices=("user", "project"),
        default="user",
        help="Install as a personal or project skill.",
    )
    claude.add_argument(
        "--project-dir",
        help="Project root used when --scope project is selected. Defaults to current directory.",
    )
    claude.add_argument("--force", action="store_true", help="Replace existing install.")

    both = subparsers.add_parser("both", help="Install for both Codex and Claude Code.")
    both.add_argument("--force", action="store_true", help="Replace existing installs.")
    both.add_argument(
        "--claude-scope",
        choices=("user", "project"),
        default="user",
        help="Claude install scope when using the both target.",
    )
    both.add_argument(
        "--project-dir",
        help="Project root used when --claude-scope project is selected.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.platform == "codex":
        dest = Path(args.dest).expanduser().resolve() if args.dest else codex_default_dir()
        install_codex(dest, force=args.force)
        print(f"Installed Codex skill at {dest}")
        return 0

    if args.platform == "claude":
        dest = (
            Path(args.dest).expanduser().resolve()
            if args.dest
            else claude_default_dir(args.scope, args.project_dir)
        )
        install_claude(dest, force=args.force)
        print(f"Installed Claude Code skill at {dest}")
        return 0

    codex_dest = codex_default_dir()
    claude_dest = claude_default_dir(args.claude_scope, args.project_dir)
    install_codex(codex_dest, force=args.force)
    install_claude(claude_dest, force=args.force)
    print(f"Installed Codex skill at {codex_dest}")
    print(f"Installed Claude Code skill at {claude_dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
