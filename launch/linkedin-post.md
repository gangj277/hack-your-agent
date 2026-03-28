# LinkedIn Post

I just open-sourced HackYourAgent:

an adversarial skill bundle for red-teaming coding agents like Codex and Claude Code.

The motivation was simple: most AI security work still feels disconnected from the place builders actually ship. In real agent systems, the failure is often not that the model says something strange. The failure is that untrusted content crosses a trust boundary and changes downstream action.

That can look like:

- a retrieved document overriding policy
- tool or MCP metadata introducing a new objective
- a poisoned memory entry changing future behavior
- an agent performing a side effect and then hiding it in the final summary

HackYourAgent is designed to be run inside coding-agent workflows. It maps the target system, selects relevant attack families, creates paired control and attack trials, saves raw evidence under `redteam/`, and leaves behind regressions and hardening recommendations.

I also added seeded vulnerable example targets so people can see the workflow quickly instead of needing a full production app.

Repo:
https://github.com/gangj277/hack-your-agent

If you are building agentic coding tools, MCP-heavy systems, or memory-enabled assistants, I would genuinely like the hardest feedback.
