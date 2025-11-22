"""
Smoke test for persona loading.

Verify all 21 skill personas load correctly.
"""

from pathlib import Path
from sensei_mcp.personas import PersonaRegistry

def test_all_personas_load():
    """Test that all 21 skill files load successfully."""
    skills_dir = Path(__file__).parent.parent / "src" / "sensei_mcp" / "personas" / "skills"

    registry = PersonaRegistry(skills_dir)

    # Test loading
    all_personas = registry.get_all()

    print(f"\n✅ Loaded {len(all_personas)} personas:")
    for name, persona in all_personas.items():
        print(f"  - {name}: {persona.description[:60]}...")
        assert len(persona.core_principles) > 0, f"{name} has no principles"

    assert len(all_personas) >= 21, "Expected at least 21 personas"

    # Test specific personas
    snarky = registry.get('snarky-senior-engineer')
    assert snarky is not None
    assert 'snarky' in snarky.name.lower() or 'senior' in snarky.name.lower()

    orchestrator = registry.get('skill-orchestrator')
    assert orchestrator is not None

    architect = registry.get('pragmatic-architect')
    assert architect is not None

    print("\n✅ All personas loaded successfully!")

if __name__ == "__main__":
    test_all_personas_load()
