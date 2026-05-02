#!/usr/bin/env python3
"""Scan outbound content before sending, posting, uploading, or submitting."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from aegisgate_common import Finding, decision_from_findings, scan_text_common
except ImportError:  # pragma: no cover
    sys.path.append(str(Path(__file__).resolve().parent))
    from aegisgate_common import Finding, decision_from_findings, scan_text_common


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan outbound agent content.")
    parser.add_argument("--recipient", default="", help="Recipient, URL, domain, or destination")
    parser.add_argument("--body", required=True, help="Outbound body/content summary")
    parser.add_argument("--goal", default="", help="User-authorized goal summary")
    args = parser.parse_args()

    findings = scan_text_common(args.body)
    base_risk = 3 if args.recipient else 2

    if args.recipient:
        findings.append(Finding(
            rule_id="external_destination",
            severity="medium",
            category="outbound_risk",
            message="Outbound action has an external recipient or destination and requires confirmation.",
            evidence=args.recipient,
        ))

    if not args.goal:
        findings.append(Finding(
            rule_id="missing_user_goal",
            severity="medium",
            category="intent_contract",
            message="No user-authorized goal was supplied for this outbound action.",
            evidence=None,
        ))

    result = decision_from_findings(findings, base_risk=base_risk)
    print(result.to_json())
    return 1 if result.decision == "block" else 0


if __name__ == "__main__":
    raise SystemExit(main())
