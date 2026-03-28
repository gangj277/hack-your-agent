# Vulnerable RAG Agent

This example is intentionally vulnerable. It demonstrates the classic mistake of taking retrieved content and placing it directly into a high-authority prompt block.

## Seeded Weakness

`app/agent.py` assembles the prompt like this:

- trusted system prompt
- raw retrieved documents, joined directly into the same message
- user request

That means a poisoned retrieved document can look like data while actually changing downstream behavior.

## Files To Inspect

- `app/agent.py`
- `prompts/system_prompt.md`
- `kb/employee-handbook.md`
- `kb/vendor-onboarding-note.md`

## What HackYourAgent Should Catch

- the trust boundary between retrieved markdown and control instructions is broken
- a malicious document can add objectives or permission claims
- the hardening recommendation should point toward provenance separation or structured extraction
