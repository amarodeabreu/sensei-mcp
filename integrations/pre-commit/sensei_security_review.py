#!/usr/bin/env python3
"""
Sensei Pre-Commit Hook: Security Review

Performs basic security checks on staged code changes using Sensei's
Security Sentinel persona.

Usage:
  Add to .pre-commit-config.yaml:
    - id: sensei-security-review
      name: Sensei Security Review
      entry: python integrations/pre-commit/sensei_security_review.py
      language: system
      files: \.(py|js|ts|tsx|jsx)$
"""

import subprocess
import sys
import re
from pathlib import Path

# Security patterns to check for
SECURITY_PATTERNS = {
    'hardcoded_secrets': {
        'pattern': r'(password|api_key|secret|token)\s*=\s*["\'][^"\']+["\']',
        'severity': 'HIGH',
        'message': 'Potential hardcoded secret detected'
    },
    'sql_injection': {
        'pattern': r'execute\s*\([^)]*%s[^)]*\)|cursor\.execute\s*\([^)]*\+',
        'severity': 'HIGH',
        'message': 'Potential SQL injection vulnerability'
    },
    'eval_usage': {
        'pattern': r'\beval\s*\(',
        'severity': 'MEDIUM',
        'message': 'Use of eval() can be dangerous'
    },
    'weak_crypto': {
        'pattern': r'(md5|sha1)\s*\(',
        'severity': 'MEDIUM',
        'message': 'Weak cryptographic algorithm (use SHA-256 or better)'
    },
    'unsafe_deserialization': {
        'pattern': r'pickle\.loads|yaml\.load\([^)]*\)|json\.loads\([^)]*safe',
        'severity': 'HIGH',
        'message': 'Unsafe deserialization detected'
    },
}

def get_staged_diff():
    """Get the diff of staged changes."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error getting staged diff: {e}")
        return None

def scan_for_security_issues(diff_content):
    """Scan staged changes for security issues."""
    issues = {
        'HIGH': [],
        'MEDIUM': [],
        'LOW': []
    }

    lines = diff_content.split('\n')
    current_file = None

    for line_num, line in enumerate(lines, 1):
        # Track current file
        if line.startswith('+++'):
            current_file = line[6:].strip()
            continue

        # Only check added lines
        if not line.startswith('+') or line.startswith('+++'):
            continue

        # Remove the '+' prefix
        code_line = line[1:]

        # Check each security pattern
        for pattern_name, pattern_info in SECURITY_PATTERNS.items():
            if re.search(pattern_info['pattern'], code_line, re.IGNORECASE):
                issues[pattern_info['severity']].append({
                    'file': current_file or 'unknown',
                    'line': line_num,
                    'pattern': pattern_name,
                    'message': pattern_info['message'],
                    'code': code_line.strip()
                })

    return issues

def print_security_report(issues):
    """Print formatted security report."""
    print("\n🎭 Sensei Security Review")
    print("🔒 Persona: Security Sentinel")
    print("=" * 70)

    total_issues = sum(len(v) for v in issues.values())

    if total_issues == 0:
        print("\n✅ No security issues detected in staged changes")
        print("=" * 70)
        return True

    print(f"\n⚠️  Found {total_issues} potential security issue(s):\n")

    # Print HIGH severity issues
    if issues['HIGH']:
        print("🔴 HIGH SEVERITY:")
        for issue in issues['HIGH']:
            print(f"  • {issue['file']}:{issue['line']}")
            print(f"    {issue['message']}")
            print(f"    Code: {issue['code'][:80]}...")
            print()

    # Print MEDIUM severity issues
    if issues['MEDIUM']:
        print("🟡 MEDIUM SEVERITY:")
        for issue in issues['MEDIUM']:
            print(f"  • {issue['file']}:{issue['line']}")
            print(f"    {issue['message']}")
            print(f"    Code: {issue['code'][:80]}...")
            print()

    print("=" * 70)
    print("\n💡 Recommendations from Security Sentinel:")
    print("  • Review flagged code for security implications")
    print("  • Use environment variables for secrets")
    print("  • Use parameterized queries to prevent SQL injection")
    print("  • Prefer secure alternatives to eval()")
    print("  • Use modern cryptographic algorithms (SHA-256+)")
    print("\n💡 To proceed anyway: git commit --no-verify")

    # Fail on HIGH severity issues
    return len(issues['HIGH']) == 0

def main():
    """Main entry point for pre-commit hook."""
    print("\n🔍 Running Sensei security review...")

    diff = get_staged_diff()
    if not diff:
        print("ℹ️  No staged changes to review")
        return 0

    issues = scan_for_security_issues(diff)
    passed = print_security_report(issues)

    return 0 if passed else 1

if __name__ == "__main__":
    sys.exit(main())
