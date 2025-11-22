"""
Skill loader for parsing SKILL.md files.

Following Snarky Senior Engineer: Simple regex parsing, no fancy libraries.
Following Platform Builder: Validation and clear error messages.
"""

import re
from pathlib import Path
from typing import Dict, List
import yaml


class SkillLoader:
    """
    Loads and parses SKILL.md files into persona definitions.

    Each SKILL.md has this structure:
    ```
    ---
    name: skill-name
    description: "Brief description"
    ---

    # The [Persona Name]

    ## 0. Core Principles
    1. Principle 1
    ...

    ## 1. Personality & Tone
    ...
    ```
    """

    @staticmethod
    def load_skill(skill_path: Path) -> Dict:
        """
        Parse a SKILL.md file and extract metadata + content.

        Args:
            skill_path: Path to the SKILL.md file

        Returns:
            Dict with keys: metadata, principles, personality, expertise, full_content

        Raises:
            FileNotFoundError: If skill file doesn't exist
            ValueError: If skill file is malformed
        """
        if not skill_path.exists():
            raise FileNotFoundError(f"Skill file not found: {skill_path}")

        try:
            content = skill_path.read_text(encoding='utf-8')
        except Exception as e:
            raise ValueError(f"Failed to read skill file {skill_path}: {e}")

        # Extract YAML frontmatter
        metadata = SkillLoader._extract_frontmatter(content, skill_path)

        # Extract sections
        principles = SkillLoader._extract_principles(content)
        personality = SkillLoader._extract_personality(content)
        expertise = SkillLoader._extract_expertise(content, metadata)

        return {
            'metadata': metadata,
            'principles': principles,
            'personality': personality,
            'expertise': expertise,
            'full_content': content
        }

    @staticmethod
    def _extract_frontmatter(content: str, skill_path: Path) -> Dict:
        """Extract YAML frontmatter from skill file."""
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)

        if not frontmatter_match:
            raise ValueError(
                f"No YAML frontmatter found in {skill_path}. "
                f"Expected format:\n---\nname: skill-name\ndescription: \"...\"\n---"
            )

        try:
            metadata = yaml.safe_load(frontmatter_match.group(1))
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML frontmatter in {skill_path}: {e}")

        # Validate required fields
        if 'name' not in metadata:
            raise ValueError(f"Missing required field 'name' in {skill_path} frontmatter")
        if 'description' not in metadata:
            raise ValueError(f"Missing required field 'description' in {skill_path} frontmatter")

        return metadata

    @staticmethod
    def _extract_principles(content: str) -> List[str]:
        """Extract core principles from Section 0."""
        # Look for "## 0. Core Principles" section
        section_match = re.search(
            r'## 0\. Core Principles.*?\n\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL
        )

        if not section_match:
            return []

        principles_text = section_match.group(1)

        # Extract numbered or bulleted items
        principles = []
        for line in principles_text.split('\n'):
            # Match patterns like "1. Principle" or "- Principle" or "* Principle"
            match = re.match(r'^\s*(?:\d+\.|\-|\*)\s+\*\*(.+?)\*\*', line)
            if match:
                principles.append(match.group(1).strip())
            else:
                # Also try without bold
                match = re.match(r'^\s*(?:\d+\.|\-|\*)\s+(.+)', line)
                if match:
                    principle = match.group(1).strip()
                    # Remove any trailing description after newline
                    if ':' in principle:
                        principle = principle.split(':')[0].strip()
                    principles.append(principle)

        return principles[:10]  # Return max 10 principles

    @staticmethod
    def _extract_personality(content: str) -> str:
        """Extract personality/tone description from Section 1."""
        # Look for "## 1. Personality" section
        section_match = re.search(
            r'## 1\. Personality.*?\n\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL
        )

        if not section_match:
            return ""

        return section_match.group(1).strip()[:500]  # Limit to 500 chars

    @staticmethod
    def _extract_expertise(content: str, metadata: Dict) -> List[str]:
        """
        Extract expertise keywords from content.

        Uses description and core principles to identify key topics.
        """
        expertise = []

        # Extract from description
        description = metadata.get('description', '').lower()

        # Common expertise keywords to extract
        keywords = [
            'security', 'architecture', 'scalability', 'performance', 'cost',
            'api', 'database', 'cloud', 'devops', 'testing', 'frontend',
            'mobile', 'data', 'analytics', 'ml', 'compliance', 'observability',
            'incident', 'team', 'leadership', 'product', 'documentation',
            'platform', 'infrastructure', 'deployment', 'monitoring'
        ]

        for keyword in keywords:
            if keyword in description:
                expertise.append(keyword)

        # Extract from section headers
        section_headers = re.findall(r'## \d+\.\s+([^\n]+)', content)
        for header in section_headers:
            header_lower = header.lower()
            for keyword in keywords:
                if keyword in header_lower and keyword not in expertise:
                    expertise.append(keyword)

        return expertise

    @staticmethod
    def load_all_skills(skills_dir: Path) -> Dict[str, Dict]:
        """
        Load all SKILL.md files from a directory.

        Args:
            skills_dir: Directory containing SKILL.md files

        Returns:
            Dict mapping persona name to skill data

        Raises:
            ValueError: If no skills found or if any skill is malformed
        """
        if not skills_dir.exists():
            raise ValueError(f"Skills directory not found: {skills_dir}")

        skills = {}
        skill_files = list(skills_dir.glob('*.md'))

        if not skill_files:
            raise ValueError(f"No SKILL.md files found in {skills_dir}")

        for skill_file in skill_files:
            try:
                skill_data = SkillLoader.load_skill(skill_file)
                persona_name = skill_data['metadata']['name']
                skills[persona_name] = skill_data
            except Exception as e:
                # Log error but continue loading other skills
                print(f"Warning: Failed to load {skill_file.name}: {e}")
                continue

        if not skills:
            raise ValueError(f"Failed to load any valid skills from {skills_dir}")

        return skills
