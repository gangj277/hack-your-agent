# Scope Checklist

Run this before any testing. If authorization is unclear, stop.

## Required Questions

- What exact repo, service, or staging endpoint is in scope?
- Is the user authorized to test it?
- Is the environment local, development, or staging?
- Which actions are forbidden?
- Is network access allowed, and if so, only to which hosts?
- Is write access allowed, and if so, only for reports and tests or also for patches?
- Which credentials, secrets, and third-party tools are available?
- Which sinks are high risk: filesystem writes, shell execution, outbound network, email, payments, tenant data, or admin actions?

## Safe Defaults

If any answer is missing, assume:

- local-first execution
- no production targets
- no real-user data
- no destructive writes
- no outbound network beyond explicitly named staging services
- write scope limited to `redteam/` artifacts and new regression fixtures
- canaries instead of real secrets

## Stop Conditions

Do not proceed if:

- authorization is missing or disputed
- the only target is production
- the task requires real credential harvesting or broad scanning
- the user asks for public exploit payloads instead of defensive validation

## Preflight Notes To Record

Add these to `redteam/summary.md` before running probes:

- target
- scope owner
- environment
- forbidden actions
- writable areas
- available test harnesses
- high-risk sinks
- assumptions taken because information was missing
