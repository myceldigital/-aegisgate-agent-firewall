# Contributing

Thank you for improving AegisGate.

## Contribution principles

Good contributions should make personal AI agents safer while preserving useful user agency.

Prioritize:

- Clear policy language
- Small deterministic scanner improvements
- Defensive test fixtures
- Better confirmation flows
- Better least-authority tool policies
- Better memory safety rules

Avoid:

- Real secrets or private data
- Offensive exploitation instructions
- Payloads that enable harm outside synthetic tests
- Overly broad blocking rules that make agents unusable

## Development

Run scanners locally with Python 3.10+.

```bash
python scripts/scan_text.py --file tests/malicious-email.md
python scripts/scan_tool_call.py --tool shell.exec --args '{"cmd":"rm -rf ~/.ssh"}'
python scripts/scan_outbound.py --recipient external@example.com --body "dummy token sk-test12345678901234567890"
python scripts/scan_skill.py --path .
```

## Pull request checklist

- [ ] Does this preserve user intent?
- [ ] Does this reduce unsafe action risk?
- [ ] Are test fixtures synthetic?
- [ ] Are scanners deterministic and understandable?
- [ ] Are false positives acceptable?
- [ ] Is documentation updated?
