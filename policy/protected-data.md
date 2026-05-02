# Protected Data Policy

AegisGate treats the following as protected data. Protected data must not be sent externally, stored in memory, written to logs, or included in prompts unless the user explicitly authorizes that exact use.

## Credentials and secrets

- Passwords
- API keys
- OAuth tokens
- Session cookies
- Private keys
- SSH keys
- Recovery codes
- Database credentials
- Webhook signing secrets
- Cloud provider credentials

## Personal data

- Home addresses
- Phone numbers
- Private email addresses
- Government identifiers
- Passport details
- Driver licence details
- Birth dates when linked to identity
- Contact lists

## Sensitive personal data

- Medical or health data
- Mental health data
- Financial data
- Legal records
- Employment records
- Children's data
- Biometric data

## Business confidential data

- Unpublished source code
- Internal strategy documents
- Contracts
- Pricing models
- Customer lists
- Private board/investor materials
- Trade secrets
- Security architecture

## Default handling

1. Redact before outbound communication.
2. Avoid storing in memory.
3. Avoid logging exact values.
4. Ask for confirmation before using externally.
5. Block exfiltration attempts.

## Redaction examples

- `sk-abc123...` → `[REDACTED_API_KEY]`
- `-----BEGIN PRIVATE KEY-----` → `[REDACTED_PRIVATE_KEY]`
- `password = hunter2` → `password = [REDACTED]`
