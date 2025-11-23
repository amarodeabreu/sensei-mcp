"""
Tests for session merge functionality (v0.5.0 Feature #3).

Testing SessionMerger, merge_sessions(), compare_sessions(), and conflict resolution strategies.
"""

import pytest
from datetime import datetime, timedelta
from sensei_mcp.merge import SessionMerger, MergeResult, MergeConflict, format_merge_result, format_comparison
from sensei_mcp.models import SessionState, Decision, Consultation
from sensei_mcp.session import SessionManager


@pytest.fixture
def session_manager(tmp_path):
    """Create a SessionManager with temporary directory."""
    manager = SessionManager(global_session_dir=tmp_path)
    return manager


@pytest.fixture
def sample_session_a():
    """Create sample session A for testing."""
    base_time = datetime.now()

    return SessionState(
        session_id="alice-session",
        started_at=(base_time - timedelta(days=5)).isoformat(),
        last_updated=(base_time - timedelta(days=1)).isoformat(),
        decisions=[
            Decision(
                id="d1",
                timestamp=(base_time - timedelta(days=4)).isoformat(),
                category="architecture",
                description="Use microservices architecture",
                rationale="Better scalability and team autonomy",
                context={}
            ),
            Decision(
                id="d2",
                timestamp=(base_time - timedelta(days=3)).isoformat(),
                category="security",
                description="Implement OAuth2 authentication",
                rationale="Industry standard security",
                context={}
            ),
        ],
        active_constraints=[
            "Must support 10k RPS",
            "GDPR compliance required"
        ],
        patterns_agreed=[
            "Event-driven architecture",
            "API versioning with /v1 prefix"
        ],
        consultations=[
            Consultation(
                id="c1",
                timestamp=(base_time - timedelta(days=2)).isoformat(),
                query="How to scale API?",
                mode="orchestrated",
                personas_consulted=["pragmatic-architect", "site-reliability-engineer"],
                context="ARCHITECTURAL",
                synthesis="Use load balancers and horizontal scaling"
            )
        ]
    )


@pytest.fixture
def sample_session_b():
    """Create sample session B for testing (with some overlapping and conflicting data)."""
    base_time = datetime.now()

    return SessionState(
        session_id="bob-session",
        started_at=(base_time - timedelta(days=4)).isoformat(),
        last_updated=(base_time - timedelta(hours=12)).isoformat(),
        decisions=[
            Decision(
                id="d3",
                timestamp=(base_time - timedelta(days=2)).isoformat(),
                category="architecture",
                description="Use microservices architecture",
                rationale="Easier to maintain and deploy independently",  # Different rationale
                context={}
            ),
            Decision(
                id="d4",
                timestamp=(base_time - timedelta(days=1)).isoformat(),
                category="database",
                description="Use PostgreSQL for primary database",
                rationale="Better JSON support and reliability",
                context={}
            ),
        ],
        active_constraints=[
            "Must support 10k RPS",  # Overlap
            "SOC2 compliance required"  # Different
        ],
        patterns_agreed=[
            "Event-driven architecture",  # Overlap
            "REST API with OpenAPI specs"  # Different
        ],
        consultations=[
            Consultation(
                id="c2",
                timestamp=(base_time - timedelta(days=1)).isoformat(),
                query="Database selection?",
                mode="orchestrated",
                personas_consulted=["database-architect", "data-engineer"],
                context="DATABASE",
                synthesis="PostgreSQL for ACID guarantees"
            )
        ]
    )


class TestSessionMerger:
    """Test SessionMerger functionality."""

    def test_merger_initialization(self):
        """Test creating a SessionMerger."""
        merger = SessionMerger()
        assert merger is not None

    def test_merge_two_sessions_latest_strategy(self, session_manager, sample_session_a, sample_session_b):
        """Test merging two sessions with latest strategy."""
        # Save sample sessions
        session_manager.current_session = sample_session_a
        session_manager.save_session()

        session_manager.current_session = sample_session_b
        session_manager.save_session()

        # Merge
        merger = SessionMerger()
        result = merger.merge_sessions(
            session_ids=["alice-session", "bob-session"],
            target_session_id="team-session",
            session_manager=session_manager,
            conflict_strategy="latest"
        )

        assert result.success is True
        assert result.merged_session_id == "team-session"
        assert len(result.source_sessions) == 2
        assert "alice-session" in result.source_sessions
        assert "bob-session" in result.source_sessions

        # Should have 3 unique decisions (d1=OAuth2, d4=Postgres, and d3 with latest timestamp from conflicting microservices)
        assert result.decisions_merged == 3

        # Should have 3 unique constraints
        assert result.constraints_merged == 3

        # Should have 3 unique patterns
        assert result.patterns_merged == 3

        # Should have 2 consultations
        assert result.consultations_merged == 2

    def test_merge_conflict_detection(self, session_manager, sample_session_a, sample_session_b):
        """Test that conflicts are detected correctly."""
        session_manager.current_session = sample_session_a
        session_manager.save_session()

        session_manager.current_session = sample_session_b
        session_manager.save_session()

        merger = SessionMerger()

        # Use manual strategy to detect conflicts
        result = merger.merge_sessions(
            session_ids=["alice-session", "bob-session"],
            target_session_id="team-session",
            session_manager=session_manager,
            conflict_strategy="manual"
        )

        # Should detect conflict in microservices decision (same description, different rationale)
        assert len(result.conflicts) > 0

        # Find the microservices conflict
        microservices_conflicts = [c for c in result.conflicts if "microservices" in c.item_a.lower()]
        assert len(microservices_conflicts) > 0

    def test_merge_oldest_strategy(self, session_manager, sample_session_a, sample_session_b):
        """Test merging with oldest strategy."""
        session_manager.current_session = sample_session_a
        session_manager.save_session()

        session_manager.current_session = sample_session_b
        session_manager.save_session()

        merger = SessionMerger()
        result = merger.merge_sessions(
            session_ids=["alice-session", "bob-session"],
            target_session_id="team-session",
            session_manager=session_manager,
            conflict_strategy="oldest"
        )

        assert result.success is True
        assert result.strategy_used == "oldest"

    def test_merge_all_strategy(self, session_manager, sample_session_a, sample_session_b):
        """Test merging with 'all' strategy (keeps all variants)."""
        session_manager.current_session = sample_session_a
        session_manager.save_session()

        session_manager.current_session = sample_session_b
        session_manager.save_session()

        merger = SessionMerger()
        result = merger.merge_sessions(
            session_ids=["alice-session", "bob-session"],
            target_session_id="team-session",
            session_manager=session_manager,
            conflict_strategy="all"
        )

        assert result.success is True
        assert result.strategy_used == "all"
        # Should have more decisions since conflicts create numbered versions
        assert result.decisions_merged >= 3

    def test_compare_sessions(self, session_manager, sample_session_a, sample_session_b):
        """Test comparing two sessions."""
        session_manager.current_session = sample_session_a
        session_manager.save_session()

        session_manager.current_session = sample_session_b
        session_manager.save_session()

        merger = SessionMerger()
        comparison = merger.compare_sessions(
            session_a_id="alice-session",
            session_b_id="bob-session",
            session_manager=session_manager
        )

        assert comparison['session_a'] == "alice-session"
        assert comparison['session_b'] == "bob-session"

        # Check decisions comparison
        assert 'decisions' in comparison
        assert comparison['decisions']['total_a'] == 2
        assert comparison['decisions']['total_b'] == 2
        assert len(comparison['decisions']['in_both']) == 1  # "Use microservices architecture"
        assert len(comparison['decisions']['only_in_a']) == 1  # OAuth2
        assert len(comparison['decisions']['only_in_b']) == 1  # PostgreSQL

        # Check constraints comparison
        assert 'constraints' in comparison
        assert len(comparison['constraints']['in_both']) == 1  # "Must support 10k RPS"
        assert len(comparison['constraints']['only_in_a']) == 1  # GDPR
        assert len(comparison['constraints']['only_in_b']) == 1  # SOC2

        # Check patterns comparison
        assert 'patterns' in comparison
        assert len(comparison['patterns']['in_both']) == 1  # Event-driven

    def test_merge_result_formatting(self, session_manager, sample_session_a, sample_session_b):
        """Test formatting merge results as markdown."""
        session_manager.current_session = sample_session_a
        session_manager.save_session()

        session_manager.current_session = sample_session_b
        session_manager.save_session()

        merger = SessionMerger()
        result = merger.merge_sessions(
            session_ids=["alice-session", "bob-session"],
            target_session_id="team-session",
            session_manager=session_manager,
            conflict_strategy="latest"
        )

        formatted = format_merge_result(result)

        assert "# 🔄 Session Merge Result" in formatted
        assert "team-session" in formatted
        assert "alice-session" in formatted
        assert "bob-session" in formatted
        assert "Decisions Merged:" in formatted
        assert "Constraints Merged:" in formatted
        assert "Patterns Merged:" in formatted

    def test_comparison_formatting(self, session_manager, sample_session_a, sample_session_b):
        """Test formatting comparison results as markdown."""
        session_manager.current_session = sample_session_a
        session_manager.save_session()

        session_manager.current_session = sample_session_b
        session_manager.save_session()

        merger = SessionMerger()
        comparison = merger.compare_sessions(
            session_a_id="alice-session",
            session_b_id="bob-session",
            session_manager=session_manager
        )

        formatted = format_comparison(comparison)

        assert "# 🔍 Session Comparison" in formatted
        assert "alice-session" in formatted
        assert "bob-session" in formatted
        assert "## 📋 Decisions" in formatted
        assert "## 🔒 Constraints" in formatted
        assert "## 🎯 Patterns" in formatted

    def test_merge_empty_sessions(self, session_manager):
        """Test merging when one session is empty."""
        empty_session = SessionState(
            session_id="empty-session",
            started_at=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat(),
            decisions=[],
            active_constraints=[],
            patterns_agreed=[],
            consultations=[]
        )

        full_session = SessionState(
            session_id="full-session",
            started_at=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat(),
            decisions=[
                Decision(
                    id="d1",
                    timestamp=datetime.now().isoformat(),
                    category="test",
                    description="Test decision",
                    rationale="Testing",
                    context={}
                )
            ],
            active_constraints=["Test constraint"],
            patterns_agreed=["Test pattern"],
            consultations=[]
        )

        session_manager.current_session = empty_session
        session_manager.save_session()

        session_manager.current_session = full_session
        session_manager.save_session()

        merger = SessionMerger()
        result = merger.merge_sessions(
            session_ids=["empty-session", "full-session"],
            target_session_id="merged-session",
            session_manager=session_manager,
            conflict_strategy="latest"
        )

        assert result.success is True
        assert result.decisions_merged == 1
        assert result.constraints_merged == 1
        assert result.patterns_merged == 1

    def test_merge_nonexistent_session(self, session_manager, sample_session_a):
        """Test merging with a nonexistent session (creates empty session)."""
        session_manager.current_session = sample_session_a
        session_manager.save_session()

        merger = SessionMerger()
        result = merger.merge_sessions(
            session_ids=["alice-session", "nonexistent-session"],
            target_session_id="merged-session",
            session_manager=session_manager,
            conflict_strategy="latest"
        )

        # SessionManager creates empty session for nonexistent ID, so merge succeeds
        # This is actually correct behavior - creates new session
        assert result.success is True
        # Should have merged data from alice-session
        assert result.decisions_merged > 0

    def test_consultations_merge_chronologically(self, session_manager, sample_session_a, sample_session_b):
        """Test that consultations are merged and sorted chronologically."""
        session_manager.current_session = sample_session_a
        session_manager.save_session()

        session_manager.current_session = sample_session_b
        session_manager.save_session()

        merger = SessionMerger()
        result = merger.merge_sessions(
            session_ids=["alice-session", "bob-session"],
            target_session_id="team-session",
            session_manager=session_manager,
            conflict_strategy="latest"
        )

        # Load merged session to verify
        merged = session_manager.get_or_create_session("team-session")

        # Should have 2 consultations
        assert len(merged.consultations) == 2

        # Should be sorted by timestamp
        timestamps = [c.timestamp for c in merged.consultations]
        assert timestamps == sorted(timestamps)


class TestMergeConflict:
    """Test MergeConflict data structure."""

    def test_conflict_creation(self):
        """Test creating a merge conflict."""
        conflict = MergeConflict(
            type="decision",
            source_a_id="alice-session",
            source_b_id="bob-session",
            item_a="Use MongoDB",
            item_b="Use PostgreSQL",
            timestamp_a="2025-01-20T10:00:00",
            timestamp_b="2025-01-21T10:00:00"
        )

        assert conflict.type == "decision"
        assert conflict.source_a_id == "alice-session"
        assert conflict.source_b_id == "bob-session"
        assert conflict.resolution is None


class TestMergeResult:
    """Test MergeResult data structure."""

    def test_merge_result_creation(self):
        """Test creating a merge result."""
        result = MergeResult(
            merged_session_id="team-session",
            source_sessions=["alice", "bob"],
            conflicts=[],
            decisions_merged=5,
            constraints_merged=3,
            patterns_merged=4,
            consultations_merged=10,
            strategy_used="latest",
            merged_at=datetime.now().isoformat(),
            success=True,
            errors=[]
        )

        assert result.merged_session_id == "team-session"
        assert len(result.source_sessions) == 2
        assert result.success is True
        assert result.decisions_merged == 5
        assert len(result.errors) == 0
