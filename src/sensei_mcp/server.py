#!/usr/bin/env python3
"""
Sensei MCP Server

A production-ready MCP server that actively injects engineering standards
into Claude's context based on file types, operations, and maintains session
memory of architectural decisions.

This transforms your 57-section rulebook from passive documentation into
an active engineering mentor that ensures standards actually influence behavior.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, asdict
from enum import Enum

from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("sensei")

# Paths
SERVER_DIR = Path(__file__).parent
DIRECTIVES_PATH = SERVER_DIR / "core-directives.md"
SESSION_DIR = Path.home() / ".sensei" / "sessions"
SESSION_DIR.mkdir(parents=True, exist_ok=True)


class ContextType(Enum):
    """Types of engineering contexts mapped to rulebook sections"""
    CORE_PRINCIPLES = "core_principles"          # Section 0
    PERSONALITY = "personality"                   # Section 1
    CORE_PHILOSOPHY = "core_philosophy"          # Section 2
    CODE_QUALITY = "code_quality"                # Section 3
    APIS_CONTRACTS = "apis_contracts"            # Section 4
    DATA_PERSISTENCE = "data_persistence"        # Section 5
    SECURITY_PRIVACY = "security_privacy"        # Section 6
    TESTING = "testing"                          # Section 7
    DOCUMENTATION = "documentation"              # Section 8
    CLOUD_PLATFORM = "cloud_platform"            # Section 9
    DEPENDENCIES = "dependencies"                # Section 10
    OBSERVABILITY = "observability"              # Section 11
    CLAUDE_BEHAVIOR = "claude_behavior"          # Section 12
    COMMAND_SHORTCUTS = "command_shortcuts"      # Section 13
    ANTI_PATTERNS = "anti_patterns"              # Section 14
    SANITY_CHECKLIST = "sanity_checklist"        # Section 15
    MANTRAS = "mantras"                          # Section 16
    PRODUCT_ALIGNMENT = "product_alignment"      # Section 17
    COMPLIANCE = "compliance"                    # Section 18
    COST_CAPACITY = "cost_capacity"              # Section 19
    CODE_REVIEW = "code_review"                  # Section 20
    DELIVERY = "delivery"                        # Section 21
    COMMUNICATION = "communication"              # Section 22
    SUMMARY = "summary"                          # Section 23
    UNCERTAINTY = "uncertainty"                  # Section 24
    MULTI_TENANCY = "multi_tenancy"             # Section 25
    PERFORMANCE_UX = "performance_ux"            # Section 26
    AI_SAFETY = "ai_safety"                      # Section 27
    CONTEXT_AWARENESS = "context_awareness"      # Section 28
    TOOLS_MCP = "tools_mcp"                      # Section 29
    SESSION_MEMORY = "session_memory"            # Section 30
    TASK_SHAPING = "task_shaping"                # Section 31
    CONFLICTS = "conflicts"                      # Section 32
    PROTOTYPE_MODE = "prototype_mode"            # Section 33
    COMMENTS = "comments"                        # Section 34
    ARCHITECTURE = "architecture"                # Section 35
    ALWAYS_ON_DEFAULTS = "always_on_defaults"    # Section 36
    CTO_MODE = "cto_mode"                        # Section 37
    QUALITY_BAR = "quality_bar"                  # Section 38
    CONCURRENCY = "concurrency"                  # Section 39
    ANALYTICS = "analytics"                      # Section 40
    I18N_A11Y = "i18n_a11y"                     # Section 41
    AI_HONESTY = "ai_honesty"                    # Section 42
    META_GOVERNANCE = "meta_governance"          # Section 43
    SUBAGENTS = "subagents"                      # Section 44
    SUBAGENT_SHAPING = "subagent_shaping"        # Section 45
    FILE_EDITING = "file_editing"                # Section 46
    TESTS_LINTERS = "tests_linters"              # Section 47
    WORKSPACE_HYGIENE = "workspace_hygiene"      # Section 48
    REFACTORING = "refactoring"                  # Section 49
    TOKEN_CONSTRAINTS = "token_constraints"      # Section 50
    FORMATTING = "formatting"                    # Section 51
    SELF_CONSISTENCY = "self_consistency"        # Section 52
    ASSUMPTIONS = "assumptions"                  # Section 53
    INSTRUCTION_HIERARCHY = "instruction_hierarchy"  # Section 54
    PERSONA_CONSISTENCY = "persona_consistency"  # Section 55
    ONE_LINE_SUMMARY = "one_line_summary"       # Section 56
    INTEGRATION = "integration"                  # Section 57


@dataclass
class Decision:
    """Record of an architectural or technical decision"""
    id: str
    timestamp: str
    category: str  # "architecture", "pattern", "constraint", "standard"
    description: str
    rationale: str
    context: Dict[str, Any]


@dataclass
class SessionState:
    """Current session's accumulated context"""
    session_id: str
    started_at: str
    decisions: List[Decision]
    active_constraints: List[str]
    patterns_agreed: List[str]
    last_updated: str


class SessionManager:
    """Manages session state persistence"""

    def __init__(self, session_dir: Path):
        self.session_dir = session_dir
        self.current_session: Optional[SessionState] = None

    def get_or_create_session(self, session_id: str = "default") -> SessionState:
        """Load existing session or create new one"""
        session_file = self.session_dir / f"{session_id}.json"

        if session_file.exists():
            with open(session_file, 'r') as f:
                data = json.load(f)
                self.current_session = SessionState(
                    session_id=data['session_id'],
                    started_at=data['started_at'],
                    decisions=[Decision(**d) for d in data['decisions']],
                    active_constraints=data['active_constraints'],
                    patterns_agreed=data['patterns_agreed'],
                    last_updated=data['last_updated']
                )
        else:
            self.current_session = SessionState(
                session_id=session_id,
                started_at=datetime.now().isoformat(),
                decisions=[],
                active_constraints=[],
                patterns_agreed=[],
                last_updated=datetime.now().isoformat()
            )

        return self.current_session

    def save_session(self):
        """Persist current session to disk"""
        if not self.current_session:
            return

        session_file = self.session_dir / f"{self.current_session.session_id}.json"
        self.current_session.last_updated = datetime.now().isoformat()

        with open(session_file, 'w') as f:
            data = {
                'session_id': self.current_session.session_id,
                'started_at': self.current_session.started_at,
                'decisions': [asdict(d) for d in self.current_session.decisions],
                'active_constraints': self.current_session.active_constraints,
                'patterns_agreed': self.current_session.patterns_agreed,
                'last_updated': self.current_session.last_updated
            }
            json.dump(data, f, indent=2)

    def add_decision(self, category: str, description: str, rationale: str,
                     context: Dict[str, Any] = None):
        """Record a new decision"""
        if not self.current_session:
            self.get_or_create_session()

        decision = Decision(
            id=f"dec_{len(self.current_session.decisions) + 1}",
            timestamp=datetime.now().isoformat(),
            category=category,
            description=description,
            rationale=rationale,
            context=context or {}
        )

        self.current_session.decisions.append(decision)
        self.save_session()
        return decision


class RulebookLoader:
    """Loads and manages rulebook content with section extraction"""

    def __init__(self, directives_path: Path):
        self.directives_path = directives_path
        self._full_content: Optional[str] = None
        self._section_cache: Dict[str, str] = {}

    def _load_full_content(self) -> str:
        """Load full directives file"""
        if self._full_content is None:
            if not self.directives_path.exists():
                raise FileNotFoundError(f"Core directives not found at {self.directives_path}")
            self._full_content = self.directives_path.read_text()
        return self._full_content

    def extract_section(self, section_name: str) -> str:
        """Extract a specific section from the directives"""
        if section_name in self._section_cache:
            return self._section_cache[section_name]

        content = self._load_full_content()

        # Find section by HTML comment marker
        pattern = f"<!-- SECTION: {section_name} -->(.*?)(?=<!-- SECTION:|$)"
        match = re.search(pattern, content, re.DOTALL)

        if match:
            section_content = match.group(1).strip()
            self._section_cache[section_name] = section_content
            return section_content

        return f"Section '{section_name}' not found in directives."

    def extract_multiple_sections(self, section_names: List[str]) -> str:
        """Extract multiple sections and combine them"""
        sections = []
        for name in section_names:
            content = self.extract_section(name)
            if content and "not found" not in content:
                sections.append(content)

        return "\n\n---\n\n".join(sections)


class ContextInferenceEngine:
    """
    Analyzes file paths, operations, and context to determine which
    engineering standards sections are most relevant.

    Maps all 57 sections to appropriate triggers.
    """

    # File type patterns → Context sections (32 patterns covering 50+ file types)
    FILE_PATTERNS = {
        # ========== EXISTING PATTERNS (Enhanced) ==========

        # API Files
        r'(api|route|controller|handler|endpoint)': [
            ContextType.APIS_CONTRACTS,
            ContextType.SECURITY_PRIVACY,
            ContextType.MULTI_TENANCY,
            ContextType.ALWAYS_ON_DEFAULTS,
            ContextType.CONCURRENCY,
        ],

        # Database Files
        r'\.(sql|prisma)|migration|schema|query\.sql|seed\.(sql|js|ts)|knexfile|sequelize': [
            ContextType.DATA_PERSISTENCE,
            ContextType.SECURITY_PRIVACY,
            ContextType.MULTI_TENANCY,
            ContextType.ALWAYS_ON_DEFAULTS,
            ContextType.PERFORMANCE_UX,
        ],

        # Cloud/Infrastructure
        r'\.(tf|ya?ml)|dockerfile|k8s|cloud|terraform': [
            ContextType.CLOUD_PLATFORM,
            ContextType.COMPLIANCE,
            ContextType.COST_CAPACITY,
            ContextType.OBSERVABILITY,
        ],

        # Security Files
        r'(auth|security|permission|token)': [
            ContextType.SECURITY_PRIVACY,
            ContextType.MULTI_TENANCY,
            ContextType.AI_SAFETY,
            ContextType.ALWAYS_ON_DEFAULTS,
        ],

        # Test Files (enhanced with more test patterns)
        r'(test|spec|\._test\.|\.test\.|\.e2e\.|\.integration\.|\.unit\.)': [
            ContextType.TESTING,
            ContextType.CODE_QUALITY,
            ContextType.ANTI_PATTERNS,
            ContextType.TESTS_LINTERS,
        ],

        # Code Files (original 9 languages)
        r'\.(py|js|ts|go|java|rb|rs|php|cs)': [
            ContextType.CODE_QUALITY,
            ContextType.CORE_PHILOSOPHY,
            ContextType.CONTEXT_AWARENESS,
        ],

        # Frontend Files (original frameworks)
        r'\.(tsx|jsx|vue|svelte)': [
            ContextType.PERFORMANCE_UX,
            ContextType.I18N_A11Y,
            ContextType.SECURITY_PRIVACY,  # XSS, CSRF
        ],

        # Config Files
        r'\.(env|json|config|toml)': [
            ContextType.OBSERVABILITY,
            ContextType.AI_SAFETY,
        ],

        # Documentation
        r'\.(md|rst|adoc)': [
            ContextType.DOCUMENTATION,
            ContextType.COMMUNICATION,
            ContextType.FORMATTING,
        ],

        # ========== NEW PATTERNS (23 additions for 50+ file types) ==========

        # Additional Programming Languages (JVM/Mobile/Systems)
        r'\.(kt|kts|swift|scala|c|cpp|cc|cxx|h|hpp)': [
            ContextType.CODE_QUALITY,
            ContextType.CORE_PHILOSOPHY,
            ContextType.CONTEXT_AWARENESS,
            ContextType.PERFORMANCE_UX,  # C/C++ often performance-critical
        ],

        # Modern/Functional Languages
        r'\.(dart|ex|exs|clj|cljs|elm|jl|r)': [
            ContextType.CODE_QUALITY,
            ContextType.CORE_PHILOSOPHY,
            ContextType.CONTEXT_AWARENESS,
        ],

        # Web Frontend (HTML/CSS/Styles)
        r'\.(html|htm|css|scss|sass|less|styl)': [
            ContextType.PERFORMANCE_UX,
            ContextType.I18N_A11Y,
            ContextType.SECURITY_PRIVACY,  # XSS in HTML
            ContextType.FORMATTING,
        ],

        # Modern Frontend Frameworks
        r'\.(astro|qwik|solid)': [
            ContextType.PERFORMANCE_UX,
            ContextType.I18N_A11Y,
            ContextType.SECURITY_PRIVACY,
        ],

        # Shell Scripts & Build Tools
        r'\.(sh|bash|zsh|fish)|Makefile|Rakefile|Justfile': [
            ContextType.CLOUD_PLATFORM,
            ContextType.DELIVERY,
            ContextType.OBSERVABILITY,
            ContextType.WORKSPACE_HYGIENE,
        ],

        # API Schema Languages
        r'\.(graphql|gql|proto|avro)': [
            ContextType.APIS_CONTRACTS,
            ContextType.DOCUMENTATION,
            ContextType.SECURITY_PRIVACY,
        ],

        # Data Files & Formats
        r'\.(xml|csv|tsv|parquet)': [
            ContextType.DATA_PERSISTENCE,
            ContextType.ANALYTICS,
            ContextType.I18N_A11Y,  # CSV/XML often contain i18n data
        ],

        # Data Science & Notebooks
        r'\.(ipynb|rmd)': [
            ContextType.ANALYTICS,
            ContextType.OBSERVABILITY,
            ContextType.DATA_PERSISTENCE,
            ContextType.DOCUMENTATION,
        ],

        # Mobile Platform Files
        r'(AndroidManifest\.xml|Info\.plist|build\.gradle|settings\.gradle|Podfile)': [
            ContextType.CLOUD_PLATFORM,
            ContextType.DEPENDENCIES,
            ContextType.COMPLIANCE,
            ContextType.SECURITY_PRIVACY,
        ],

        # Infrastructure as Code (additional)
        r'\.(hcl|nomad)': [
            ContextType.CLOUD_PLATFORM,
            ContextType.COMPLIANCE,
            ContextType.COST_CAPACITY,
            ContextType.OBSERVABILITY,
            ContextType.SECURITY_PRIVACY,
        ],

        # Container & Orchestration
        r'(Dockerfile|docker-compose|\.dockerfile)': [
            ContextType.CLOUD_PLATFORM,
            ContextType.COST_CAPACITY,
            ContextType.OBSERVABILITY,
            ContextType.DELIVERY,
        ],

        # Web Server Configs
        r'(nginx\.conf|apache\.conf|httpd\.conf|\.htaccess)': [
            ContextType.CLOUD_PLATFORM,
            ContextType.SECURITY_PRIVACY,
            ContextType.PERFORMANCE_UX,
        ],

        # CI/CD Configs
        r'(\.github/workflows/.*\.ya?ml|\.gitlab-ci\.yml|Jenkinsfile|\.circleci/config\.yml|azure-pipelines\.yml)': [
            ContextType.DELIVERY,
            ContextType.CLOUD_PLATFORM,
            ContextType.TESTS_LINTERS,
            ContextType.OBSERVABILITY,
        ],

        # Linter/Formatter Configs
        r'(\.eslintrc.*|\.prettierrc.*|\.stylelintrc.*|\.editorconfig|pyproject\.toml|tox\.ini|setup\.cfg)': [
            ContextType.CODE_QUALITY,
            ContextType.FORMATTING,
            ContextType.TESTS_LINTERS,
            ContextType.WORKSPACE_HYGIENE,
        ],

        # Package Manager Files
        r'(package\.json|package-lock\.json|yarn\.lock|pnpm-lock\.yaml|Gemfile|Gemfile\.lock|requirements\.txt|Pipfile|Cargo\.toml|go\.mod|go\.sum)': [
            ContextType.DEPENDENCIES,
            ContextType.SECURITY_PRIVACY,  # Dependency vulnerabilities
            ContextType.COST_CAPACITY,  # Bundle size
        ],

        # Test Framework Configs
        r'(jest\.config.*|vitest\.config.*|playwright\.config.*|cypress\.config.*|pytest\.ini|phpunit\.xml)': [
            ContextType.TESTING,
            ContextType.TESTS_LINTERS,
            ContextType.CODE_QUALITY,
        ],

        # Build Tool Configs
        r'(webpack\.config.*|vite\.config.*|rollup\.config.*|esbuild\.config.*|tsconfig\.json|babel\.config.*)': [
            ContextType.CLOUD_PLATFORM,
            ContextType.PERFORMANCE_UX,  # Build optimization
            ContextType.DEPENDENCIES,
        ],

        # Ignore Files
        r'(\.gitignore|\.dockerignore|\.npmignore|\.eslintignore)': [
            ContextType.WORKSPACE_HYGIENE,
            ContextType.SECURITY_PRIVACY,  # What to exclude
        ],

        # Environment & Secrets
        r'(\.env.*|secrets.*|credentials.*|\.aws/|\.gcloud/)': [
            ContextType.SECURITY_PRIVACY,
            ContextType.AI_SAFETY,  # Don't leak secrets
            ContextType.CLOUD_PLATFORM,
        ],

        # License & Legal
        r'(LICENSE|COPYING|NOTICE|PATENTS)': [
            ContextType.COMPLIANCE,
            ContextType.DOCUMENTATION,
        ],

        # Monitoring/Observability Configs
        r'(prometheus\.yml|grafana\.json|datadog\.ya?ml|newrelic\.yml|sentry\.config.*)': [
            ContextType.OBSERVABILITY,
            ContextType.CLOUD_PLATFORM,
            ContextType.COST_CAPACITY,
        ],

        # Email/Notification Templates
        r'(templates/.*\.(html|txt)|emails/|notifications/)': [
            ContextType.I18N_A11Y,
            ContextType.SECURITY_PRIVACY,  # Email injection
            ContextType.COMMUNICATION,
        ],
    }

    # Operation types → Context sections
    OPERATION_PATTERNS = {
        'CREATE': [
            ContextType.CORE_PHILOSOPHY,
            ContextType.PROTOTYPE_MODE,
            ContextType.QUALITY_BAR,
        ],
        'REFACTOR': [
            ContextType.CORE_PHILOSOPHY,
            ContextType.CODE_QUALITY,
            ContextType.MANTRAS,
            ContextType.SELF_CONSISTENCY,
            ContextType.REFACTORING,
        ],
        'DEBUG': [
            ContextType.OBSERVABILITY,
            ContextType.CLAUDE_BEHAVIOR,
            ContextType.UNCERTAINTY,
            ContextType.TESTS_LINTERS,
        ],
        'DESIGN': [
            ContextType.CORE_PHILOSOPHY,
            ContextType.PRODUCT_ALIGNMENT,
            ContextType.ARCHITECTURE,
            ContextType.TASK_SHAPING,
        ],
        'REVIEW': [
            ContextType.CODE_QUALITY,
            ContextType.ANTI_PATTERNS,
            ContextType.SANITY_CHECKLIST,
            ContextType.CODE_REVIEW,
        ],
        'OPTIMIZE': [
            ContextType.COST_CAPACITY,
            ContextType.PERFORMANCE_UX,
            ContextType.DATA_PERSISTENCE,
        ],
        'SECURITY': [
            ContextType.SECURITY_PRIVACY,
            ContextType.MULTI_TENANCY,
            ContextType.AI_SAFETY,
            ContextType.COMPLIANCE,
        ],
        'DEPLOY': [
            ContextType.DELIVERY,
            ContextType.CLOUD_PLATFORM,
            ContextType.OBSERVABILITY,
        ],
        'TEST': [
            ContextType.TESTING,
            ContextType.TESTS_LINTERS,
        ],
        'DOCUMENTATION': [
            ContextType.DOCUMENTATION,
            ContextType.COMMUNICATION,
            ContextType.FORMATTING,
        ],
    }

    # Keyword triggers → Context sections
    KEYWORD_PATTERNS = {
        r'(tenant|multi.?tenant|isolation)': [
            ContextType.MULTI_TENANCY,
            ContextType.ALWAYS_ON_DEFAULTS,
        ],
        r'(payment|billing|charge)': [
            ContextType.SECURITY_PRIVACY,
            ContextType.CONCURRENCY,
            ContextType.AI_SAFETY,
        ],
        r'(async|queue|background|concurrent)': [
            ContextType.CONCURRENCY,
        ],
        r'(scale|performance|slow|latency)': [
            ContextType.COST_CAPACITY,
            ContextType.PERFORMANCE_UX,
        ],
        r'(junior|explain|help|teach)': [
            ContextType.PERSONALITY,
            ContextType.COMMUNICATION,
        ],
        r'(cost|expensive|bill)': [
            ContextType.COST_CAPACITY,
        ],
        r'(legacy|inherited|old.?code)': [
            ContextType.CONTEXT_AWARENESS,
            ContextType.DELIVERY,
        ],
        r'(prototype|spike|poc)': [
            ContextType.PROTOTYPE_MODE,
        ],
        r'(breaking.?change|migration)': [
            ContextType.APIS_CONTRACTS,
            ContextType.DOCUMENTATION,
        ],
    }

    @classmethod
    def infer_contexts(cls,
                      file_paths: Optional[List[str]] = None,
                      operation: Optional[str] = None,
                      description: Optional[str] = None) -> Set[ContextType]:
        """
        Infer which directive sections are relevant based on context.

        Returns: Set of ContextType enums to load
        """
        contexts = set()

        # ALWAYS include core sections
        contexts.add(ContextType.CORE_PRINCIPLES)
        contexts.add(ContextType.PERSONALITY)

        # Analyze file paths
        if file_paths:
            for file_path in file_paths:
                file_lower = file_path.lower()
                for pattern, context_types in cls.FILE_PATTERNS.items():
                    if re.search(pattern, file_lower):
                        contexts.update(context_types)

        # Analyze operation
        if operation:
            op_upper = operation.upper()
            for op_keyword in cls.OPERATION_PATTERNS.keys():
                if op_keyword in op_upper:
                    contexts.update(cls.OPERATION_PATTERNS[op_keyword])

        # Analyze description for keywords
        if description:
            desc_lower = description.lower()
            for pattern, context_types in cls.KEYWORD_PATTERNS.items():
                if re.search(pattern, desc_lower):
                    contexts.update(context_types)

        return contexts


# Initialize managers
session_mgr = SessionManager(SESSION_DIR)
rulebook = RulebookLoader(DIRECTIVES_PATH)


# ============================================================================
# MCP Tools - Complete Implementation
# ============================================================================

@mcp.tool()
def get_engineering_context(
    operation: str = "",
    file_paths: List[str] = None,
    description: str = "",
    session_id: str = "default"
) -> str:
    """
    Get relevant Sensei engineering context for the current task.

    Intelligently selects and returns the most relevant sections of the
    engineering rulebook (all 57 sections available) based on:
    - File types involved (API, database, cloud, tests, etc.)
    - Operation being performed (CREATE, REFACTOR, DEBUG, REVIEW, etc.)
    - Description keywords (tenant, payment, async, scale, etc.)
    - Current session constraints and decisions

    This is the core context injection tool - call it at the start of any
    significant task to load only relevant portions (5-15% vs 100%).

    Args:
        operation: What you're doing (e.g., "reviewing API endpoints", "designing database schema")
        file_paths: List of file paths involved (helps determine context)
        description: Additional context about the task
        session_id: Session identifier (default: "default")

    Returns:
        Markdown-formatted engineering standards relevant to this task
    """
    # Load session
    session = session_mgr.get_or_create_session(session_id)

    # Infer relevant contexts
    contexts = ContextInferenceEngine.infer_contexts(
        file_paths=file_paths,
        operation=operation,
        description=description
    )

    # Convert ContextType enums to section names
    section_names = [ctx.value for ctx in contexts]

    # Build response
    response = []

    response.append("# 🥋 ACTIVE: Sensei Mode\n")
    response.append("*Context-aware engineering standards loaded for this task*\n")

    # Add session context if any
    if session.active_constraints or session.patterns_agreed or session.decisions:
        response.append("\n## 📋 Session Context\n")

        if session.active_constraints:
            response.append(f"**Active Constraints:** {', '.join(session.active_constraints)}\n")

        if session.patterns_agreed:
            response.append(f"**Agreed Patterns:** {', '.join(session.patterns_agreed)}\n")

        if session.decisions:
            response.append(f"\n**Recent Decisions ({len(session.decisions)} total):**\n")
            for dec in session.decisions[-3:]:  # Last 3 decisions
                response.append(f"- [{dec.category}] {dec.description} - {dec.rationale}\n")

        response.append("\n---\n")

    # Add inferred contexts summary
    response.append(f"\n## 🔍 Active Contexts ({len(contexts)} sections loaded)\n")
    response.append(f"*Loaded {len(section_names)} of 57 available sections based on your task*\n\n")

    # Load and append relevant sections
    relevant_content = rulebook.extract_multiple_sections(section_names)
    response.append(relevant_content)

    # Add footer
    response.append("\n\n---\n")
    response.append(f"*Token efficiency: ~{len(relevant_content.split())} words loaded vs ~15,000 full rulebook*\n")
    response.append(f"*Session: {session_id} | Last updated: {session.last_updated}*\n")

    return "\n".join(response)


@mcp.tool()
def record_decision(
    category: str,
    description: str,
    rationale: str,
    session_id: str = "default",
    constraint: str = None,
    pattern: str = None
) -> str:
    """
    Record an architectural or technical decision for this session.

    Use this when you and the user agree on:
    - Architectural patterns (e.g., "hexagonal architecture")
    - Technical constraints (e.g., "Postgres only", "GCP-first", "multi-tenant-by-default")
    - Design standards (e.g., "REST over GraphQL", "event-driven")
    - Implementation patterns (e.g., "repository pattern for data access")

    These decisions are remembered for the entire session and included in
    future context requests to maintain consistency (Section 30: Session Memory).

    Args:
        category: Type of decision ("architecture", "pattern", "constraint", "standard")
        description: Brief description of the decision
        rationale: Why this decision was made
        session_id: Session identifier (default: "default")
        constraint: Optional constraint to add to active constraints
        pattern: Optional pattern to add to agreed patterns

    Returns:
        Confirmation message with decision ID
    """
    session = session_mgr.get_or_create_session(session_id)

    decision = session_mgr.add_decision(
        category=category,
        description=description,
        rationale=rationale,
        context={"constraint": constraint, "pattern": pattern}
    )

    # Update session constraints/patterns
    if constraint and constraint not in session.active_constraints:
        session.active_constraints.append(constraint)
        session_mgr.save_session()

    if pattern and pattern not in session.patterns_agreed:
        session.patterns_agreed.append(pattern)
        session_mgr.save_session()

    return f"""✅ Decision recorded: {decision.id}

**Decision:** {description}
**Rationale:** {rationale}
**Category:** {category}

This will be remembered for the rest of the session and included in future context requests.

Session '{session_id}' now has:
- {len(session.decisions)} decisions
- {len(session.active_constraints)} active constraints
- {len(session.patterns_agreed)} agreed patterns
"""


@mcp.tool()
def validate_against_standards(
    code_snippet: str = None,
    design_description: str = None,
    focus_areas: List[str] = None,
    session_id: str = "default"
) -> str:
    """
    Validate code or design against Sensei engineering standards.

    Returns a structured review highlighting:
    - Violations of core principles
    - Conflicts with session decisions
    - Security/multi-tenancy concerns
    - Specific improvement suggestions

    This is the pre-implementation validation tool - use it BEFORE writing
    code to catch issues early (Section 15: Sanity Checklist).

    Args:
        code_snippet: Code to validate (optional)
        design_description: Design/architecture to validate (optional)
        focus_areas: Specific areas to check (e.g., ["security", "multi-tenant", "api-design"])
        session_id: Session identifier

    Returns:
        Structured validation report with specific issues and recommendations
    """
    session = session_mgr.get_or_create_session(session_id)

    report = ["# 🔍 Standards Validation Report\n"]

    # Check against session constraints
    if session.active_constraints:
        report.append("## Session Constraints Check\n")
        report.append(f"**Active constraints:** {', '.join(session.active_constraints)}\n")
        report.append("⚠️ Verify the code/design adheres to these constraints.\n")

    # Map focus areas to context types
    area_map = {
        "security": [ContextType.SECURITY_PRIVACY, ContextType.AI_SAFETY],
        "multi-tenant": [ContextType.MULTI_TENANCY, ContextType.ALWAYS_ON_DEFAULTS],
        "api-design": [ContextType.APIS_CONTRACTS],
        "api": [ContextType.APIS_CONTRACTS],
        "data": [ContextType.DATA_PERSISTENCE],
        "database": [ContextType.DATA_PERSISTENCE],
        "testing": [ContextType.TESTING],
        "test": [ContextType.TESTING],
        "cloud": [ContextType.CLOUD_PLATFORM, ContextType.COST_CAPACITY],
        "performance": [ContextType.PERFORMANCE_UX, ContextType.COST_CAPACITY],
        "code-quality": [ContextType.CODE_QUALITY, ContextType.ANTI_PATTERNS],
    }

    # Load relevant standards
    contexts = set()
    if focus_areas:
        for area in focus_areas:
            area_lower = area.lower()
            if area_lower in area_map:
                contexts.update(area_map[area_lower])

    # Always include core checklist
    contexts.add(ContextType.SANITY_CHECKLIST)
    contexts.add(ContextType.ANTI_PATTERNS)

    if contexts:
        section_names = [ctx.value for ctx in contexts]
        relevant_content = rulebook.extract_multiple_sections(section_names)

        report.append(f"\n## 📚 Applicable Standards ({len(contexts)} sections)\n")
        report.append(relevant_content)

    report.append("\n## ✅ Core Principles Checklist (Section 0)\n")
    report.append("Validate against these 10 Iron Laws:\n\n")
    report.append("- [ ] **Explain why, not just what** - Non-trivial choices have rationale\n")
    report.append("- [ ] **Simple, not shallow** - Full implementation, not pseudocode\n")
    report.append("- [ ] **Production-grade by default** - Unless marked as spike\n")
    report.append("- [ ] **Security & multi-tenancy non-negotiable** - Not optional\n")
    report.append("- [ ] **Check reality before inventing** - Use tools to verify\n")
    report.append("- [ ] **Contracts are promises** - Backward compatibility considered\n")
    report.append("- [ ] **Cost and operability count** - Considered in design\n")
    report.append("- [ ] **Assumptions beat paralysis** - Stated if made\n")
    report.append("- [ ] **Honesty over bravado** - Uncertainties marked\n")
    report.append("- [ ] **Consistency over whim** - Aligns with session decisions\n")

    # Add session-specific checks
    if session.patterns_agreed:
        report.append(f"\n## 🏗️ Pattern Compliance Check\n")
        report.append(f"**Agreed patterns:** {', '.join(session.patterns_agreed)}\n")
        report.append("⚠️ Ensure the code/design follows these established patterns.\n")

    return "\n".join(report)


@mcp.tool()
def get_session_summary(session_id: str = "default") -> str:
    """
    Get a summary of the current session's decisions and context.

    Useful for:
    - Resuming work after a break
    - Reviewing what's been agreed
    - Checking active constraints and patterns

    Implements Section 30: Session Memory, Decisions & Consistency

    Args:
        session_id: Session identifier (default: "default")

    Returns:
        Summary of session state including all decisions, constraints, and patterns
    """
    session = session_mgr.get_or_create_session(session_id)

    summary = [f"# 📊 Session Summary: {session.session_id}\n"]
    summary.append(f"**Started:** {session.started_at}\n")
    summary.append(f"**Last updated:** {session.last_updated}\n\n")

    if session.active_constraints:
        summary.append("## 🚧 Active Constraints\n")
        for constraint in session.active_constraints:
            summary.append(f"- {constraint}\n")
        summary.append("\n")

    if session.patterns_agreed:
        summary.append("## 🏗️ Agreed Patterns\n")
        for pattern in session.patterns_agreed:
            summary.append(f"- {pattern}\n")
        summary.append("\n")

    if session.decisions:
        summary.append(f"## 📝 Decisions ({len(session.decisions)})\n")
        for dec in session.decisions:
            summary.append(f"\n### {dec.id} - {dec.timestamp}\n")
            summary.append(f"**Category:** {dec.category}\n")
            summary.append(f"**Decision:** {dec.description}\n")
            summary.append(f"**Rationale:** {dec.rationale}\n")
            if dec.context:
                summary.append(f"**Context:** {dec.context}\n")
    else:
        summary.append("## 📝 Decisions\n")
        summary.append("No decisions recorded yet. Use `record_decision()` to start tracking architectural choices.\n")

    summary.append("\n---\n")
    summary.append("*This session state is automatically included in all context requests.*\n")

    return "".join(summary)


@mcp.tool()
def list_sessions() -> str:
    """
    List all available sessions.

    Useful for managing multiple projects or switching between different
    codebases, each with their own decisions and constraints.

    Returns:
        List of session IDs with their last updated timestamps and decision counts
    """
    sessions = []
    for session_file in SESSION_DIR.glob("*.json"):
        try:
            with open(session_file, 'r') as f:
                data = json.load(f)
                sessions.append({
                    'id': data['session_id'],
                    'started': data['started_at'],
                    'updated': data['last_updated'],
                    'decisions': len(data['decisions']),
                    'constraints': len(data['active_constraints']),
                    'patterns': len(data['patterns_agreed'])
                })
        except (json.JSONDecodeError, KeyError):
            continue

    if not sessions:
        return """# 📂 Available Sessions

No sessions found. A new session will be created on first use of `get_engineering_context()`.

Sessions are stored in: {SESSION_DIR}
"""

    result = ["# 📂 Available Sessions\n"]
    result.append(f"*Found {len(sessions)} session(s)*\n\n")

    for s in sorted(sessions, key=lambda x: x['updated'], reverse=True):
        result.append(f"## {s['id']}\n")
        result.append(f"- **Started:** {s['started']}\n")
        result.append(f"- **Last updated:** {s['updated']}\n")
        result.append(f"- **Decisions:** {s['decisions']}\n")
        result.append(f"- **Constraints:** {s['constraints']}\n")
        result.append(f"- **Patterns:** {s['patterns']}\n\n")

    result.append("---\n")
    result.append(f"*Sessions stored in: {SESSION_DIR}*\n")

    return "".join(result)


@mcp.tool()
def query_specific_standard(
    section_name: str,
    session_id: str = "default"
) -> str:
    """
    Query a specific section of the rulebook directly by name.

    Use this when you need to reference a particular standard without
    going through context inference. All 57 sections are available.

    Available sections: core_principles, personality, core_philosophy,
    code_quality, apis_contracts, data_persistence, security_privacy,
    testing, documentation, cloud_platform, dependencies, observability,
    and 45 more (see ContextType enum for complete list).

    Args:
        section_name: Name of the section to query (e.g., "multi_tenancy", "concurrency")
        session_id: Session identifier (default: "default")

    Returns:
        The requested section content
    """
    session = session_mgr.get_or_create_session(session_id)

    # Validate section name
    try:
        context_type = ContextType(section_name)
    except ValueError:
        available = [ct.value for ct in ContextType]
        return f"""❌ Section '{section_name}' not found.

Available sections (57 total):
{', '.join(sorted(available))}

Use one of these exact names with query_specific_standard().
"""

    content = rulebook.extract_section(section_name)

    response = [f"# 📖 Section: {section_name}\n"]
    response.append(f"*Requested from session: {session_id}*\n\n")
    response.append("---\n\n")
    response.append(content)

    return "\n".join(response)


@mcp.tool()
def check_consistency(
    proposed_change: str,
    session_id: str = "default"
) -> str:
    """
    Check if a proposed change is consistent with session decisions and constraints.

    This validates against Section 30 (Session Memory) and Section 52 (Self-Consistency).
    Use this before implementing changes that might conflict with earlier decisions.

    Args:
        proposed_change: Description of the proposed change
        session_id: Session identifier (default: "default")

    Returns:
        Consistency check report highlighting any conflicts
    """
    session = session_mgr.get_or_create_session(session_id)

    report = ["# 🔄 Consistency Check Report\n"]
    report.append(f"**Proposed change:** {proposed_change}\n\n")

    issues = []

    # Check against constraints
    if session.active_constraints:
        report.append("## 🚧 Constraint Validation\n")
        for constraint in session.active_constraints:
            constraint_lower = constraint.lower()
            change_lower = proposed_change.lower()

            # Simple keyword matching (could be enhanced)
            if "postgres" in constraint_lower and any(db in change_lower for db in ["mysql", "mongodb", "dynamodb"]):
                issues.append(f"⚠️ **Conflicts with constraint:** '{constraint}' - proposed change mentions alternative database")

            if "multi-tenant" in constraint_lower and "single-tenant" in change_lower:
                issues.append(f"⚠️ **Conflicts with constraint:** '{constraint}' - proposed change suggests single-tenant approach")

            if "gcp" in constraint_lower and any(cloud in change_lower for cloud in ["aws", "azure"]):
                issues.append(f"⚠️ **Conflicts with constraint:** '{constraint}' - proposed change mentions alternative cloud provider")

        if not issues:
            report.append("✅ No conflicts detected with active constraints\n\n")
        else:
            for issue in issues:
                report.append(f"{issue}\n")
            report.append("\n")

    # Check against patterns
    if session.patterns_agreed:
        report.append("## 🏗️ Pattern Alignment\n")
        report.append("**Agreed patterns:**\n")
        for pattern in session.patterns_agreed:
            report.append(f"- {pattern}\n")
        report.append("\n⚠️ Ensure proposed change follows these established patterns.\n\n")

    # Check against recent decisions
    if session.decisions:
        report.append("## 📝 Recent Decision Context\n")
        report.append(f"**{len(session.decisions)} decisions in session** (showing last 5):\n\n")
        for dec in session.decisions[-5:]:
            report.append(f"- **[{dec.category}]** {dec.description}\n")
            report.append(f"  *Rationale: {dec.rationale}*\n\n")

        report.append("⚠️ Review these decisions - does your proposed change align or conflict?\n\n")

    # Summary
    report.append("## 📊 Summary\n")
    if issues:
        report.append(f"❌ **{len(issues)} potential conflict(s) detected**\n\n")
        report.append("Recommendation: Resolve conflicts before proceeding, or explicitly document why you're deviating from established constraints.\n")
    else:
        report.append("✅ **No obvious conflicts detected**\n\n")
        report.append("Proposed change appears consistent with session constraints and patterns. Proceed with implementation.\n")

    return "".join(report)


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
