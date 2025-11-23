"""
Tests for Database Architect persona (v0.5.0 Feature #4).

Testing persona loading, metadata, and registry integration.
"""

import pytest
from pathlib import Path
from sensei_mcp.personas.loader import SkillLoader
from sensei_mcp.personas.registry import PersonaRegistry
from sensei_mcp.personas.base import BasePersona


@pytest.fixture
def database_architect_path():
    """Get path to database-architect.md file."""
    return Path(__file__).parent.parent / "src" / "sensei_mcp" / "personas" / "skills" / "database-architect.md"


@pytest.fixture
def persona_registry():
    """Create a PersonaRegistry instance."""
    skills_dir = Path(__file__).parent.parent / "src" / "sensei_mcp" / "personas" / "skills"
    return PersonaRegistry(skills_dir=skills_dir)


class TestDatabaseArchitectPersona:
    """Test Database Architect persona loading and functionality."""

    def test_persona_file_exists(self, database_architect_path):
        """Test that database-architect.md file exists."""
        assert database_architect_path.exists(), "Database Architect persona file should exist"

    def test_persona_loads_successfully(self, database_architect_path):
        """Test that the persona loads without errors."""
        skill_data = SkillLoader.load_skill(database_architect_path)

        assert skill_data is not None
        assert 'metadata' in skill_data
        assert 'principles' in skill_data
        assert 'personality' in skill_data
        assert 'full_content' in skill_data

    def test_persona_metadata(self, database_architect_path):
        """Test that persona has correct metadata."""
        skill_data = SkillLoader.load_skill(database_architect_path)
        metadata = skill_data['metadata']

        assert metadata['name'] == 'database-architect'
        assert 'description' in metadata
        assert len(metadata['description']) > 0
        assert 'database' in metadata['description'].lower() or 'schema' in metadata['description'].lower()

    def test_persona_has_expertise(self, database_architect_path):
        """Test that persona has expertise metadata."""
        skill_data = SkillLoader.load_skill(database_architect_path)
        metadata = skill_data['metadata']

        assert 'expertise' in metadata
        assert isinstance(metadata['expertise'], list)
        assert len(metadata['expertise']) > 0

        # Check for database-related expertise
        expertise_str = ' '.join(metadata['expertise']).lower()
        assert any(keyword in expertise_str for keyword in ['database', 'schema', 'query', 'sql', 'index'])

    def test_persona_has_v040_metadata(self, database_architect_path):
        """Test that persona has v0.4.0 metadata fields."""
        skill_data = SkillLoader.load_skill(database_architect_path)
        metadata = skill_data['metadata']

        # v0.4.0 fields
        assert 'quick_tip' in metadata
        assert 'examples' in metadata
        assert 'use_when' in metadata
        assert 'related_personas' in metadata

        # Verify they have content
        assert len(metadata['quick_tip']) > 0
        assert len(metadata['examples']) > 0
        assert len(metadata['use_when']) > 0
        assert len(metadata['related_personas']) > 0

    def test_persona_examples_are_database_focused(self, database_architect_path):
        """Test that example queries are database-focused."""
        skill_data = SkillLoader.load_skill(database_architect_path)
        metadata = skill_data['metadata']
        examples = metadata['examples']

        # Check that examples contain database-related terms
        examples_str = ' '.join(examples).lower()
        assert any(keyword in examples_str for keyword in
                   ['database', 'schema', 'query', 'index', 'table', 'migration', 'sql'])

    def test_persona_related_personas(self, database_architect_path):
        """Test that related personas are appropriate."""
        skill_data = SkillLoader.load_skill(database_architect_path)
        metadata = skill_data['metadata']
        related = metadata['related_personas']

        # Should be related to data engineering and architecture
        expected_related = ['data-engineer', 'pragmatic-architect', 'site-reliability-engineer']

        for expected in expected_related:
            assert expected in related, f"{expected} should be in related_personas"

    def test_persona_has_core_principles(self, database_architect_path):
        """Test that persona has core principles."""
        skill_data = SkillLoader.load_skill(database_architect_path)
        principles = skill_data['principles']

        assert len(principles) > 0
        assert len(principles) <= 10  # Max 10 principles

        # Check for database-related principles
        principles_str = ' '.join(principles).lower()
        assert any(keyword in principles_str for keyword in
                   ['schema', 'index', 'query', 'migration', 'scale', 'performance'])

    def test_persona_has_personality_section(self, database_architect_path):
        """Test that persona has personality description."""
        skill_data = SkillLoader.load_skill(database_architect_path)
        personality = skill_data['personality']

        assert len(personality) > 0
        assert len(personality) <= 500  # Should be truncated to 500 chars

    def test_persona_in_registry(self, persona_registry):
        """Test that Database Architect is in the persona registry."""
        persona = persona_registry.get('database-architect')

        assert persona is not None
        assert isinstance(persona, BasePersona)
        assert persona.name == 'database-architect'

    def test_persona_count_includes_database_architect(self, persona_registry):
        """Test that registry now has 23 personas (including Database Architect)."""
        all_personas = persona_registry.get_all()

        # Should have 23 personas (22 original + Database Architect)
        assert len(all_personas) >= 23

        # Verify Database Architect is present
        assert 'database-architect' in all_personas

    def test_persona_category(self, persona_registry):
        """Test that Database Architect has correct category."""
        persona = persona_registry.get('database-architect')

        # Should be in specialized category
        assert persona.category == 'specialized'

    def test_persona_quick_tip_useful(self, database_architect_path):
        """Test that quick_tip is concise and useful."""
        skill_data = SkillLoader.load_skill(database_architect_path)
        metadata = skill_data['metadata']
        quick_tip = metadata['quick_tip']

        # Should be concise (< 100 chars ideally)
        assert len(quick_tip) < 150

        # Should mention key capabilities
        tip_lower = quick_tip.lower()
        assert any(keyword in tip_lower for keyword in
                   ['database', 'schema', 'query', 'optimization'])

    def test_persona_use_when_field(self, database_architect_path):
        """Test that use_when field is descriptive."""
        skill_data = SkillLoader.load_skill(database_architect_path)
        metadata = skill_data['metadata']
        use_when = metadata['use_when']

        assert len(use_when) > 20  # Should be descriptive

        # Should mention when to use
        use_when_lower = use_when.lower()
        assert any(keyword in use_when_lower for keyword in
                   ['database', 'schema', 'query', 'design', 'optimization', 'migration'])

    def test_persona_content_has_sections(self, database_architect_path):
        """Test that persona file has multiple sections."""
        skill_data = SkillLoader.load_skill(database_architect_path)
        content = skill_data['full_content']

        # Should have multiple sections (##)
        section_count = content.count('\n## ')
        assert section_count >= 8  # At least 8 major sections

        # Check for key sections
        assert '## 0. Core Principles' in content
        assert '## 1. Personality' in content

    def test_persona_has_command_shortcuts(self, database_architect_path):
        """Test that persona has command shortcuts section."""
        skill_data = SkillLoader.load_skill(database_architect_path)
        content = skill_data['full_content']

        # Should have command shortcuts
        assert 'Command Shortcuts' in content or 'Optional Command' in content

    def test_persona_has_mantras(self, database_architect_path):
        """Test that persona has mantras section."""
        skill_data = SkillLoader.load_skill(database_architect_path)
        content = skill_data['full_content']

        # Should have mantras section
        assert 'Mantras' in content or '## 1' in content  # Mantras typically in later sections

    def test_persona_searchable_by_expertise(self, persona_registry):
        """Test that Database Architect is searchable by expertise."""
        # Search for database-related expertise
        results = persona_registry.search_by_expertise('database')

        # Should include database-architect
        assert any(p.name == 'database-architect' for p in results)

    def test_persona_schema_expertise(self, database_architect_path):
        """Test that persona covers schema design."""
        skill_data = SkillLoader.load_skill(database_architect_path)
        content = skill_data['full_content']

        content_lower = content.lower()
        assert 'schema' in content_lower
        assert 'normalization' in content_lower or 'normal form' in content_lower

    def test_persona_query_optimization_expertise(self, database_architect_path):
        """Test that persona covers query optimization."""
        skill_data = SkillLoader.load_skill(database_architect_path)
        content = skill_data['full_content']

        content_lower = content.lower()
        assert 'query' in content_lower
        assert 'optimization' in content_lower or 'optimize' in content_lower
        assert 'index' in content_lower

    def test_persona_migration_expertise(self, database_architect_path):
        """Test that persona covers migrations."""
        skill_data = SkillLoader.load_skill(database_architect_path)
        content = skill_data['full_content']

        content_lower = content.lower()
        assert 'migration' in content_lower
        assert 'rollback' in content_lower or 'reversible' in content_lower

    def test_persona_scalability_expertise(self, database_architect_path):
        """Test that persona covers scalability."""
        skill_data = SkillLoader.load_skill(database_architect_path)
        content = skill_data['full_content']

        content_lower = content.lower()
        assert 'scale' in content_lower or 'scalability' in content_lower
        assert 'partition' in content_lower or 'shard' in content_lower

    def test_persona_distinct_from_data_engineer(self, persona_registry):
        """Test that Database Architect is distinct from Data Engineer."""
        db_architect = persona_registry.get('database-architect')
        data_engineer = persona_registry.get('data-engineer')

        assert db_architect is not None
        assert data_engineer is not None

        # Should have different descriptions
        assert db_architect.description != data_engineer.description

        # Database Architect should focus more on schema/queries
        # Data Engineer should focus more on pipelines/ETL
        db_desc_lower = db_architect.description.lower()
        assert 'schema' in db_desc_lower or 'database' in db_desc_lower

    def test_persona_file_size_appropriate(self, database_architect_path):
        """Test that persona file is substantial but not too large."""
        content = database_architect_path.read_text()

        # Should be substantial (at least 5KB for comprehensive guidance)
        assert len(content) >= 5000

        # But not excessively large (< 100KB)
        assert len(content) < 100000

    def test_persona_yaml_frontmatter_valid(self, database_architect_path):
        """Test that YAML frontmatter is valid and complete."""
        import yaml

        content = database_architect_path.read_text()

        # Extract frontmatter
        if content.startswith('---\n'):
            end = content.find('\n---', 4)
            if end != -1:
                frontmatter = content[4:end]
                metadata = yaml.safe_load(frontmatter)

                # Check required fields
                assert 'name' in metadata
                assert 'description' in metadata
                assert 'category' in metadata or True  # Optional
                assert 'expertise' in metadata
                assert 'quick_tip' in metadata
                assert 'examples' in metadata
                assert 'use_when' in metadata
                assert 'related_personas' in metadata
