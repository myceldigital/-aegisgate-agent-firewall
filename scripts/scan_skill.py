#!/usr/bin/env python3
"""Scan an Agent Skill folder or repository before installation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from aegisgate_common import DANGEROUS_COMMAND_PATTERNS, Finding, decision_from_findings, find_patterns, scan_text_common
except ImportError:  # pragma: no cover
    sys.path.append(str(Path(__file__).resolve().parent))
    from aegisgate_common import DANGEROUS_COMMAND_PATTERNS, Finding, decision_from_findings, find_patterns, scan_text_common

SUSPICIOUS_FILES = {
    ".env",
    "id_rsa",
    "id_ed25519",
    "authorized_keys",
}

AUTO_RUN_FILES = {
    ".bashrc",
    ".zshrc",
    ".profile",
    "postinstall.sh",
    "install.sh",
}

SCAN_EXTENSIONS = {".md", ".py", ".js", ".ts", ".sh", ".json", ".yaml", ".yml", ".toml", ".txt"}


def iter_files(root: Path):
    for path in root.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a skill folder before installation.")
    parser.add_argument("--path", required=True, help="Skill folder or repository path")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    findings: list[Finding] = []
    base_risk = 4

    if not root.exists():
        findings.append(Finding("missing_path", "critical", "skill_scan", "Path does not exist", str(root)))
        result = decision_from_findings(findings, base_risk=5)
        print(result.to_json())
        return 1

    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        findings.append(Finding(
            "missing_skill_md",
            "high",
            "skill_install",
            "No SKILL.md found. Agent skill cannot be safely evaluated against declared behaviour.",
            str(skill_md),
        ))

    for path in iter_files(root):
        rel = path.relative_to(root).as_posix()
        lower_name = path.name.lower()
        if lower_name in SUSPICIOUS_FILES:
            findings.append(Finding("suspicious_file", "high", "skill_install", "Skill contains credential-like file name.", rel))
        if lower_name in AUTO_RUN_FILES:
            findings.append(Finding("autorun_file", "high", "skill_install", "Skill contains install/startup-style file requiring review.", rel))
        if path.suffix.lower() in SCAN_EXTENSIONS:
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for finding in scan_text_common(text):
                finding.evidence = f"{rel}: {finding.evidence}"
                findings.append(finding)
            for finding in find_patterns(text, DANGEROUS_COMMAND_PATTERNS, "dangerous_command", "critical"):
                finding.evidence = f"{rel}: {finding.evidence}"
                findings.append(finding)

    result = decision_from_findings(findings, base_risk=base_risk)
    print(result.to_json())
    return 1 if result.decision == "block" else 0


if __name__ == "__main__":
    raise SystemExit(main())
