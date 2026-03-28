# Frontier Research Snapshot

This file captures the primary-source evidence that shaped HackYourAgent as of 2026-03-28. Use it when updating the skill, defending a finding, or choosing which defenses to recommend.

## Official Guidance

- Fact, 2026-03: OpenAI's [Safety in building agents](https://developers.openai.com/api/docs/guides/agent-builder-safety) recommends keeping tool approvals on, running evals and trace graders, and designing workflows so untrusted data never directly drives agent behavior. It specifically recommends extracting only specific structured fields from external inputs.
  Implication: treat every text-to-action edge as suspicious, especially when arbitrary text can flow into tool parameters or state changes.

- Fact, 2025-11: OpenAI's [Understanding prompt injections: a frontier security challenge](https://openai.com/index/prompt-injections/) frames prompt injection as an evolving frontier problem and advises least privilege, user confirmation for consequential actions, and cautious handling of connected apps.
  Implication: red-team approvals, least-privilege boundaries, and cross-system data access rather than only model refusals.

- Fact, 2026-03: OpenAI's [Designing AI agents to resist prompt injection](https://openai.com/index/designing-ai-agents-to-resist-prompt-injection/) argues that prompt injection behaves more like social engineering across sources and trust boundaries than a single-string exploit.
  Implication: include long-context drift, authority confusion, and concealment checks.

- Fact, current: Anthropic's [Claude Code MCP docs](https://code.claude.com/docs/en/mcp) note that when Claude Code tools are exposed over MCP, the client remains responsible for confirming individual tool calls.
  Implication: explicitly test whether the target incorrectly assumes approvals travel across MCP boundaries or tool wrappers.

- Fact, current: OWASP's [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) lists direct injection, remote or indirect injection, typoglycemia, multi-turn attacks, RAG poisoning, multimodal injection, and agent-specific tool and context poisoning.
  Implication: probe obfuscation, persistence, and tool traces, not only clean-text prompts.

## Frontier Attack Evidence

- Fact, 2024-06: [AgentDojo](https://arxiv.org/abs/2406.13352) introduced a dynamic benchmark with 97 realistic tasks and 629 security test cases for tool-using agents. The authors argue that static prompt lists are not enough because attacks and defenses co-evolve.
  Implication: the skill must map the actual architecture and select probes by surface.

- Fact, 2024-07: [AgentPoison](https://arxiv.org/abs/2407.12784) showed that poisoning long-term memory or RAG stores can produce attack success above 80% with poison rate below 0.1% while barely affecting benign behavior.
  Implication: persistence and delayed-trigger probes are mandatory whenever memory or retrieval exists.

- Fact, 2025-08: [MCPTox](https://arxiv.org/abs/2508.14925) built a benchmark from 45 live MCP servers and 353 authentic tools, generating 1,312 malicious cases. It found widespread tool-poisoning vulnerability, including 72.8% attack success for one evaluated agent and refusal rates under 3% for the best-refusing model.
  Implication: tool and MCP metadata deserve their own attack family even before tool execution begins.

- Fact, 2025-04: [Adaptive Attacks Break Defenses Against Indirect Prompt Injection Attacks on LLM Agents](https://aclanthology.org/2025.findings-naacl.395/) reports bypassing eight existing defenses with adaptive attacks, consistently pushing attack success above 50%.
  Implication: never trust a single defense claim without re-testing against local adaptive variants.

- Fact, 2026-03: [How Vulnerable Are AI Agents to Indirect Prompt Injections? Insights from a Large-Scale Public Competition](https://arxiv.org/abs/2603.15714) describes 464 participants, 272,000 attack attempts, and 8,648 successful attacks across 41 scenarios and 13 frontier models. The paper highlights concealment as a first-class problem and reports success rates from 0.5% to 8.5%, with all models vulnerable.
  Implication: test whether harmful actions can occur while the user-visible summary stays clean.

## Emerging Defenses Worth Testing

- Fact, 2024-03: [Spotlighting](https://arxiv.org/abs/2403.14720) uses provenance-marking transformations so the model can better distinguish sources. In the authors' setup, attack success fell from above 50% to below 2% with minimal task degradation.
  Implication: recommend explicit provenance markers and source labeling where raw text from multiple trust levels is merged.

- Fact, 2025-07: [PromptArmor](https://arxiv.org/abs/2507.15219) prompts an LLM to detect and remove injected content before the main agent sees it. The paper reports false-positive and false-negative rates below 1% on AgentDojo and attack success below 1% after filtering.
  Implication: a scrubber model can be a useful baseline, but it still requires local adversarial testing before trust.

- Fact, 2026-01: [Defense Against Indirect Prompt Injection via Tool Result Parsing](https://arxiv.org/abs/2601.04795) argues that most prompt-only defenses remain brittle and shows stronger results by parsing tool outputs into precise data before the agent consumes them.
  Implication: prefer structured tool returns and schema validation over raw-text tool observations.

- Fact, 2026-02: [AgentSys](https://arxiv.org/abs/2602.07398) isolates worker memory and only allows schema-validated return values to cross back into the main agent. It reports attack success of 0.78% on AgentDojo and 4.25% on ASB while slightly improving benign utility.
  Implication: isolation and memory minimization are now serious design baselines, not optional extras.

## What This Means For HackYourAgent

- Inference: the skill should optimize for trust-boundary mapping, not raw jailbreak creativity.
- Inference: the minimum viable artifact is a finding plus evidence plus regression, not a scary prompt transcript.
- Inference: every serious run should include concealment checks, because frontier evidence shows users may see a clean final answer even after compromise.
- Inference: the strongest hardening recommendations will usually be architectural: structured tool parsing, memory isolation, approvals, least privilege, and provenance-aware routing.
