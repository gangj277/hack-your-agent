# Attack Taxonomy

Use this taxonomy to pick surfaces that actually exist in the target. Do not spray all categories blindly.

## 1. Direct Instruction Override And Policy Leakage

- Entry surfaces: raw user input, chat history, copied prompts, issue descriptions, CLI arguments
- What to test: can lower-priority text override higher-priority instructions, leak hidden prompts, or fake authorization through role-play
- Compromise looks like: hidden instructions revealed, permission checks skipped, or task goals changed by raw user text
- Common fixes: stronger policy separation, explicit refusal invariants, approval checks backed by runtime state

## 2. Indirect Prompt Injection Through External Content

- Entry surfaces: retrieved docs, API responses, web pages, emails, logs, markdown, hidden comments
- What to test: can untrusted content inject instructions that alter later reasoning or actions
- Compromise looks like: agent follows instructions from data instead of using data as input
- Common fixes: provenance markers, data and instruction separation, structured extraction, scrubbers, staged review

## 3. Codebase Poisoning

- Entry surfaces: `README.md`, `CONTRIBUTING.md`, issue bodies, PR comments, fixtures, examples, generated comments
- What to test: can repo-local text become a hidden policy source for a coding agent
- Compromise looks like: unauthorized edits, incorrect task prioritization, or files treated as policy instead of context
- Common fixes: repo source trust labels, ignore lists, restricted file classes, human confirmation before high-risk edits

## 4. Tool And MCP Poisoning

- Entry surfaces: tool descriptions, tool schemas, server metadata, capability lists, tool outputs
- What to test: can metadata or outputs add objectives, expand permissions, or redirect execution before any legitimate task need exists
- Compromise looks like: unnecessary tool calls, unsafe tool selection, or schema fields used to smuggle instructions
- Common fixes: least-privilege tools, explicit approval nodes, structured tool parsing, trusted-server allowlists, metadata review

## 5. Sink Abuse And Dangerous Action Routing

- Entry surfaces: any compromised reasoning path that reaches a sink
- What to test: can poisoned content route the agent into shell, file writes, outbound network, email, or tenant data actions
- Compromise looks like: side effects not justified by the user task
- Common fixes: policy gates at sinks, approval requirements, dry-run mode, canary checks, per-sink allowlists

## 6. Memory And RAG Poisoning

- Entry surfaces: vector stores, long-term memory tables, cached summaries, session state, replay buffers
- What to test: can poisoned content persist and later reactivate as if trustworthy
- Compromise looks like: delayed trigger behavior, cross-task drift, or repeated unsafe decisions after a poisoned write
- Common fixes: write-time validation, trust labels, TTLs, review queues, memory isolation, worker-context trimming

## 7. Permission And Approval Confusion

- Entry surfaces: documents that claim authority, tool text that implies approval, labels like `admin` or `internal`, stale cached approvals
- What to test: can content or metadata impersonate runtime authorization
- Compromise looks like: actions occurring without real user confirmation or beyond current principal privileges
- Common fixes: runtime-backed auth checks, ephemeral approvals, signed state instead of text assertions

## 8. Concealment And False Reporting

- Entry surfaces: any attack that also instructs the agent to hide what happened
- What to test: can the agent act unsafely and still report a clean outcome
- Compromise looks like: missing tool calls in the final summary, fabricated reasons, or omission of side effects
- Common fixes: trace-to-summary reconciliation, action receipts, immutable audit logs, summary graders

## 9. Multi-Turn Social Engineering And Long-Context Drift

- Entry surfaces: prolonged chats, ticket threads, planning docs, slowly escalating context
- What to test: can plausible benign context erode safety over time without a single obvious injection string
- Compromise looks like: gradual policy drift, unsafe deference, or relaxed approval behavior late in the conversation
- Common fixes: periodic re-grounding on invariants, context pruning, resettable worker contexts, repeated authorization checks
