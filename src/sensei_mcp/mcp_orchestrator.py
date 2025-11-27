"""
MCP Orchestration Layer

This module provides intelligent orchestration of multiple MCP servers
to create comprehensive, multi-source analysis workflows.

Design Philosophy:
- Suggest which MCP servers to use based on query analysis
- Provide pre-built workflow templates for common scenarios
- Enable compound intelligence from Sensei + external MCPs
"""

import json
from typing import List, Dict, Optional, Set
from enum import Enum


class MCPServer(Enum):
    """Available MCP servers for orchestration."""
    SENSEI = "sensei"
    SERENA = "serena"
    CONTEXT7 = "context7"
    TAVILY = "tavily"
    PLAYWRIGHT = "playwright"
    CHROME_DEVTOOLS = "chrome-devtools"
    GITHUB = "github"
    OPENMEMORY = "openmemory"
    SEQUENTIAL_THINKING = "sequential-thinking"


class WorkflowTemplate(Enum):
    """Pre-built workflow templates."""
    AUTH_SECURITY_REVIEW = "auth-security-review"
    PERFORMANCE_DEBUG = "performance-debug"
    COST_OPTIMIZATION = "cost-optimization"
    TECH_DUE_DILIGENCE = "tech-due-diligence"
    INCIDENT_POSTMORTEM = "incident-postmortem"
    ACCESSIBILITY_AUDIT = "accessibility-audit"
    API_DESIGN_REVIEW = "api-design-review"
    ARCHITECTURE_REFACTORING = "architecture-refactoring"
    CODE_PATTERN_ENFORCEMENT = "code-pattern-enforcement"
    DEPENDENCY_INJECTION_MIGRATION = "dependency-injection-migration"
    PR_SECURITY_REVIEW = "pr-security-review"
    COMMIT_PATTERN_ANALYSIS = "commit-pattern-analysis"
    ISSUE_TRIAGE = "issue-triage"


class MCPOrchestrator:
    """
    Intelligent MCP server orchestration.

    Analyzes queries and suggests which MCP servers to use,
    and provides pre-built workflow templates for common scenarios.
    """

    # Keyword patterns for MCP server suggestions
    MCP_PATTERNS = {
        MCPServer.SERENA: {
            "keywords": [
                "refactor", "refactoring", "rename", "move", "reorganize",
                "find", "search", "navigate", "code", "symbol", "class", "method",
                "function", "variable", "replace", "update", "change code",
                "codebase", "repository", "source", "implementation",
                "surgical", "precise", "symbol-level", "semantic search",
                "dependency injection", "pattern enforcement", "code structure"
            ],
            "contexts": ["TECHNICAL", "ARCHITECTURAL"],
            "description": "Semantic code analysis, refactoring, and surgical code changes"
        },
        MCPServer.CONTEXT7: {
            "keywords": [
                "documentation", "docs", "library", "framework", "api reference",
                "best practices", "official docs", "current version", "latest",
                "upgrade", "migration", "compare libraries", "which library",
                "owasp", "wcag", "rfc", "specification", "standard"
            ],
            "contexts": ["TECHNICAL", "ARCHITECTURAL", "SECURITY"],
            "description": "Fetch up-to-date library/framework documentation"
        },
        MCPServer.TAVILY: {
            "keywords": [
                "recent", "latest", "current", "2025", "2024", "cve", "vulnerability",
                "pricing", "cost", "outage", "incident", "news", "announcement",
                "maintained", "active", "abandoned", "trend", "popular",
                "benchmark", "comparison", "vs", "alternative"
            ],
            "contexts": ["SECURITY", "COST", "CRISIS", "TECHNICAL"],
            "description": "Search recent data, CVEs, pricing, incidents"
        },
        MCPServer.PLAYWRIGHT: {
            "keywords": [
                "performance", "slow", "page load", "lcp", "cls", "fid",
                "core web vitals", "speed", "optimize", "screenshot", "ui",
                "inspect", "network", "waterfall", "debug", "live", "production",
                "accessibility", "wcag", "screen reader", "keyboard navigation"
            ],
            "contexts": ["TECHNICAL", "CRISIS"],
            "description": "Inspect live systems, measure performance, debug UI"
        },
        MCPServer.GITHUB: {
            "keywords": [
                "pr", "pull request", "code review", "diff", "commit",
                "branch", "merge", "issue", "repository", "repo"
            ],
            "contexts": ["TECHNICAL", "TEAM"],
            "description": "Fetch PR context, code review, CI status"
        },
        MCPServer.SEQUENTIAL_THINKING: {
            "keywords": [
                "complex", "trade-off", "analyze", "pros and cons", "should we",
                "architecture decision", "design decision", "evaluate",
                "consider", "weigh options"
            ],
            "contexts": ["ARCHITECTURAL", "POLITICAL", "COST"],
            "description": "Multi-step reasoning for complex decisions"
        },
        MCPServer.OPENMEMORY: {
            "keywords": [
                "remember", "always", "never", "preference", "standard",
                "across all projects", "team standard", "global", "everywhere",
                "lesson learned", "past project", "previous experience"
            ],
            "contexts": ["GENERAL"],
            "description": "Cross-project memory and organizational knowledge"
        }
    }

    # Workflow templates with MCP combinations
    WORKFLOW_TEMPLATES = {
        WorkflowTemplate.AUTH_SECURITY_REVIEW: {
            "name": "Authentication Security Review",
            "description": "Comprehensive security review of authentication implementation",
            "mcps": [MCPServer.SENSEI, MCPServer.CONTEXT7, MCPServer.TAVILY, MCPServer.PLAYWRIGHT],
            "personas": ["security-sentinel", "api-platform-engineer", "privacy-engineer"],
            "steps": [
                {
                    "step": 1,
                    "action": "suggest_personas_for_query",
                    "mcp": MCPServer.SENSEI,
                    "params": {"query": "{user_query}", "max_suggestions": 3}
                },
                {
                    "step": 2,
                    "action": "get_library_docs",
                    "mcp": MCPServer.CONTEXT7,
                    "params": {
                        "libraries": ["owasp/asvs", "oauth", "framework-specific-auth"]
                    }
                },
                {
                    "step": 3,
                    "action": "tavily_search",
                    "mcp": MCPServer.TAVILY,
                    "params": {
                        "queries": ["{framework} vulnerabilities 2025", "OAuth security 2025"]
                    }
                },
                {
                    "step": 4,
                    "action": "browser_navigate",
                    "mcp": MCPServer.PLAYWRIGHT,
                    "params": {"url": "{app_url}/login"},
                    "optional": True
                },
                {
                    "step": 5,
                    "action": "browser_network_requests",
                    "mcp": MCPServer.PLAYWRIGHT,
                    "optional": True
                }
            ],
            "output_format": "security_review_report",
            "cost_estimate": "$0.05-0.10",
            "time_estimate": "30-60 seconds"
        },
        WorkflowTemplate.PERFORMANCE_DEBUG: {
            "name": "Performance Debugging",
            "description": "Diagnose and fix page performance issues",
            "mcps": [MCPServer.SENSEI, MCPServer.PLAYWRIGHT, MCPServer.CONTEXT7],
            "personas": ["performance-engineer", "frontend-ux-specialist"],
            "steps": [
                {
                    "step": 1,
                    "action": "suggest_personas_for_query",
                    "mcp": MCPServer.SENSEI,
                    "params": {"query": "performance debugging", "max_suggestions": 2}
                },
                {
                    "step": 2,
                    "action": "browser_navigate",
                    "mcp": MCPServer.PLAYWRIGHT,
                    "params": {"url": "{page_url}"}
                },
                {
                    "step": 3,
                    "action": "performance_start_trace",
                    "mcp": MCPServer.PLAYWRIGHT,
                    "params": {"reload": True, "autoStop": True}
                },
                {
                    "step": 4,
                    "action": "browser_network_requests",
                    "mcp": MCPServer.PLAYWRIGHT
                },
                {
                    "step": 5,
                    "action": "get_library_docs",
                    "mcp": MCPServer.CONTEXT7,
                    "params": {"topic": "performance optimization"},
                    "optional": True
                }
            ],
            "output_format": "performance_report",
            "cost_estimate": "$0.00-0.05",
            "time_estimate": "45-90 seconds"
        },
        WorkflowTemplate.COST_OPTIMIZATION: {
            "name": "Cloud Cost Optimization",
            "description": "Analyze and optimize cloud infrastructure costs",
            "mcps": [MCPServer.SENSEI, MCPServer.TAVILY],
            "personas": ["finops-optimizer", "cloud-architect"],
            "steps": [
                {
                    "step": 1,
                    "action": "suggest_personas_for_query",
                    "mcp": MCPServer.SENSEI,
                    "params": {"query": "cost optimization", "max_suggestions": 2}
                },
                {
                    "step": 2,
                    "action": "tavily_search",
                    "mcp": MCPServer.TAVILY,
                    "params": {
                        "queries": [
                            "{cloud_provider} pricing 2025",
                            "{service_type} cost optimization"
                        ]
                    }
                },
                {
                    "step": 3,
                    "action": "get_session_context",
                    "mcp": MCPServer.SENSEI,
                    "params": {"session_id": "{session_id}"}
                }
            ],
            "output_format": "cost_analysis_report",
            "cost_estimate": "$0.01-0.03",
            "time_estimate": "20-40 seconds"
        },
        WorkflowTemplate.TECH_DUE_DILIGENCE: {
            "name": "Technology Due Diligence",
            "description": "Evaluate if a technology/library is production-ready",
            "mcps": [MCPServer.SENSEI, MCPServer.TAVILY, MCPServer.CONTEXT7],
            "personas": ["pragmatic-architect", "snarky-senior-engineer"],
            "steps": [
                {
                    "step": 1,
                    "action": "suggest_personas_for_query",
                    "mcp": MCPServer.SENSEI,
                    "params": {"query": "technology evaluation", "max_suggestions": 2}
                },
                {
                    "step": 2,
                    "action": "tavily_search",
                    "mcp": MCPServer.TAVILY,
                    "params": {
                        "queries": [
                            "{technology} production ready 2025",
                            "{technology} issues problems",
                            "{technology} vs {alternative}"
                        ]
                    }
                },
                {
                    "step": 3,
                    "action": "get_library_docs",
                    "mcp": MCPServer.CONTEXT7,
                    "params": {"library": "{technology}"},
                    "optional": True
                }
            ],
            "output_format": "tech_evaluation_report",
            "cost_estimate": "$0.03-0.05",
            "time_estimate": "30-50 seconds"
        },
        WorkflowTemplate.INCIDENT_POSTMORTEM: {
            "name": "Incident Postmortem Analysis",
            "description": "Analyze incidents and generate prevention strategies",
            "mcps": [MCPServer.SENSEI, MCPServer.TAVILY],
            "personas": ["site-reliability-engineer", "incident-commander"],
            "steps": [
                {
                    "step": 1,
                    "action": "suggest_personas_for_query",
                    "mcp": MCPServer.SENSEI,
                    "params": {
                        "query": "incident analysis",
                        "context_hint": "crisis",
                        "max_suggestions": 2
                    }
                },
                {
                    "step": 2,
                    "action": "tavily_search",
                    "mcp": MCPServer.TAVILY,
                    "params": {
                        "queries": [
                            "{service} outage 2025",
                            "{service} postmortem",
                            "{incident_type} prevention"
                        ],
                        "topic": "news",
                        "days": 30
                    }
                }
            ],
            "output_format": "incident_postmortem",
            "cost_estimate": "$0.02-0.04",
            "time_estimate": "20-40 seconds"
        },
        WorkflowTemplate.ACCESSIBILITY_AUDIT: {
            "name": "Accessibility Audit (WCAG)",
            "description": "Comprehensive accessibility compliance check",
            "mcps": [MCPServer.SENSEI, MCPServer.PLAYWRIGHT, MCPServer.CONTEXT7],
            "personas": ["accessibility-specialist", "frontend-ux-specialist"],
            "steps": [
                {
                    "step": 1,
                    "action": "suggest_personas_for_query",
                    "mcp": MCPServer.SENSEI,
                    "params": {"query": "accessibility audit", "max_suggestions": 2}
                },
                {
                    "step": 2,
                    "action": "browser_navigate",
                    "mcp": MCPServer.PLAYWRIGHT,
                    "params": {"url": "{page_url}"}
                },
                {
                    "step": 3,
                    "action": "browser_snapshot",
                    "mcp": MCPServer.PLAYWRIGHT
                },
                {
                    "step": 4,
                    "action": "get_library_docs",
                    "mcp": MCPServer.CONTEXT7,
                    "params": {"library": "wcag", "topic": "accessibility"}
                }
            ],
            "output_format": "accessibility_report",
            "cost_estimate": "$0.00-0.01",
            "time_estimate": "30-45 seconds"
        },
        WorkflowTemplate.API_DESIGN_REVIEW: {
            "name": "API Design Review",
            "description": "Review API design for best practices and standards",
            "mcps": [MCPServer.SENSEI, MCPServer.CONTEXT7, MCPServer.TAVILY],
            "personas": ["api-platform-engineer", "pragmatic-architect", "security-sentinel"],
            "steps": [
                {
                    "step": 1,
                    "action": "suggest_personas_for_query",
                    "mcp": MCPServer.SENSEI,
                    "params": {"query": "API design review", "max_suggestions": 3}
                },
                {
                    "step": 2,
                    "action": "get_library_docs",
                    "mcp": MCPServer.CONTEXT7,
                    "params": {
                        "libraries": ["openapi", "rest-api-guidelines", "graphql"]
                    }
                },
                {
                    "step": 3,
                    "action": "tavily_search",
                    "mcp": MCPServer.TAVILY,
                    "params": {
                        "queries": ["API design best practices 2025", "REST API security"]
                    },
                    "optional": True
                }
            ],
            "output_format": "api_review_report",
            "cost_estimate": "$0.01-0.03",
            "time_estimate": "20-40 seconds"
        },
        WorkflowTemplate.ARCHITECTURE_REFACTORING: {
            "name": "Architecture-Driven Refactoring",
            "description": "Refactor code to follow architectural patterns with validation",
            "mcps": [MCPServer.SENSEI, MCPServer.SERENA, MCPServer.CONTEXT7],
            "personas": ["pragmatic-architect", "security-sentinel"],
            "steps": [
                {
                    "step": 1,
                    "action": "suggest_personas_for_query",
                    "mcp": MCPServer.SENSEI,
                    "params": {"query": "{user_query}", "max_suggestions": 2}
                },
                {
                    "step": 2,
                    "action": "get_library_docs",
                    "mcp": MCPServer.CONTEXT7,
                    "params": {"topic": "{pattern_type}"},
                    "optional": True
                },
                {
                    "step": 3,
                    "action": "get_symbols_overview",
                    "mcp": MCPServer.SERENA,
                    "params": {"relative_path": "{target_file}"}
                },
                {
                    "step": 4,
                    "action": "find_symbol",
                    "mcp": MCPServer.SERENA,
                    "params": {
                        "name_path_pattern": "{symbol_pattern}",
                        "include_body": True
                    }
                },
                {
                    "step": 5,
                    "action": "validate_against_standards",
                    "mcp": MCPServer.SENSEI,
                    "params": {"code_snippet": "{current_code}"}
                },
                {
                    "step": 6,
                    "action": "replace_symbol_body",
                    "mcp": MCPServer.SERENA,
                    "params": {
                        "name_path": "{symbol_name}",
                        "relative_path": "{target_file}",
                        "body": "{refactored_code}"
                    }
                },
                {
                    "step": 7,
                    "action": "check_consistency",
                    "mcp": MCPServer.SENSEI,
                    "params": {"proposed_change": "Applied {pattern_type} pattern"}
                }
            ],
            "output_format": "refactoring_report",
            "cost_estimate": "$0.00",
            "time_estimate": "30-60 seconds"
        },
        WorkflowTemplate.CODE_PATTERN_ENFORCEMENT: {
            "name": "Code Pattern Enforcement",
            "description": "Find and fix code pattern violations across codebase",
            "mcps": [MCPServer.SENSEI, MCPServer.SERENA],
            "personas": ["pragmatic-architect", "security-sentinel"],
            "steps": [
                {
                    "step": 1,
                    "action": "get_session_context",
                    "mcp": MCPServer.SENSEI,
                    "params": {"session_id": "{session_id}"}
                },
                {
                    "step": 2,
                    "action": "search_for_pattern",
                    "mcp": MCPServer.SERENA,
                    "params": {
                        "substring_pattern": "{violation_pattern}",
                        "restrict_search_to_code_files": True
                    }
                },
                {
                    "step": 3,
                    "action": "suggest_personas_for_query",
                    "mcp": MCPServer.SENSEI,
                    "params": {
                        "query": "Review pattern violations",
                        "max_suggestions": 2
                    }
                },
                {
                    "step": 4,
                    "action": "find_symbol",
                    "mcp": MCPServer.SERENA,
                    "params": {
                        "name_path_pattern": "{symbol_pattern}",
                        "include_body": True
                    }
                },
                {
                    "step": 5,
                    "action": "replace_symbol_body",
                    "mcp": MCPServer.SERENA,
                    "params": {
                        "name_path": "{symbol_name}",
                        "relative_path": "{file_path}",
                        "body": "{corrected_code}"
                    }
                },
                {
                    "step": 6,
                    "action": "record_decision",
                    "mcp": MCPServer.SENSEI,
                    "params": {
                        "category": "pattern",
                        "description": "Enforced {pattern_name} pattern"
                    }
                }
            ],
            "output_format": "pattern_enforcement_report",
            "cost_estimate": "$0.00",
            "time_estimate": "20-40 seconds"
        },
        WorkflowTemplate.DEPENDENCY_INJECTION_MIGRATION: {
            "name": "Dependency Injection Migration",
            "description": "Migrate code to dependency injection pattern with SOLID principles",
            "mcps": [MCPServer.SENSEI, MCPServer.SERENA, MCPServer.CONTEXT7],
            "personas": ["pragmatic-architect", "api-platform-engineer"],
            "steps": [
                {
                    "step": 1,
                    "action": "get_persona_content",
                    "mcp": MCPServer.SENSEI,
                    "params": {"persona_name": "pragmatic-architect"}
                },
                {
                    "step": 2,
                    "action": "get_library_docs",
                    "mcp": MCPServer.CONTEXT7,
                    "params": {"topic": "dependency injection"},
                    "optional": True
                },
                {
                    "step": 3,
                    "action": "find_symbol",
                    "mcp": MCPServer.SERENA,
                    "params": {
                        "name_path_pattern": "{class_name}",
                        "include_body": True,
                        "depth": 1
                    }
                },
                {
                    "step": 4,
                    "action": "find_referencing_symbols",
                    "mcp": MCPServer.SERENA,
                    "params": {
                        "name_path": "{class_name}",
                        "relative_path": "{file_path}"
                    }
                },
                {
                    "step": 5,
                    "action": "insert_before_symbol",
                    "mcp": MCPServer.SERENA,
                    "params": {
                        "name_path": "{class_name}",
                        "relative_path": "{file_path}",
                        "body": "{dependency_interfaces}"
                    }
                },
                {
                    "step": 6,
                    "action": "replace_symbol_body",
                    "mcp": MCPServer.SERENA,
                    "params": {
                        "name_path": "{class_name}/__init__",
                        "relative_path": "{file_path}",
                        "body": "{di_constructor}"
                    }
                },
                {
                    "step": 7,
                    "action": "validate_against_standards",
                    "mcp": MCPServer.SENSEI,
                    "params": {"code_snippet": "{refactored_code}"}
                },
                {
                    "step": 8,
                    "action": "record_decision",
                    "mcp": MCPServer.SENSEI,
                    "params": {
                        "category": "architecture",
                        "description": "Migrated {class_name} to DI pattern",
                        "rationale": "Improves testability and follows SOLID principles"
                    }
                }
            ],
            "output_format": "di_migration_report",
            "cost_estimate": "$0.00-0.01",
            "time_estimate": "40-80 seconds"
        },
        WorkflowTemplate.PR_SECURITY_REVIEW: {
            "name": "PR Security & Architecture Review",
            "description": "Multi-persona review of pull requests with security and architectural analysis",
            "mcps": [MCPServer.SENSEI, MCPServer.GITHUB, MCPServer.CONTEXT7],
            "personas": ["security-sentinel", "pragmatic-architect", "privacy-engineer"],
            "steps": [
                {
                    "step": 1,
                    "action": "gh_pr_view",
                    "mcp": MCPServer.GITHUB,
                    "params": {"pr_number": "{pr_number}"}
                },
                {
                    "step": 2,
                    "action": "gh_pr_diff",
                    "mcp": MCPServer.GITHUB,
                    "params": {"pr_number": "{pr_number}"}
                },
                {
                    "step": 3,
                    "action": "suggest_personas_for_query",
                    "mcp": MCPServer.SENSEI,
                    "params": {
                        "query": "Review PR #{pr_number}: {pr_title}",
                        "context_hint": "security"
                    }
                },
                {
                    "step": 4,
                    "action": "get_library_docs",
                    "mcp": MCPServer.CONTEXT7,
                    "params": {"topic": "{security_standard}"},
                    "optional": True
                },
                {
                    "step": 5,
                    "action": "validate_against_standards",
                    "mcp": MCPServer.SENSEI,
                    "params": {"code_snippet": "{pr_diff}"}
                },
                {
                    "step": 6,
                    "action": "check_consistency",
                    "mcp": MCPServer.SENSEI,
                    "params": {"proposed_change": "{pr_title}"}
                }
            ],
            "output_format": "pr_review_report",
            "cost_estimate": "$0.01-0.03",
            "time_estimate": "20-40 seconds"
        },
        WorkflowTemplate.COMMIT_PATTERN_ANALYSIS: {
            "name": "Commit Pattern Analysis",
            "description": "Analyze commit history for architectural drift and pattern violations",
            "mcps": [MCPServer.SENSEI, MCPServer.GITHUB, MCPServer.SERENA],
            "personas": ["pragmatic-architect", "api-platform-engineer"],
            "steps": [
                {
                    "step": 1,
                    "action": "gh_api",
                    "mcp": MCPServer.GITHUB,
                    "params": {
                        "endpoint": "repos/{owner}/{repo}/commits",
                        "params": {"per_page": "{commit_count}"}
                    }
                },
                {
                    "step": 2,
                    "action": "get_session_context",
                    "mcp": MCPServer.SENSEI,
                    "params": {"session_id": "{session_id}"}
                },
                {
                    "step": 3,
                    "action": "search_for_pattern",
                    "mcp": MCPServer.SERENA,
                    "params": {
                        "substring_pattern": "{pattern}",
                        "restrict_search_to_code_files": True
                    },
                    "optional": True
                },
                {
                    "step": 4,
                    "action": "validate_against_standards",
                    "mcp": MCPServer.SENSEI,
                    "params": {"code_snippet": "{commit_diffs}"}
                },
                {
                    "step": 5,
                    "action": "record_decision",
                    "mcp": MCPServer.SENSEI,
                    "params": {
                        "category": "pattern",
                        "description": "Identified pattern violations in commits"
                    }
                }
            ],
            "output_format": "commit_analysis_report",
            "cost_estimate": "$0.00",
            "time_estimate": "30-60 seconds"
        },
        WorkflowTemplate.ISSUE_TRIAGE: {
            "name": "Issue Triage & Prioritization",
            "description": "Smart issue categorization with persona assignment and priority recommendation",
            "mcps": [MCPServer.SENSEI, MCPServer.GITHUB, MCPServer.TAVILY],
            "personas": ["site-reliability-engineer", "security-sentinel", "empathetic-team-lead"],
            "steps": [
                {
                    "step": 1,
                    "action": "gh_issue_view",
                    "mcp": MCPServer.GITHUB,
                    "params": {"issue_number": "{issue_number}"}
                },
                {
                    "step": 2,
                    "action": "suggest_personas_for_query",
                    "mcp": MCPServer.SENSEI,
                    "params": {
                        "query": "{issue_title}: {issue_body}",
                        "max_suggestions": 3
                    }
                },
                {
                    "step": 3,
                    "action": "tavily_search",
                    "mcp": MCPServer.TAVILY,
                    "params": {
                        "query": "{issue_title} {framework}",
                        "search_depth": "basic"
                    },
                    "optional": True
                },
                {
                    "step": 4,
                    "action": "get_session_context",
                    "mcp": MCPServer.SENSEI,
                    "params": {"session_id": "{session_id}"}
                }
            ],
            "output_format": "issue_triage_report",
            "cost_estimate": "$0.01-0.03",
            "time_estimate": "15-30 seconds"
        }
    }

    def __init__(self):
        """Initialize the MCP orchestrator."""
        pass

    def suggest_mcps_for_query(
        self,
        query: str,
        context: str = "GENERAL",
        user_mcps: Optional[List[str]] = None
    ) -> Dict:
        """
        Suggest which MCP servers to use for a given query.

        Args:
            query: The user's query
            context: Detected query context (from context_detector)
            user_mcps: Optional list of user-specified MCPs to filter

        Returns:
            Dict with suggested MCPs, rationale, and workflow suggestions
        """
        suggested_mcps = []
        query_lower = query.lower()

        # Always include Sensei
        suggested_mcps.append({
            "mcp": MCPServer.SENSEI.value,
            "confidence": 1.0,
            "rationale": "Core persona orchestration and expert analysis",
            "priority": 1
        })

        # Score each MCP server
        mcp_scores = {}
        for mcp, patterns in self.MCP_PATTERNS.items():
            score = 0.0
            matched_keywords = []

            # Keyword matching
            for keyword in patterns["keywords"]:
                if keyword in query_lower:
                    score += 0.2
                    matched_keywords.append(keyword)

            # Context relevance
            if context.upper() in patterns["contexts"]:
                score += 0.3

            # Only suggest if score > threshold
            if score > 0.2:
                mcp_scores[mcp] = {
                    "score": min(score, 1.0),
                    "keywords": matched_keywords[:3]
                }

        # Sort by score and add to suggestions
        priority = 2
        for mcp, data in sorted(mcp_scores.items(), key=lambda x: x[1]["score"], reverse=True):
            pattern_info = self.MCP_PATTERNS[mcp]
            rationale = pattern_info["description"]

            if data["keywords"]:
                rationale += f" (matched: {', '.join(data['keywords'])})"

            suggested_mcps.append({
                "mcp": mcp.value,
                "confidence": round(data["score"], 2),
                "rationale": rationale,
                "priority": priority
            })
            priority += 1

        # Filter by user-specified MCPs if provided
        if user_mcps:
            suggested_mcps = [
                s for s in suggested_mcps
                if s["mcp"] in user_mcps
            ]

        # Suggest matching workflow templates
        matching_workflows = self._suggest_workflows(query, context, suggested_mcps)

        return {
            "query": query,
            "context": context,
            "suggested_mcps": suggested_mcps,
            "total_mcps": len(suggested_mcps),
            "matching_workflows": matching_workflows,
            "estimated_cost": self._estimate_cost(suggested_mcps),
            "estimated_time": self._estimate_time(suggested_mcps)
        }

    def _suggest_workflows(
        self,
        query: str,
        context: str,
        suggested_mcps: List[Dict]
    ) -> List[Dict]:
        """Suggest pre-built workflow templates that match the query."""
        matching_workflows = []
        query_lower = query.lower()

        # Workflow keyword patterns
        workflow_keywords = {
            WorkflowTemplate.AUTH_SECURITY_REVIEW: [
                "auth", "authentication", "login", "security", "oauth", "jwt"
            ],
            WorkflowTemplate.PERFORMANCE_DEBUG: [
                "performance", "slow", "speed", "optimize", "lcp", "cls"
            ],
            WorkflowTemplate.COST_OPTIMIZATION: [
                "cost", "pricing", "expensive", "optimize", "cheaper"
            ],
            WorkflowTemplate.TECH_DUE_DILIGENCE: [
                "should we", "evaluate", "adopt", "use", "technology", "library"
            ],
            WorkflowTemplate.INCIDENT_POSTMORTEM: [
                "outage", "incident", "down", "failure", "postmortem"
            ],
            WorkflowTemplate.ACCESSIBILITY_AUDIT: [
                "accessibility", "wcag", "a11y", "screen reader"
            ],
            WorkflowTemplate.API_DESIGN_REVIEW: [
                "api", "endpoint", "rest", "graphql", "design"
            ],
            WorkflowTemplate.ARCHITECTURE_REFACTORING: [
                "refactor", "refactoring", "architecture", "pattern", "clean up"
            ],
            WorkflowTemplate.CODE_PATTERN_ENFORCEMENT: [
                "enforce", "pattern", "violation", "consistency", "standard"
            ],
            WorkflowTemplate.DEPENDENCY_INJECTION_MIGRATION: [
                "dependency injection", "di", "solid", "testability", "constructor"
            ],
            WorkflowTemplate.PR_SECURITY_REVIEW: [
                "pr", "pull request", "code review", "review pr", "pr #"
            ],
            WorkflowTemplate.COMMIT_PATTERN_ANALYSIS: [
                "commit", "commits", "history", "git log", "recent changes"
            ],
            WorkflowTemplate.ISSUE_TRIAGE: [
                "issue", "bug", "triage", "priority", "categorize"
            ]
        }

        for template, keywords in workflow_keywords.items():
            if any(kw in query_lower for kw in keywords):
                template_info = self.WORKFLOW_TEMPLATES[template]

                # Check if suggested MCPs match workflow requirements
                suggested_mcp_names = [s["mcp"] for s in suggested_mcps]
                required_mcps = [m.value for m in template_info["mcps"]]
                coverage = len(set(suggested_mcp_names) & set(required_mcps))

                matching_workflows.append({
                    "template": template.value,
                    "name": template_info["name"],
                    "description": template_info["description"],
                    "mcp_coverage": f"{coverage}/{len(required_mcps)}",
                    "cost_estimate": template_info["cost_estimate"],
                    "time_estimate": template_info["time_estimate"]
                })

        return matching_workflows[:3]  # Top 3 matches

    def _estimate_cost(self, suggested_mcps: List[Dict]) -> str:
        """Estimate total cost based on suggested MCPs."""
        has_tavily = any(s["mcp"] == "tavily" for s in suggested_mcps)

        if has_tavily:
            return "$0.01-0.10 (Tavily searches)"
        else:
            return "$0.00 (free MCPs only)"

    def _estimate_time(self, suggested_mcps: List[Dict]) -> str:
        """Estimate total time based on suggested MCPs."""
        mcp_count = len(suggested_mcps)

        if mcp_count <= 2:
            return "10-20 seconds"
        elif mcp_count <= 3:
            return "20-40 seconds"
        else:
            return "40-60 seconds"

    def get_workflow_template(
        self,
        template_name: str,
        parameters: Optional[Dict[str, str]] = None
    ) -> Dict:
        """
        Get a pre-built workflow template with optional parameter substitution.

        Args:
            template_name: Name of the workflow template
            parameters: Optional dict of parameters to substitute in steps
                       (e.g., {"user_query": "Review auth", "app_url": "https://..."})

        Returns:
            Dict with workflow definition and substituted parameters
        """
        try:
            template_enum = WorkflowTemplate(template_name)
        except ValueError:
            return {
                "error": f"Unknown workflow template: {template_name}",
                "available_templates": [t.value for t in WorkflowTemplate]
            }

        template = self.WORKFLOW_TEMPLATES[template_enum].copy()

        # Substitute parameters in steps if provided
        if parameters:
            for step in template["steps"]:
                if "params" in step:
                    step["params"] = self._substitute_params(
                        step["params"],
                        parameters
                    )

        return {
            "template": template_name,
            "workflow": template,
            "parameters_used": parameters or {}
        }

    def _substitute_params(self, params: Dict, values: Dict[str, str]) -> Dict:
        """Recursively substitute {param} placeholders in params dict."""
        result = {}
        for key, value in params.items():
            if isinstance(value, str):
                # Replace {param} placeholders
                for param_name, param_value in values.items():
                    value = value.replace(f"{{{param_name}}}", param_value)
                result[key] = value
            elif isinstance(value, list):
                result[key] = [
                    self._substitute_params({"item": v}, values)["item"]
                    if isinstance(v, str) else v
                    for v in value
                ]
            elif isinstance(value, dict):
                result[key] = self._substitute_params(value, values)
            else:
                result[key] = value
        return result

    def list_workflow_templates(self) -> List[Dict]:
        """List all available workflow templates."""
        templates = []
        for template_enum, template_data in self.WORKFLOW_TEMPLATES.items():
            templates.append({
                "id": template_enum.value,
                "name": template_data["name"],
                "description": template_data["description"],
                "mcps_required": [m.value for m in template_data["mcps"]],
                "personas": template_data["personas"],
                "steps": len(template_data["steps"]),
                "cost_estimate": template_data["cost_estimate"],
                "time_estimate": template_data["time_estimate"]
            })

        return sorted(templates, key=lambda x: x["name"])
