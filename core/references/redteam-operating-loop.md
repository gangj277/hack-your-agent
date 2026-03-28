# Red-Team Operating Loop

Use this file for the detailed workflow after the scope gate passes.

## Phase 0: Bootstrap

- Create or refresh `redteam/` with `python3 ../../../scripts/init_redteam_run.py --target "<target>"`.
- Record scope assumptions before running any probe.
- Decide up front whether you may only write reports and tests, or whether patch suggestions are also allowed.

## Phase 1: Architecture Mapping

Map the full agent path from input to action:

- model entry points
- system or developer prompts
- prompt assembly code
- tool definitions and schemas
- MCP server configuration
- retrieval and ranking code
- memory persistence and replay
- approvals, authz, and policy checks
- output sinks and side effects

Search fast before reading deeply. Good starting patterns:

```bash
rg -n "system prompt|developer prompt|messages\\s*=|tool_choice|tools\\s*=|mcp|retriev|vector|embed|memory|history|approval|auth|allow|shell|exec|write_file|send_email|browser|fetch"
```

Populate `redteam/architecture-map.md` using the shared template.

## Phase 2: Trust-Boundary Mapping

For each component, label one trust class:

- trusted control logic
- semi-trusted configuration
- user-controlled content
- third-party metadata
- untrusted external content
- persistent state
- side-effecting sink

Then draw the actual flows:

- content source
- parser or transport
- prompt or state injection point
- decision node
- tool or action sink
- user-visible reporting path

Populate `redteam/threat-surfaces.md`.

## Phase 3: Invariant Selection

Choose the smallest useful set of invariants from `seeded-invariants.md`.

Examples:

- untrusted content must not add objectives
- tool metadata must not expand permissions
- memory entries must not alter policy
- summaries must reflect actual actions

Do not run probes without naming the broken invariant you are testing for.

## Phase 4: Probe Design

Use `attack-taxonomy.md` to choose families and `probe-library.md` to build concrete probes.

Rules:

- start with a control case
- use synthetic canaries and harmless markers
- vary only one trust-boundary assumption at a time
- keep probes narrow enough that failure is explainable
- include at least one concealment probe when tools or side effects exist
- after selecting families, seed a concrete matrix with `python3 ../../../scripts/init_redteam_run.py --target "<target>" --families "<family-1>,<family-2>"`

Populate `redteam/trials/trial-matrix.csv` before execution starts.

## Phase 5: Controlled Execution

Order of operations:

1. local fixtures
2. unit or integration tests
3. staging endpoints

Avoid broad or uncontrolled exploration. Prefer replayable harnesses over manual poking.

Use the protocol in `forensic-execution.md`:

- execute one row at a time
- save raw outputs before summarizing
- compare each attack row against its paired control
- update the matrix after every run

## Phase 6: Evidence Capture

For each meaningful result, capture:

- exact input conditions
- attacked surface
- expected invariant
- observed behavior
- whether the issue changed downstream action
- whether the issue was visible to the user
- minimal repro
- likely root cause
- differential against the paired control row

If the behavior is ambiguous, mark it as a hypothesis instead of a finding.

## Phase 7: Hardening And Regression

Every confirmed finding should leave behind:

- a finding file
- an evidence folder
- a regression prompt or fixture
- a hardening action

If patching is allowed, tie the recommendation to the exact trust boundary that failed.
