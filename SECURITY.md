# Security Policy

HackYourAgent is a defensive project for red-teaming systems you own or are authorized to test.

## Scope

This repository includes:

- defensive skill bundles for Codex and Claude Code
- seeded vulnerable example targets intended for local testing and demos
- research-backed red-team guidance for prompt injection, MCP poisoning, memory poisoning, approval confusion, sink abuse, and concealment

The examples are intentionally vulnerable. Do not deploy them.

## Responsible Use

Use HackYourAgent only against:

- your own repos
- your own development or staging systems
- targets you are explicitly authorized to test

Do not use this project for:

- mass scanning
- credential theft
- production exploitation
- unauthorized testing
- destructive actions on third-party systems

## Reporting A Security Issue In This Repository

If you find a vulnerability in the HackYourAgent code itself, open a private report instead of publishing an exploit first.

Suggested process:

1. Email the maintainer or use GitHub private vulnerability reporting if enabled.
2. Include reproduction steps, affected files, and impact.
3. Allow time for acknowledgement and remediation before public disclosure.

## Example Targets

The contents of `examples/` are deliberately unsafe by design so users can test the skill on realistic seeded flaws. Findings against those example targets are expected behavior, not vulnerabilities in the main project.
