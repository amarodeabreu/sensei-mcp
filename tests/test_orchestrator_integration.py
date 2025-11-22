"""
Integration tests for the Skill Orchestrator.

Tests multi-persona coordination, context detection, and session integration.
"""

from pathlib import Path
from sensei_mcp.orchestrator import SkillOrchestrator
from sensei_mcp.personas import PersonaRegistry
from sensei_mcp.context_detector import ContextDetector, QueryContext
from sensei_mcp.session import SessionManager


def test_orchestrator_initialization():
    """Test that the orchestrator initializes correctly with all personas."""
    skills_dir = Path(__file__).parent.parent / "src" / "sensei_mcp" / "personas" / "skills"
    registry = PersonaRegistry(skills_dir)
    orchestrator = SkillOrchestrator(registry)

    assert orchestrator.registry is not None
    assert orchestrator.detector is not None
    print("\n✅ Orchestrator initialized successfully")


def test_context_detection():
    """Test that context detection works across all 8 context types."""
    detector = ContextDetector()

    test_cases = {
        "The production database is down!": QueryContext.CRISIS,
        "We found a security vulnerability in our auth system": QueryContext.SECURITY,
        "The CEO's nephew wants us to use MongoDB": QueryContext.POLITICAL,
        "Should we use microservices or a monolith?": QueryContext.ARCHITECTURAL,
        "Our AWS bill is $50k/month, how do we reduce it?": QueryContext.COST,
        "The team is burning out, we need help": QueryContext.TEAM,
        "How do I implement this API endpoint?": QueryContext.TECHNICAL,
        "What's the best way to learn Python?": QueryContext.GENERAL,
    }

    for query, expected_context in test_cases.items():
        detected = detector.get_primary_context(query)
        assert detected == expected_context, f"Query '{query}' detected as {detected}, expected {expected_context}"
        print(f"✅ '{query[:50]}...' → {detected.value}")

    print("\n✅ All context detection tests passed")


def test_persona_selection():
    """Test that the orchestrator selects appropriate personas for different contexts."""
    skills_dir = Path(__file__).parent.parent / "src" / "sensei_mcp" / "personas" / "skills"
    registry = PersonaRegistry(skills_dir)
    orchestrator = SkillOrchestrator(registry)

    # Crisis query
    crisis_query = "Production is down! Database crashed!"
    crisis_personas = orchestrator.select_personas(crisis_query, mode='auto')
    crisis_names = [p.name for p in crisis_personas]
    print(f"\n🚨 Crisis Query: {crisis_query}")
    print(f"   Selected: {', '.join(crisis_names)}")
    assert any('incident' in name or 'reliability' in name for name in crisis_names), \
        "Crisis query should select incident/reliability personas"

    # Security query
    security_query = "We found a SQL injection vulnerability"
    security_personas = orchestrator.select_personas(security_query, mode='auto')
    security_names = [p.name for p in security_personas]
    print(f"\n🔒 Security Query: {security_query}")
    print(f"   Selected: {', '.join(security_names)}")
    assert any('security' in name for name in security_names), \
        "Security query should select security personas"

    # Quick mode should return just Snarky
    quick_personas = orchestrator.select_personas("any query", mode='quick')
    assert len(quick_personas) == 1
    assert quick_personas[0].name == 'snarky-senior-engineer'
    print(f"\n⚡ Quick Mode: Selected {quick_personas[0].name}")

    print("\n✅ All persona selection tests passed")


def test_orchestration_modes():
    """Test different orchestration modes (auto, quick, crisis)."""
    skills_dir = Path(__file__).parent.parent / "src" / "sensei_mcp" / "personas" / "skills"
    registry = PersonaRegistry(skills_dir)
    orchestrator = SkillOrchestrator(registry)

    query = "Should we migrate to microservices?"

    # Auto mode (default)
    result_auto = orchestrator.orchestrate(query, mode='auto')
    assert 'synthesis' in result_auto
    assert 'personas_consulted' in result_auto
    assert len(result_auto['personas_consulted']) >= 2
    print(f"\n🤖 Auto Mode consulted: {', '.join(result_auto['personas_consulted'])}")

    # Quick mode
    result_quick = orchestrator.orchestrate(query, mode='quick')
    assert len(result_quick['personas_consulted']) == 1
    assert result_quick['personas_consulted'][0] == 'snarky-senior-engineer'
    print(f"⚡ Quick Mode consulted: {result_quick['personas_consulted'][0]}")

    # Crisis mode
    crisis_query = "Production database is corrupted!"
    result_crisis = orchestrator.orchestrate(crisis_query, mode='crisis')
    assert any('incident' in name or 'reliability' in name for name in result_crisis['personas_consulted'])
    print(f"🚨 Crisis Mode consulted: {', '.join(result_crisis['personas_consulted'])}")

    print("\n✅ All orchestration mode tests passed")


def test_session_context_integration():
    """Test that session context (constraints, patterns, decisions) flows to personas."""
    skills_dir = Path(__file__).parent.parent / "src" / "sensei_mcp" / "personas" / "skills"
    registry = PersonaRegistry(skills_dir)
    orchestrator = SkillOrchestrator(registry)

    # Create mock session context
    session_context = {
        'constraints': ['Must use PostgreSQL', 'Budget limit $10k/month'],
        'patterns': ['Event-driven architecture', 'CQRS pattern'],
        'decisions': [
            {'description': 'Chose Kubernetes over ECS', 'rationale': 'Better portability'}
        ]
    }

    query = "How should we handle user notifications?"
    result = orchestrator.orchestrate(query, mode='auto', session_context=session_context)

    assert result is not None
    assert 'synthesis' in result
    print(f"\n💾 Session Context Integration:")
    print(f"   Constraints: {len(session_context['constraints'])}")
    print(f"   Patterns: {len(session_context['patterns'])}")
    print(f"   Decisions: {len(session_context['decisions'])}")
    print(f"   Personas consulted: {', '.join(result['personas_consulted'])}")

    print("\n✅ Session context integration test passed")


def test_specific_persona_selection():
    """Test requesting specific personas by name."""
    skills_dir = Path(__file__).parent.parent / "src" / "sensei_mcp" / "personas" / "skills"
    registry = PersonaRegistry(skills_dir)
    orchestrator = SkillOrchestrator(registry)

    query = "How do we optimize our cloud costs?"
    specific_personas = ['finops-optimizer', 'pragmatic-architect']

    result = orchestrator.orchestrate(
        query,
        mode='auto',
        specific_personas=specific_personas
    )

    assert set(result['personas_consulted']) == set(specific_personas)
    print(f"\n🎯 Specific Persona Selection:")
    print(f"   Requested: {', '.join(specific_personas)}")
    print(f"   Consulted: {', '.join(result['personas_consulted'])}")

    print("\n✅ Specific persona selection test passed")


def test_output_formats():
    """Test different output formats (standard, executive, technical)."""
    skills_dir = Path(__file__).parent.parent / "src" / "sensei_mcp" / "personas" / "skills"
    registry = PersonaRegistry(skills_dir)
    orchestrator = SkillOrchestrator(registry)

    query = "Should we adopt Kubernetes?"

    for output_format in ['standard', 'executive', 'technical']:
        result = orchestrator.orchestrate(query, mode='auto', output_format=output_format)
        assert 'synthesis' in result
        assert len(result['synthesis']) > 0
        print(f"\n📄 {output_format.upper()} format: {len(result['synthesis'])} chars")

    print("\n✅ All output format tests passed")


if __name__ == "__main__":
    print("=" * 70)
    print("SENSEI MCP v0.3.0 - ORCHESTRATOR INTEGRATION TESTS")
    print("=" * 70)

    test_orchestrator_initialization()
    test_context_detection()
    test_persona_selection()
    test_orchestration_modes()
    test_session_context_integration()
    test_specific_persona_selection()
    test_output_formats()

    print("\n" + "=" * 70)
    print("✅ ALL INTEGRATION TESTS PASSED!")
    print("=" * 70)
