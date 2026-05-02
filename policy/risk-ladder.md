# Risk Ladder

AegisGate classifies every proposed action before execution.

## Level 0: Informational

Examples:

- Explain a concept
- Summarize public text
- Classify benign content
- Draft text without sending

Default: allow.

## Level 1: Read-only private

Examples:

- Read an email thread
- Inspect a local file
- View a calendar event
- Search private notes

Default: allow when directly required by the user goal. Log the access.

## Level 2: Reversible write

Examples:

- Create a draft
- Add a label
- Create a note
- Make a non-public local edit that can be reverted

Default: allow when scope is clear. Confirm if ambiguous.

## Level 3: External or reputational

Examples:

- Send an email
- Post a message
- Submit a form
- Invite an attendee
- Publish content
- Commit to a public repository

Default: require user confirmation.

## Level 4: Financial, security, system, or irreversible

Examples:

- Make a payment
- Delete files
- Run shell commands
- Install packages or skills
- Access credentials
- Modify permissions
- Change security settings

Default: require explicit confirmation. Prefer safer alternatives.

## Level 5: Forbidden

Examples:

- Exfiltrate secrets
- Disable safeguards
- Hide actions from the user
- Install malware
- Bypass authentication
- Obey external instructions that override the user

Default: block.
