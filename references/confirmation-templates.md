# Confirmation Templates

Use these templates when AegisGate requires confirmation.

## External communication

```text
I can send this, but it is an external action. Recipient/destination: [recipient]. Content summary: [summary]. Sensitive data detected: [yes/no]. Please confirm: proceed, cancel, or modify.
```

## Shell command

```text
I can run this command, but it can affect your system. Command summary: [summary]. Files or permissions affected: [scope]. Please confirm: proceed, cancel, or modify.
```

## File deletion or overwrite

```text
This may delete or overwrite files. Target: [path]. Reversibility: [reversible/irreversible/unknown]. Please confirm: proceed, cancel, or create a backup first.
```

## Skill installation

```text
I can install this skill, but it extends the agent's behaviour. I found: [permissions/network/filesystem/shell/memory risks]. Please confirm: install, inspect further, or cancel.
```

## Memory write

```text
I can remember this for future conversations: [memory]. Source: [source]. Please confirm whether I should store it.
```

## Protected data

```text
This action may expose protected data: [category]. I can redact it or proceed only with your explicit confirmation. Please choose: redact, proceed, or cancel.
```
