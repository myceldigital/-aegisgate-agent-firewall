#!/usr/bin/env python3
"""Scan a proposed tool call before execution."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from aegisgate_common import (
        DANGEROUS_COMMAND_PATTERNS,
        EXTERNAL_ACTION_TOOLS,
        SYSTEM_ACTION_TOOLS,
        Finding,
        decision_from_findings,
        find_patterns,
        scan_text_common,
    )
except ImportError:  # pragma: no cover
    sys.path.append(str(Path(__file__).resolve().parent))
    from aegisgate_common import (
        DANGEROUS_COMMAND_PATTERNS,
        EXTERNAL_ACTION_TOOLS,
        SYSTEM_ACTION_TOOLS,
        Finding,
        decision_from_findings,
        find_patterns,
        scan_text_common,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a proposed agent tool call.")
    parser.add_argument("--tool", required=True, help="Tool name, e.g. shell.exec or gmail.send_email")
    parser.add_argument("--args", default="{}", help="JSON string or plain text summary of tool arguments")
    parser.add_argument("--goal", default="", help="User-authorized goal summary")
    args = parser.parse_args()

    tool = args.tool.lower()
    raw_args = args.args
    combined = f"tool={tool}\nargs={raw_args}\ngoal={args.goal}"

    findings: list[Finding] = []
    findings.extend(scan_text_common(combined))
    findings.extend(find_patterns(combined, DANGEROUS_COMMAND_PATTERNS, "dangerous_command", "critical"))

    base_risk = 0
    if any(marker in tool for marker in EXTERNAL_ACTION_TOOLS):
        findings.append(Finding(
            rule_id="external_action_tool",
            severity="medium",
            category="tool_risk",
            message="Tool appears to perform an external or reputational action requiring confirmation.",
            evidence=args.tool,
        ))
        base_risk = max(base_risk, 3)

    if any(marker in tool for marker in SYSTEM_ACTION_TOOLS):
        findings.append(Finding(
            rule_id="system_action_tool",
            severity="high",
            category="tool_risk",
            message="Tool appears to perform system, filesystem, credential, or execution actions.",
            evidence=args.tool,
        ))
        base_risk = max(base_risk, 4)

    # Lightweight argument parsing for more useful evidence.
    try:
        parsed = json.loads(raw_args)
        if isinstance(parsed, dict):
            for key in parsed:
                key_lower = str(key).lower()
                if key_lower in {"password", "token", "secret", "api_key", "apikey", "private_key"}:
                    findings.append(Finding(
                        rule_id="sensitive_argument_key",
                        severity="critical",
                        category="protected_data",
                        message="Tool arguments contain a sensitive key name.",
                        evidence=key_lower,
                    ))
    except json.JSONDecodeError:
        pass

    result = decision_from_findings(findings, base_risk=base_risk)
    print(result.to_json())
    return 1 if result.decision == "block" else 0


if __name__ == "__main__":
    raise SystemExit(main())
