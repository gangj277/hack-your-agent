# Demo Script

Goal: record a 30-60 second proof-first demo that shows a real seeded weakness getting surfaced by HackYourAgent.

## Demo Target

Use `examples/vulnerable-rag-agent` first. It is the easiest to understand quickly.

## Terminal Flow

```bash
cd HackYourAgent
python3 scripts/install_skill.py both
```

Then in the coding agent:

```text
Use $hack-your-agent on examples/vulnerable-rag-agent.
Write only to redteam/ artifacts.
Build a paired control/attack trial matrix, inspect outputs one by one,
and leave findings, evidence, and hardening actions.
```

## What To Show On Screen

1. The repo root and the example target.
2. The skill install command.
3. The prompt invoking HackYourAgent.
4. `redteam/trials/trial-matrix.csv`.
5. One trial dossier under `redteam/trials/`.
6. One evidence note under `redteam/evidence/`.
7. One finding showing the broken trust boundary.

## Demo Narration

- "This repo has a seeded vulnerable RAG agent."
- "HackYourAgent creates paired control and attack trials instead of throwing random jailbreak prompts."
- "It saves raw evidence under `redteam/` and only promotes a result to a finding after comparing attack behavior against a clean control."
- "Here it flags that retrieved markdown is being merged into a high-authority system prompt."

## Recording Tips

- Keep the terminal zoomed in.
- Do not scroll excessively.
- Show the file tree and the resulting artifact tree.
- End on the finding and the hardening recommendation.
