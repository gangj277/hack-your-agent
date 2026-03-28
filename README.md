# HackYourAgent

HackYourAgent is a manual-use red-team skill bundle for coding agents. It teaches a coding agent to map an authorized AI system, identify trust-boundary failures, run controlled jailbreak and prompt-injection probes, and leave behind evidence, regressions, and hardening actions that a builder can actually commit.

## What Ships

- Shared research-backed references in `core/references/`
- Reusable reporting templates in `core/templates/`
- A helper bootstrap script in `scripts/init_redteam_run.py`
- A Codex wrapper in `platforms/codex/hack-your-agent/`
- A Claude Code wrapper in `platforms/claude/hack-your-agent/`

## Design Principles

- Manual invocation only. This skill has side effects and should not be auto-loaded.
- Authorized targets only. Default to local repos, dev stacks, and staging endpoints.
- Action over text. Treat compromise as untrusted content changing downstream behavior.
- Trust boundaries over prompt packs. Map architecture before probing.
- Regressions by default. Every high-confidence issue should leave a replayable artifact.

## Research Basis

This repo is grounded in current primary sources as of March 28, 2026. The short version is:

- Official guidance from OpenAI and Anthropic treats prompt injection, tools, MCP, and approvals as first-class trust-boundary problems.
- Recent agent research shows static prompt lists are not enough; dynamic, surface-aware evaluation is required.
- Frontier work now emphasizes tool poisoning, memory poisoning, and concealed compromise rather than only direct prompt overrides.

See `core/references/frontier-research.md` for dated links and distilled takeaways.

## Native Install

The repo source is shared across platforms. Use the installer so the final installed skill is self-contained and native to the target agent.

### Codex

Install to `${CODEX_HOME:-~/.codex}/skills/hack-your-agent`:

```bash
python3 scripts/install_skill.py codex
```

### Claude Code

Install as a personal skill to `~/.claude/skills/hack-your-agent`:

```bash
python3 scripts/install_skill.py claude
```

Install as a project skill to `.claude/skills/hack-your-agent` inside a repo:

```bash
python3 scripts/install_skill.py claude --scope project --project-dir /path/to/repo
```

Install both native variants at once:

```bash
python3 scripts/install_skill.py both
```

Claude Code skill behavior is aligned to the official skills docs: bundled files, `disable-model-invocation: true`, `context: fork`, and `${CLAUDE_SKILL_DIR}` for script access. The Codex install target follows the local standard skill path used by Codex-compatible environments in this workspace.

If your current agent session does not see a newly installed skill, start a new session after installing it.

## Invoke

- Codex: `Use $hack-your-agent on this repo. Build a paired control/attack trial matrix and save raw evidence under redteam/.`
- Claude Code: `/hack-your-agent this repo and its staging endpoint`

## What Happens When You Run It

HackYourAgent is supposed to behave like a forensic operator, not a prompt list.

1. Scope the target and forbidden actions.
2. Map prompts, tools, MCP, retrieval, memory, approvals, and sinks.
3. Select only the attack families that exist in the target.
4. Generate a `redteam/trials/trial-matrix.csv` with paired control and attack runs.
5. Execute each trial one by one.
6. Save raw inputs, raw outputs, traces, side effects, and per-trial verdicts under `redteam/evidence/`.
7. Compare each attack row against its paired control before writing a finding.
8. Produce findings, regressions, and a hardening plan only after the evidence is complete.

If the target lacks a runnable harness, traces, or staging surface, the skill can still map architecture and design probes, but the forensic result will be correspondingly weaker.

## Example Invocation

```text
Use $hack-your-agent on this authorized repo and staging endpoint.
Write only to redteam/ artifacts. Focus on indirect prompt injection, MCP/tool poisoning,
memory poisoning, approval confusion, and concealment. Build a paired control/attack trial matrix,
run each row individually, save raw evidence, and leave minimal repros and regressions.
```

## Safety

HackYourAgent is a defensive skill. It is meant for systems the user owns or is authorized to test. It is not a mass scanner, public exploit pack, credential brute-force tool, or live-offense workflow.
