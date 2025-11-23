"""
Persona registry for discovery and management.

Following Pragmatic Architect: Lazy loading with caching.
Following Platform Builder: Introspection and categorization.
"""

from pathlib import Path
from typing import Dict, List, Optional
from .base import BasePersona
from .loader import SkillLoader


class ConcretePersona(BasePersona):
    """
    Concrete implementation of BasePersona.

    This class is used for all loaded skill personas.
    The analyze() method would be enhanced by the orchestrator
    with actual LLM-based analysis using the skill content.
    """

    def __init__(self, skill_data: Dict):
        super().__init__(skill_data)
        self._category = skill_data.get('metadata', {}).get('category', self._infer_category())

    def _infer_category(self) -> str:
        """Infer category from PersonaRegistry.CATEGORIES."""
        for category, names in PersonaRegistry.CATEGORIES.items():
            if self.name in names:
                return category
        return 'unknown'

    @property
    def category(self) -> str:
        """Category this persona belongs to (core, specialized, operations, etc.)"""
        return self._category


class PersonaRegistry:
    """
    Registry for discovering and managing skill personas.

    Provides lazy loading, caching, and categorization of personas.
    """

    # Persona categories based on the README
    CATEGORIES = {
        'core': ['snarky-senior-engineer', 'pragmatic-architect', 'legacy-archaeologist'],
        'specialized': [
            'api-platform-engineer', 'data-engineer', 'database-architect',
            'frontend-ux-specialist', 'ml-pragmatist', 'mobile-platform-engineer'
        ],
        'operations': [
            'site-reliability-engineer', 'incident-commander', 'observability-engineer'
        ],
        'security': ['security-sentinel', 'compliance-guardian'],
        'platform': ['devex-champion', 'platform-builder', 'qa-automation-engineer'],
        'cost': ['finops-optimizer'],
        'leadership': [
            'empathetic-team-lead', 'product-engineering-lead',
            'executive-liaison', 'technical-writer'
        ],
        'meta': ['skill-orchestrator']
    }

    def __init__(self, skills_dir: Path):
        """
        Initialize the persona registry.

        Args:
            skills_dir: Directory containing SKILL.md files
        """
        self.skills_dir = skills_dir
        self._personas: Dict[str, BasePersona] = {}
        self._skill_data: Optional[Dict[str, Dict]] = None
        self._loaded = False

    def _load_all(self):
        """Lazy load all skill data."""
        if self._loaded:
            return

        self._skill_data = SkillLoader.load_all_skills(self.skills_dir)
        self._loaded = True

    def get(self, name: str) -> Optional[BasePersona]:
        """
        Get a persona by name.

        Args:
            name: Persona name (e.g., 'snarky-senior-engineer')

        Returns:
            BasePersona instance or None if not found
        """
        # Check cache first
        if name in self._personas:
            return self._personas[name]

        # Lazy load if needed
        if not self._loaded:
            self._load_all()

        # Get skill data
        if not self._skill_data or name not in self._skill_data:
            return None

        # Create and cache persona
        persona = ConcretePersona(self._skill_data[name])
        self._personas[name] = persona
        return persona

    def get_all(self) -> Dict[str, BasePersona]:
        """
        Get all personas.

        Returns:
            Dict mapping persona name to BasePersona instance
        """
        if not self._loaded:
            self._load_all()

        # Load any not yet cached
        for name in self._skill_data.keys():
            if name not in self._personas:
                self._personas[name] = ConcretePersona(self._skill_data[name])

        return self._personas.copy()

    def get_by_category(self, category: str) -> List[BasePersona]:
        """
        Get all personas in a category.

        Args:
            category: Category name (core, specialized, operations, security, etc.)

        Returns:
            List of BasePersona instances
        """
        if category not in self.CATEGORIES:
            return []

        personas = []
        for name in self.CATEGORIES[category]:
            persona = self.get(name)
            if persona:
                personas.append(persona)

        return personas

    def list_names(self, category: Optional[str] = None) -> List[str]:
        """
        List all persona names.

        Args:
            category: Optional category filter

        Returns:
            List of persona names
        """
        if not self._loaded:
            self._load_all()

        if category:
            return self.CATEGORIES.get(category, [])

        return list(self._skill_data.keys())

    def search_by_expertise(self, keywords) -> List[BasePersona]:
        """
        Search for personas by expertise keywords.

        Args:
            keywords: String or list of keywords to match against expertise areas

        Returns:
            List of personas sorted by relevance
        """
        # Convert string to list
        if isinstance(keywords, str):
            keywords = [keywords]

        all_personas = self.get_all()

        # Score each persona by matching keywords in expertise areas OR description
        scored = []
        for persona in all_personas.values():
            # Check expertise areas
            expertise_matches = sum(
                1 for keyword in keywords
                if any(keyword.lower() in e.lower() for e in persona.expertise_areas)
            )
            # Check description
            description_matches = sum(
                1 for keyword in keywords
                if keyword.lower() in persona.description.lower()
            )
            score = expertise_matches + description_matches

            if score > 0:
                scored.append((score, persona))

        # Sort by score descending
        scored.sort(key=lambda x: x[0], reverse=True)

        return [persona for _, persona in scored]

    def get_categories(self) -> Dict[str, List[str]]:
        """
        Get all categories and their persona names.

        Returns:
            Dict mapping category name to list of persona names
        """
        return self.CATEGORIES.copy()

    def __len__(self) -> int:
        """Return number of available personas."""
        if not self._loaded:
            self._load_all()
        return len(self._skill_data)

    def __contains__(self, name: str) -> bool:
        """Check if a persona exists."""
        if not self._loaded:
            self._load_all()
        return name in self._skill_data

    def __repr__(self) -> str:
        if not self._loaded:
            return f"<PersonaRegistry: {self.skills_dir} (not loaded)>"
        return f"<PersonaRegistry: {len(self._skill_data)} personas loaded>"
