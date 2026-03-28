
## PRD: Red-Team AI Service Skill for Coding Agents

### 1. Product definition

We are building an **open-source agent skill** that teaches a coding agent how to red-team an **authorized AI service or agentic codebase**. This is not a standalone product, dashboard, or CLI-first security platform. The shipped artifact is a `SKILL.md`-centered bundle with supporting references and a small number of optional helper scripts, designed to work naturally in coding-agent environments. That design matches how both Codex and Claude Code currently structure skills: a skill is centered on `SKILL.md`, can include supporting files and scripts, and is loaded selectively based on description or explicit invocation. ([OpenAI Developers][1])

**One-sentence product thesis:**
Give a coding agent a reusable adversarial playbook so it can inspect an AI service, identify jailbreak and prompt-injection weaknesses, probe tool and memory attack surfaces, and leave behind actionable findings, repros, and regression artifacts.

### 2. Why this needs to exist

The real failure mode in modern AI systems is no longer just “the model says something bad.” The real failure mode is that **untrusted content changes downstream action**: a retrieved document, tool description, MCP server, repo file, memory entry, or browser page causes the agent to exfiltrate data, make an unsafe call, corrupt code, or silently misreport what it did. OpenAI’s agent safety guidance defines prompt injection in exactly these terms, and OWASP distinguishes jailbreaking as a subset of the broader prompt-injection problem. ([OpenAI Developers][2])

Recent public agent evaluations make this much more concrete. AgentDojo was created because static prompt lists are not enough for agents and instead uses realistic tasks and adaptive attacks. A 2026 large-scale public competition on indirect prompt injection showed that frontier agents in **tool-calling, coding, and computer-use** settings were all still vulnerable, and it explicitly highlighted **concealment** as part of the problem: the user may see a clean final answer while the harmful action already happened. MCP-specific work such as MCPTox shows that **tool poisoning through metadata alone** is a real attack surface, and AgentPoison shows that **persistent memory or RAG stores** can be poisoned and later weaponized. ([arXiv][3])

That means the missing thing is not “more jailbreak prompts.” The missing thing is a **developer-native red-team skill** that a coding agent can use against the actual system a builder is shipping.

### 3. Vision

The skill becomes the default adversarial pass a builder runs before trusting an AI feature.

A developer should be able to say, in effect:

> “Use the red-team skill on this repo and staging service. Find where untrusted content can hijack the agent, where tools or MCP definitions can mislead it, where memory persists dangerous instructions, and where the system might hide the compromise from the user.”

The result should not be a vague discussion. It should be concrete engineering output:

* a scoped threat map
* reproducible findings
* severity
* hardening suggestions
* regression tests or regression prompts to keep the issue fixed

### 4. Target users

The first users are:

* engineers building AI products with prompts, tools, MCP, RAG, or memory
* open-source maintainers shipping coding agents or copilots
* infra/security-minded founders who want a red-team pass before launch
* teams using Codex or Claude Code as their main implementation surface

### 5. Product principles

#### 5.1 This is a **manual** skill, not an auto-triggered helper

This skill has side effects. It will inspect the repo, design probes, run controlled tests, and possibly modify local artifacts such as reports or regression cases. Because of that, it should be **manually invoked**, not auto-loaded opportunistically. Claude Code explicitly recommends `disable-model-invocation: true` for side-effectful workflows, and Codex also distinguishes between explicit and implicit skill invocation with scope determined largely by the description. ([Claude API Docs][4])

#### 5.2 Action is the unit of failure, not text

The skill should judge compromise based on **what the target system actually did**, not just whether the model produced a suspicious sentence. This follows both current agent-safety guidance and the newest competition-style evaluations, which care about harmful actions and concealed compromise, not merely text refusals. ([OpenAI Developers][2])

#### 5.3 Trust boundaries matter more than model branding

Robustness does not cleanly track “capability,” and attacks transfer across model families. The skill should therefore attack the **workflow and boundaries** of the service, not assume safety based on which frontier model the builder chose. ([arXiv][5])

#### 5.4 The skill should be instruction-first, script-second

Codex skills are naturally instruction-centric, and its docs explicitly note that instruction-only skills are the default. Claude Code likewise supports heavy use of supporting references while keeping `SKILL.md` focused. The core of this repo should therefore be a strong playbook and taxonomy, with scripts used only where they materially improve repeatability or artifact generation. ([OpenAI Developers][1])

#### 5.5 Safe use is part of the design

This skill must be explicitly scoped to **targets the user owns or is authorized to test**. It should default to local repos, dev environments, and staging endpoints. It should not turn into a live exploit pack, a mass scanner, or an offensive toolkit.

### 6. Problem statement

Builders today can easily assemble:

* a model
* a system prompt
* retrieval
* tools or MCP
* memory
* approval settings
* output formatting

But they usually do **not** have a good way to answer:

* Can retrieved text override my intended policy?
* Can MCP metadata or tool descriptions poison the agent?
* Can a repo file or issue comment act like a hidden adversarial instruction?
* Can memory persist a malicious instruction that later alters behavior?
* Can the agent do something harmful and still tell the user everything is fine?

That is the exact gap this skill should fill.

### 7. Scope

#### In scope for v1

V1 should focus on **AI services and agentic codebases** that a coding agent can reason about with high leverage:

* prompt-based or system-prompted services
* tool-using or MCP-connected services
* RAG-backed or memory-enabled services
* coding assistants or repo-local agents
* staging or dev endpoints exposed by the repo
* local test harnesses and synthetic fixtures

#### Out of scope for v1

V1 should not attempt to be:

* a generic web exploitation framework
* a browser/computer-use attack platform
* a network scanner
* a credential brute-force tool
* a zero-day hunting project
* a public exploit-payload archive

Browser/computer-use can be a later pack, but it should not slow down the initial open-source release.

### 8. Core first-principles model

At the center of the skill is a simple security model:

**An AI service is compromised when untrusted content crosses a trust boundary and changes downstream action in a way the builder did not intend.**

That means the skill should always map these four things:

1. **Entry surfaces**
   Where can adversarial content enter?

2. **Authority illusions**
   Why might the agent treat that content as legitimate?

3. **Sinks / actions**
   What actions could that content influence?

4. **Visibility**
   Would the user actually notice the compromise?

This model reflects both current official guidance and recent agent research. OpenAI now describes effective prompt injection increasingly as a social-engineering problem, not just a malicious string problem, and the 2026 public competition made concealment a first-class evaluation target. ([OpenAI][6])

### 9. Skill behavior

When invoked, the skill should behave like a disciplined adversarial security engineer.

#### Phase 0: Scope gate

Before doing anything else, the skill asks or infers:

* What is the target?
* Is this authorized?
* Is the environment local, dev, or staging?
* What actions are forbidden?
* What credentials or tools are available?
* Is write access allowed, and if so, only for reports/tests or also for patches?

If these answers are missing, the skill should default to the safest possible behavior.

#### Phase 1: Architecture mapping

The skill reads the codebase and builds a map of the AI workflow:

* model entry points
* system/developer prompts
* tool definitions
* MCP configs
* retrieval components
* memory or persistence layers
* approval or permission logic
* endpoints and test harnesses
* output sinks

The output of this phase is an `architecture-map.md` artifact.

#### Phase 2: Trust-boundary mapping

The skill then labels each component by trust level:

* trusted control logic
* semi-trusted configuration
* untrusted external content
* user-controlled content
* third-party tool metadata
* persistent state
* side-effecting sinks

The purpose is to determine **where injection can happen** and **what it can influence**.

#### Phase 3: Invariant selection

For each surface, the skill defines concrete invariants such as:

* untrusted content must not override system policy
* tool metadata must not introduce new objectives
* retrieval results must not expand permissions
* memory entries must not alter future policy or authorization
* user-facing summaries must truthfully reflect actions taken

#### Phase 4: Probe design

The skill chooses a subset of attack families based on the target architecture, then generates **controlled probes**. These should be structured test prompts, malicious fixtures, poisoned metadata samples, synthetic retrieval documents, or repo-local poisoned files, depending on the surface under test.

#### Phase 5: Controlled execution

The skill runs the probes in the narrowest environment possible:

* local fixtures first
* unit/integration tests second
* staging endpoints third
* never broad uncontrolled exploration

#### Phase 6: Evidence capture

For every meaningful result, the skill stores:

* input conditions
* exact surface attacked
* observed behavior
* expected invariant
* severity
* minimal repro
* likely root cause

#### Phase 7: Hardening and regression

The skill proposes specific hardening actions and, where possible, leaves behind:

* a regression prompt or fixture
* a failing test or eval stub
* a patch suggestion
* a hardening checklist entry

### 10. Attack taxonomy

The attack taxonomy is the heart of the skill. It should be broad enough to match current frontier failure modes, but structured enough that the coding agent can systematically reason over it instead of merely trying random jailbreak prompts. The taxonomy below is intentionally centered on current agent research and official guidance around prompt injection, MCP risk, and persistent memory risk. ([OWASP Gen AI Security Project][7])

#### 10.1 Direct instruction override and policy leakage

The skill checks whether the target can be manipulated by direct adversarial user input to:

* ignore or reinterpret higher-priority instructions
* reveal hidden prompts or sensitive internal instructions
* weaken refusal boundaries
* treat simulated or role-play framing as authorization

#### 10.2 Indirect prompt injection through external content

The skill checks whether untrusted content in:

* retrieved documents
* emails
* markdown files
* API responses
* logs
* comments
* hidden text blobs

can change the target’s goals or downstream actions.

#### 10.3 Codebase poisoning

Because this is a coding-agent skill, repo-local poisoning is especially important. The skill checks whether files such as:

* `README.md`
* `CONTRIBUTING.md`
* issue descriptions
* PR comments
* test fixtures
* example prompts
* generated code comments

can act as hidden policy sources and redirect the agent.

#### 10.4 Tool and MCP poisoning

The skill checks whether:

* tool descriptions
* tool argument schemas
* MCP server metadata
* tool outputs
* server descriptions

can inject new instructions, expand permissions, or steer the agent toward unsafe actions. This is critical because both OpenAI and Anthropic treat MCP exposure and third-party tools as real trust boundaries, and current research shows tool poisoning is not theoretical. ([OpenAI Developers][8])

#### 10.5 Sink abuse and dangerous action routing

The skill checks whether compromised reasoning can trigger unsafe sinks, including:

* data exfiltration
* silent code changes
* unauthorized writes
* cross-tenant leakage
* destructive or privacy-sensitive tool calls

The key question is not “did the model sound wrong?” but “did the system actually cross a dangerous boundary?”

#### 10.6 Memory and RAG poisoning

The skill checks whether malicious content can be:

* stored in memory
* indexed into retrieval
* replayed later as if trustworthy
* used to alter future tasks or policy

This should include both immediate and delayed compromise patterns.

#### 10.7 Permission and approval confusion

The skill checks whether the target can be tricked into acting as though:

* a user granted approval when they did not
* a document implies authorization
* a tool description expands authority
* environment labels such as “admin,” “internal,” or “trusted” are accepted from content rather than runtime state

#### 10.8 Concealment and false reporting

The skill checks whether the target can perform a harmful or policy-violating action and then:

* omit that fact
* fabricate a clean explanation
* claim success on the intended task while hiding the real action
* misreport the source of its decision

This is a crucial category because modern attack research shows concealed compromise is one of the most practically dangerous forms of agent failure. ([arXiv][5])

#### 10.9 Multi-turn social engineering and long-context drift

The skill checks whether prolonged, plausible, benign-seeming context can gradually erode the target’s safety behavior. This category matters because current prompt injection is increasingly social-engineering shaped rather than purely string shaped. ([OpenAI][6])

### 11. What the skill should optimize for

The skill should optimize for four things:

**Coverage.**
It should notice the major attack surfaces present in a real agentic service.

**Actionability.**
Findings should point to code, config, prompt, tool, or memory changes the builder can make immediately.

**Reproducibility.**
Every high-confidence finding should be easy to replay.

**Credibility.**
The skill should minimize “the model seemed weird” style findings and maximize evidence-backed engineering findings.

### 12. Deliverables produced by the skill

A successful run should create a folder such as `redteam/` in the target repo with artifacts like:

```text
redteam/
  architecture-map.md
  threat-surfaces.md
  summary.md
  findings/
    RT-001.md
    RT-002.md
  evidence/
    RT-001/
    RT-002/
  regressions/
    rt_001_regression.md
    rt_002_regression.md
  hardening-plan.md
```

Each finding file should include:

* title
* target surface
* severity
* exploit preconditions
* observed behavior
* expected invariant
* evidence
* minimal repro
* likely root cause
* hardening recommendation
* regression recommendation

### 13. Severity model

Severity should be based on:

* **impact**: what bad thing becomes possible
* **exploitability**: how easy it is to trigger
* **stealth**: whether the compromise is visible
* **persistence**: whether it can influence future runs
* **scope**: whether the issue stays local or affects multiple tenants/users

A hidden, repeatable memory-poisoning issue should rank higher than a one-off visible prompt leak in a toy path.

### 14. Skill package architecture

The repo should be designed as **one shared core skill body plus platform-specific wrappers**, because both OpenAI and Anthropic support the open Agent Skills standard, but Claude Code adds frontmatter controls such as `disable-model-invocation` and `allowed-tools` that are not simply identical to Codex behavior. ([OpenAI Developers][9])

Recommended structure:

```text
redteam-ai-skill/
  README.md

  core/
    references/
      attack-taxonomy.md
      operating-loop.md
      report-format.md
      hardening-playbook.md
      scope-checklist.md
      seeded-invariants.md
    templates/
      finding-template.md
      regression-template.md
      architecture-map-template.md

  platforms/
    codex/
      redteam-ai/
        SKILL.md
        references -> ../../../core/references
        templates -> ../../../core/templates
        scripts/
    claude/
      redteam-ai/
        SKILL.md
        references -> ../../../core/references
        templates -> ../../../core/templates
        scripts/

  examples/
    vulnerable-rag-service/
    vulnerable-mcp-service/
    vulnerable-coding-agent/

  scripts/
    collect_architecture.py
    create_regression_stub.py
    normalize_findings.py
```

### 15. `SKILL.md` design requirements

The `SKILL.md` should stay concise and operational. Claude Code explicitly recommends keeping `SKILL.md` under roughly 500 lines and moving heavier materials into supporting files. Codex also uses progressive disclosure, starting from metadata and loading the full skill body only when needed. That means the main manifest should focus on mission, invocation rules, workflow, and pointers to deeper references. ([OpenAI Developers][1])

The core `SKILL.md` should contain:

1. mission
2. authorized-use rule
3. invocation arguments
4. scope-gating checklist
5. red-team operating loop
6. attack-suite selection logic
7. evidence and reporting contract
8. hardening output requirements
9. references to deeper docs

For the Claude wrapper, the frontmatter should explicitly disable auto-invocation. The skill should **not** broadly pre-authorize dangerous tools through `allowed-tools`. Claude’s docs note that an active skill with `allowed-tools` can grant access without per-use approval, and its security docs emphasize the importance of approvals and careful treatment of prompt injection. ([Claude API Docs][4])

So the Claude wrapper should look conceptually like:

```markdown
---
name: redteam-ai
description: Manually invoked skill for red-teaming an authorized AI service or agentic codebase for prompt-injection, tool, MCP, memory, and concealment vulnerabilities. Use only on systems you own or are authorized to test.
disable-model-invocation: true
argument-hint: "[target-or-scope]"
---
```

For the Codex wrapper, the description should be tight and explicit because Codex relies on skill metadata for discovery and scope. A mostly instruction-first skill is appropriate there as well. ([OpenAI Developers][1])

### 16. Tooling policy inside the skill

The skill should prefer:

* repo reading
* grep/search
* local tests
* synthetic fixtures
* staging-only calls explicitly provided by the user

It should avoid default reliance on:

* arbitrary internet fetches
* wide network exploration
* unrestricted shell execution
* destructive writes

That design is both safer and more compatible with current agent environments. Anthropic’s security docs explicitly note risky fetch commands like `curl` and `wget` are blocked by default, and both Anthropic and OpenAI recommend limiting tool surface and using approval controls around external integrations. ([Claude API Docs][10])

### 17. What makes this skill different from a “jailbreak prompt pack”

This skill should not be a bag of prompt strings. That would be shallow, easy to copy, and strategically weak.

Its real differentiation is:

* **architecture mapping** before attacking
* **trust-boundary reasoning** instead of random prompting
* **surface-specific probes** for repo, tools, MCP, memory, and sinks
* **concealment checks**
* **repo-local artifacts** builders can actually commit
* **regression generation**
* **hardening recommendations grounded in the exact service**

That is how it becomes something coding-agent users actually install and keep using.

### 18. Success criteria

The skill is successful when:

* it finds real seeded vulnerabilities in intentionally vulnerable demo repos
* its findings are concrete enough that builders can patch them
* it produces low-noise reports rather than generic fear
* it leaves regression artifacts behind
* it works naturally in Codex and Claude Code workflows
* it becomes an obvious addition to “before merge” or “before launch” agent workflows

Internal quality metrics should include:

* actionable finding rate
* false positive rate
* time to first meaningful finding
* percent of findings with minimal repro
* percent of findings convertible into regression artifacts

### 19. Release strategy

The initial open-source release should include:

* the skill itself
* three small vulnerable example targets
* sample reports
* a short hardening playbook
* installation docs for Codex and Claude Code
* a clear responsible-use statement

It should **not** launch with a giant public exploit library. The open-source asset is the **agent skill and methodology**, not a viral dump of dangerous payloads.

### 20. Roadmap

#### Phase 1: Core release

* shared attack taxonomy
* shared reporting contract
* Codex wrapper
* Claude wrapper
* repo analysis + prompt/retrieval/tool attack coverage
* sample vulnerable repos

#### Phase 2: Deeper agent surfaces

* MCP poisoning pack
* memory/RAG poisoning pack
* concealment-focused checks
* regression artifact generation

#### Phase 3: Continuous freshness

* attack packs versioned by surface
* quarterly refreshes to avoid benchmark staleness
* community-submitted safe scenario packs

The case for freshness is real: current public agent evaluations already warn about saturation and obsolescence, and the 2026 public competition explicitly committed to refreshed iterations. ([arXiv][5])

## Important sources and why they matter

**OpenAI Codex Skills docs** explain how Codex skills are packaged, discovered, and loaded, and they support the decision to ship this as an instruction-first `SKILL.md` bundle with supporting references rather than a separate product shell. ([OpenAI Developers][1])

**OpenAI Skills guide** is useful because it makes explicit that skills are versioned bundles around a `SKILL.md` manifest and that the format follows the open Agent Skills standard, which is what makes a shared-core plus platform-wrapper architecture sensible. ([OpenAI Developers][9])

**Claude Code skills docs** matter because they confirm that Claude skills are also `SKILL.md`-centered, support supporting files, allow invocation control, and are the right place to encode a strong red-team playbook. They also justify making this a **manual** skill with tightly controlled tool access. ([Claude API Docs][4])

**OpenAI Safety in Building Agents** is the cleanest product-level definition of prompt injection for agentic systems and grounds the skill’s action-oriented threat model. ([OpenAI Developers][2])

**OWASP LLM01:2025 Prompt Injection** gives the broad taxonomy distinction between prompt injection and jailbreaking and helps anchor the skill’s vocabulary in a standard security framing. ([OWASP Gen AI Security Project][7])

**OpenAI’s March 2026 prompt-injection article** is important because it captures a key frontier insight: prompt injection is increasingly social engineering, so defenses and red teaming must constrain impact rather than merely filter strings. ([OpenAI][6])

**AgentDojo** matters because it shows why agent testing must be dynamic and environment-based rather than a flat test list. It supports the PRD’s insistence on architecture-aware red teaming. ([arXiv][3])

**The 2026 large-scale public competition on indirect prompt injection** is one of the strongest signals for this whole project. It shows that tool-calling, coding, and computer-use agents are all still vulnerable, that concealment matters, and that robustness does not trivially follow from model capability. ([arXiv][5])

**MCPTox** matters because it demonstrates that MCP tool poisoning is a first-class attack surface, which means any serious red-team skill for AI services must inspect tool metadata and MCP boundaries. ([arXiv][11])

**AgentPoison** matters because it shows that long-term memory and RAG stores can be turned into delayed compromise channels, which is exactly why memory-poisoning needs its own pack in the skill. ([arXiv][12])

The next step is turning this PRD into the actual `SKILL.md`, reference files, and repo skeleton.

[1]: https://developers.openai.com/codex/skills/ "Agent Skills – Codex | OpenAI Developers"
[2]: https://developers.openai.com/api/docs/guides/agent-builder-safety/ "Safety in building agents | OpenAI API"
[3]: https://arxiv.org/abs/2406.13352?utm_source=chatgpt.com "AgentDojo: A Dynamic Environment to Evaluate Prompt ..."
[4]: https://docs.anthropic.com/en/docs/claude-code/slash-commands "Extend Claude with skills - Claude Code Docs"
[5]: https://arxiv.org/pdf/2603.15714 "How Vulnerable Are AI Agents to Indirect Prompt Injections? Insights from a Large-Scale Public Competition"
[6]: https://openai.com/index/designing-agents-to-resist-prompt-injection/ "Designing AI agents to resist prompt injection | OpenAI"
[7]: https://genai.owasp.org/llmrisk/llm01-prompt-injection/?utm_source=chatgpt.com "LLM01:2025 Prompt Injection - OWASP Gen AI Security Project"
[8]: https://developers.openai.com/api/docs/guides/tools-connectors-mcp/ "MCP and Connectors | OpenAI API"
[9]: https://developers.openai.com/api/docs/guides/tools-skills/ "Skills | OpenAI API"
[10]: https://docs.anthropic.com/en/docs/claude-code/security "Security - Claude Code Docs"
[11]: https://www.arxiv.org/pdf/2508.14925 "MCPTox: A Benchmark for Tool Poisoning Attack on Real-World MCP Servers"
[12]: https://arxiv.org/abs/2407.12784?utm_source=chatgpt.com "AgentPoison: Red-teaming LLM Agents via Poisoning ..."
