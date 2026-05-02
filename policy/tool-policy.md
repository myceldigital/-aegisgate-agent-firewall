# Tool Policy

Every proposed tool call must be checked against the user's authorized goal.

## Required preflight checks

1. What user goal authorizes this tool call?
2. What data will the tool access?
3. What data will the tool modify?
4. Could the action affect money, reputation, identity, files, memory, credentials, or permissions?
5. Is the tool call read-only, reversible, or irreversible?
6. Is the tool call broader than necessary?
7. Is the tool call based on untrusted content?

## High-risk tool categories

Require confirmation for:

- Shell commands
- Code execution
- Package installation
- Skill installation
- File deletion or overwrite
- Git pushes or public commits
- Email/message sending
- Calendar invitation changes
- Payments or purchases
- Browser form submissions
- Credential or secret access
- Permission changes
- Database writes
- API calls to production services

## Forbidden tool behaviour

Block tools that:

- hide actions from the user
- bypass confirmation
- disable safety checks
- exfiltrate secrets
- send data to unknown external domains
- execute remote scripts without inspection
- modify security settings without explicit authorization

## Principle of least authority

Prefer the narrowest available tool and smallest possible scope. A read-only tool should be used before a write tool. A draft should be created before a message is sent. A preview should be shown before a destructive change.
