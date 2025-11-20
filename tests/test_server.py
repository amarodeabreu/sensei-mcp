#!/usr/bin/env python3
"""
Sensei MCP Server - Test Suite

Comprehensive tests to validate:
1. All 57 sections are extractable from core-directives.md
2. File type patterns map to correct contexts (32 patterns for 50+ file types)
3. Operation patterns map to correct contexts
4. Session persistence works correctly
5. Context inference accuracy
6. Tool functionality
"""

import json
import sys
from pathlib import Path
import tempfile
import pytest

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sensei_mcp.server import (
    ContextType,
    ContextInferenceEngine,
    RulebookLoader,
    SessionManager,
    DIRECTIVES_PATH,
)


# ============================================================================
# Test Suite 1: Directives File
# ============================================================================

def test_directives_file_exists():
    """Test that core-directives.md exists and is readable"""
    assert DIRECTIVES_PATH.exists(), f"core-directives.md not found at {DIRECTIVES_PATH}"


def test_directives_file_readable():
    """Test that directives file is readable and substantial"""
    content = DIRECTIVES_PATH.read_text()
    assert len(content) > 1000, "Directives file is too short"


def test_directives_has_section_markers():
    """Test that directives file has all section markers"""
    content = DIRECTIVES_PATH.read_text()
    markers_found = content.count("<!-- SECTION:")
    assert markers_found >= 57, f"Expected 57+ section markers, found {markers_found}"


# ============================================================================
# Test Suite 2: Section Extraction
# ============================================================================

@pytest.mark.parametrize("context_type", list(ContextType))
def test_section_extraction(context_type):
    """Test that each section can be extracted"""
    rulebook = RulebookLoader(DIRECTIVES_PATH)
    section_name = context_type.value
    content = rulebook.extract_section(section_name)

    assert content, f"Section {section_name} returned empty content"
    assert "not found" not in content.lower(), f"Section {section_name} not found"
    assert len(content) > 50, f"Section {section_name} is too short"


# ============================================================================
# Test Suite 3: File Pattern Mapping
# ============================================================================

@pytest.mark.parametrize("file_path,expected_contexts", [
    ("api/billing.py", [ContextType.APIS_CONTRACTS, ContextType.SECURITY_PRIVACY, ContextType.MULTI_TENANCY]),
    ("database/migrations/001_init.sql", [ContextType.DATA_PERSISTENCE, ContextType.MULTI_TENANCY]),
    ("infra/main.tf", [ContextType.CLOUD_PLATFORM, ContextType.COST_CAPACITY]),
    ("auth/tokens.py", [ContextType.SECURITY_PRIVACY, ContextType.MULTI_TENANCY]),
    ("tests/test_api.py", [ContextType.TESTING, ContextType.TESTS_LINTERS]),
    ("src/utils.js", [ContextType.CODE_QUALITY, ContextType.CORE_PHILOSOPHY]),
    ("frontend/App.tsx", [ContextType.PERFORMANCE_UX, ContextType.I18N_A11Y]),
    (".env.example", [ContextType.OBSERVABILITY, ContextType.AI_SAFETY]),
    ("README.md", [ContextType.DOCUMENTATION, ContextType.COMMUNICATION]),
])
def test_file_pattern_mapping(file_path, expected_contexts):
    """Test that file patterns map to correct contexts"""
    contexts = ContextInferenceEngine.infer_contexts(file_paths=[file_path])

    # Check if at least one expected context is present
    matches = [exp for exp in expected_contexts if exp in contexts]
    assert len(matches) > 0, f"Expected one of {[e.value for e in expected_contexts]}, got {[c.value for c in contexts]}"


# ============================================================================
# Test Suite 4: Operation Mapping
# ============================================================================

@pytest.mark.parametrize("operation,expected_contexts", [
    ("CREATE new service", [ContextType.CORE_PHILOSOPHY, ContextType.PROTOTYPE_MODE]),
    ("REFACTOR authentication", [ContextType.CODE_QUALITY, ContextType.REFACTORING]),
    ("DEBUG payment failures", [ContextType.OBSERVABILITY, ContextType.TESTS_LINTERS]),
    ("DESIGN database schema", [ContextType.ARCHITECTURE, ContextType.TASK_SHAPING]),
    ("REVIEW pull request", [ContextType.CODE_REVIEW, ContextType.ANTI_PATTERNS]),
    ("OPTIMIZE query performance", [ContextType.COST_CAPACITY, ContextType.PERFORMANCE_UX]),
    ("SECURITY audit", [ContextType.SECURITY_PRIVACY, ContextType.AI_SAFETY]),
])
def test_operation_mapping(operation, expected_contexts):
    """Test that operations map to correct contexts"""
    contexts = ContextInferenceEngine.infer_contexts(operation=operation)

    matches = [exp for exp in expected_contexts if exp in contexts]
    assert len(matches) > 0, f"Expected one of {[e.value for e in expected_contexts]}, got {[c.value for c in contexts]}"


# ============================================================================
# Test Suite 5: Keyword Triggers
# ============================================================================

@pytest.mark.parametrize("description,expected_contexts", [
    ("Handle multi-tenant isolation", [ContextType.MULTI_TENANCY]),
    ("Process payment with async queue", [ContextType.CONCURRENCY, ContextType.SECURITY_PRIVACY]),
    ("Scale for performance", [ContextType.COST_CAPACITY, ContextType.PERFORMANCE_UX]),
    ("Help junior developer understand", [ContextType.PERSONALITY, ContextType.COMMUNICATION]),
    ("Migrate legacy codebase", [ContextType.CONTEXT_AWARENESS, ContextType.DELIVERY]),
    ("Build prototype spike", [ContextType.PROTOTYPE_MODE]),
])
def test_keyword_triggers(description, expected_contexts):
    """Test that keywords trigger appropriate contexts"""
    contexts = ContextInferenceEngine.infer_contexts(description=description)

    matches = [exp for exp in expected_contexts if exp in contexts]
    assert len(matches) > 0, f"Expected one of {[e.value for e in expected_contexts]}"


# ============================================================================
# Test Suite 6: Session Persistence
# ============================================================================

def test_session_create_new():
    """Test creating a new session"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_session_dir = Path(temp_dir)
        session_mgr = SessionManager(temp_session_dir)

        session = session_mgr.get_or_create_session("test-session")
        assert session.session_id == "test-session"
        assert len(session.decisions) == 0


def test_session_add_decision():
    """Test adding a decision to session"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_session_dir = Path(temp_dir)
        session_mgr = SessionManager(temp_session_dir)
        session_mgr.get_or_create_session("test-session")

        decision = session_mgr.add_decision(
            category="architecture",
            description="Use Postgres",
            rationale="Proven at scale"
        )

        assert decision is not None
        assert session_mgr.current_session.decisions[0].description == "Use Postgres"


def test_session_persist_to_disk():
    """Test persisting session to disk"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_session_dir = Path(temp_dir)
        session_mgr = SessionManager(temp_session_dir)
        session_mgr.get_or_create_session("test-session")

        session_mgr.add_decision(
            category="architecture",
            description="Use Postgres",
            rationale="Proven at scale"
        )

        session_file = temp_session_dir / "test-session.json"
        assert session_file.exists(), "Session file not created"


def test_session_load_existing():
    """Test loading an existing session from disk"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_session_dir = Path(temp_dir)

        # Create and save session
        session_mgr = SessionManager(temp_session_dir)
        session_mgr.get_or_create_session("test-session")
        session_mgr.add_decision(
            category="architecture",
            description="Use Postgres",
            rationale="Proven at scale"
        )

        # Load in new manager
        new_mgr = SessionManager(temp_session_dir)
        loaded_session = new_mgr.get_or_create_session("test-session")

        assert len(loaded_session.decisions) == 1
        assert loaded_session.decisions[0].description == "Use Postgres"


def test_session_constraints_and_patterns():
    """Test persisting constraints and patterns"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_session_dir = Path(temp_dir)

        # Create session with constraints and patterns
        session_mgr = SessionManager(temp_session_dir)
        session = session_mgr.get_or_create_session("test-session")
        session.active_constraints.append("postgres-only")
        session.patterns_agreed.append("hexagonal-architecture")
        session_mgr.save_session()

        # Load and verify
        check_mgr = SessionManager(temp_session_dir)
        check_session = check_mgr.get_or_create_session("test-session")

        assert "postgres-only" in check_session.active_constraints
        assert "hexagonal-architecture" in check_session.patterns_agreed


# ============================================================================
# Test Suite 7: Context Inference Integration
# ============================================================================

@pytest.mark.parametrize("scenario", [
    {
        "name": "API security review",
        "file_paths": ["api/billing.py"],
        "operation": "REVIEW for security",
        "description": "Check multi-tenant isolation",
        "expected_contexts": [
            ContextType.APIS_CONTRACTS,
            ContextType.SECURITY_PRIVACY,
            ContextType.MULTI_TENANCY,
        ]
    },
    {
        "name": "Database migration design",
        "file_paths": ["db/migrations/001_add_tenants.sql"],
        "operation": "DESIGN",
        "description": "Add tenant_id column",
        "expected_contexts": [
            ContextType.DATA_PERSISTENCE,
            ContextType.MULTI_TENANCY,
            ContextType.ARCHITECTURE,
        ]
    },
    {
        "name": "Cloud infrastructure",
        "file_paths": ["infra/main.tf"],
        "operation": "DEPLOY",
        "description": "Cost-optimized GCP setup",
        "expected_contexts": [
            ContextType.CLOUD_PLATFORM,
            ContextType.COST_CAPACITY,
            ContextType.DELIVERY,
        ]
    },
])
def test_context_inference_integration(scenario):
    """Test complete context inference scenarios"""
    contexts = ContextInferenceEngine.infer_contexts(
        file_paths=scenario["file_paths"],
        operation=scenario["operation"],
        description=scenario["description"]
    )

    # Check if we get at least 2 of the expected contexts
    matches = sum(1 for exp in scenario["expected_contexts"] if exp in contexts)
    assert matches >= 2, f"Expected at least 2 of {[e.value for e in scenario['expected_contexts']]}"


# ============================================================================
# Test Suite 8: Core Always Loaded
# ============================================================================

@pytest.mark.parametrize("file_paths,operation,description", [
    ([], None, None),  # Empty
    (["random.txt"], None, None),  # Unknown file
    (None, "UNKNOWN_OP", None),  # Unknown operation
])
def test_core_always_loaded(file_paths, operation, description):
    """Test that core principles are always loaded"""
    contexts = ContextInferenceEngine.infer_contexts(
        file_paths=file_paths,
        operation=operation,
        description=description
    )

    assert ContextType.CORE_PRINCIPLES in contexts, "Core principles not loaded"
    assert ContextType.PERSONALITY in contexts, "Personality not loaded"
