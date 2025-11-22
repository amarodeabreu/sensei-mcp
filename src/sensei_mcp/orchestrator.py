"""
Skill Orchestrator - The meta-persona coordinating all 21 specialists.

Following Skill Orchestrator principles:
- Synthesis over Noise
- Context-Aware Casting
- Conflict Resolution via mediation
- Chief of Staff tone

Following Pragmatic Architect:
- Structured decision-making
- Trade-off analysis
- Evolution paths

Following Executive Liaison:
- Executive-friendly format
- Clear recommendations
- Transparent about constraints
"""

from typing import List, Dict, Optional, Tuple
from pathlib import Path

from .context_detector import ContextDetector, QueryContext
from .personas.registry import PersonaRegistry
from .personas.base import BasePersona


class SkillOrchestrator:
    """
    The meta-persona that coordinates all 21 specialized skills.

    Acts as Chief of Staff, convening relevant experts and synthesizing
    their perspectives into holistic, actionable recommendations.
    """

    # Context → Persona mapping for intelligent selection
    CONTEXT_PERSONAS = {
        QueryContext.CRISIS: ['incident-commander', 'site-reliability-engineer', 'executive-liaison'],
        QueryContext.SECURITY: ['security-sentinel', 'compliance-guardian', 'site-reliability-engineer'],
        QueryContext.POLITICAL: ['executive-liaison', 'empathetic-team-lead', 'snarky-senior-engineer'],
        QueryContext.ARCHITECTURAL: ['pragmatic-architect', 'snarky-senior-engineer', 'site-reliability-engineer'],
        QueryContext.COST: ['finops-optimizer', 'pragmatic-architect', 'platform-builder'],
        QueryContext.TEAM: ['empathetic-team-lead', 'devex-champion', 'product-engineering-lead'],
        QueryContext.TECHNICAL: ['snarky-senior-engineer', 'pragmatic-architect', 'devex-champion'],
        QueryContext.GENERAL: ['snarky-senior-engineer', 'pragmatic-architect', 'product-engineering-lead'],
    }

    def __init__(self, registry: PersonaRegistry):
        """
        Initialize the orchestrator.

        Args:
            registry: PersonaRegistry instance with all loaded personas
        """
        self.registry = registry
        self.detector = ContextDetector()

    def select_personas(
        self,
        query: str,
        mode: str = 'auto',
        specific_personas: Optional[List[str]] = None,
        max_personas: int = 5
    ) -> List[BasePersona]:
        """
        Intelligently select relevant personas for the query.

        Args:
            query: The user's query
            mode: Selection mode ('auto', 'crisis', 'quick', 'full')
            specific_personas: Override with explicit persona list
            max_personas: Maximum personas to select in auto mode

        Returns:
            List of selected BasePersona instances
        """
        # Explicit persona selection
        if specific_personas:
            personas = []
            for name in specific_personas:
                persona = self.registry.get(name)
                if persona:
                    personas.append(persona)
            return personas

        # Quick mode: just Snarky
        if mode == 'quick':
            snarky = self.registry.get('snarky-senior-engineer')
            return [snarky] if snarky else []

        # Crisis mode: emergency team
        if mode == 'crisis':
            return [
                self.registry.get(name)
                for name in self.CONTEXT_PERSONAS[QueryContext.CRISIS]
                if self.registry.get(name)
            ]

        # Full mode: all personas (expensive!)
        if mode == 'full':
            all_personas = self.registry.get_all()
            return list(all_personas.values())

        # Auto mode: intelligent selection
        primary_context = self.detector.get_primary_context(query)

        # Start with context-specific personas
        selected_names = self.CONTEXT_PERSONAS.get(primary_context, ['snarky-senior-engineer'])
        personas = [self.registry.get(name) for name in selected_names if self.registry.get(name)]

        # Add personas by relevance scoring (keyword matching)
        all_personas = self.registry.get_all()
        relevance_scores = []

        for name, persona in all_personas.items():
            if name not in selected_names:
                score = persona.relevance_score(query)
                if score > 0.2:  # Threshold for relevance
                    relevance_scores.append((score, name, persona))

        # Sort by relevance and add top scorers
        relevance_scores.sort(key=lambda x: x[0], reverse=True)

        for score, name, persona in relevance_scores:
            if len(personas) >= max_personas:
                break
            if name not in [p.name for p in personas]:
                personas.append(persona)

        # Always ensure Snarky is included (default voice)
        snarky = self.registry.get('snarky-senior-engineer')
        if snarky and snarky not in personas:
            personas.insert(0, snarky)

        return personas[:max_personas]

    def gather_perspectives(
        self,
        query: str,
        personas: List[BasePersona],
        session_context: Optional[Dict] = None
    ) -> Dict[str, str]:
        """
        Gather perspectives from selected personas.

        Args:
            query: The user's query
            personas: List of personas to consult
            session_context: Session memory (constraints, decisions, patterns)

        Returns:
            Dict mapping persona name to their perspective
        """
        perspectives = {}

        for persona in personas:
            # Each persona analyzes with session context
            perspective = persona.analyze(query, session_context)
            perspectives[persona.name] = perspective

        return perspectives

    def synthesize(
        self,
        query: str,
        perspectives: Dict[str, str],
        primary_context: QueryContext,
        output_format: str = 'standard'
    ) -> str:
        """
        Synthesize multiple perspectives into a coherent recommendation.

        Following Skill Orchestrator principles:
        1. Identify consensus points
        2. Identify tensions/disagreements
        3. Resolve conflicts via mediation
        4. Provide clear recommendation

        Args:
            query: The original query
            perspectives: Dict of persona name → perspective
            primary_context: The detected primary context
            output_format: 'brief', 'standard', or 'executive'

        Returns:
            Synthesized response as formatted string
        """
        if output_format == 'brief':
            return self._brief_synthesis(query, perspectives)
        elif output_format == 'executive':
            return self._executive_synthesis(query, perspectives, primary_context)
        else:
            return self._standard_synthesis(query, perspectives, primary_context)

    def _standard_synthesis(
        self,
        query: str,
        perspectives: Dict[str, str],
        context: QueryContext
    ) -> str:
        """Standard synthesis format."""
        lines = []

        lines.append("🎭 ORCHESTRATED ANALYSIS")
        lines.append(f"Context: {context.value.upper()}")
        lines.append(f"Personas Consulted: {len(perspectives)}")
        lines.append("")
        lines.append("━" * 60)
        lines.append("")

        # Show each perspective
        for name, perspective in perspectives.items():
            display_name = name.replace('-', ' ').title()
            lines.append(f"💭 {display_name}:")
            lines.append(perspective.strip())
            lines.append("")

        lines.append("━" * 60)
        lines.append("")

        # Synthesis placeholder (would be LLM-generated in practice)
        lines.append("✅ SYNTHESIS & RECOMMENDATION:")
        lines.append("")
        lines.append("[The orchestrator would synthesize these perspectives here,")
        lines.append(" identifying consensus, tensions, and providing a clear recommendation]")
        lines.append("")
        lines.append("**Recommended Path:**")
        lines.append("[Specific, actionable recommendation based on all perspectives]")
        lines.append("")
        lines.append("**Disagree and Commit:**")
        lines.append("[Explanation of any conflicts and how to proceed despite them]")
        lines.append("")
        lines.append("**Revisit When:**")
        lines.append("[Conditions that would change this recommendation]")

        return "\n".join(lines)

    def _brief_synthesis(self, query: str, perspectives: Dict[str, str]) -> str:
        """Brief synthesis format - just the recommendation."""
        lines = []
        lines.append(f"🎭 Quick Guidance ({len(perspectives)} personas)")
        lines.append("")
        lines.append("[Brief recommendation synthesized from all perspectives]")
        return "\n".join(lines)

    def _executive_synthesis(
        self,
        query: str,
        perspectives: Dict[str, str],
        context: QueryContext
    ) -> str:
        """Executive-friendly synthesis format - TL;DR first."""
        lines = []

        lines.append("🎭 EXECUTIVE SUMMARY")
        lines.append("")
        lines.append("**TL;DR:**")
        lines.append("[One-sentence recommendation]")
        lines.append("")
        lines.append("**Context:**")
        lines.append(f"- Type: {context.value.upper()}")
        lines.append(f"- Experts Consulted: {len(perspectives)}")
        lines.append("")
        lines.append("**Recommendation:**")
        lines.append("[Clear, actionable recommendation]")
        lines.append("")
        lines.append("**Trade-offs:**")
        lines.append("- Pro: [Key benefit]")
        lines.append("- Con: [Key risk/cost]")
        lines.append("")
        lines.append("**Next Steps:**")
        lines.append("1. [Immediate action]")
        lines.append("2. [Follow-up]")

        return "\n".join(lines)

    def orchestrate(
        self,
        query: str,
        mode: str = 'auto',
        specific_personas: Optional[List[str]] = None,
        output_format: str = 'standard',
        session_context: Optional[Dict] = None
    ) -> Dict:
        """
        Main orchestration method - coordinates the entire multi-persona analysis.

        This is the primary entry point for getting orchestrated guidance.

        Args:
            query: The user's query or scenario
            mode: Selection mode ('auto', 'crisis', 'quick', 'full')
            specific_personas: Override auto-selection with explicit list
            output_format: 'brief', 'standard', or 'executive'
            session_context: Session memory (constraints, decisions, patterns)

        Returns:
            Dict with:
                - query: Original query
                - context: Detected primary context
                - personas_consulted: List of persona names
                - perspectives: Dict of persona → perspective
                - synthesis: Synthesized recommendation
        """
        # 1. Select relevant personas
        personas = self.select_personas(query, mode, specific_personas)

        # 2. Detect context
        primary_context = self.detector.get_primary_context(query)

        # 3. Gather perspectives (each persona analyzes with session context)
        perspectives = self.gather_perspectives(query, personas, session_context)

        # 4. Synthesize perspectives
        synthesis = self.synthesize(query, perspectives, primary_context, output_format)

        return {
            'query': query,
            'context': primary_context.value,
            'personas_consulted': [p.name for p in personas],
            'perspectives': perspectives,
            'synthesis': synthesis,
            'mode': mode,
            'output_format': output_format
        }
