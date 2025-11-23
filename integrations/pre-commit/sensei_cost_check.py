#!/usr/bin/env python3
"""
Sensei Pre-Commit Hook: Cost Impact Check

Analyzes infrastructure changes for cost implications using Sensei's
FinOps Optimizer persona.

Usage:
  Add to .pre-commit-config.yaml:
    - id: sensei-cost-check
      name: Sensei Cost Impact Check
      entry: python integrations/pre-commit/sensei_cost_check.py
      language: system
      files: (terraform|cloudformation|kubernetes|docker-compose)\.(tf|yaml|yml|json)$
"""

import subprocess
import sys
import re
import json
from pathlib import Path

# Cost-impacting resource patterns
COST_PATTERNS = {
    'ec2_instances': {
        'pattern': r'(aws_instance|instance_type|ec2\.Instance)',
        'category': 'Compute',
        'impact': 'HIGH'
    },
    'rds_instances': {
        'pattern': r'(aws_db_instance|db\.instance\.class|RDS)',
        'category': 'Database',
        'impact': 'HIGH'
    },
    'lambda_functions': {
        'pattern': r'(aws_lambda_function|Lambda|serverless)',
        'category': 'Serverless',
        'impact': 'LOW'
    },
    's3_buckets': {
        'pattern': r'(aws_s3_bucket|S3Bucket)',
        'category': 'Storage',
        'impact': 'MEDIUM'
    },
    'load_balancers': {
        'pattern': r'(aws_lb|aws_elb|LoadBalancer)',
        'category': 'Networking',
        'impact': 'MEDIUM'
    },
    'nat_gateways': {
        'pattern': r'(aws_nat_gateway|NatGateway)',
        'category': 'Networking',
        'impact': 'HIGH'
    },
}

def get_infra_changes():
    """Get infrastructure file changes from staged diff."""
    try:
        # Get list of staged infrastructure files
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )

        infra_files = [
            f for f in result.stdout.strip().split('\n')
            if any(ext in f.lower() for ext in ['.tf', 'terraform', 'cloudformation', 'kubernetes', 'docker-compose'])
        ]

        if not infra_files:
            return None

        # Get full diff for these files
        diff_result = subprocess.run(
            ["git", "diff", "--cached", "--"] + infra_files,
            capture_output=True,
            text=True,
            check=True
        )

        return {
            'files': infra_files,
            'diff': diff_result.stdout
        }

    except subprocess.CalledProcessError as e:
        print(f"❌ Error getting infrastructure changes: {e}")
        return None

def analyze_cost_impact(changes):
    """Analyze cost impact of infrastructure changes."""
    findings = {
        'HIGH': [],
        'MEDIUM': [],
        'LOW': []
    }

    lines = changes['diff'].split('\n')
    current_file = None

    for line_num, line in enumerate(lines, 1):
        # Track current file
        if line.startswith('+++'):
            current_file = line[6:].strip()
            continue

        # Only check added lines
        if not line.startswith('+') or line.startswith('+++'):
            continue

        code_line = line[1:]

        # Check each cost pattern
        for pattern_name, pattern_info in COST_PATTERNS.items():
            if re.search(pattern_info['pattern'], code_line, re.IGNORECASE):
                findings[pattern_info['impact']].append({
                    'file': current_file or 'unknown',
                    'line': line_num,
                    'resource': pattern_name,
                    'category': pattern_info['category'],
                    'code': code_line.strip()
                })

    return findings

def estimate_monthly_cost(findings):
    """Provide rough cost estimates (placeholder)."""
    # In a real implementation, this would integrate with cloud pricing APIs
    # or use Sensei's FinOps Optimizer for accurate estimates

    cost_estimates = {
        'ec2_instances': {'min': 30, 'max': 500},
        'rds_instances': {'min': 50, 'max': 1000},
        'lambda_functions': {'min': 0, 'max': 50},
        's3_buckets': {'min': 5, 'max': 100},
        'load_balancers': {'min': 20, 'max': 50},
        'nat_gateways': {'min': 45, 'max': 150},
    }

    total_min = 0
    total_max = 0

    for severity, items in findings.items():
        for item in items:
            resource = item['resource']
            if resource in cost_estimates:
                total_min += cost_estimates[resource]['min']
                total_max += cost_estimates[resource]['max']

    return {'min': total_min, 'max': total_max}

def print_cost_report(findings, cost_estimate):
    """Print formatted cost impact report."""
    print("\n🎭 Sensei Cost Impact Analysis")
    print("💰 Persona: FinOps Optimizer")
    print("=" * 70)

    total_resources = sum(len(v) for v in findings.values())

    if total_resources == 0:
        print("\n✅ No cost-impacting infrastructure changes detected")
        print("=" * 70)
        return

    print(f"\n📊 Found {total_resources} cost-impacting resource(s):\n")

    # Print HIGH impact resources
    if findings['HIGH']:
        print("🔴 HIGH COST IMPACT:")
        for finding in findings['HIGH']:
            print(f"  • {finding['category']}: {finding['resource']}")
            print(f"    File: {finding['file']}")
            print(f"    Code: {finding['code'][:70]}...")
            print()

    # Print MEDIUM impact resources
    if findings['MEDIUM']:
        print("🟡 MEDIUM COST IMPACT:")
        for finding in findings['MEDIUM']:
            print(f"  • {finding['category']}: {finding['resource']}")
            print(f"    File: {finding['file']}")
            print()

    # Print LOW impact resources
    if findings['LOW']:
        print("🟢 LOW COST IMPACT:")
        for finding in findings['LOW']:
            print(f"  • {finding['category']}: {finding['resource']}")

    print("\n" + "=" * 70)
    print(f"\n💵 Estimated Monthly Cost Impact:")
    print(f"   ${cost_estimate['min']:,} - ${cost_estimate['max']:,} USD/month")

    print("\n💡 Recommendations from FinOps Optimizer:")
    print("  • Review instance sizing - are you using appropriate instance types?")
    print("  • Consider Reserved Instances for long-running resources")
    print("  • Use Spot Instances where possible for non-critical workloads")
    print("  • Enable auto-scaling to match actual demand")
    print("  • Set up cost alerts and budgets in your cloud provider")

    if findings['HIGH']:
        print("\n⚠️  High-cost resources detected. Please review before committing.")
        print("💡 To proceed anyway: git commit --no-verify")

def main():
    """Main entry point for pre-commit hook."""
    print("\n🔍 Running Sensei cost impact check...")

    changes = get_infra_changes()
    if not changes:
        print("ℹ️  No infrastructure changes to analyze")
        return 0

    findings = analyze_cost_impact(changes)
    cost_estimate = estimate_monthly_cost(findings)
    print_cost_report(findings, cost_estimate)

    # Don't fail the commit, just warn
    # Teams can configure this to fail based on their policies
    return 0

if __name__ == "__main__":
    sys.exit(main())
