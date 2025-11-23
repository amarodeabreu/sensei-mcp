#!/usr/bin/env python3
"""
Sensei Pre-Commit Hook: Consistency Check

Validates that staged changes align with established architectural decisions
and patterns in the Sensei session.

Usage:
  Add to .pre-commit-config.yaml:
    - id: sensei-consistency-check
      name: Sensei Consistency Check
      entry: python integrations/pre-commit/sensei_consistency_check.py
      language: system
      pass_filenames: false
"""

import subprocess
import sys
import json
from pathlib import Path

def get_staged_changes():
    """Get summary of staged changes from git."""
    try:
        # Get list of staged files
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )
        staged_files = result.stdout.strip().split('\n')

        # Get diff summary
        diff_result = subprocess.run(
            ["git", "diff", "--cached", "--stat"],
            capture_output=True,
            text=True,
            check=True
        )

        return {
            "files": staged_files,
            "summary": diff_result.stdout
        }
    except subprocess.CalledProcessError as e:
        print(f"❌ Error getting git changes: {e}")
        return None

def check_consistency_with_sensei(changes):
    """
    Check if changes are consistent with Sensei session decisions.

    In a real implementation, this would:
    1. Load Sensei session for this project
    2. Call check_consistency(proposed_change=summary)
    3. Return consistency report
    """
    # For now, a placeholder implementation
    # Real implementation would import and use Sensei MCP:
    #
    # from sensei_mcp.session import SessionManager
    # session_mgr = SessionManager()
    # result = session_mgr.check_consistency(
    #     session_id="my-project",
    #     proposed_change=changes['summary']
    # )

    print("🎭 Sensei Consistency Check")
    print("=" * 60)

    # Analyze file types
    has_api_changes = any('api' in f.lower() for f in changes['files'])
    has_db_changes = any('migration' in f.lower() or 'schema' in f.lower() for f in changes['files'])
    has_infra_changes = any('terraform' in f.lower() or 'docker' in f.lower() for f in changes['files'])

    violations = []
    warnings = []

    # Example consistency checks based on common patterns
    if has_api_changes:
        # Check if OpenAPI spec is updated
        has_openapi = any('openapi' in f.lower() or 'swagger' in f.lower() for f in changes['files'])
        if not has_openapi:
            warnings.append("API changes detected but no OpenAPI spec update found")

    if has_db_changes:
        # Check if migration and rollback exist
        has_migration = any('migration' in f.lower() for f in changes['files'])
        if has_migration:
            print("✅ Database migration detected")
        else:
            violations.append("Database schema changes must include migration scripts")

    if has_infra_changes:
        warnings.append("Infrastructure changes detected - ensure cost impact is reviewed")

    # Print results
    print(f"\n📊 Analyzed {len(changes['files'])} staged files")

    if violations:
        print("\n❌ Consistency Violations:")
        for v in violations:
            print(f"  • {v}")

    if warnings:
        print("\n⚠️  Warnings:")
        for w in warnings:
            print(f"  • {w}")

    if not violations and not warnings:
        print("\n✅ All changes are consistent with established patterns")

    print("=" * 60)

    # Return exit code
    return 1 if violations else 0

def main():
    """Main entry point for pre-commit hook."""
    print("\n🔍 Running Sensei consistency check...")

    changes = get_staged_changes()
    if not changes or not changes['files'] or changes['files'] == ['']:
        print("ℹ️  No staged changes to check")
        return 0

    exit_code = check_consistency_with_sensei(changes)

    if exit_code != 0:
        print("\n💡 Tip: Use 'git commit --no-verify' to bypass this check (not recommended)")
        print("💡 Better: Update your changes to align with architectural decisions")
        print("💡 Or: Document a new decision with Sensei's record_decision() tool")

    return exit_code

if __name__ == "__main__":
    sys.exit(main())
