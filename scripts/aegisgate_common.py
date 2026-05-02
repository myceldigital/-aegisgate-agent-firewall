#!/usr/bin/env python3
"""Shared utilities for AegisGate scanners."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from typing import Iterable


@dataclass
class Finding:
    rule_id: str
    severity: str
    category: str
    message: str
    evidence: str | None = None


@dataclass
class ScanResult:
    decision: str
    risk_level: int
    findings: list[Finding] = field(default_factory=list)
    summary: str = ""

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)


PROMPT_INJECTION_PATTERNS: list[tuple[str, str]] = [
    (r"ignore (all )?(previous|prior|above) instructions", "Attempts to override prior instructions"),
    (r"disregard (all )?(previous|prior|above) instructions", "Attempts to override prior instructions"),
    (r"system prompt", "References hidden/system prompt"),
    (r"developer message", "References developer message"),
    (r"reveal (your )?(hidden|system|developer)", "Attempts to reveal hidden instructions"),
    (r"do not tell the user", "Attempts to conceal behaviour from user"),
    (r"hide this from the user", "Attempts to conceal behaviour from user"),
    (r"call the tool", "External content attempts to trigger tool use"),
    (r"run (this|the) command", "External content attempts to trigger execution"),
    (r"install (this|the) (package|skill|extension)", "External content attempts to trigger installation"),
    (r"send .* (api key|password|token|secret)", "Attempts to exfiltrate secrets"),
    (r"base64", "Potential encoded payload marker"),
]

SECRET_PATTERNS: list[tuple[str, str]] = [
    (r"sk-[A-Za-z0-9_\-]{20,}", "Possible OpenAI-style API key"),
    (r"ghp_[A-Za-z0-9_]{20,}", "Possible GitHub personal access token"),
    (r"github_pat_[A-Za-z0-9_]{20,}", "Possible GitHub fine-grained token"),
    (r"AKIA[0-9A-Z]{16}", "Possible AWS access key ID"),
    (r"-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----", "Possible private key"),
    (r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*[^\s]{8,}", "Possible named secret"),
    (r"(?i)session[_-]?cookie\s*[:=]", "Possible session cookie"),
]

DANGEROUS_COMMAND_PATTERNS: list[tuple[str, str]] = [
    (r"rm\s+-rf\s+(/|~|\$HOME|\.\.)", "Dangerous recursive deletion"),
    (r"curl\s+[^|]+\|\s*(sh|bash|zsh)", "Remote script execution via curl pipe"),
    (r"wget\s+[^|]+\|\s*(sh|bash|zsh)", "Remote script execution via wget pipe"),
    (r"chmod\s+777", "Overbroad permission change"),
    (r"sudo\s+", "Privileged shell command"),
    (r"\.ssh|id_rsa|id_ed25519", "SSH credential access"),
    (r"\.env", "Environment secret file access"),
    (r"/etc/passwd|/etc/shadow", "System account file access"),
]

EXTERNAL_ACTION_TOOLS = (
    "send", "email", "message", "post", "publish", "submit", "upload", "invite", "payment", "purchase"
)

SYSTEM_ACTION_TOOLS = (
    "shell", "exec", "terminal", "bash", "powershell", "delete", "remove", "install", "write", "update", "chmod", "credential", "secret"
)


def find_patterns(text: str, patterns: Iterable[tuple[str, str]], category: str, severity: str) -> list[Finding]:
    findings: list[Finding] = []
    for pattern, message in patterns:
        match = re.search(pattern, text or "", flags=re.IGNORECASE | re.MULTILINE)
        if match:
            evidence = match.group(0)
            if len(evidence) > 120:
                evidence = evidence[:117] + "..."
            findings.append(Finding(rule_id=pattern, severity=severity, category=category, message=message, evidence=evidence))
    return findings


def decision_from_findings(findings: list[Finding], base_risk: int = 0) -> ScanResult:
    risk = base_risk
    decision = "allow"
    for finding in findings:
        if finding.severity == "critical":
            risk = max(risk, 5)
            decision = "block"
        elif finding.severity == "high":
            risk = max(risk, 4)
            if decision != "block":
                decision = "confirm"
        elif finding.severity == "medium":
            risk = max(risk, 3)
            if decision == "allow":
                decision = "confirm"
        elif finding.severity == "low":
            risk = max(risk, 1)
    summary = f"{decision.upper()} with risk level {risk}. {len(findings)} finding(s)."
    return ScanResult(decision=decision, risk_level=risk, findings=findings, summary=summary)


def scan_text_common(text: str) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(find_patterns(text, PROMPT_INJECTION_PATTERNS, "prompt_injection", "high"))
    findings.extend(find_patterns(text, SECRET_PATTERNS, "protected_data", "critical"))
    return findings
