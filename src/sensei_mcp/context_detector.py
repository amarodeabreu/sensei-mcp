"""
Context detector for intelligent persona selection.

Following Snarky Senior Engineer: Simple regex patterns, max 10 contexts.
Following Pragmatic Architect: Priority ordering, multiple contexts.
Following Platform Builder: Debuggable with confidence scores.
"""

import re
from enum import Enum
from typing import List, Tuple


class QueryContext(Enum):
    """
    Query context types for persona selection.

    Priority order (highest first):
    1. CRISIS - Production emergencies
    2. SECURITY - Security vulnerabilities
    3. POLITICAL - Organizational/political challenges
    4. ARCHITECTURAL - System design decisions
    5. COST - Budget/cost optimization
    6. TEAM - People/culture issues
    7. TECHNICAL - Implementation details
    8. GENERAL - Default catch-all
    """
    CRISIS = "crisis"
    SECURITY = "security"
    POLITICAL = "political"
    ARCHITECTURAL = "architectural"
    COST = "cost"
    TEAM = "team"
    TECHNICAL = "technical"
    GENERAL = "general"


class ContextDetector:
    """
    Detect query context to intelligently select personas.

    Uses regex pattern matching against predefined contexts.
    Returns primary context (highest priority match) plus all matching contexts.
    """

    # Context patterns (regex)
    PATTERNS = {
        QueryContext.CRISIS: [
            r'\b(down|outage|emergency|crisis|broken|crash|incident|critical)\b',
            r'\b(production|prod).*(down|broken|failed|crash)',
            r'\b(customer|user).*(angry|screaming|complaining|upset)',
            r'\b(database|db).*(down|corrupt|lost)',
            r'\b(site|service|system).*(down|unavailable|offline)',
        ],
        QueryContext.SECURITY: [
            r'\b(security|vulnerability|CVE|breach|attack|hack|exploit)\b',
            r'\b(auth|authentication|authorization).*(broken|bypass|flaw)',
            r'\b(encrypt|certificate|SSL|TLS|pentest|audit)\b',
            r'\b(password|credential|secret).*(leak|exposed|stolen)',
            r'\b(injection|XSS|CSRF|SSRF)\b',
        ],
        QueryContext.POLITICAL: [
            r'\b(CEO|CTO|board|executive|VP|director).*(wants|demands|insists)',
            r'\b(convince|sell|pitch|buy-in|approval)\b',
            r"(brother-in-law|nephew|friend of|consultant|vendor)",
            r'\b(politics|political|org chart|reporting|stakeholder)\b',
            r'\b(hired|hiring).*(questionable|problematic|unqualified)',
        ],
        QueryContext.ARCHITECTURAL: [
            r'\b(architect|design|pattern|refactor|rewrite)\b',
            r'\b(microservice|monolith|serverless|event-driven)\b',
            r'\b(scale|scaling|scalability|performance|latency)\b',
            r'\b(database|cache|queue|event|message|stream)\b',
            r'\b(system design|high-level design|architecture)\b',
        ],
        QueryContext.COST: [
            r'\b(cost|expensive|budget|cheap|ROI|TCO)\b',
            r'\b(AWS|GCP|Azure|cloud).*(bill|cost|pricing|expensive)',
            r'\$[\d,]+',
            r'\b(save|reduce|optimize|cut).*(cost|spend|budget)',
            r'\b(finops|cost optimization)\b',
        ],
        QueryContext.TEAM: [
            r'\b(team|culture|morale|burnout|attrition|retention)\b',
            r'\b(hiring|onboarding|training|mentor)\b',
            r'\b(psychological safety|toxic|conflict)\b',
            r'\b(one-on-one|1:1|feedback|performance review)\b',
            r'\b(remote|distributed|hybrid).*(team|work)',
        ],
        QueryContext.TECHNICAL: [
            r'\b(implement|code|debug|fix|bug|error)\b',
            r'\b(API|endpoint|function|class|method)\b',
            r'\b(test|testing|unit test|integration test)\b',
            r'\b(library|framework|dependency|package)\b',
            r'\b(deploy|deployment|CI/CD|pipeline)\b',
        ],
    }

    # Priority order (highest first) - used when multiple contexts match
    PRIORITY_ORDER = [
        QueryContext.CRISIS,
        QueryContext.SECURITY,
        QueryContext.POLITICAL,
        QueryContext.ARCHITECTURAL,
        QueryContext.COST,
        QueryContext.TEAM,
        QueryContext.TECHNICAL,
        QueryContext.GENERAL,
    ]

    def detect_contexts(self, query: str) -> List[Tuple[QueryContext, int]]:
        """
        Detect all relevant contexts in the query with match counts.

        Args:
            query: The user's query string

        Returns:
            List of (context, match_count) tuples, sorted by match_count descending
        """
        detected = {}
        query_lower = query.lower()

        for context, patterns in self.PATTERNS.items():
            matches = 0
            for pattern in patterns:
                if re.search(pattern, query_lower, re.IGNORECASE):
                    matches += 1

            if matches > 0:
                detected[context] = matches

        # Sort by match count descending
        sorted_contexts = sorted(detected.items(), key=lambda x: x[1], reverse=True)

        # Return as list of tuples
        return sorted_contexts if sorted_contexts else [(QueryContext.GENERAL, 0)]

    def get_primary_context(self, query: str) -> QueryContext:
        """
        Get the most important context for the query.

        Uses priority ordering when multiple contexts match.

        Args:
            query: The user's query string

        Returns:
            The primary QueryContext
        """
        all_contexts = self.detect_contexts(query)
        detected_contexts = [ctx for ctx, _ in all_contexts]

        # Apply priority ordering
        for priority_ctx in self.PRIORITY_ORDER:
            if priority_ctx in detected_contexts:
                return priority_ctx

        return QueryContext.GENERAL

    def get_context_explanation(self, query: str) -> str:
        """
        Get a human-readable explanation of detected contexts.

        Useful for debugging and transparency.

        Args:
            query: The user's query string

        Returns:
            Explanation string
        """
        contexts = self.detect_contexts(query)

        if not contexts or contexts[0][0] == QueryContext.GENERAL:
            return "No specific context detected (GENERAL query)"

        primary = self.get_primary_context(query)

        lines = [f"Primary Context: {primary.value.upper()}"]
        if len(contexts) > 1:
            others = ", ".join(f"{ctx.value} ({count} matches)" for ctx, count in contexts[1:])
            lines.append(f"Secondary Contexts: {others}")

        return "\n".join(lines)
