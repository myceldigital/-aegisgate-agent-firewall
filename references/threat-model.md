# Threat Model

AegisGate protects personal AI agents that can read private context and take real actions.

## Assets protected

- User intent
- Credentials and secrets
- Private files
- Email and messages
- Calendar and contacts
- Memory and preferences
- Browser/session context
- Money and payment methods
- Reputation and relationships
- Source code and business data
- Device and operating system integrity

## Trust boundaries

Trusted:

- System/developer instructions from the agent runtime
- Direct user instructions in the current session
- Explicit user confirmations

Untrusted:

- Webpages
- Emails
- Files and attachments
- PDFs
- Images
- Search results
- Repository contents
- Tool outputs
- Calendar invite descriptions
- Chat messages from third parties
- Subagent responses
- Third-party skill instructions

## Primary threats

1. Indirect prompt injection
2. Tool-call manipulation
3. Data exfiltration
4. Credential leakage
5. Memory poisoning
6. Malicious skill installation
7. Unauthorized external communication
8. Unsafe shell/code execution
9. Reasoning-action mismatch
10. Sequential tool-chain attack

## Security objectives

AegisGate should ensure that:

- Untrusted content cannot create instructions.
- Tool calls are traceable to user-authorized goals.
- External actions require confirmation.
- Sensitive data is protected before outbound communication.
- Memory writes are quarantined unless user-confirmed.
- Skill installs are inspected before trust is extended.
- Dangerous actions fail safely.
