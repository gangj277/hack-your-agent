# X Thread

## Tweet 1

I open-sourced HackYourAgent.

It red-teams Codex and Claude Code agents for:

- prompt injection
- MCP/tool poisoning
- memory poisoning
- approval confusion
- concealed side effects

And it leaves behind evidence + regressions, not just vibes.

https://github.com/gangj277/hack-your-agent

## Tweet 2

Most "AI red teaming" still misses the real failure mode:

untrusted content changes downstream action.

Not just "the model said something weird" but:

- a retrieved doc overrides policy
- MCP metadata expands authority
- memory replays a poisoned instruction
- the agent hides what it actually did

## Tweet 3

HackYourAgent is the native red-team skill for coding agents.

Instead of a giant eval stack, it runs where builders already work:

- Codex
- Claude Code

## Tweet 4

The workflow is intentionally concrete:

1. map trust boundaries
2. choose attack families that actually exist
3. build paired control + attack trials
4. inspect outputs one by one
5. save evidence under `redteam/`
6. leave a hardening plan + regression artifact

## Tweet 5

I added seeded vulnerable examples so people can see it work fast:

- vulnerable RAG agent
- vulnerable MCP/tool agent
- vulnerable concealment agent

That makes the repo demoable in minutes instead of requiring a full app.

## Tweet 6

The wedge is narrow on purpose.

This is not "general AI safety."

It is:

"before you trust your coding agent, run this."

## Tweet 7

Comparable OSS projects like promptfoo and garak show there is real demand here.

My bet is that the coding-agent-native lane is still underbuilt.

If you’re building with Codex, Claude Code, MCP, tools, or memory, I’d love brutal feedback.

## Tweet 8

If you try it, reply with:

- what target you ran it on
- whether it found anything real
- what felt too loose or too rigid

That feedback will shape the next version.
