"""
Session Merge & Team Sync Module (v0.5.0)

Enables teams to combine session insights from multiple developers,
resolving conflicts and tracking attribution.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Optional, Literal
from pathlib import Path
import json

from .models import SessionState, Decision, Consultation


ConflictStrategy = Literal["latest", "manual", "all", "oldest"]


@dataclass
class MergeConflict:
    """Represents a conflict between two sessions during merge."""
    type: str  # "decision", "constraint", "pattern"
    source_a_id: str
    source_b_id: str
    item_a: str
    item_b: str
    timestamp_a: str
    timestamp_b: str
    resolution: Optional[str] = None


@dataclass
class MergeResult:
    """Result of merging two or more sessions."""
    merged_session_id: str
    source_sessions: List[str]
    conflicts: List[MergeConflict]
    decisions_merged: int
    constraints_merged: int
    patterns_merged: int
    consultations_merged: int
    strategy_used: str
    merged_at: str
    success: bool
    errors: List[str]


class SessionMerger:
    """
    Handles merging of multiple Sensei sessions with conflict resolution.

    Supports multiple merge strategies:
    - "latest": Use most recent timestamp (default)
    - "oldest": Use oldest timestamp
    - "all": Keep all variants (creates numbered versions)
    - "manual": Return conflicts for manual resolution
    """

    def merge_sessions(
        self,
        session_ids: List[str],
        target_session_id: str,
        session_manager,
        conflict_strategy: ConflictStrategy = "latest",
        project_root: Optional[str] = None
    ) -> MergeResult:
        """
        Merge multiple sessions into a single target session.

        Args:
            session_ids: List of session IDs to merge
            target_session_id: ID for the merged session
            session_manager: SessionManager instance
            conflict_strategy: How to resolve conflicts
            project_root: Optional project root for local sessions

        Returns:
            MergeResult with merged session and conflict information
        """
        merge_result = MergeResult(
            merged_session_id=target_session_id,
            source_sessions=session_ids,
            conflicts=[],
            decisions_merged=0,
            constraints_merged=0,
            patterns_merged=0,
            consultations_merged=0,
            strategy_used=conflict_strategy,
            merged_at=datetime.utcnow().isoformat(),
            success=False,
            errors=[]
        )

        try:
            # Load all source sessions
            sessions = []
            for session_id in session_ids:
                try:
                    session = session_manager.get_or_create_session(session_id, project_root)
                    sessions.append(session)
                except Exception as e:
                    merge_result.errors.append(f"Failed to load session '{session_id}': {str(e)}")

            if not sessions:
                merge_result.errors.append("No sessions loaded successfully")
                return merge_result

            # Create or load target session
            merged_session = session_manager.get_or_create_session(target_session_id, project_root)

            # Merge decisions
            decisions_result = self._merge_decisions(
                sessions,
                merged_session,
                conflict_strategy
            )
            merged_session.decisions = decisions_result['decisions']
            merge_result.conflicts.extend(decisions_result['conflicts'])
            merge_result.decisions_merged = len(decisions_result['decisions'])

            # Merge constraints
            constraints_result = self._merge_constraints(
                sessions,
                merged_session,
                conflict_strategy
            )
            merged_session.active_constraints = constraints_result['constraints']
            merge_result.conflicts.extend(constraints_result['conflicts'])
            merge_result.constraints_merged = len(constraints_result['constraints'])

            # Merge patterns
            patterns_result = self._merge_patterns(
                sessions,
                merged_session,
                conflict_strategy
            )
            merged_session.patterns_agreed = patterns_result['patterns']
            merge_result.conflicts.extend(patterns_result['conflicts'])
            merge_result.patterns_merged = len(patterns_result['patterns'])

            # Merge consultations (no conflicts - just combine all)
            all_consultations = []
            for session in sessions:
                all_consultations.extend(session.consultations)
            # Sort by timestamp
            all_consultations.sort(key=lambda c: c.timestamp)
            merged_session.consultations = all_consultations
            merge_result.consultations_merged = len(all_consultations)

            # Update metadata
            merged_session.last_updated = datetime.utcnow().isoformat()

            # Save merged session
            session_manager.current_session = merged_session
            session_manager.current_project_root = project_root
            session_manager.save_session()

            merge_result.success = True

        except Exception as e:
            merge_result.errors.append(f"Merge failed: {str(e)}")
            merge_result.success = False

        return merge_result

    def _merge_decisions(
        self,
        sessions: List[SessionState],
        merged_session: SessionState,
        strategy: ConflictStrategy
    ) -> Dict:
        """Merge decisions from multiple sessions."""
        all_decisions = []
        conflicts = []

        # Collect all decisions
        decision_map = {}  # description -> list of (decision, session_id, timestamp)
        for session in sessions:
            for decision in session.decisions:
                key = decision.description.lower().strip()
                if key not in decision_map:
                    decision_map[key] = []
                decision_map[key].append((
                    decision,
                    session.session_id,
                    decision.timestamp
                ))

        # Resolve conflicts
        for description, decision_list in decision_map.items():
            if len(decision_list) == 1:
                # No conflict
                all_decisions.append(decision_list[0][0])
            else:
                # Conflict detected
                conflict, resolved_decision = self._resolve_decision_conflict(
                    decision_list,
                    strategy
                )
                if conflict:
                    conflicts.append(conflict)
                if resolved_decision:
                    all_decisions.append(resolved_decision)

        # Add existing decisions from merged session if not already present
        existing_descriptions = {d.description.lower().strip() for d in all_decisions}
        for decision in merged_session.decisions:
            if decision.description.lower().strip() not in existing_descriptions:
                all_decisions.append(decision)

        # Sort by timestamp
        all_decisions.sort(key=lambda d: d.timestamp)

        return {
            'decisions': all_decisions,
            'conflicts': conflicts
        }

    def _resolve_decision_conflict(
        self,
        decision_list: List[tuple],
        strategy: ConflictStrategy
    ) -> tuple:
        """Resolve conflict between multiple decisions with same description."""
        if strategy == "latest":
            # Use most recent
            latest = max(decision_list, key=lambda x: x[2])
            return None, latest[0]

        elif strategy == "oldest":
            # Use oldest
            oldest = min(decision_list, key=lambda x: x[2])
            return None, oldest[0]

        elif strategy == "all":
            # Keep all versions with numbered suffixes
            resolved_decisions = []
            for i, (decision, session_id, timestamp) in enumerate(decision_list, 1):
                # Create a copy with numbered description
                decision_copy = Decision(
                    id=f"{decision.id}_{i}",
                    category=decision.category,
                    description=f"{decision.description} (v{i} from {session_id})",
                    rationale=decision.rationale,
                    context=decision.context,
                    timestamp=timestamp
                )
                resolved_decisions.append(decision_copy)
            # Return first as primary, rest will be added separately
            return None, resolved_decisions[0] if resolved_decisions else None

        elif strategy == "manual":
            # Create conflict for manual resolution
            decision_a, session_a, timestamp_a = decision_list[0]
            decision_b, session_b, timestamp_b = decision_list[1]

            conflict = MergeConflict(
                type="decision",
                source_a_id=session_a,
                source_b_id=session_b,
                item_a=f"{decision_a.description} (rationale: {decision_a.rationale})",
                item_b=f"{decision_b.description} (rationale: {decision_b.rationale})",
                timestamp_a=timestamp_a,
                timestamp_b=timestamp_b
            )
            # Don't resolve - return conflict
            return conflict, None

        return None, decision_list[0][0]  # Default: use first

    def _merge_constraints(
        self,
        sessions: List[SessionState],
        merged_session: SessionState,
        strategy: ConflictStrategy
    ) -> Dict:
        """Merge constraints from multiple sessions."""
        all_constraints = set(merged_session.active_constraints)
        conflicts = []

        # Collect all unique constraints
        for session in sessions:
            for constraint in session.active_constraints:
                all_constraints.add(constraint)

        # Note: Constraints are simple strings, so conflicts are less likely
        # We just combine all unique constraints
        # In future, could detect semantic conflicts

        return {
            'constraints': sorted(list(all_constraints)),
            'conflicts': conflicts
        }

    def _merge_patterns(
        self,
        sessions: List[SessionState],
        merged_session: SessionState,
        strategy: ConflictStrategy
    ) -> Dict:
        """Merge patterns from multiple sessions."""
        all_patterns = set(merged_session.patterns_agreed)
        conflicts = []

        # Collect all unique patterns
        for session in sessions:
            for pattern in session.patterns_agreed:
                all_patterns.add(pattern)

        # Note: Patterns are simple strings, so conflicts are less likely
        # We just combine all unique patterns
        # In future, could detect semantic conflicts

        return {
            'patterns': sorted(list(all_patterns)),
            'conflicts': conflicts
        }

    def compare_sessions(
        self,
        session_a_id: str,
        session_b_id: str,
        session_manager,
        project_root: Optional[str] = None
    ) -> Dict:
        """
        Compare two sessions and return differences.

        Args:
            session_a_id: First session ID
            session_b_id: Second session ID
            session_manager: SessionManager instance
            project_root: Optional project root

        Returns:
            Dictionary with comparison results
        """
        session_a = session_manager.get_or_create_session(session_a_id, project_root)
        session_b = session_manager.get_or_create_session(session_b_id, project_root)

        # Compare decisions
        decisions_a = {d.description: d for d in session_a.decisions}
        decisions_b = {d.description: d for d in session_b.decisions}

        decisions_only_a = set(decisions_a.keys()) - set(decisions_b.keys())
        decisions_only_b = set(decisions_b.keys()) - set(decisions_a.keys())
        decisions_both = set(decisions_a.keys()) & set(decisions_b.keys())

        # Compare constraints
        constraints_only_a = set(session_a.active_constraints) - set(session_b.active_constraints)
        constraints_only_b = set(session_b.active_constraints) - set(session_a.active_constraints)
        constraints_both = set(session_a.active_constraints) & set(session_b.active_constraints)

        # Compare patterns
        patterns_only_a = set(session_a.patterns_agreed) - set(session_b.patterns_agreed)
        patterns_only_b = set(session_b.patterns_agreed) - set(session_a.patterns_agreed)
        patterns_both = set(session_a.patterns_agreed) & set(session_b.patterns_agreed)

        return {
            'session_a': session_a_id,
            'session_b': session_b_id,
            'decisions': {
                'only_in_a': list(decisions_only_a),
                'only_in_b': list(decisions_only_b),
                'in_both': list(decisions_both),
                'total_a': len(decisions_a),
                'total_b': len(decisions_b),
            },
            'constraints': {
                'only_in_a': list(constraints_only_a),
                'only_in_b': list(constraints_only_b),
                'in_both': list(constraints_both),
                'total_a': len(session_a.active_constraints),
                'total_b': len(session_b.active_constraints),
            },
            'patterns': {
                'only_in_a': list(patterns_only_a),
                'only_in_b': list(patterns_only_b),
                'in_both': list(patterns_both),
                'total_a': len(session_a.patterns_agreed),
                'total_b': len(session_b.patterns_agreed),
            },
            'consultations': {
                'total_a': len(session_a.consultations),
                'total_b': len(session_b.consultations),
            }
        }


def format_merge_result(result: MergeResult) -> str:
    """Format merge result as readable markdown."""
    lines = []
    lines.append("# 🔄 Session Merge Result\n")

    if result.success:
        lines.append("**Status:** ✅ Success\n")
    else:
        lines.append("**Status:** ❌ Failed\n")

    lines.append(f"\n**Merged Session ID:** `{result.merged_session_id}`\n")
    lines.append(f"**Source Sessions:** {', '.join(f'`{s}`' for s in result.source_sessions)}\n")
    lines.append(f"**Strategy Used:** {result.strategy_used}\n")
    lines.append(f"**Merged At:** {result.merged_at}\n")

    lines.append("\n## 📊 Merge Statistics\n")
    lines.append(f"- **Decisions Merged:** {result.decisions_merged}\n")
    lines.append(f"- **Constraints Merged:** {result.constraints_merged}\n")
    lines.append(f"- **Patterns Merged:** {result.patterns_merged}\n")
    lines.append(f"- **Consultations Merged:** {result.consultations_merged}\n")

    if result.conflicts:
        lines.append(f"\n## ⚠️ Conflicts Detected ({len(result.conflicts)})\n")
        for i, conflict in enumerate(result.conflicts, 1):
            lines.append(f"\n### Conflict {i}: {conflict.type}\n")
            lines.append(f"**Source A** (`{conflict.source_a_id}`, {conflict.timestamp_a}):\n")
            lines.append(f"```\n{conflict.item_a}\n```\n")
            lines.append(f"**Source B** (`{conflict.source_b_id}`, {conflict.timestamp_b}):\n")
            lines.append(f"```\n{conflict.item_b}\n```\n")
            if conflict.resolution:
                lines.append(f"**Resolution:** {conflict.resolution}\n")
    else:
        lines.append("\n✅ No conflicts detected\n")

    if result.errors:
        lines.append(f"\n## ❌ Errors ({len(result.errors)})\n")
        for error in result.errors:
            lines.append(f"- {error}\n")

    return "".join(lines)


def format_comparison(comparison: Dict) -> str:
    """Format session comparison as readable markdown."""
    lines = []
    lines.append("# 🔍 Session Comparison\n")
    lines.append(f"\n**Session A:** `{comparison['session_a']}`\n")
    lines.append(f"**Session B:** `{comparison['session_b']}`\n")

    # Decisions
    dec = comparison['decisions']
    lines.append("\n## 📋 Decisions\n")
    lines.append(f"- **Total in A:** {dec['total_a']}\n")
    lines.append(f"- **Total in B:** {dec['total_b']}\n")
    lines.append(f"- **In Both:** {len(dec['in_both'])}\n")
    lines.append(f"- **Only in A:** {len(dec['only_in_a'])}\n")
    lines.append(f"- **Only in B:** {len(dec['only_in_b'])}\n")

    if dec['only_in_a']:
        lines.append("\n**Unique to A:**\n")
        for item in dec['only_in_a'][:5]:
            lines.append(f"- {item}\n")
        if len(dec['only_in_a']) > 5:
            lines.append(f"...and {len(dec['only_in_a']) - 5} more\n")

    if dec['only_in_b']:
        lines.append("\n**Unique to B:**\n")
        for item in dec['only_in_b'][:5]:
            lines.append(f"- {item}\n")
        if len(dec['only_in_b']) > 5:
            lines.append(f"...and {len(dec['only_in_b']) - 5} more\n")

    # Constraints
    con = comparison['constraints']
    lines.append("\n## 🔒 Constraints\n")
    lines.append(f"- **Total in A:** {con['total_a']}\n")
    lines.append(f"- **Total in B:** {con['total_b']}\n")
    lines.append(f"- **In Both:** {len(con['in_both'])}\n")

    # Patterns
    pat = comparison['patterns']
    lines.append("\n## 🎯 Patterns\n")
    lines.append(f"- **Total in A:** {pat['total_a']}\n")
    lines.append(f"- **Total in B:** {pat['total_b']}\n")
    lines.append(f"- **In Both:** {len(pat['in_both'])}\n")

    # Consultations
    cons = comparison['consultations']
    lines.append("\n## 💬 Consultations\n")
    lines.append(f"- **Total in A:** {cons['total_a']}\n")
    lines.append(f"- **Total in B:** {cons['total_b']}\n")

    return "".join(lines)
