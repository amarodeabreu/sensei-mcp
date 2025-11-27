"""
Demo Execution Module

Provides executable demo workflows that showcase multi-MCP orchestration capabilities.
Designed for:
- Live demonstrations of Sensei MCP orchestration
- Testing and validation of multi-MCP workflows
- Example output generation for documentation

Design Philosophy:
- Executable examples over static documentation
- Real workflow execution with actual MCP calls
- Structured output for report generation
"""

import json
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime


class DemoType(Enum):
    """Available demo workflows."""
    AUTH_REVIEW = "auth-review"
    PERFORMANCE_DEBUG = "performance-debug"
    COST_ANALYSIS = "cost-analysis"
    API_REVIEW = "api-review"
    ARCHITECTURE_REFACTORING = "architecture-refactoring"
    CODE_NAVIGATION = "code-navigation"
    PATTERN_ENFORCEMENT = "pattern-enforcement"
    PR_REVIEW = "pr-review"
    COMMIT_ANALYSIS = "commit-analysis"
    ISSUE_TRIAGE = "issue-triage"


class DemoExecutor:
    """
    Execute demonstration workflows that showcase multi-MCP orchestration.

    Each demo is a self-contained workflow that:
    1. Uses the MCP orchestrator to get workflow template
    2. Provides realistic parameters and context
    3. Generates structured output showing MCP coordination
    4. Can be used as documentation examples
    """

    # Demo configurations with realistic parameters
    DEMO_CONFIGS = {
        DemoType.AUTH_REVIEW: {
            "name": "Authentication Security Review Demo",
            "description": "Demonstrates comprehensive auth security review using Sensei + Context7 + Tavily + Playwright",
            "template": "auth-security-review",
            "default_params": {
                "user_query": "Review authentication implementation for security vulnerabilities",
                "app_url": "https://example.com/login",
                "framework": "FastAPI"
            },
            "example_findings": [
                {
                    "severity": "HIGH",
                    "category": "Authentication",
                    "finding": "No rate limiting on login endpoint",
                    "source": "sensei:security-sentinel",
                    "recommendation": "Implement exponential backoff rate limiting"
                },
                {
                    "severity": "MEDIUM",
                    "category": "Session Management",
                    "finding": "Session tokens not rotated after privilege elevation",
                    "source": "context7:owasp-asvs",
                    "recommendation": "Rotate session IDs on authentication state changes"
                },
                {
                    "severity": "INFO",
                    "category": "Recent Vulnerabilities",
                    "finding": "FastAPI 0.104.0 has known OAuth vulnerability (CVE-2024-xxxx)",
                    "source": "tavily:cve-search",
                    "recommendation": "Upgrade to FastAPI 0.109.0+"
                }
            ],
            "expected_output_sections": [
                "Executive Summary",
                "MCP Coordination",
                "Security Findings",
                "Persona Analysis",
                "Recommendations",
                "Next Steps"
            ]
        },
        DemoType.PERFORMANCE_DEBUG: {
            "name": "Performance Debugging Demo",
            "description": "Demonstrates performance analysis using Sensei + Playwright + Context7",
            "template": "performance-debug",
            "default_params": {
                "page_url": "https://example.com/dashboard"
            },
            "example_findings": [
                {
                    "severity": "HIGH",
                    "category": "Core Web Vitals",
                    "finding": "LCP: 4.2s (Target: <2.5s)",
                    "source": "playwright:performance-trace",
                    "recommendation": "Optimize image loading and reduce render-blocking resources"
                },
                {
                    "severity": "MEDIUM",
                    "category": "Network",
                    "finding": "48 network requests on page load",
                    "source": "playwright:network-requests",
                    "recommendation": "Bundle and minify assets, implement request batching"
                },
                {
                    "severity": "INFO",
                    "category": "Framework Optimization",
                    "finding": "React 18 concurrent features not enabled",
                    "source": "context7:react-docs",
                    "recommendation": "Enable React 18 concurrent rendering for better UX"
                }
            ],
            "expected_output_sections": [
                "Performance Summary",
                "Core Web Vitals",
                "Network Analysis",
                "Optimization Recommendations"
            ]
        },
        DemoType.COST_ANALYSIS: {
            "name": "Cloud Cost Optimization Demo",
            "description": "Demonstrates cost analysis using Sensei + Tavily",
            "template": "cost-optimization",
            "default_params": {
                "cloud_provider": "AWS",
                "service_type": "EC2",
                "session_id": "cost-demo"
            },
            "example_findings": [
                {
                    "severity": "HIGH",
                    "category": "Resource Optimization",
                    "finding": "12 t3.xlarge instances running at <20% CPU utilization",
                    "source": "sensei:finops-optimizer",
                    "recommendation": "Right-size to t3.medium, save ~$600/month"
                },
                {
                    "severity": "MEDIUM",
                    "category": "Pricing",
                    "finding": "On-demand pricing for steady-state workloads",
                    "source": "tavily:aws-pricing",
                    "recommendation": "Move to Reserved Instances for 40% savings"
                }
            ],
            "expected_output_sections": [
                "Cost Analysis Summary",
                "Optimization Opportunities",
                "Savings Estimate"
            ]
        },
        DemoType.API_REVIEW: {
            "name": "API Design Review Demo",
            "description": "Demonstrates API review using Sensei + Context7 + Tavily",
            "template": "api-design-review",
            "default_params": {
                "user_query": "Review REST API design for best practices"
            },
            "example_findings": [
                {
                    "severity": "MEDIUM",
                    "category": "API Design",
                    "finding": "Inconsistent error response format across endpoints",
                    "source": "sensei:api-platform-engineer",
                    "recommendation": "Standardize on RFC 7807 Problem Details format"
                },
                {
                    "severity": "INFO",
                    "category": "Documentation",
                    "finding": "OpenAPI 3.1 spec available but not using discriminators",
                    "source": "context7:openapi-spec",
                    "recommendation": "Add discriminator fields for polymorphic responses"
                }
            ],
            "expected_output_sections": [
                "API Design Summary",
                "Standards Compliance",
                "Design Recommendations"
            ]
        },
        DemoType.ARCHITECTURE_REFACTORING: {
            "name": "Architecture-Driven Refactoring Demo",
            "description": "Demonstrates refactoring code with Sensei architectural guidance + Serena surgical execution",
            "template": "architecture-refactoring",
            "default_params": {
                "user_query": "Refactor authentication to use dependency injection",
                "target_file": "src/auth/auth_handler.py",
                "pattern_type": "dependency injection"
            },
            "example_findings": [
                {
                    "severity": "MEDIUM",
                    "category": "Architecture",
                    "finding": "Direct database access in auth handler violates separation of concerns",
                    "source": "sensei:pragmatic-architect",
                    "recommendation": "Inject UserRepository interface for testability"
                },
                {
                    "severity": "INFO",
                    "category": "Code Structure",
                    "finding": "AuthHandler has 8 dependencies instantiated in constructor",
                    "source": "serena:code-analysis",
                    "recommendation": "Apply constructor injection pattern"
                },
                {
                    "severity": "INFO",
                    "category": "Best Practices",
                    "finding": "SOLID principles documentation updated for 2025",
                    "source": "context7:solid-principles",
                    "recommendation": "Follow Interface Segregation Principle for repositories"
                }
            ],
            "expected_output_sections": [
                "Refactoring Summary",
                "Architecture Analysis",
                "Code Changes",
                "Validation Results"
            ]
        },
        DemoType.CODE_NAVIGATION: {
            "name": "Semantic Code Navigation Demo",
            "description": "Demonstrates code discovery with Serena + architectural analysis with Sensei",
            "template": "code-pattern-enforcement",
            "default_params": {
                "user_query": "Find all database queries and check tenant isolation",
                "violation_pattern": "SELECT.*FROM|INSERT.*INTO",
                "session_id": "multi-tenant-audit"
            },
            "example_findings": [
                {
                    "severity": "HIGH",
                    "category": "Multi-Tenancy",
                    "finding": "Query in UserRepository.find_by_email missing tenant_id filter",
                    "source": "serena:semantic-search",
                    "recommendation": "Add WHERE tenant_id = ? to all queries"
                },
                {
                    "severity": "HIGH",
                    "category": "Security",
                    "finding": "15 database queries missing tenant isolation",
                    "source": "sensei:security-sentinel",
                    "recommendation": "Enforce row-level security pattern across all repositories"
                },
                {
                    "severity": "MEDIUM",
                    "category": "Impact Analysis",
                    "finding": "UserRepository referenced in 23 locations",
                    "source": "serena:find-references",
                    "recommendation": "Update all call sites to pass tenant context"
                }
            ],
            "expected_output_sections": [
                "Discovery Summary",
                "Pattern Violations",
                "Security Analysis",
                "Remediation Plan"
            ]
        },
        DemoType.PATTERN_ENFORCEMENT: {
            "name": "Code Pattern Enforcement Demo",
            "description": "Demonstrates finding and fixing pattern violations with Serena + Sensei validation",
            "template": "code-pattern-enforcement",
            "default_params": {
                "user_query": "Ensure all API responses use consistent error format",
                "violation_pattern": "return.*\\{.*error.*\\}",
                "pattern_name": "RFC 7807 Problem Details"
            },
            "example_findings": [
                {
                    "severity": "MEDIUM",
                    "category": "API Consistency",
                    "finding": "12 endpoints return custom error format instead of RFC 7807",
                    "source": "serena:pattern-search",
                    "recommendation": "Standardize on ProblemDetails class"
                },
                {
                    "severity": "MEDIUM",
                    "category": "API Design",
                    "finding": "Inconsistent error responses violate API contract",
                    "source": "sensei:api-platform-engineer",
                    "recommendation": "Create ErrorResponse base class with RFC 7807 schema"
                },
                {
                    "severity": "INFO",
                    "category": "Standards",
                    "finding": "RFC 7807 Problem Details spec provides standard error format",
                    "source": "context7:rfc-7807",
                    "recommendation": "Include type, title, status, detail fields in all errors"
                }
            ],
            "expected_output_sections": [
                "Pattern Analysis",
                "Violations Found",
                "Refactoring Applied",
                "Consistency Check"
            ]
        },
        DemoType.PR_REVIEW: {
            "name": "PR Security & Architecture Review Demo",
            "description": "Demonstrates multi-persona PR review with GitHub + Sensei + Context7",
            "template": "pr-security-review",
            "default_params": {
                "pr_number": "123",
                "pr_title": "Add JWT authentication to API endpoints",
                "security_standard": "OWASP ASVS"
            },
            "example_findings": [
                {
                    "severity": "HIGH",
                    "category": "Security",
                    "finding": "JWT secret stored in code instead of secret manager",
                    "source": "sensei:security-sentinel",
                    "recommendation": "Move JWT_SECRET to AWS Secrets Manager with rotation policy"
                },
                {
                    "severity": "MEDIUM",
                    "category": "Architecture",
                    "finding": "Auth middleware directly accesses database, violating layering",
                    "source": "sensei:pragmatic-architect",
                    "recommendation": "Inject UserRepository through dependency injection"
                },
                {
                    "severity": "INFO",
                    "category": "Standards",
                    "finding": "OWASP ASVS 3.5.2 recommends JWT expiry < 1 hour for high-risk operations",
                    "source": "context7:owasp-asvs",
                    "recommendation": "Reduce token expiry from 24h to 1h for admin endpoints"
                },
                {
                    "severity": "MEDIUM",
                    "category": "CI/CD",
                    "finding": "PR has 1 failing check: security-scan",
                    "source": "github:pr-checks",
                    "recommendation": "Fix security vulnerabilities before merging"
                }
            ],
            "expected_output_sections": [
                "PR Summary",
                "Multi-Persona Analysis",
                "Security Findings",
                "Architectural Review",
                "CI Status",
                "Recommendations"
            ]
        },
        DemoType.COMMIT_ANALYSIS: {
            "name": "Commit Pattern Analysis Demo",
            "description": "Demonstrates architectural drift detection via GitHub commit history + Serena + Sensei",
            "template": "commit-pattern-analysis",
            "default_params": {
                "owner": "acme-corp",
                "repo": "api-backend",
                "commit_count": "50",
                "session_id": "api-backend-patterns"
            },
            "example_findings": [
                {
                    "severity": "MEDIUM",
                    "category": "Architectural Drift",
                    "finding": "8 commits in last month bypass UserRepository abstraction",
                    "source": "serena:pattern-search",
                    "recommendation": "Refactor direct SQL calls to use repository pattern"
                },
                {
                    "severity": "HIGH",
                    "category": "Pattern Violation",
                    "finding": "3 new service classes violate dependency injection constraint",
                    "source": "sensei:session-consistency",
                    "recommendation": "Apply constructor injection per project standards"
                },
                {
                    "severity": "INFO",
                    "category": "Code Evolution",
                    "finding": "Commit abc123: 'Quick fix for tenant filtering' adds direct WHERE clause",
                    "source": "github:commit-history",
                    "recommendation": "Replace with tenant-aware repository method"
                }
            ],
            "expected_output_sections": [
                "Commit Analysis Summary",
                "Architectural Drift Detected",
                "Pattern Violations",
                "Session Consistency Check",
                "Remediation Plan"
            ]
        },
        DemoType.ISSUE_TRIAGE: {
            "name": "Issue Triage & Prioritization Demo",
            "description": "Demonstrates smart issue categorization with GitHub + Sensei + Tavily",
            "template": "issue-triage",
            "default_params": {
                "issue_number": "456",
                "issue_title": "Login endpoint returns 500 under load",
                "issue_body": "After 100 concurrent users, /auth/login crashes with database timeout",
                "framework": "FastAPI"
            },
            "example_findings": [
                {
                    "severity": "HIGH",
                    "category": "Priority Assessment",
                    "finding": "Critical severity - login is core functionality under active load",
                    "source": "sensei:site-reliability-engineer",
                    "recommendation": "Priority: P0 (Critical), Assign to: SRE + Backend teams"
                },
                {
                    "severity": "HIGH",
                    "category": "Root Cause Hypothesis",
                    "finding": "Database timeout suggests connection pool exhaustion or N+1 queries",
                    "source": "sensei:performance-engineer",
                    "recommendation": "Labels: performance, database, auth. Check connection pool size and query patterns"
                },
                {
                    "severity": "INFO",
                    "category": "Similar Issues",
                    "finding": "FastAPI 0.108.0 had known connection pool issue (fixed in 0.109.0)",
                    "source": "tavily:issue-search",
                    "recommendation": "Check FastAPI version and consider upgrade"
                },
                {
                    "severity": "MEDIUM",
                    "category": "Team Assignment",
                    "finding": "Based on issue context, relevant experts: SRE, Performance, Database",
                    "source": "sensei:persona-matching",
                    "recommendation": "Assign personas: [site-reliability-engineer, performance-engineer, database-reliability-engineer]"
                }
            ],
            "expected_output_sections": [
                "Issue Summary",
                "Priority & Severity",
                "Root Cause Hypotheses",
                "Recommended Personas",
                "Suggested Labels",
                "Similar Issues"
            ]
        }
    }

    def __init__(self, mcp_orchestrator):
        """
        Initialize demo executor with MCP orchestrator.

        Args:
            mcp_orchestrator: MCPOrchestrator instance for workflow coordination
        """
        self.orchestrator = mcp_orchestrator

    def run_demo(
        self,
        demo_type: str,
        custom_params: Optional[Dict] = None,
        output_format: str = "markdown"
    ) -> Dict:
        """
        Execute a demonstration workflow.

        Args:
            demo_type: Type of demo to run (e.g., "auth-review")
            custom_params: Optional custom parameters to override defaults
            output_format: Output format ("markdown", "json", "text")

        Returns:
            Dict containing:
            - demo_info: Metadata about the demo
            - workflow: The workflow template used
            - execution_plan: Step-by-step execution plan
            - example_output: Example structured output
            - formatted_report: Human-readable report in requested format
        """
        try:
            demo_enum = DemoType(demo_type)
        except ValueError:
            return {
                "error": f"Unknown demo type: {demo_type}",
                "available_demos": [d.value for d in DemoType]
            }

        config = self.DEMO_CONFIGS[demo_enum]

        # Merge default and custom params
        params = config["default_params"].copy()
        if custom_params:
            params.update(custom_params)

        # Get workflow template from orchestrator
        workflow = self.orchestrator.get_workflow_template(
            template_name=config["template"],
            parameters=params
        )

        # Build execution plan
        execution_plan = self._build_execution_plan(workflow, params)

        # Generate example output
        example_output = self._generate_example_output(config, params)

        # Format report
        formatted_report = self._format_report(
            config=config,
            workflow=workflow,
            execution_plan=execution_plan,
            example_output=example_output,
            format=output_format
        )

        return {
            "demo_type": demo_type,
            "demo_info": {
                "name": config["name"],
                "description": config["description"],
                "timestamp": datetime.utcnow().isoformat() + "Z"
            },
            "workflow": workflow["workflow"],
            "parameters": params,
            "execution_plan": execution_plan,
            "example_output": example_output,
            "formatted_report": formatted_report
        }

    def list_demos(self) -> List[Dict]:
        """List all available demo workflows."""
        demos = []
        for demo_enum, config in self.DEMO_CONFIGS.items():
            demos.append({
                "id": demo_enum.value,
                "name": config["name"],
                "description": config["description"],
                "template": config["template"],
                "example_params": list(config["default_params"].keys())
            })

        return sorted(demos, key=lambda x: x["name"])

    def _build_execution_plan(self, workflow: Dict, params: Dict) -> List[Dict]:
        """Build a detailed execution plan from workflow template."""
        plan = []

        if "workflow" not in workflow:
            return plan

        for step_def in workflow["workflow"]["steps"]:
            step_info = {
                "step": step_def["step"],
                "action": step_def["action"],
                "mcp": step_def["mcp"].value if hasattr(step_def["mcp"], "value") else step_def["mcp"],
                "params": step_def.get("params", {}),
                "optional": step_def.get("optional", False),
                "description": self._get_step_description(step_def)
            }
            plan.append(step_info)

        return plan

    def _get_step_description(self, step_def: Dict) -> str:
        """Generate human-readable description for a workflow step."""
        action = step_def["action"]
        mcp = step_def["mcp"].value if hasattr(step_def["mcp"], "value") else step_def["mcp"]

        descriptions = {
            "suggest_personas_for_query": f"Query Sensei for relevant expert personas",
            "get_library_docs": f"Fetch documentation from Context7",
            "get_persona_content": f"Load persona expertise from Sensei",
            "tavily_search": f"Search recent data and vulnerabilities via Tavily",
            "browser_navigate": f"Navigate to target URL with Playwright",
            "browser_network_requests": f"Analyze network requests with Playwright",
            "performance_start_trace": f"Start performance trace with Playwright",
            "browser_snapshot": f"Capture accessibility snapshot with Playwright",
            "get_session_context": f"Load session context from Sensei",
            "get_symbols_overview": f"Analyze code structure with Serena",
            "find_symbol": f"Locate code symbols with Serena",
            "search_for_pattern": f"Search codebase patterns with Serena",
            "find_referencing_symbols": f"Find code references with Serena",
            "replace_symbol_body": f"Refactor code with Serena",
            "insert_before_symbol": f"Insert code with Serena",
            "insert_after_symbol": f"Insert code with Serena",
            "rename_symbol": f"Rename symbols with Serena",
            "validate_against_standards": f"Validate with Sensei standards",
            "check_consistency": f"Check consistency with Sensei",
            "record_decision": f"Record architectural decision in Sensei",
            "gh_pr_view": f"Fetch PR metadata from GitHub",
            "gh_pr_diff": f"Get PR diff from GitHub",
            "gh_api": f"Query GitHub API",
            "gh_issue_view": f"Fetch issue details from GitHub"
        }

        return descriptions.get(action, f"Execute {action} via {mcp}")

    def _generate_example_output(self, config: Dict, params: Dict) -> Dict:
        """Generate example structured output for the demo."""
        return {
            "summary": {
                "demo": config["name"],
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "parameters": params,
                "mcps_used": len(config.get("example_findings", [])),
                "findings_count": len(config.get("example_findings", []))
            },
            "findings": config.get("example_findings", []),
            "coordination": {
                "description": "Multi-MCP orchestration coordinated by Sensei",
                "sequence": [
                    "Sensei selected relevant personas based on query context",
                    "Context7 provided up-to-date documentation and standards",
                    "Serena (if applicable) analyzed code structure and patterns",
                    "Tavily searched for recent vulnerabilities and best practices",
                    "Playwright (if applicable) performed live system inspection",
                    "Serena (if applicable) performed surgical code refactoring",
                    "Sensei synthesized findings into actionable recommendations"
                ]
            },
            "expected_sections": config.get("expected_output_sections", [])
        }

    def _format_report(
        self,
        config: Dict,
        workflow: Dict,
        execution_plan: List[Dict],
        example_output: Dict,
        format: str = "markdown"
    ) -> str:
        """Format demo results as a human-readable report."""
        if format == "json":
            return json.dumps({
                "config": config,
                "workflow": workflow,
                "execution_plan": execution_plan,
                "example_output": example_output
            }, indent=2)

        if format == "markdown":
            return self._format_markdown_report(config, workflow, execution_plan, example_output)

        # Default to text
        return self._format_text_report(config, workflow, execution_plan, example_output)

    def _format_markdown_report(
        self,
        config: Dict,
        workflow: Dict,
        execution_plan: List[Dict],
        example_output: Dict
    ) -> str:
        """Format as markdown report."""
        lines = []

        # Header
        lines.append(f"# {config['name']}\n")
        lines.append(f"**Demo Execution Report**\n")
        lines.append(f"*Generated: {example_output['summary']['timestamp']}*\n")
        lines.append("\n---\n")

        # Overview
        lines.append("## 📋 Overview\n")
        lines.append(f"{config['description']}\n\n")
        lines.append(f"**Workflow Template:** `{config['template']}`\n")
        lines.append(f"**MCPs Involved:** {len(workflow['workflow']['mcps'])} servers\n")
        lines.append(f"**Execution Steps:** {len(execution_plan)} steps\n")
        lines.append("\n")

        # Parameters
        lines.append("## ⚙️ Parameters\n")
        lines.append("```json\n")
        lines.append(json.dumps(example_output['summary']['parameters'], indent=2))
        lines.append("\n```\n\n")

        # Execution Plan
        lines.append("## 🔄 Execution Plan\n")
        lines.append("*Multi-MCP workflow coordination sequence:*\n\n")
        for step in execution_plan:
            optional_marker = " *(optional)*" if step["optional"] else ""
            lines.append(f"**Step {step['step']}:** {step['description']}{optional_marker}\n")
            lines.append(f"- **MCP:** `{step['mcp']}`\n")
            lines.append(f"- **Action:** `{step['action']}`\n")
            if step['params']:
                lines.append(f"- **Params:** {json.dumps(step['params'])}\n")
            lines.append("\n")

        # Example Findings
        if example_output.get('findings'):
            lines.append("## 🔍 Example Findings\n")
            lines.append("*Simulated output showing multi-MCP coordination:*\n\n")

            for i, finding in enumerate(example_output['findings'], 1):
                severity_emoji = {
                    "HIGH": "🔴",
                    "MEDIUM": "🟡",
                    "LOW": "🟢",
                    "INFO": "ℹ️"
                }.get(finding['severity'], "•")

                lines.append(f"### {severity_emoji} Finding {i}: {finding['category']}\n")
                lines.append(f"**Severity:** {finding['severity']}\n\n")
                lines.append(f"**Finding:** {finding['finding']}\n\n")
                lines.append(f"**Source:** `{finding['source']}`\n\n")
                lines.append(f"**Recommendation:** {finding['recommendation']}\n\n")

        # MCP Coordination
        lines.append("## 🎯 Multi-MCP Coordination\n")
        for step in example_output['coordination']['sequence']:
            lines.append(f"1. {step}\n")
        lines.append("\n")

        # Expected Output Structure
        lines.append("## 📄 Expected Output Sections\n")
        lines.append("*A real execution would include:*\n\n")
        for section in example_output['expected_sections']:
            lines.append(f"- {section}\n")
        lines.append("\n")

        # Footer
        lines.append("---\n")
        lines.append("## 💡 How to Run This Demo\n\n")
        lines.append("```python\n")
        lines.append("# Using Sensei MCP tools:\n")
        lines.append(f'run_demo(demo_type="{config["template"]}")\n')
        lines.append("\n# Or with custom parameters:\n")
        lines.append(f'run_demo(\n')
        lines.append(f'    demo_type="{config["template"]}",\n')
        lines.append(f'    custom_params={{\n')
        first_param = list(example_output['summary']['parameters'].keys())[0]
        lines.append(f'        "{first_param}": "your-value"\n')
        lines.append(f'    }}\n')
        lines.append(f')\n')
        lines.append("```\n\n")

        lines.append("**Note:** This is a demonstration output. Real execution would fetch live data from Context7, Tavily, and Playwright.\n")

        return "".join(lines)

    def _format_text_report(
        self,
        config: Dict,
        workflow: Dict,
        execution_plan: List[Dict],
        example_output: Dict
    ) -> str:
        """Format as plain text report."""
        lines = []

        lines.append("=" * 80)
        lines.append(f"{config['name']}")
        lines.append("=" * 80)
        lines.append(f"Generated: {example_output['summary']['timestamp']}\n")

        lines.append("\nOVERVIEW:")
        lines.append(f"  {config['description']}")
        lines.append(f"  Workflow: {config['template']}")
        lines.append(f"  Steps: {len(execution_plan)}\n")

        lines.append("\nEXECUTION PLAN:")
        for step in execution_plan:
            optional = " (optional)" if step["optional"] else ""
            lines.append(f"  Step {step['step']}: {step['description']}{optional}")
            lines.append(f"    MCP: {step['mcp']}")
            lines.append(f"    Action: {step['action']}\n")

        if example_output.get('findings'):
            lines.append("\nEXAMPLE FINDINGS:")
            for i, finding in enumerate(example_output['findings'], 1):
                lines.append(f"  {i}. [{finding['severity']}] {finding['category']}")
                lines.append(f"     Finding: {finding['finding']}")
                lines.append(f"     Source: {finding['source']}")
                lines.append(f"     Recommendation: {finding['recommendation']}\n")

        lines.append("\n" + "=" * 80)

        return "\n".join(lines)
