# Show HN

## Recommended Title

Show HN: HackYourAgent - red-team Codex and Claude Code agents

## Alternate Titles

- Show HN: HackYourAgent - find prompt injection and MCP poisoning in coding agents
- Show HN: HackYourAgent - a native red-team skill for Codex and Claude Code

## Post Body

Hi HN,

I built HackYourAgent because most agent security tooling still felt too far away from the actual place builders work.

If you are using Codex or Claude Code, the failure mode is usually not just "the model said something weird." The real failure mode is that untrusted content crosses a trust boundary and changes downstream action: a retrieved document, tool description, MCP server, memory entry, or repo file causes the agent to do something it should not do, and sometimes to hide that it happened.

HackYourAgent is an open-source skill bundle that runs inside coding-agent workflows. It maps the repo or staging agent, selects relevant attack families, creates paired control and attack trials, and saves findings, evidence, regressions, and hardening actions under `redteam/`.

I also included seeded vulnerable example targets for:

- indirect prompt injection through retrieved docs
- tool and MCP poisoning
- concealment where the final summary hides a side effect

The main idea is to make this feel like "run this on my repo now," not "set up a whole evaluation framework first."

If this sounds useful, I would especially love feedback from people building agentic coding tools, MCP-heavy systems, or anything with memory and tool calls.

Repo:
https://github.com/gangj277/hack-your-agent

## Opening Comment If Asked "How Is This Different From promptfoo Or garak?"

Promptfoo and garak are both strong tools, but they sit in a different part of the workflow.

HackYourAgent is narrower: it is meant to be the native red-team skill for coding-agent environments like Codex and Claude Code. The emphasis is on repo-local trust boundaries, MCP/tool metadata, memory, and concealment, with paired control-vs-attack evidence and commit-ready regressions.

## Opening Comment If Asked "Why A Skill Instead Of A CLI?"

Because the user’s agent is already the thing reading the repo, inspecting prompts, tracing tools, and writing the fix artifacts.

The skill format lets the adversarial workflow live where the implementation workflow already happens, instead of forcing people into a separate stack first.

## Opening Comment If Asked "What Should I Try First?"

Start with the seeded examples in the repo, especially `examples/vulnerable-rag-agent`.

The fast path is:

1. install the skill
2. run it on the vulnerable example
3. inspect `redteam/trials/` and `redteam/findings/`

That makes the before-and-after workflow obvious very quickly.
