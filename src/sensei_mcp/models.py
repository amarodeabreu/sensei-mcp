from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Any, Optional

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
class Consultation:
    """Record of a persona consultation"""
    id: str
    timestamp: str
    query: str
    mode: str  # orchestrated, quick, standards
    personas_consulted: List[str]
    context: str  # CRISIS, SECURITY, etc.
    synthesis: str
    decision_id: Optional[str] = None  # Link to decision if made


@dataclass
class SessionState:
    """Current session's accumulated context"""
    session_id: str
    started_at: str
    decisions: List[Decision]
    active_constraints: List[str]
    patterns_agreed: List[str]
    consultations: List[Consultation]
    last_updated: str
