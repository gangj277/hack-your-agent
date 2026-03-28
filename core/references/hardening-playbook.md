# Hardening Playbook

Use this after a finding is confirmed. Match the recommendation to the failed trust boundary.

## 1. Separate Data From Instructions

- Keep untrusted text out of system or developer prompt slots.
- Pass external content as data only, preferably with explicit provenance labels.
- Where possible, summarize or extract structured fields before the planner sees raw text.

Why: OpenAI guidance and Spotlighting both point to provenance separation as a core defense.

## 2. Parse Tool Results Into Schemas

- Convert raw tool output into validated JSON, enums, or typed fields before handing it to the planner.
- Drop free-form residue that looks like instructions, URLs to visit next, or capability claims.
- Reject or quarantine malformed results instead of "best effort" parsing them into the main context.

Why: Tool Result Parsing and AgentSys both show that structured crossings beat raw-text trust.

## 3. Reduce Tool And MCP Authority

- Use allowlists for trusted MCP servers and high-risk tools.
- Scope tools by task and environment; do not expose broad shell or network access if a narrower tool exists.
- Require explicit approval for sensitive reads and writes, not just writes.
- Log which data was sent to which tool or server.

Why: MCPTox shows metadata alone can redirect capable agents before execution begins.

## 4. Isolate Memory

- Separate transient worker context from long-lived planner memory.
- Add write-time validation before memory or RAG ingestion.
- Store trust labels, source IDs, TTLs, and review state with each memory entry.
- Prefer short-lived task memory over indefinite accumulation.

Why: AgentPoison and AgentSys both show persistence is a major attack and defense surface.

## 5. Make Approvals Runtime-Backed

- Tie approval to a concrete principal, action, scope, and expiry.
- Never infer approval from repo text, tool descriptions, or prior conversations alone.
- Re-check approvals when a plan expands scope or adds a new sink.

Why: agent systems fail when content can impersonate authority.

## 6. Detect Concealment

- Compare final summaries against the actual trace of tool calls and side effects.
- Generate action receipts for sinks such as filesystem writes, shell commands, emails, or outbound requests.
- Add graders or assertions that fail if a summary omits a real action.

Why: the 2026 public competition shows concealed compromise is practical and dangerous.

## 7. Use A Layered Defense, Then Re-Test Adaptively

- Combine source separation, structured parsing, approvals, isolation, and monitoring.
- If using a detector or scrubber model, treat it as one layer rather than the whole defense.
- Re-run the same family with mild variants and obfuscations after every mitigation.

Why: adaptive-attack results show brittle single defenses fail under targeted pressure.

## 8. Leave Regressions Behind

- Preserve the minimal malicious fixture or prompt that reproduced the issue.
- Add a failing test, eval, or trace assertion before shipping the fix.
- Keep one clean control and one malicious variant so future regressions stay interpretable.

Why: without a replayable artifact, the fix will drift or be disputed later.
