"""
Session Analytics & Insights for Sensei MCP v0.4.0

Provides data-driven insights into persona usage, consultation patterns,
and decision-making trends.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from sensei_mcp.models import SessionState, Consultation, Decision


@dataclass
class PersonaStats:
    """Statistics for a single persona."""
    name: str
    consultation_count: int
    decisions_influenced: int  # Number of decisions where this persona was consulted
    first_used: Optional[str]
    last_used: Optional[str]
    avg_synthesis_length: float
    contexts_used: List[str]  # CRISIS, SECURITY, etc.


@dataclass
class SessionInsights:
    """Comprehensive analytics for a session."""
    session_id: str
    total_consultations: int
    total_decisions: int
    total_constraints: int
    total_patterns: int

    # Persona insights
    most_used_personas: List[tuple[str, int]]  # (persona_name, count)
    least_used_personas: List[tuple[str, int]]
    persona_stats: Dict[str, PersonaStats]

    # Context distribution
    context_distribution: Dict[str, int]  # CRISIS: 5, SECURITY: 10, etc.

    # Mode usage
    mode_distribution: Dict[str, int]  # orchestrated: 50, quick: 20, etc.

    # Time-based insights
    first_consultation: Optional[str]
    last_consultation: Optional[str]
    consultations_by_day: Dict[str, int]  # "2025-01-22": 5

    # Decision patterns
    avg_time_to_decision: Optional[float]  # Average consultations before decision
    decision_velocity: float  # Decisions per day

    # Session health
    session_age_days: int
    active_days: int
    avg_consultations_per_day: float


class SessionAnalyzer:
    """Analyzes session data to provide insights."""

    def __init__(self, session_state: SessionState):
        self.session = session_state

    def get_insights(
        self,
        time_range: str = "all_time",  # "all_time", "last_7_days", "last_30_days"
        min_consultations: int = 1
    ) -> SessionInsights:
        """
        Generate comprehensive insights for the session.

        Args:
            time_range: Time window for analysis
            min_consultations: Minimum consultations to include persona in stats

        Returns:
            SessionInsights with complete analytics
        """
        # Filter consultations by time range
        consultations = self._filter_by_time_range(
            self.session.consultations,
            time_range
        )

        if not consultations:
            return self._empty_insights()

        # Analyze personas
        persona_stats = self._analyze_personas(consultations, min_consultations)
        most_used = self._get_most_used_personas(persona_stats, limit=5)
        least_used = self._get_least_used_personas(persona_stats, limit=5)

        # Analyze contexts
        context_dist = self._analyze_contexts(consultations)

        # Analyze modes
        mode_dist = self._analyze_modes(consultations)

        # Time-based analysis
        time_stats = self._analyze_timeline(consultations)

        # Decision analysis
        decision_stats = self._analyze_decisions(consultations)

        # Session health
        health_stats = self._analyze_session_health(consultations)

        return SessionInsights(
            session_id=self.session.session_id,
            total_consultations=len(consultations),
            total_decisions=len(self.session.decisions),
            total_constraints=len(self.session.active_constraints),
            total_patterns=len(getattr(self.session, 'patterns_agreed', [])),
            most_used_personas=most_used,
            least_used_personas=least_used,
            persona_stats=persona_stats,
            context_distribution=context_dist,
            mode_distribution=mode_dist,
            first_consultation=time_stats['first'],
            last_consultation=time_stats['last'],
            consultations_by_day=time_stats['by_day'],
            avg_time_to_decision=decision_stats['avg_time'],
            decision_velocity=decision_stats['velocity'],
            session_age_days=health_stats['age_days'],
            active_days=health_stats['active_days'],
            avg_consultations_per_day=health_stats['avg_per_day']
        )

    def _filter_by_time_range(
        self,
        consultations: List[Consultation],
        time_range: str
    ) -> List[Consultation]:
        """Filter consultations by time range."""
        if time_range == "all_time":
            return consultations

        now = datetime.now()
        if time_range == "last_7_days":
            cutoff = now - timedelta(days=7)
        elif time_range == "last_30_days":
            cutoff = now - timedelta(days=30)
        else:
            return consultations

        filtered = []
        for c in consultations:
            try:
                ts = datetime.fromisoformat(c.timestamp)
                if ts >= cutoff:
                    filtered.append(c)
            except (ValueError, AttributeError):
                # Skip malformed timestamps
                continue

        return filtered

    def _analyze_personas(
        self,
        consultations: List[Consultation],
        min_consultations: int
    ) -> Dict[str, PersonaStats]:
        """Analyze persona usage patterns."""
        stats = defaultdict(lambda: {
            'count': 0,
            'decisions': set(),
            'timestamps': [],
            'synthesis_lengths': [],
            'contexts': []
        })

        # Aggregate data
        for c in consultations:
            for persona in c.personas_consulted:
                stats[persona]['count'] += 1
                stats[persona]['timestamps'].append(c.timestamp)
                stats[persona]['synthesis_lengths'].append(len(c.synthesis))
                stats[persona]['contexts'].append(c.context)
                if c.decision_id:
                    stats[persona]['decisions'].add(c.decision_id)

        # Convert to PersonaStats objects
        persona_stats = {}
        for name, data in stats.items():
            if data['count'] >= min_consultations:
                persona_stats[name] = PersonaStats(
                    name=name,
                    consultation_count=data['count'],
                    decisions_influenced=len(data['decisions']),
                    first_used=min(data['timestamps']) if data['timestamps'] else None,
                    last_used=max(data['timestamps']) if data['timestamps'] else None,
                    avg_synthesis_length=sum(data['synthesis_lengths']) / len(data['synthesis_lengths'])
                        if data['synthesis_lengths'] else 0.0,
                    contexts_used=list(set(data['contexts']))
                )

        return persona_stats

    def _get_most_used_personas(
        self,
        persona_stats: Dict[str, PersonaStats],
        limit: int = 5
    ) -> List[tuple[str, int]]:
        """Get top N most used personas."""
        sorted_personas = sorted(
            persona_stats.items(),
            key=lambda x: x[1].consultation_count,
            reverse=True
        )
        return [(name, stats.consultation_count) for name, stats in sorted_personas[:limit]]

    def _get_least_used_personas(
        self,
        persona_stats: Dict[str, PersonaStats],
        limit: int = 5
    ) -> List[tuple[str, int]]:
        """Get bottom N least used personas."""
        sorted_personas = sorted(
            persona_stats.items(),
            key=lambda x: x[1].consultation_count
        )
        return [(name, stats.consultation_count) for name, stats in sorted_personas[:limit]]

    def _analyze_contexts(self, consultations: List[Consultation]) -> Dict[str, int]:
        """Analyze context distribution."""
        contexts = [c.context for c in consultations]
        return dict(Counter(contexts))

    def _analyze_modes(self, consultations: List[Consultation]) -> Dict[str, int]:
        """Analyze mode distribution."""
        modes = [c.mode for c in consultations]
        return dict(Counter(modes))

    def _analyze_timeline(self, consultations: List[Consultation]) -> Dict[str, Any]:
        """Analyze timeline patterns."""
        if not consultations:
            return {'first': None, 'last': None, 'by_day': {}}

        timestamps = [c.timestamp for c in consultations]
        by_day = defaultdict(int)

        for ts in timestamps:
            try:
                dt = datetime.fromisoformat(ts)
                day = dt.date().isoformat()
                by_day[day] += 1
            except (ValueError, AttributeError):
                continue

        return {
            'first': min(timestamps),
            'last': max(timestamps),
            'by_day': dict(by_day)
        }

    def _analyze_decisions(self, consultations: List[Consultation]) -> Dict[str, Any]:
        """Analyze decision-making patterns."""
        consultations_with_decisions = [c for c in consultations if c.decision_id]

        # Simple heuristic: average consultations before each decision
        if consultations_with_decisions:
            avg_time = len(consultations) / len(consultations_with_decisions)
        else:
            avg_time = None

        # Decision velocity (decisions per day)
        if consultations:
            first_ts = datetime.fromisoformat(consultations[0].timestamp)
            last_ts = datetime.fromisoformat(consultations[-1].timestamp)
            days = max((last_ts - first_ts).days, 1)
            velocity = len(self.session.decisions) / days
        else:
            velocity = 0.0

        return {
            'avg_time': avg_time,
            'velocity': velocity
        }

    def _analyze_session_health(self, consultations: List[Consultation]) -> Dict[str, Any]:
        """Analyze session health metrics."""
        if not consultations:
            return {'age_days': 0, 'active_days': 0, 'avg_per_day': 0.0}

        first_ts = datetime.fromisoformat(consultations[0].timestamp)
        last_ts = datetime.fromisoformat(consultations[-1].timestamp)

        age_days = (datetime.now() - first_ts).days

        # Count unique active days
        active_days_set = set()
        for c in consultations:
            try:
                dt = datetime.fromisoformat(c.timestamp)
                active_days_set.add(dt.date().isoformat())
            except (ValueError, AttributeError):
                continue

        active_days = len(active_days_set)
        avg_per_day = len(consultations) / max(age_days, 1)

        return {
            'age_days': age_days,
            'active_days': active_days,
            'avg_per_day': avg_per_day
        }

    def _empty_insights(self) -> SessionInsights:
        """Return empty insights when no consultations exist."""
        return SessionInsights(
            session_id=self.session.session_id,
            total_consultations=0,
            total_decisions=0,
            total_constraints=0,
            total_patterns=0,
            most_used_personas=[],
            least_used_personas=[],
            persona_stats={},
            context_distribution={},
            mode_distribution={},
            first_consultation=None,
            last_consultation=None,
            consultations_by_day={},
            avg_time_to_decision=None,
            decision_velocity=0.0,
            session_age_days=0,
            active_days=0,
            avg_consultations_per_day=0.0
        )

    def format_insights(self, insights: SessionInsights, format: str = "markdown") -> str:
        """
        Format insights for human consumption.

        Args:
            insights: SessionInsights to format
            format: "markdown", "json", or "text"

        Returns:
            Formatted string
        """
        if format == "json":
            import json
            # Convert to dict for JSON serialization
            return json.dumps({
                'session_id': insights.session_id,
                'total_consultations': insights.total_consultations,
                'total_decisions': insights.total_decisions,
                'most_used_personas': insights.most_used_personas,
                'context_distribution': insights.context_distribution,
                'mode_distribution': insights.mode_distribution,
                'avg_consultations_per_day': insights.avg_consultations_per_day
            }, indent=2)

        elif format == "markdown":
            return self._format_markdown(insights)

        else:  # text
            return self._format_text(insights)

    def _format_markdown(self, insights: SessionInsights) -> str:
        """Format as markdown report."""
        lines = [
            f"# Session Analytics: {insights.session_id}",
            "",
            "## Overview",
            f"- **Total Consultations:** {insights.total_consultations}",
            f"- **Total Decisions:** {insights.total_decisions}",
            f"- **Active Constraints:** {insights.total_constraints}",
            f"- **Agreed Patterns:** {insights.total_patterns}",
            f"- **Session Age:** {insights.session_age_days} days",
            f"- **Active Days:** {insights.active_days}",
            f"- **Avg Consultations/Day:** {insights.avg_consultations_per_day:.1f}",
            "",
            "## Most Used Personas",
        ]

        for name, count in insights.most_used_personas:
            lines.append(f"- **{name}**: {count} consultations")

        lines.extend(["", "## Context Distribution"])
        for context, count in sorted(insights.context_distribution.items(), key=lambda x: -x[1]):
            lines.append(f"- **{context}**: {count}")

        lines.extend(["", "## Mode Usage"])
        for mode, count in sorted(insights.mode_distribution.items(), key=lambda x: -x[1]):
            lines.append(f"- **{mode}**: {count}")

        if insights.avg_time_to_decision:
            lines.extend([
                "",
                "## Decision Metrics",
                f"- **Avg Consultations per Decision:** {insights.avg_time_to_decision:.1f}",
                f"- **Decision Velocity:** {insights.decision_velocity:.2f} decisions/day"
            ])

        return "\n".join(lines)

    def _format_text(self, insights: SessionInsights) -> str:
        """Format as plain text."""
        lines = [
            f"Session Analytics: {insights.session_id}",
            "=" * 60,
            f"Total Consultations: {insights.total_consultations}",
            f"Total Decisions: {insights.total_decisions}",
            f"Session Age: {insights.session_age_days} days",
            "",
            "Most Used Personas:"
        ]

        for name, count in insights.most_used_personas:
            lines.append(f"  {name}: {count}")

        return "\n".join(lines)
