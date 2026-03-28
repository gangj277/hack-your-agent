# Reporting Contract

Use this file to decide what counts as a real finding and how to record it.

## A Finding Must Contain

- title
- target surface
- broken invariant
- severity
- exploit preconditions
- exact input conditions
- observed behavior
- expected behavior
- minimal repro
- likely root cause
- hardening recommendation
- regression recommendation

If any item is missing, treat the result as a draft or hypothesis.

## Severity Model

Score each dimension from 1 to 5:

- impact: what harmful capability became possible
- exploitability: how easy it is to trigger
- stealth: how likely the issue is to stay hidden from the user
- persistence: whether it can affect future runs
- scope: whether the blast radius is local or multi-user

Suggested mapping:

- 21-25: Critical
- 16-20: High
- 11-15: Medium
- 6-10: Low
- 0-5: Informational or hardening gap

Escalate by one band if concealment or cross-tenant exposure is present.

## Evidence Rules

- Save exact probe inputs and relevant outputs.
- Save the tool trace or test log if any side effect occurred.
- Keep one control case and one malicious case when possible.
- Avoid screenshots as the only evidence if a text trace exists.
- Update the trial matrix row status after every execution.
- Do not promote a row to a finding unless the paired control and attack both exist and are materially different.
- Save concealment reconciliation notes whenever a sink is touched.

## Regression Rules

- Regressions must be replayable by another engineer.
- Prefer a fixture, test, or eval over prose alone.
- If code changes are allowed, point to the exact file or gate that should enforce the invariant.

## Directory Layout

- `redteam/summary.md`: ranked overview and scope notes
- `redteam/architecture-map.md`: system structure and trust boundaries
- `redteam/threat-surfaces.md`: attackable surfaces and invariants
- `redteam/findings/RT-XXX.md`: one file per issue
- `redteam/evidence/RT-XXX/`: logs, traces, fixtures
- `redteam/regressions/`: prompts, fixtures, tests, or eval stubs
- `redteam/trials/trial-matrix.csv`: control and attack execution plan
- `redteam/trials/RTT-XXX.md`: per-trial forensic dossier
- `redteam/hardening-plan.md`: prioritized fixes and owners
