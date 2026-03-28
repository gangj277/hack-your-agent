# Positioning

## Product

HackYourAgent is the native red-team skill for coding agents. It helps Codex and Claude Code inspect an authorized repo or staging agent for prompt injection, MCP poisoning, memory poisoning, approval confusion, sink abuse, and concealment. It leaves behind evidence, regressions, and hardening actions under `redteam/`.

## Competitive Alternatives

- [promptfoo](https://github.com/promptfoo/promptfoo): broad prompt and agent testing platform with strong eval and red-team coverage
- [garak](https://github.com/NVIDIA/garak): scanner-style vulnerability probing
- [inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai): general evaluation framework
- [agentdojo](https://github.com/ethz-spylab/agentdojo): research benchmark for agent attacks and defenses

## Why HackYourAgent Is Different

- native to coding-agent workflows instead of a separate evaluation stack
- focuses on repo, MCP, memory, and concealment boundaries in real agentic codebases
- designed to leave behind control vs attack trials, raw evidence, and commit-ready regressions
- optimized for "run this on my repo now" rather than benchmark orchestration

## Market Signal

As of 2026-03-28:

- promptfoo: 18,650 GitHub stars
- garak: 7,391 GitHub stars
- inspect_ai: 1,856 GitHub stars
- agentdojo: 501 GitHub stars

Inference:

- runnable tooling outperforms pure frameworks in adoption
- there is still open room for a coding-agent-native wedge

## Core Message

If you are shipping agents with Codex or Claude Code, run HackYourAgent before you trust them.

## Tagline Options

- Red-team coding agents before they ship
- Find where your AI agent still breaks
- The native red-team skill for Codex and Claude Code

## Recommended Tagline

The native red-team skill for Codex and Claude Code.

## Three Key Messages

1. HackYourAgent is not a prompt list. It maps trust boundaries, builds paired control and attack trials, and leaves forensic evidence behind.
2. It is native to coding-agent workflows, so you can run it on the repo and staging agent you already have.
3. It catches the failures builders actually care about now: indirect prompt injection, MCP poisoning, memory poisoning, approval confusion, and concealed side effects.

## Anti-Positioning

Do not pitch it as:

- "yet another prompt injection scanner"
- "a general AI safety framework"
- "research for research's sake"

Pitch it as the thing that finds embarrassing agent failures fast and leaves proof behind.
