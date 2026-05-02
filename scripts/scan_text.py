#!/usr/bin/env python3
"""Scan untrusted text for prompt injection and protected-data risk."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from aegisgate_common import decision_from_findings, scan_text_common
except ImportError:  # pragma: no cover
    sys.path.append(str(Path(__file__).resolve().parent))
    from aegisgate_common import decision_from_findings, scan_text_common


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan text for AegisGate risk signals.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Text to scan")
    group.add_argument("--file", help="Path to a text file to scan")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8", errors="replace")
    else:
        text = args.text

    findings = scan_text_common(text)
    result = decision_from_findings(findings)
    print(result.to_json())
    return 1 if result.decision == "block" else 0


if __name__ == "__main__":
    raise SystemExit(main())
