#!/usr/bin/env python3
from pathlib import Path
import re, sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

IGNORE_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", "dist", "build"}
IGNORE_FILES = {".env.example"}

PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "aws_access_key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "github_token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b"),
    "openai_key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "slack_token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "generic_secret_assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|secret|token|password|passwd)\b\s*[:=]\s*['\"][^'\"\n]{12,}['\"]"
    ),
}

def should_skip(path: Path) -> bool:
    if path.name in IGNORE_FILES:
        return True
    return any(part in IGNORE_DIRS for part in path.parts)

findings = []
for path in ROOT.rglob("*"):
    if not path.is_file() or should_skip(path):
        continue
    try:
        data = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    for lineno, line in enumerate(data.splitlines(), 1):
        for kind, rx in PATTERNS.items():
            if rx.search(line):
                findings.append((path.relative_to(ROOT), lineno, kind))

if findings:
    print("SECRET_SCAN_FAIL")
    for path, line, kind in findings:
        print(f"{path}:{line}:{kind}")
    sys.exit(1)

print("SECRET_SCAN_PASS")
sys.exit(0)
