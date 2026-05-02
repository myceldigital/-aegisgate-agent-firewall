# Security Policy

AegisGate is a defensive security project for personal AI agents.

## Reporting vulnerabilities

If you find a vulnerability, open a GitHub issue with:

- affected file or behaviour
- reproduction steps
- expected behaviour
- actual behaviour
- suggested mitigation, if available

Do not include real credentials, secrets, private keys, or sensitive personal data in reports.

## Scope

In scope:

- Prompt-injection bypasses
- Unsafe tool-call approvals
- Data-loss detection failures
- Memory-poisoning failures
- Skill-install scanning failures
- Scanner false negatives on common dangerous patterns

Out of scope:

- Requests to build offensive payloads
- Requests to bypass third-party systems
- Real secret collection or disclosure

## Safe research standard

Use synthetic fixtures and dummy credentials only.
