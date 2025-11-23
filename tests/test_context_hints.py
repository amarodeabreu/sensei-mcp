"""
Tests for context hint generation (v0.5.0 Feature #1C).

Testing _generate_context_hint() functionality for intelligent persona suggestions.
"""

import pytest
from sensei_mcp.server import _generate_context_hint


class TestContextHintGeneration:
    """Test context hint generation functionality."""

    def test_no_hint_when_enough_personas(self):
        """Test that no hint is generated when 2+ personas are selected."""
        hint = _generate_context_hint(
            query="How do I implement caching?",
            context="ARCHITECTURAL",
            num_personas=2
        )

        assert hint == ""

    def test_hint_generated_for_few_personas(self):
        """Test that hint is generated when <2 personas are selected."""
        hint = _generate_context_hint(
            query="How do I implement caching?",
            context="ARCHITECTURAL",
            num_personas=1
        )

        assert hint != ""
        assert "💡" in hint
        assert "Context Hint:" in hint

    def test_database_keyword_detection(self):
        """Test database keyword detection."""
        hint = _generate_context_hint(
            query="How should I design my database schema?",
            context="TECHNICAL",
            num_personas=1
        )

        assert "DATABASE" in hint
        assert "database-architect" in hint or "data-engineer" in hint or "pragmatic-architect" in hint

    def test_sql_keyword_detection(self):
        """Test SQL keyword triggers database context."""
        hint = _generate_context_hint(
            query="Help me optimize this SQL query",
            context="TECHNICAL",
            num_personas=1
        )

        assert "DATABASE" in hint

    def test_api_keyword_detection(self):
        """Test API keyword detection."""
        hint = _generate_context_hint(
            query="How do I design a REST API?",
            context="ARCHITECTURAL",
            num_personas=1
        )

        assert "API" in hint
        assert "api-platform-engineer" in hint

    def test_security_keyword_detection(self):
        """Test security keyword detection."""
        hint = _generate_context_hint(
            query="Review this authentication code for security issues",
            context="SECURITY",
            num_personas=1
        )

        assert "SECURITY" in hint
        assert "security-sentinel" in hint

    def test_frontend_keyword_detection(self):
        """Test frontend keyword detection."""
        hint = _generate_context_hint(
            query="How do I optimize my React components?",
            context="TECHNICAL",
            num_personas=1
        )

        assert "FRONTEND" in hint
        assert "frontend-ux-specialist" in hint

    def test_mobile_keyword_detection(self):
        """Test mobile keyword detection."""
        hint = _generate_context_hint(
            query="Best practices for iOS app architecture",
            context="ARCHITECTURAL",
            num_personas=1
        )

        assert "MOBILE" in hint
        assert "mobile-platform-engineer" in hint

    def test_machine_learning_keyword_detection(self):
        """Test ML keyword detection."""
        hint = _generate_context_hint(
            query="How do I deploy a machine learning model?",
            context="TECHNICAL",
            num_personas=1
        )

        assert "ML" in hint
        assert "ml-pragmatist" in hint

    def test_team_keyword_detection(self):
        """Test team/culture keyword detection."""
        hint = _generate_context_hint(
            query="How can I improve team collaboration?",
            context="TECHNICAL",
            num_personas=1
        )

        assert "TEAM" in hint
        assert "empathetic-team-lead" in hint or "product-engineering-lead" in hint

    def test_architectural_context_fallback(self):
        """Test that ARCHITECTURAL context provides default suggestions."""
        hint = _generate_context_hint(
            query="How do we scale this system?",
            context="ARCHITECTURAL",
            num_personas=1
        )

        assert hint != ""
        assert "pragmatic-architect" in hint or "snarky-senior-engineer" in hint

    def test_security_context_suggestions(self):
        """Test SECURITY context provides security personas."""
        hint = _generate_context_hint(
            query="Generic security question",
            context="SECURITY",
            num_personas=1
        )

        assert "security-sentinel" in hint
        assert "compliance-guardian" in hint

    def test_cost_context_suggestions(self):
        """Test COST context provides FinOps persona."""
        hint = _generate_context_hint(
            query="How do we reduce costs?",
            context="COST",
            num_personas=1
        )

        assert "finops-optimizer" in hint

    def test_crisis_context_suggestions(self):
        """Test CRISIS context provides incident response personas."""
        hint = _generate_context_hint(
            query="Production is down!",
            context="CRISIS",
            num_personas=1
        )

        assert "incident-commander" in hint
        assert "site-reliability-engineer" in hint

    def test_persona_limit_to_three(self):
        """Test that hints suggest max 3 personas."""
        hint = _generate_context_hint(
            query="database api security",  # Multiple keywords
            context="ARCHITECTURAL",
            num_personas=1
        )

        # Count persona names in hint
        personas_mentioned = hint.count("- `")

        # Should suggest exactly 3 personas (top 3)
        assert personas_mentioned == 3

    def test_usage_example_included(self):
        """Test that hint includes usage example."""
        hint = _generate_context_hint(
            query="How do I design a database schema?",
            context="TECHNICAL",
            num_personas=1
        )

        assert "get_engineering_guidance" in hint
        assert "specific_personas" in hint

    def test_case_insensitive_matching(self):
        """Test that keyword matching is case-insensitive."""
        hint_lower = _generate_context_hint(
            query="how do i use postgres?",
            context="TECHNICAL",
            num_personas=1
        )

        hint_upper = _generate_context_hint(
            query="How do I use POSTGRES?",
            context="TECHNICAL",
            num_personas=1
        )

        # Both should detect database context
        assert "DATABASE" in hint_lower
        assert "DATABASE" in hint_upper

    def test_multiple_keywords_first_match_wins(self):
        """Test that first keyword match determines context."""
        # "database" appears before "api"
        hint = _generate_context_hint(
            query="database api integration",
            context="TECHNICAL",
            num_personas=1
        )

        # Should prioritize database context
        assert "DATABASE" in hint

    def test_zero_personas_edge_case(self):
        """Test with 0 personas selected."""
        hint = _generate_context_hint(
            query="How do I do X?",
            context="TECHNICAL",
            num_personas=0
        )

        # Should still provide hint
        assert hint != ""
        assert "💡" in hint

    def test_no_keyword_match_uses_context(self):
        """Test that when no keyword matches, original context is used."""
        hint = _generate_context_hint(
            query="How do I xyz something?",  # No special keywords
            context="ARCHITECTURAL",
            num_personas=1
        )

        # Should fall back to ARCHITECTURAL suggestions
        assert "pragmatic-architect" in hint or "snarky-senior-engineer" in hint

    def test_technical_context_suggestions(self):
        """Test TECHNICAL context provides general engineering personas."""
        hint = _generate_context_hint(
            query="Generic technical question",
            context="TECHNICAL",
            num_personas=1
        )

        assert hint != ""
        # Should suggest technical personas
        assert ("snarky-senior-engineer" in hint or
                "legacy-archaeologist" in hint or
                "qa-automation-engineer" in hint)

    def test_postgres_specific_detection(self):
        """Test PostgreSQL keyword detection."""
        hint = _generate_context_hint(
            query="How do I optimize postgres performance?",
            context="TECHNICAL",
            num_personas=1
        )

        assert "DATABASE" in hint

    def test_mongodb_specific_detection(self):
        """Test MongoDB keyword detection."""
        hint = _generate_context_hint(
            query="Schema design for mongodb",
            context="TECHNICAL",
            num_personas=1
        )

        assert "DATABASE" in hint

    def test_graphql_api_detection(self):
        """Test GraphQL keyword detection."""
        hint = _generate_context_hint(
            query="How do I build a graphql API?",
            context="TECHNICAL",
            num_personas=1
        )

        assert "API" in hint

    def test_vue_framework_detection(self):
        """Test Vue.js keyword detection."""
        hint = _generate_context_hint(
            query="Best practices for vue components?",
            context="TECHNICAL",
            num_personas=1
        )

        assert "FRONTEND" in hint

    def test_android_platform_detection(self):
        """Test Android keyword detection."""
        hint = _generate_context_hint(
            query="Android app performance optimization",
            context="TECHNICAL",
            num_personas=1
        )

        assert "MOBILE" in hint

    def test_model_training_detection(self):
        """Test ML model training keyword detection."""
        hint = _generate_context_hint(
            query="How do I improve model training speed?",
            context="TECHNICAL",
            num_personas=1
        )

        assert "ML" in hint

    def test_culture_keyword_detection(self):
        """Test team culture keyword detection."""
        hint = _generate_context_hint(
            query="How to improve engineering culture?",
            context="TECHNICAL",
            num_personas=1
        )

        assert "TEAM" in hint

    def test_hiring_keyword_detection(self):
        """Test hiring keyword detection."""
        hint = _generate_context_hint(
            query="Best practices for hiring engineers?",
            context="TECHNICAL",
            num_personas=1
        )

        assert "TEAM" in hint
