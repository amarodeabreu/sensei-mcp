"""
Tests for session analytics functionality (v0.4.0 Feature #1).

Testing SessionAnalyzer, PersonaStats, and SessionInsights.
"""

import pytest
from datetime import datetime, timedelta
from sensei_mcp.analytics import SessionAnalyzer, PersonaStats, SessionInsights
from sensei_mcp.models import SessionState, Consultation, Decision


@pytest.fixture
def sample_consultations():
    """Create sample consultations for testing."""
    base_time = datetime.now()

    return [
        Consultation(
            id="c1",
            timestamp=(base_time - timedelta(days=1)).isoformat(),
            query="How to implement caching?",
            mode="multi-persona",
            personas_consulted=["platform-builder", "pragmatic-architect"],
            context="performance",
            synthesis="Use Redis with TTL strategy"
        ),
        Consultation(
            id="c2",
            timestamp=(base_time - timedelta(hours=12)).isoformat(),
            query="Security review needed",
            mode="quick",
            personas_consulted=["security-guardian"],
            context="security",
            synthesis="Add input validation and rate limiting"
        ),
        Consultation(
            id="c3",
            timestamp=(base_time - timedelta(hours=6)).isoformat(),
            query="API design patterns",
            mode="multi-persona",
            personas_consulted=["platform-builder", "api-architect", "pragmatic-architect"],
            context="api-design",
            synthesis="Use RESTful design with versioning"
        ),
        Consultation(
            id="c4",
            timestamp=(base_time - timedelta(days=10)).isoformat(),
            query="Old consultation",
            mode="standards",
            personas_consulted=["standards-keeper"],
            context="general",
            synthesis="Follow existing patterns"
        ),
    ]


@pytest.fixture
def sample_decisions():
    """Create sample decisions for testing."""
    base_time = datetime.now()

    return [
        Decision(
            id="d1",
            timestamp=(base_time - timedelta(days=2)).isoformat(),
            category="architecture",
            description="Use microservices",
            rationale="Better scalability",
            context={'constraint': 'Must support 10k RPS'}
        ),
        Decision(
            id="d2",
            timestamp=(base_time - timedelta(hours=8)).isoformat(),
            category="security",
            description="Implement OAuth2",
            rationale="Industry standard",
            context={'pattern': 'Token-based auth'}
        ),
    ]


@pytest.fixture
def sample_session(sample_consultations, sample_decisions):
    """Create a sample session for testing."""
    return SessionState(
        session_id="test-session",
        started_at=(datetime.now() - timedelta(days=5)).isoformat(),
        last_updated=datetime.now().isoformat(),
        consultations=sample_consultations,
        decisions=sample_decisions,
        active_constraints=["Must support 10k RPS", "GDPR compliance"],
        patterns_agreed=["Token-based auth", "Event-driven"]
    )


class TestPersonaStats:
    """Test PersonaStats data class."""

    def test_persona_stats_creation(self):
        """Test creating PersonaStats."""
        stats = PersonaStats(
            name="platform-builder",
            consultation_count=5,
            decisions_influenced=2,
            first_used="2025-01-20T10:00:00",
            last_used="2025-01-22T10:00:00",
            avg_synthesis_length=150.5,
            contexts_used=["api-design", "performance"]
        )

        assert stats.name == "platform-builder"
        assert stats.consultation_count == 5
        assert stats.decisions_influenced == 2
        assert len(stats.contexts_used) == 2
        assert stats.avg_synthesis_length == 150.5


class TestSessionInsights:
    """Test SessionInsights data class."""

    def test_session_insights_creation(self):
        """Test creating SessionInsights."""
        persona_stats_dict = {
            "platform-builder": PersonaStats(
                name="platform-builder",
                consultation_count=3,
                decisions_influenced=1,
                first_used="2025-01-20T10:00:00",
                last_used="2025-01-22T10:00:00",
                avg_synthesis_length=120.0,
                contexts_used=["api-design"]
            )
        }

        insights = SessionInsights(
            session_id="test",
            total_consultations=10,
            total_decisions=3,
            total_constraints=2,
            total_patterns=3,
            most_used_personas=[("platform-builder", 3)],
            least_used_personas=[],
            persona_stats=persona_stats_dict,
            context_distribution={"api-design": 5, "security": 3},
            mode_distribution={"multi-persona": 7, "quick": 3},
            first_consultation="2025-01-20T10:00:00",
            last_consultation="2025-01-22T15:00:00",
            consultations_by_day={"2025-01-20": 3, "2025-01-22": 7},
            avg_time_to_decision=3.3,
            decision_velocity=0.5,
            session_age_days=5,
            active_days=2,
            avg_consultations_per_day=2.0
        )

        assert insights.session_id == "test"
        assert insights.total_consultations == 10
        assert len(insights.persona_stats) == 1
        assert insights.most_used_personas[0][0] == "platform-builder"
        assert insights.decision_velocity == 0.5


class TestSessionAnalyzer:
    """Test SessionAnalyzer functionality."""

    def test_analyzer_initialization(self, sample_session):
        """Test analyzer initialization."""
        analyzer = SessionAnalyzer(sample_session)
        assert analyzer.session.session_id == "test-session"

    def test_get_insights_all_time(self, sample_session):
        """Test getting insights for all time."""
        analyzer = SessionAnalyzer(sample_session)
        insights = analyzer.get_insights(time_range="all_time")

        assert insights.session_id == "test-session"
        assert insights.total_consultations == 4
        assert insights.total_decisions == 2
        assert len(insights.persona_stats) > 0

    def test_get_insights_last_7_days(self, sample_session):
        """Test getting insights for last 7 days (should exclude 10-day-old consultation)."""
        analyzer = SessionAnalyzer(sample_session)
        insights = analyzer.get_insights(time_range="last_7_days")

        # Should have 3 consultations (excluding the 10-day-old one)
        assert insights.total_consultations == 3

    def test_get_insights_last_30_days(self, sample_session):
        """Test getting insights for last 30 days."""
        analyzer = SessionAnalyzer(sample_session)
        insights = analyzer.get_insights(time_range="last_30_days")

        # Should have all 4 consultations
        assert insights.total_consultations == 4

    def test_persona_stats_calculation(self, sample_session):
        """Test persona statistics calculation."""
        analyzer = SessionAnalyzer(sample_session)
        insights = analyzer.get_insights()

        # platform-builder appears in 2 consultations
        platform_stats = insights.persona_stats.get("platform-builder")
        assert platform_stats is not None
        assert platform_stats.consultation_count == 2

    def test_context_distribution(self, sample_session):
        """Test context distribution calculation."""
        analyzer = SessionAnalyzer(sample_session)
        insights = analyzer.get_insights()

        assert "performance" in insights.context_distribution
        assert "security" in insights.context_distribution
        assert "api-design" in insights.context_distribution
        assert insights.context_distribution["performance"] == 1

    def test_mode_distribution(self, sample_session):
        """Test mode distribution calculation."""
        analyzer = SessionAnalyzer(sample_session)
        insights = analyzer.get_insights()

        assert "multi-persona" in insights.mode_distribution
        assert "quick" in insights.mode_distribution
        # 2 multi-persona + 1 quick + 1 standards
        assert insights.mode_distribution["multi-persona"] == 2
        assert insights.mode_distribution["quick"] == 1

    def test_decision_velocity(self, sample_session):
        """Test decision velocity calculation."""
        analyzer = SessionAnalyzer(sample_session)
        insights = analyzer.get_insights()

        # Decision velocity is calculated as decisions per day
        assert insights.decision_velocity >= 0.0

    def test_min_consultations_filter(self, sample_session):
        """Test min_consultations filter."""
        analyzer = SessionAnalyzer(sample_session)

        # Only personas with 2+ consultations
        insights = analyzer.get_insights(min_consultations=2)

        # Only platform-builder and pragmatic-architect have 2 consultations
        assert len(insights.persona_stats) == 2

    def test_top_contexts(self, sample_session):
        """Test context distribution."""
        analyzer = SessionAnalyzer(sample_session)
        insights = analyzer.get_insights()

        # Should have context distribution
        assert len(insights.context_distribution) > 0
        # All contexts should be present
        assert "performance" in insights.context_distribution or \
               "security" in insights.context_distribution or \
               "api-design" in insights.context_distribution

    def test_format_markdown(self, sample_session):
        """Test markdown formatting."""
        analyzer = SessionAnalyzer(sample_session)
        insights = analyzer.get_insights()
        markdown = analyzer.format_insights(insights, format="markdown")

        assert "# Session Analytics" in markdown
        assert "test-session" in markdown
        assert "## Overview" in markdown
        assert "## Most Used Personas" in markdown
        assert "## Context Distribution" in markdown

    def test_format_json(self, sample_session):
        """Test JSON formatting."""
        import json

        analyzer = SessionAnalyzer(sample_session)
        insights = analyzer.get_insights()
        json_output = analyzer.format_insights(insights, format="json")

        # Should be valid JSON
        data = json.loads(json_output)
        assert data["session_id"] == "test-session"
        assert "total_consultations" in data
        assert "most_used_personas" in data

    def test_format_text(self, sample_session):
        """Test text formatting."""
        analyzer = SessionAnalyzer(sample_session)
        insights = analyzer.get_insights()
        text = analyzer.format_insights(insights, format="text")

        assert "Session Analytics" in text
        assert "test-session" in text
        assert "Most Used Personas:" in text

    def test_empty_session(self):
        """Test analyzer with empty session."""
        empty_session = SessionState(
            session_id="empty",
            started_at=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat(),
            consultations=[],
            decisions=[],
            active_constraints=[],
            patterns_agreed=[]
        )

        analyzer = SessionAnalyzer(empty_session)
        insights = analyzer.get_insights()

        assert insights.total_consultations == 0
        assert insights.total_decisions == 0
        assert len(insights.persona_stats) == 0
        assert insights.decision_velocity == 0.0

    def test_invalid_time_range(self, sample_session):
        """Test invalid time range defaults to all_time."""
        analyzer = SessionAnalyzer(sample_session)

        # Invalid time range should default to all_time (not raise error)
        insights = analyzer.get_insights(time_range="invalid_range")
        assert insights.total_consultations == 4  # Should get all consultations
