#!/usr/bin/env python3
"""
Sensei MCP Server

A production-ready MCP server that actively injects engineering standards
into Claude's context based on file types, operations, and maintains session
memory of architectural decisions.
"""

import json
import subprocess
from pathlib import Path
from typing import List, Optional

from mcp.server.fastmcp import FastMCP

from .models import ContextType
from .session import SessionManager
from .engine import ContextInferenceEngine, RulebookLoader
from .personas.registry import PersonaRegistry
from .orchestrator import SkillOrchestrator
from .analytics import SessionAnalyzer
from .exporter import ConsultationExporter, SessionExporter
from .merge import SessionMerger, format_merge_result, format_comparison

# Initialize MCP server
mcp = FastMCP("sensei")

# Paths
SERVER_DIR = Path(__file__).parent
DIRECTIVES_PATH = SERVER_DIR / "core-directives.md"
SESSION_DIR = Path.home() / ".sensei" / "sessions"
SKILLS_DIR = SERVER_DIR / "personas" / "skills"

# Initialize managers
session_mgr = SessionManager(SESSION_DIR)
rulebook = RulebookLoader(DIRECTIVES_PATH)

# Initialize orchestrator (v0.3.0 - Multi-persona mode)
persona_registry = PersonaRegistry(SKILLS_DIR)
orchestrator = SkillOrchestrator(persona_registry)


@mcp.tool()
def get_engineering_context(
    operation: str = "",
    file_paths: List[str] = None,
    description: str = "",
    session_id: str = "default",
    project_root: str = None
) -> str:
    """
    Get relevant Sensei engineering context for the current task.

    Args:
        operation: What you're doing (e.g., "reviewing API endpoints")
        file_paths: List of file paths involved
        description: Additional context about the task
        session_id: Session identifier
        project_root: Absolute path to the project root (for local rules/sessions)

    Returns:
        Markdown-formatted engineering standards relevant to this task
    """
    # Load session (and local rules if project_root provided)
    session = session_mgr.get_or_create_session(session_id, project_root)
    rulebook.load_local_rules(project_root)

    # Infer relevant contexts
    contexts = ContextInferenceEngine.infer_contexts(
        file_paths=file_paths,
        operation=operation,
        description=description
    )

    # Convert ContextType enums to section names
    section_names = [ctx.value for ctx in contexts]

    # Build response
    response = []

    response.append("# 🥋 ACTIVE: Sensei Mode\n")
    response.append("*Context-aware engineering standards loaded for this task*\n")

    # Add session context if any
    if session.active_constraints or session.patterns_agreed or session.decisions:
        response.append("\n## 📋 Session Context\n")

        if session.active_constraints:
            response.append(f"**Active Constraints:** {', '.join(session.active_constraints)}\n")

        if session.patterns_agreed:
            response.append(f"**Agreed Patterns:** {', '.join(session.patterns_agreed)}\n")

        if session.decisions:
            response.append(f"\n**Recent Decisions ({len(session.decisions)} total):**\n")
            for dec in session.decisions[-3:]:  # Last 3 decisions
                response.append(f"- [{dec.category}] {dec.description} - {dec.rationale}\n")

        response.append("\n---\n")

    # Add inferred contexts summary
    response.append(f"\n## 🔍 Active Contexts ({len(contexts)} sections loaded)\n")
    response.append(f"*Loaded {len(section_names)} of 57 available sections based on your task*\n\n")

    # Load and append relevant sections
    relevant_content = rulebook.extract_multiple_sections(section_names)
    response.append(relevant_content)

    # Add footer
    response.append("\n\n---\n")
    response.append(f"*Token efficiency: ~{len(relevant_content.split())} words loaded vs ~15,000 full rulebook*\n")
    response.append(f"*Session: {session_id} | Last updated: {session.last_updated}*\n")

    return "\n".join(response)


@mcp.tool()
def record_decision(
    category: str,
    description: str,
    rationale: str,
    session_id: str = "default",
    constraint: str = None,
    pattern: str = None,
    project_root: str = None
) -> str:
    """
    Record an architectural or technical decision for this session.

    Args:
        category: Type of decision ("architecture", "pattern", "constraint", "standard")
        description: Brief description of the decision
        rationale: Why this decision was made
        session_id: Session identifier
        constraint: Optional constraint to add to active constraints
        pattern: Optional pattern to add to agreed patterns
        project_root: Absolute path to the project root

    Returns:
        Confirmation message with decision ID
    """
    session = session_mgr.get_or_create_session(session_id, project_root)

    decision = session_mgr.add_decision(
        category=category,
        description=description,
        rationale=rationale,
        context={"constraint": constraint, "pattern": pattern},
        project_root=project_root
    )

    # Update session constraints/patterns
    if constraint and constraint not in session.active_constraints:
        session.active_constraints.append(constraint)
        session_mgr.save_session()

    if pattern and pattern not in session.patterns_agreed:
        session.patterns_agreed.append(pattern)
        session_mgr.save_session()

    return f"""✅ Decision recorded: {decision.id}

**Decision:** {description}
**Rationale:** {rationale}
**Category:** {category}

This will be remembered for the rest of the session and included in future context requests.
"""


@mcp.tool()
def validate_against_standards(
    code_snippet: str = None,
    design_description: str = None,
    focus_areas: List[str] = None,
    session_id: str = "default",
    project_root: str = None
) -> str:
    """
    Validate code or design against Sensei engineering standards.

    Args:
        code_snippet: Code to validate (optional)
        design_description: Design/architecture to validate (optional)
        focus_areas: Specific areas to check
        session_id: Session identifier
        project_root: Absolute path to the project root

    Returns:
        Structured validation report
    """
    session = session_mgr.get_or_create_session(session_id, project_root)
    rulebook.load_local_rules(project_root)

    report = ["# 🔍 Standards Validation Report\n"]

    # Check against session constraints
    if session.active_constraints:
        report.append("## Session Constraints Check\n")
        report.append(f"**Active constraints:** {', '.join(session.active_constraints)}\n")
        report.append("⚠️ Verify the code/design adheres to these constraints.\n")

    # Map focus areas to context types
    area_map = {
        "security": [ContextType.SECURITY_PRIVACY, ContextType.AI_SAFETY],
        "multi-tenant": [ContextType.MULTI_TENANCY, ContextType.ALWAYS_ON_DEFAULTS],
        "api-design": [ContextType.APIS_CONTRACTS],
        "api": [ContextType.APIS_CONTRACTS],
        "data": [ContextType.DATA_PERSISTENCE],
        "database": [ContextType.DATA_PERSISTENCE],
        "testing": [ContextType.TESTING],
        "test": [ContextType.TESTING],
        "cloud": [ContextType.CLOUD_PLATFORM, ContextType.COST_CAPACITY],
        "performance": [ContextType.PERFORMANCE_UX, ContextType.COST_CAPACITY],
        "code-quality": [ContextType.CODE_QUALITY, ContextType.ANTI_PATTERNS],
    }

    # Load relevant standards
    contexts = set()
    if focus_areas:
        for area in focus_areas:
            area_lower = area.lower()
            if area_lower in area_map:
                contexts.update(area_map[area_lower])

    # Always include core checklist
    contexts.add(ContextType.SANITY_CHECKLIST)
    contexts.add(ContextType.ANTI_PATTERNS)

    if contexts:
        section_names = [ctx.value for ctx in contexts]
        relevant_content = rulebook.extract_multiple_sections(section_names)

        report.append(f"\n## 📚 Applicable Standards ({len(contexts)} sections)\n")
        report.append(relevant_content)

    return "\n".join(report)


@mcp.tool()
def get_session_summary(session_id: str = "default", project_root: str = None) -> str:
    """
    Get a summary of the current session's decisions and context.

    Args:
        session_id: Session identifier
        project_root: Absolute path to the project root

    Returns:
        Summary of session state
    """
    session = session_mgr.get_or_create_session(session_id, project_root)

    summary = [f"# 📊 Session Summary: {session.session_id}\n"]
    summary.append(f"**Started:** {session.started_at}\n")
    summary.append(f"**Last updated:** {session.last_updated}\n\n")

    if session.active_constraints:
        summary.append("## 🚧 Active Constraints\n")
        for constraint in session.active_constraints:
            summary.append(f"- {constraint}\n")
        summary.append("\n")

    if session.patterns_agreed:
        summary.append("## 🏗️ Agreed Patterns\n")
        for pattern in session.patterns_agreed:
            summary.append(f"- {pattern}\n")
        summary.append("\n")

    if session.decisions:
        summary.append(f"## 📝 Decisions ({len(session.decisions)})\n")
        for dec in session.decisions:
            summary.append(f"\n### {dec.id} - {dec.timestamp}\n")
            summary.append(f"**Category:** {dec.category}\n")
            summary.append(f"**Decision:** {dec.description}\n")
            summary.append(f"**Rationale:** {dec.rationale}\n")
    else:
        summary.append("## 📝 Decisions\n")
        summary.append("No decisions recorded yet.\n")

    return "".join(summary)


@mcp.tool()
def list_sessions() -> str:
    """
    List all available sessions in the global directory.
    (Note: Does not list local project sessions)
    """
    sessions = []
    for session_file in SESSION_DIR.glob("*.json"):
        try:
            with open(session_file, 'r') as f:
                data = json.load(f)
                sessions.append({
                    'id': data['session_id'],
                    'updated': data['last_updated'],
                    'decisions': len(data['decisions'])
                })
        except (json.JSONDecodeError, KeyError):
            continue

    if not sessions:
        return "No global sessions found."

    result = ["# 📂 Available Global Sessions\n"]
    for s in sorted(sessions, key=lambda x: x['updated'], reverse=True):
        result.append(f"- **{s['id']}** (Decisions: {s['decisions']}, Last updated: {s['updated']})\n")

    return "".join(result)


@mcp.tool()
def query_specific_standard(
    section_name: str,
    session_id: str = "default",
    project_root: str = None
) -> str:
    """Query a specific section of the rulebook directly by name."""
    session_mgr.get_or_create_session(session_id, project_root)
    rulebook.load_local_rules(project_root)

    content = rulebook.extract_section(section_name)
    return f"# 📖 Section: {section_name}\n\n{content}"


@mcp.tool()
def check_consistency(
    proposed_change: str,
    session_id: str = "default",
    project_root: str = None
) -> str:
    """
    Check if a proposed change is consistent with session decisions and constraints.
    """
    session = session_mgr.get_or_create_session(session_id, project_root)

    report = ["# 🔄 Consistency Check Report\n"]
    report.append(f"**Proposed change:** {proposed_change}\n\n")

    issues = []

    # Enhanced Check against constraints
    if session.active_constraints:
        report.append("## 🚧 Constraint Validation\n")
        for constraint in session.active_constraints:
            constraint_lower = constraint.lower()
            change_lower = proposed_change.lower()

            # Database conflicts
            if "postgres" in constraint_lower and any(db in change_lower for db in ["mysql", "mongodb", "dynamodb", "sqlite"]):
                issues.append(f"⚠️ **Conflicts with constraint:** '{constraint}' - proposed change mentions alternative database")

            # Cloud conflicts
            if "gcp" in constraint_lower and any(cloud in change_lower for cloud in ["aws", "azure"]):
                issues.append(f"⚠️ **Conflicts with constraint:** '{constraint}' - proposed change mentions alternative cloud provider")
            
            # Language/Framework conflicts
            if "python" in constraint_lower and "node" in change_lower:
                 issues.append(f"⚠️ **Conflicts with constraint:** '{constraint}' - proposed change mentions Node.js")

            if "typescript" in constraint_lower and "javascript" in change_lower and "typescript" not in change_lower:
                 issues.append(f"⚠️ **Conflicts with constraint:** '{constraint}' - proposed change mentions JavaScript (prefer TypeScript)")

    if issues:
        report.append(f"❌ **{len(issues)} potential conflict(s) detected**\n")
        for issue in issues:
            report.append(f"{issue}\n")
    else:
        report.append("✅ **No obvious conflicts detected**\n")

    return "".join(report)


def _suggest_personas_for_contexts(contexts, files):
    """Suggest relevant personas based on detected contexts and file patterns (v0.5.0)."""
    suggestions = []

    # Map contexts to personas
    context_persona_map = {
        'ARCHITECTURAL': [
            ('pragmatic-architect', 'System design and scalability review'),
            ('snarky-senior-engineer', 'Pragmatic pattern validation'),
        ],
        'SECURITY': [
            ('security-sentinel', 'Security vulnerability analysis'),
            ('compliance-guardian', 'Regulatory compliance check'),
        ],
        'COST': [
            ('finops-optimizer', 'Cloud cost impact analysis'),
        ],
        'CRISIS': [
            ('incident-commander', 'Production impact assessment'),
            ('site-reliability-engineer', 'Reliability and monitoring review'),
        ],
    }

    # File pattern-based suggestions
    file_patterns = {
        'api': ('api-platform-engineer', 'API design and contract review'),
        'test': ('qa-automation-engineer', 'Test coverage and quality'),
        'database': ('data-engineer', 'Database schema and query optimization'),
        'migration': ('data-engineer', 'Migration safety and rollback strategy'),
        'frontend': ('frontend-ux-specialist', 'UX and accessibility review'),
        'mobile': ('mobile-platform-engineer', 'Mobile platform best practices'),
        'terraform': ('finops-optimizer', 'Infrastructure cost optimization'),
        'docker': ('platform-builder', 'Container and deployment review'),
        'kubernetes': ('site-reliability-engineer', 'K8s reliability and scaling'),
    }

    # Add suggestions based on contexts
    for ctx in contexts:
        ctx_value = ctx.value if hasattr(ctx, 'value') else str(ctx)
        if ctx_value in context_persona_map:
            suggestions.extend(context_persona_map[ctx_value])

    # Add suggestions based on file patterns
    files_lower = ' '.join(files).lower()
    for pattern, (persona, reason) in file_patterns.items():
        if pattern in files_lower:
            suggestions.append((persona, reason))

    # Remove duplicates while preserving order
    seen = set()
    unique_suggestions = []
    for persona, reason in suggestions:
        if persona not in seen:
            seen.add(persona)
            unique_suggestions.append((persona, reason))

    return unique_suggestions[:5]  # Top 5 suggestions


@mcp.tool()
def analyze_changes(
    project_root: str,
    include_diff_stats: bool = True,
    suggest_personas: bool = True
) -> str:
    """
    Analyze staged git changes to identify relevant engineering contexts (v0.5.0 enhanced).

    Args:
        project_root: Absolute path to the project root
        include_diff_stats: Include line change statistics (additions/deletions)
        suggest_personas: Suggest relevant personas based on change context

    Returns:
        Summary of changed files, contexts, and recommended personas for review
    """
    if not project_root:
        return "❌ Project root is required for git analysis."

    try:
        # Run git diff --name-only --staged
        result = subprocess.run(
            ["git", "diff", "--name-only", "--staged"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False
        )

        # If no staged changes, try HEAD (last commit)
        if not result.stdout.strip():
             result = subprocess.run(
                ["git", "diff", "--name-only", "HEAD"],
                cwd=project_root,
                capture_output=True,
                text=True,
                check=False
            )

        files = result.stdout.strip().splitlines()

        if not files:
            return "No changed files found (checked staged and HEAD)."

        # Get diff stats if requested (v0.5.0)
        diff_stats = None
        if include_diff_stats:
            stats_result = subprocess.run(
                ["git", "diff", "--staged", "--stat"],
                cwd=project_root,
                capture_output=True,
                text=True,
                check=False
            )
            if not stats_result.stdout.strip():
                stats_result = subprocess.run(
                    ["git", "diff", "HEAD", "--stat"],
                    cwd=project_root,
                    capture_output=True,
                    text=True,
                    check=False
                )
            diff_stats = stats_result.stdout.strip()

        # Infer context for these files
        contexts = ContextInferenceEngine.infer_contexts(file_paths=files)
        section_names = [ctx.value for ctx in contexts]

        # Build report
        report = ["# 🕵️ Git Change Analysis (v0.5.0)\n\n"]
        report.append(f"**Analyzed {len(files)} changed files:**\n")
        for f in files[:10]: # Limit to 10 files
            report.append(f"- `{f}`\n")
        if len(files) > 10:
            report.append(f"...and {len(files)-10} more\n")

        # Add diff stats (v0.5.0)
        if diff_stats:
            report.append(f"\n**Change Statistics:**\n```\n{diff_stats}\n```\n")

        report.append(f"\n**Inferred Contexts ({len(contexts)}):**\n")
        for ctx in section_names:
            report.append(f"- {ctx}\n")

        # Suggest personas based on contexts (v0.5.0)
        if suggest_personas:
            persona_suggestions = _suggest_personas_for_contexts(contexts, files)
            if persona_suggestions:
                report.append("\n**🎭 Recommended Personas for Review:**\n")
                for persona, reason in persona_suggestions:
                    report.append(f"- `{persona}`: {reason}\n")

                # Provide example command
                persona_list = [p for p, _ in persona_suggestions[:3]]
                report.append(f"\n**Example Command:**\n")
                report.append(f"```python\n")
                report.append(f"get_engineering_guidance(\n")
                report.append(f'    query="Review these changes for quality and impact",\n')
                report.append(f"    specific_personas={persona_list}\n")
                report.append(f")\n```\n")

        report.append("\n**Alternative:**\n")
        report.append(f"Run `get_engineering_context(file_paths={files[:5]})` to load standards for these contexts.")

        return "".join(report)

    except Exception as e:
        return f"❌ Error running git analysis: {str(e)}"


# ============================================================================
# v0.3.0 NEW TOOLS - Multi-Persona Orchestration
# ============================================================================

def _generate_context_hint(query: str, context: str, num_personas: int) -> str:
    """
    Generate helpful hints when few personas were selected (v0.5.0).

    Suggests relevant personas based on query keywords and detected context.

    Args:
        query: User's query
        context: Detected context type
        num_personas: Number of personas that were selected

    Returns:
        Hint string or empty if not applicable
    """
    # Only provide hints if very few personas matched
    if num_personas >= 2:
        return ""

    # Context-based suggestions
    context_suggestions = {
        'SECURITY': ['security-sentinel', 'compliance-guardian', 'api-platform-engineer'],
        'CRISIS': ['incident-commander', 'site-reliability-engineer', 'executive-liaison'],
        'ARCHITECTURAL': ['pragmatic-architect', 'snarky-senior-engineer', 'product-engineering-lead'],
        'COST': ['finops-optimizer', 'site-reliability-engineer', 'pragmatic-architect'],
        'DATABASE': ['data-engineer', 'pragmatic-architect', 'site-reliability-engineer'],
        'TECHNICAL': ['snarky-senior-engineer', 'legacy-archaeologist', 'qa-automation-engineer'],
        'API': ['api-platform-engineer', 'security-sentinel', 'pragmatic-architect'],
        'FRONTEND': ['frontend-ux-specialist', 'devex-champion', 'qa-automation-engineer'],
        'MOBILE': ['mobile-platform-engineer', 'frontend-ux-specialist', 'qa-automation-engineer'],
        'DATA': ['data-engineer', 'pragmatic-architect', 'observability-engineer'],
        'ML': ['ml-pragmatist', 'data-engineer', 'pragmatic-architect'],
        'TEAM': ['empathetic-team-lead', 'product-engineering-lead', 'devex-champion'],
    }

    # Keyword-based detection
    query_lower = query.lower()
    keywords_map = {
        'database': 'DATABASE',
        'sql': 'DATABASE',
        'postgres': 'DATABASE',
        'mongodb': 'DATABASE',
        'api': 'API',
        'endpoint': 'API',
        'rest': 'API',
        'graphql': 'API',
        'security': 'SECURITY',
        'vulnerability': 'SECURITY',
        'auth': 'SECURITY',
        'frontend': 'FRONTEND',
        'react': 'FRONTEND',
        'vue': 'FRONTEND',
        'mobile': 'MOBILE',
        'ios': 'MOBILE',
        'android': 'MOBILE',
        'machine learning': 'ML',
        'model': 'ML',
        'training': 'ML',
        'team': 'TEAM',
        'culture': 'TEAM',
        'hiring': 'TEAM',
    }

    # Try to find more specific context from keywords
    suggested_context = context
    for keyword, ctx in keywords_map.items():
        if keyword in query_lower:
            suggested_context = ctx
            break

    # Get suggestions for this context
    suggestions = context_suggestions.get(suggested_context, [])

    if suggestions:
        hint = f"\n\n💡 **Context Hint:** This looks like a {suggested_context} question. "
        hint += f"Consider using specific personas:\n"
        for persona in suggestions[:3]:  # Top 3
            hint += f"- `{persona}`\n"
        hint += f"\nUse: `get_engineering_guidance(query=\"...\", specific_personas=[\"persona-name\"])`"
        return hint

    return ""


@mcp.tool()
def get_engineering_guidance(
    query: str,
    mode: str = "orchestrated",
    session_id: str = "default",
    project_root: str = None,
    specific_personas: List[str] = None,
    output_format: str = "standard"
) -> str:
    """
    Get engineering guidance via multi-persona orchestration (DEFAULT in v0.3.0).

    ⚠️ DEPRECATION NOTICE (v0.6.0):
    This tool will be deprecated in v0.7.0. Please use the new granular tools instead:
    - suggest_personas_for_query() - Get persona suggestions
    - get_persona_content() - Get persona SKILL.md content
    - get_session_context() - Get session memory
    - record_consultation() - Record consultation after analysis

    The new architecture provides content for Claude to analyze, rather than
    trying to perform analysis within the MCP server.

    This is the NEW primary tool for getting engineering guidance.
    The Skill Orchestrator coordinates 21 specialized personas to provide
    holistic, multi-perspective analysis of your engineering questions.

    Args:
        query: Your question or scenario
        mode: Analysis mode:
            - "orchestrated" (DEFAULT): Multi-persona analysis with intelligent selection
            - "quick": Single persona (Snarky Senior Engineer) for fast answers
            - "crisis": Emergency team (Incident Commander, SRE, Executive)
            - "standards": Legacy mode (engineering standards only, no personas)
        session_id: Session identifier
        project_root: Absolute path to project root (for local rules/sessions)
        specific_personas: Override auto-selection (e.g., ["security-sentinel", "pragmatic-architect"])
        output_format: Response format ("brief", "standard", "executive")

    Returns:
        Orchestrated multi-perspective guidance with synthesis and recommendations

    Examples:
        # Auto-orchestrated (DEFAULT)
        get_engineering_guidance(
            query="Should we migrate to microservices?",
            session_id="saas-backend"
        )

        # Crisis mode
        get_engineering_guidance(
            query="Production database is down",
            mode="crisis"
        )

        # Specific personas
        get_engineering_guidance(
            query="Review this payment API design",
            specific_personas=["security-sentinel", "api-platform-engineer"]
        )
    """
    # Load session
    session = session_mgr.get_or_create_session(session_id, project_root)

    # Standards mode (legacy) - delegate to get_engineering_context
    if mode == "standards":
        return get_engineering_context(
            operation="",
            file_paths=None,
            description=query,
            session_id=session_id,
            project_root=project_root
        )

    # Prepare session context for personas
    session_context = {
        'active_constraints': session.active_constraints,
        'patterns_agreed': session.patterns_agreed,
        'recent_decisions': [
            {
                'id': d.id,
                'category': d.category,
                'description': d.description,
                'rationale': d.rationale
            }
            for d in session.decisions[-5:]  # Last 5 decisions
        ] if session.decisions else []
    }

    # Orchestrate
    result = orchestrator.orchestrate(
        query=query,
        mode=mode,
        specific_personas=specific_personas,
        output_format=output_format,
        session_context=session_context
    )

    # Record consultation
    session_mgr.add_consultation(
        query=query,
        mode=result['mode'],
        personas_consulted=result['personas_consulted'],
        context=result['context'],
        synthesis=result['synthesis'],
        project_root=project_root
    )

    # Generate context hint if few personas were selected (v0.5.0)
    hint = _generate_context_hint(
        query=query,
        context=result['context'],
        num_personas=len(result['personas_consulted'])
    )

    return result['synthesis'] + hint


@mcp.tool()
def consult_skill(
    skill_name: str,
    query: str,
    session_id: str = "default",
    project_root: str = None
) -> str:
    """
    Consult a single skill persona directly.

    ⚠️ DEPRECATION NOTICE (v0.6.0):
    This tool will be deprecated in v0.7.0. Please use get_persona_content() instead:
    - get_persona_content(persona_name=skill_name) - Get full SKILL.md content
    Then Claude performs the analysis using that content as context.

    Use this when you want guidance from a specific expert without orchestration.

    Args:
        skill_name: Persona name (e.g., "snarky-senior-engineer", "security-sentinel")
        query: Your question
        session_id: Session identifier
        project_root: Absolute path to project root

    Returns:
        The persona's perspective

    Available Personas:
        Core: snarky-senior-engineer, pragmatic-architect, legacy-archaeologist
        Specialized: api-platform-engineer, data-engineer, frontend-ux-specialist, ml-pragmatist, mobile-platform-engineer
        Operations: site-reliability-engineer, incident-commander, observability-engineer
        Security: security-sentinel, compliance-guardian
        Platform: devex-champion, platform-builder, qa-automation-engineer
        Cost: finops-optimizer
        Leadership: empathetic-team-lead, product-engineering-lead, executive-liaison, technical-writer
        Meta: skill-orchestrator
    """
    # Load session
    session = session_mgr.get_or_create_session(session_id, project_root)

    # Get persona
    persona = persona_registry.get(skill_name)
    if not persona:
        available = ", ".join(persona_registry.list_names())
        return f"❌ Persona '{skill_name}' not found.\n\nAvailable personas:\n{available}"

    # Prepare session context
    session_context = {
        'active_constraints': session.active_constraints,
        'patterns_agreed': session.patterns_agreed,
    }

    # Get persona's perspective
    perspective = persona.analyze(query, session_context)

    # Record consultation
    session_mgr.add_consultation(
        query=query,
        mode="single",
        personas_consulted=[skill_name],
        context="single_persona",
        synthesis=perspective,
        project_root=project_root
    )

    return f"# 💭 {persona.name.replace('-', ' ').title()}\n\n{perspective}"


@mcp.tool()
def list_available_skills(
    category: str = None,
    format: str = "standard"
) -> str:
    """
    List all available skill personas with flexible detail levels.

    Args:
        category: Optional filter (core, specialized, operations, security, platform, cost, leadership, meta)
        format: Output format:
            - "standard" (default): Name, description, and expertise areas
            - "detailed": Adds example queries, use cases, and related personas
            - "quick": One-line quick tips for each persona

    Returns:
        Formatted list of available personas

    Examples:
        # Standard list
        list_available_skills()

        # Detailed format with examples
        list_available_skills(format="detailed")

        # Quick reference
        list_available_skills(format="quick")

        # Specific category
        list_available_skills(category="operations", format="detailed")
    """
    if category:
        if category not in persona_registry.get_categories():
            available_categories = ", ".join(persona_registry.get_categories().keys())
            return f"❌ Category '{category}' not found.\n\nAvailable categories: {available_categories}"

        personas = list(persona_registry.get_by_category(category))
        title = f"# 🎭 {category.title()} Personas"
    else:
        personas = list(persona_registry.get_all().values())
        title = f"# 🎭 All Available Personas ({len(personas)} total)"

    result = [title + "\n"]

    # Quick format - one-line tips
    if format == "quick":
        for persona in personas:
            quick_tip = persona.quick_tip if hasattr(persona, 'quick_tip') and persona.quick_tip else persona.description
            result.append(f"- **{persona.name}**: {quick_tip}\n")

        result.append("\n**Tip:** Use `format=\"detailed\"` for more information.\n")
        return "".join(result)

    # Standard or detailed format
    for persona in personas:
        result.append(f"\n## {persona.name.replace('-', ' ').title()}\n")
        result.append(f"{persona.description}\n\n")

        # Expertise areas (both standard and detailed)
        if persona.expertise_areas:
            result.append(f"**Expertise:** {', '.join(persona.expertise_areas[:5])}\n")

        # Detailed format - add examples, use cases, and related personas
        if format == "detailed":
            # Example queries (v0.4.0 metadata)
            if hasattr(persona, 'examples') and persona.examples:
                result.append(f"\n**Example queries:**\n")
                for example in persona.examples[:3]:  # Limit to 3 examples
                    result.append(f'- "{example}"\n')

            # When to use (v0.4.0 metadata)
            if hasattr(persona, 'use_when') and persona.use_when:
                result.append(f"\n**Use when:** {persona.use_when}\n")

            # Related personas (v0.4.0 metadata)
            if hasattr(persona, 'related_personas') and persona.related_personas:
                result.append(f"\n**Works well with:** {', '.join(persona.related_personas)}\n")

        result.append("\n")

    # Footer
    result.append("---\n")
    if format == "standard":
        result.append("**Tip:** Use `format=\"detailed\"` for examples and use cases, or `format=\"quick\"` for one-liners.\n\n")
    result.append("**Usage:** `consult_skill(skill_name=\"...\", query=\"...\")` or `get_engineering_guidance(specific_personas=[\"...\"])`\n")

    return "".join(result)


# ============================================================================
# v0.6.0 NEW TOOLS - Option B: Granular Persona Content Access
# ============================================================================

@mcp.tool()
def get_persona_content(
    persona_name: str,
    include_metadata: bool = True
) -> str:
    """
    Get full skill content for a specific persona.

    This returns the complete SKILL.md content that defines the persona's
    expertise, principles, personality, and guidelines. The calling LLM
    should use this content to analyze queries from that persona's perspective.

    **MCP Design Philosophy:**
    This tool returns CONTENT for the LLM to use, not pre-generated analysis.
    The calling LLM (Claude) receives the persona content and performs
    the analysis itself.

    Args:
        persona_name: Name of persona (e.g., "security-sentinel", "pragmatic-architect")
        include_metadata: Include metadata header (name, description, expertise)

    Returns:
        Full persona skill content (markdown format)

    Example:
        # Get Security Sentinel's content
        content = get_persona_content("security-sentinel")

        # Claude then uses this content to analyze from that perspective
    """
    persona = persona_registry.get(persona_name)

    if not persona:
        available = ", ".join(sorted(persona_registry.list_names()))
        return f"❌ Persona '{persona_name}' not found.\n\nAvailable personas: {available}"

    result = []

    # Optional metadata header
    if include_metadata:
        result.append(f"# {persona.name.replace('-', ' ').title()}\n")
        result.append(f"**Description:** {persona.description}\n")
        if persona.expertise_areas:
            result.append(f"**Expertise:** {', '.join(persona.expertise_areas)}\n")
        result.append(f"\n---\n\n")

    # Full skill content (the complete SKILL.md)
    result.append(persona.full_content)

    return "".join(result)


@mcp.tool()
def suggest_personas_for_query(
    query: str,
    max_suggestions: int = 5,
    context_hint: str = None
) -> str:
    """
    Suggest relevant personas for a given query using intelligent selection.

    Uses keyword matching, context detection, and relevance scoring to
    recommend which personas would be most helpful for the query.

    **MCP Design Philosophy:**
    This tool helps the LLM discover which personas to consult, but doesn't
    perform analysis itself. The LLM uses the suggestions to call
    get_persona_content() for each recommended persona.

    Args:
        query: The user's question or scenario
        max_suggestions: Maximum number of personas to suggest (default: 5)
        context_hint: Optional context hint to improve suggestions
                     (e.g., "crisis", "security", "architectural")

    Returns:
        JSON list of suggested personas with relevance scores and rationale

    Example:
        # Get suggestions for a query
        suggestions = suggest_personas_for_query(
            query="How should we handle user authentication?",
            max_suggestions=3
        )

        # Returns JSON with suggested personas and why they're relevant
        # LLM then calls get_persona_content() for each suggestion
    """
    from .context_detector import ContextDetector, QueryContext

    detector = ContextDetector()

    # Detect context if not provided
    if context_hint:
        try:
            primary_context = QueryContext(context_hint.upper())
        except ValueError:
            primary_context = detector.get_primary_context(query)
    else:
        primary_context = detector.get_primary_context(query)

    # Select personas using orchestrator's selection logic
    personas = orchestrator.select_personas(
        query=query,
        mode='auto',
        specific_personas=None,
        max_personas=max_suggestions
    )

    # Build suggestions with rationale
    suggestions = []
    for persona in personas:
        relevance = persona.relevance_score(query)

        # Generate rationale based on expertise match
        matched_expertise = [
            kw for kw in persona.expertise_areas
            if kw.lower() in query.lower()
        ]

        if matched_expertise:
            rationale = f"Expert in {', '.join(matched_expertise[:3])}"
        else:
            rationale = f"Relevant for {primary_context.value} context"

        suggestions.append({
            "name": persona.name,
            "display_name": persona.name.replace('-', ' ').title(),
            "relevance": round(relevance, 2),
            "rationale": rationale
        })

    # Return as JSON
    result = {
        "query": query,
        "detected_context": primary_context.value,
        "suggestions": suggestions,
        "count": len(suggestions)
    }

    return json.dumps(result, indent=2)


@mcp.tool()
def get_session_context(
    session_id: str = "default",
    project_root: str = None
) -> str:
    """
    Get session context (constraints, decisions, patterns) for context-aware analysis.

    Returns session memory that can be included when asking personas to analyze queries.
    This ensures consistency with previous decisions and agreed patterns.

    **MCP Design Philosophy:**
    This tool returns session memory as data. The LLM includes this context
    when analyzing queries to ensure consistency with previous decisions.

    Args:
        session_id: Session identifier
        project_root: Optional project root for local sessions

    Returns:
        JSON with session constraints, patterns, and recent decisions

    Example:
        # Get session context
        context = get_session_context(session_id="my-project")

        # LLM includes this when asking persona to analyze:
        # "Given these constraints: ..., analyze this query"
    """
    session = session_mgr.get_or_create_session(session_id, project_root)

    context = {
        "session_id": session_id,
        "active_constraints": session.active_constraints,
        "patterns_agreed": session.patterns_agreed,
        "recent_decisions": [
            {
                "id": d.id,
                "category": d.category,
                "description": d.description,
                "rationale": d.rationale,
                "timestamp": d.timestamp.isoformat() if hasattr(d, 'timestamp') else None
            }
            for d in session.decisions[-5:]  # Last 5 decisions
        ] if session.decisions else []
    }

    return json.dumps(context, indent=2)


@mcp.tool()
def record_consultation(
    query: str,
    personas_used: List[str],
    session_id: str = "default",
    project_root: str = None,
    synthesis: str = None
) -> str:
    """
    Record a consultation in session history.

    After Claude analyzes a query using persona content, record the consultation
    for session analytics and history.

    Args:
        query: The original query
        personas_used: List of persona names that were consulted
        session_id: Session identifier
        project_root: Optional project root
        synthesis: Optional synthesis/recommendation from Claude

    Returns:
        Confirmation with consultation ID

    Example:
        # After Claude analyzes using persona content:
        record_consultation(
            query="Should we migrate to microservices?",
            personas_used=["pragmatic-architect", "site-reliability-engineer"],
            synthesis="[Claude's full analysis and recommendation]"
        )
    """
    # Record consultation
    consultation_id = session_mgr.add_consultation(
        query=query,
        mode="manual",  # Manual multi-persona consultation
        personas_consulted=personas_used,
        context="option_b_flow",
        synthesis=synthesis or "[Synthesis performed by calling LLM]",
        project_root=project_root
    )

    return f"""✅ Consultation recorded

**ID:** {consultation_id}
**Query:** {query}
**Personas Used:** {', '.join(personas_used)}
**Session:** {session_id}

This consultation has been added to session history and will be included in analytics.
"""


# ============================================================================
# v0.4.0 NEW TOOLS - Session Analytics & Team Collaboration
# ============================================================================

@mcp.tool()
def get_session_insights(
    session_id: str = "default",
    project_root: str = None,
    time_range: str = "all_time",
    format: str = "markdown"
) -> str:
    """
    Get comprehensive analytics and insights for a session.

    Provides data-driven insights into persona usage patterns, consultation frequency,
    decision-making trends, and session health metrics.

    Args:
        session_id: Session identifier
        project_root: Absolute path to project root (for local sessions)
        time_range: Analysis window:
            - "all_time" (default): All consultations
            - "last_7_days": Last 7 days
            - "last_30_days": Last 30 days
        format: Output format ("markdown", "json", "text")

    Returns:
        Formatted analytics report with:
        - Persona usage statistics (most/least used)
        - Context distribution (CRISIS, SECURITY, etc.)
        - Mode usage (orchestrated, quick, crisis, standards)
        - Decision metrics and velocity
        - Session health indicators

    Examples:
        # Get all-time insights
        get_session_insights(session_id="my-project")

        # Last 30 days in JSON
        get_session_insights(
            session_id="my-project",
            time_range="last_30_days",
            format="json"
        )
    """
    # Load session
    session = session_mgr.get_or_create_session(session_id, project_root)

    # Analyze
    analyzer = SessionAnalyzer(session)
    insights = analyzer.get_insights(time_range=time_range)

    # Format output
    return analyzer.format_insights(insights, format=format)


@mcp.tool()
def export_consultation(
    consultation_id: str,
    session_id: str = "default",
    project_root: str = None,
    format: str = "markdown"
) -> str:
    """
    Export a single consultation as shareable report.

    Perfect for sharing specific decision-making discussions with your team,
    documenting why you chose a particular approach, or creating ADRs.

    Args:
        consultation_id: Consultation ID (e.g., "consult_1")
        session_id: Session identifier
        project_root: Absolute path to project root
        format: Output format ("markdown", "json", "text")

    Returns:
        Formatted consultation report

    Examples:
        # Export as markdown
        export_consultation(
            consultation_id="consult_5",
            session_id="my-project"
        )

        # Export as JSON for CI/CD
        export_consultation(
            consultation_id="consult_5",
            format="json"
        )
    """
    # Load session
    session = session_mgr.get_or_create_session(session_id, project_root)

    # Find consultation
    consultation = next(
        (c for c in session.consultations if c.id == consultation_id),
        None
    )

    if not consultation:
        return f"❌ Consultation '{consultation_id}' not found in session '{session_id}'.\n\nAvailable consultations: {', '.join([c.id for c in session.consultations])}"

    # Export
    return ConsultationExporter.export_consultation(consultation, format=format)


@mcp.tool()
def export_session_summary(
    session_id: str = "default",
    project_root: str = None,
    format: str = "markdown",
    include: List[str] = None,
    max_consultations: int = 10
) -> str:
    """
    Export comprehensive session summary for team sharing.

    Generates Architecture Decision Records (ADRs), consultation history,
    and active constraints/patterns. Perfect for:
    - Onboarding new team members
    - Documenting architectural decisions
    - Sharing team knowledge
    - Creating weekly/monthly reports

    Args:
        session_id: Session identifier
        project_root: Absolute path to project root
        format: Output format ("markdown", "json", "text")
        include: Components to include (default: all)
            - "decisions": Architecture decisions
            - "consultations": Consultation history
            - "constraints": Active constraints
            - "patterns": Agreed patterns
        max_consultations: Max recent consultations to include (default: 10)

    Returns:
        Comprehensive session summary report

    Examples:
        # Full summary
        export_session_summary(session_id="my-project")

        # Just decisions and constraints
        export_session_summary(
            session_id="my-project",
            include=["decisions", "constraints"]
        )

        # JSON export for processing
        export_session_summary(
            session_id="my-project",
            format="json"
        )
    """
    # Default includes
    if include is None:
        include = ["decisions", "consultations", "constraints", "patterns"]

    # Load session
    session = session_mgr.get_or_create_session(session_id, project_root)

    # Export
    return SessionExporter.export_session_summary(
        session=session,
        format=format,
        include=include,
        max_consultations=max_consultations
    )


# ============================================================================
# v0.5.0 NEW TOOLS - Session Merge & Team Sync
# ============================================================================

# Initialize merger
merger = SessionMerger()


@mcp.tool()
def merge_sessions(
    session_ids: List[str],
    target_session_id: str,
    conflict_strategy: str = "latest",
    project_root: str = None
) -> str:
    """
    Merge multiple sessions into a single target session (v0.5.0).

    Enables teams to combine session insights from multiple developers,
    resolving conflicts and tracking attribution.

    Args:
        session_ids: List of session IDs to merge (e.g., ["dev1-session", "dev2-session"])
        target_session_id: ID for the merged session (e.g., "team-session")
        conflict_strategy: How to resolve conflicts:
            - "latest" (default): Use most recent timestamp
            - "oldest": Use oldest timestamp
            - "all": Keep all variants (creates numbered versions)
            - "manual": Return conflicts for manual resolution
        project_root: Optional project root for local sessions

    Returns:
        Formatted merge result with statistics and conflicts

    Examples:
        # Merge two developer sessions
        merge_sessions(
            session_ids=["alice-frontend", "bob-backend"],
            target_session_id="sprint-23",
            conflict_strategy="latest"
        )

        # Merge with manual conflict resolution
        merge_sessions(
            session_ids=["team-a", "team-b"],
            target_session_id="combined",
            conflict_strategy="manual"
        )

        # Keep all decision variants
        merge_sessions(
            session_ids=["experiment-1", "experiment-2"],
            target_session_id="final",
            conflict_strategy="all"
        )
    """
    result = merger.merge_sessions(
        session_ids=session_ids,
        target_session_id=target_session_id,
        session_manager=session_mgr,
        conflict_strategy=conflict_strategy,
        project_root=project_root
    )

    return format_merge_result(result)


@mcp.tool()
def compare_sessions(
    session_a_id: str,
    session_b_id: str,
    project_root: str = None
) -> str:
    """
    Compare two sessions and return differences (v0.5.0).

    Useful for understanding what decisions and patterns differ between
    two developer sessions or team branches before merging.

    Args:
        session_a_id: First session ID
        session_b_id: Second session ID
        project_root: Optional project root for local sessions

    Returns:
        Formatted comparison showing unique and shared items

    Examples:
        # Compare two developer sessions
        compare_sessions(
            session_a_id="alice-session",
            session_b_id="bob-session"
        )

        # Compare feature branches
        compare_sessions(
            session_a_id="feature-auth",
            session_b_id="feature-payments"
        )
    """
    comparison = merger.compare_sessions(
        session_a_id=session_a_id,
        session_b_id=session_b_id,
        session_manager=session_mgr,
        project_root=project_root
    )

    return format_comparison(comparison)


# ============================================================================
# v0.8.0 NEW TOOLS - Multi-MCP Orchestration
# ============================================================================

from .mcp_orchestrator import MCPOrchestrator
from .demo_executor import DemoExecutor

# Initialize MCP orchestrator
mcp_orchestrator = MCPOrchestrator()

# Initialize demo executor
demo_executor = DemoExecutor(mcp_orchestrator)


@mcp.tool()
def suggest_mcps_for_query(
    query: str,
    context: str = "GENERAL",
    user_mcps: List[str] = None
) -> str:
    """
    Suggest which MCP servers to use for a given query.

    Analyzes the query and recommends which MCP servers (Context7, Tavily,
    Playwright, etc.) would be most helpful, along with pre-built workflow
    templates if available.

    Args:
        query: The user's query
        context: Detected query context (default: "GENERAL")
                Options: SECURITY, COST, CRISIS, ARCHITECTURAL, TECHNICAL, etc.
        user_mcps: Optional list of MCPs to filter suggestions
                  (e.g., ["context7", "tavily"])

    Returns:
        JSON with suggested MCPs, rationale, matching workflows, and cost/time estimates

    Example:
        # Get MCP suggestions
        suggest_mcps_for_query(
            query="Review authentication for security issues",
            context="SECURITY"
        )

        # Returns: sensei + context7 (OWASP docs) + tavily (CVEs) + playwright (live inspection)
    """
    result = mcp_orchestrator.suggest_mcps_for_query(
        query=query,
        context=context,
        user_mcps=user_mcps
    )

    return json.dumps(result, indent=2)


@mcp.tool()
def get_mcp_workflow_template(
    template_name: str,
    parameters: dict = None
) -> str:
    """
    Get a pre-built multi-MCP workflow template.

    Returns step-by-step workflow definitions for common scenarios,
    with optional parameter substitution for customization.

    Args:
        template_name: Workflow template name
            Available templates:
            - "auth-security-review": Comprehensive auth security review
            - "performance-debug": Performance debugging workflow
            - "cost-optimization": Cloud cost analysis
            - "tech-due-diligence": Technology evaluation
            - "incident-postmortem": Incident analysis
            - "accessibility-audit": WCAG compliance check
            - "api-design-review": API design review

        parameters: Optional dict of parameters to substitute
            Example: {
                "user_query": "Review FastAPI auth",
                "app_url": "https://app.example.com",
                "framework": "FastAPI"
            }

    Returns:
        JSON with workflow steps, required MCPs, personas, and estimates

    Example:
        # Get auth security review workflow
        get_mcp_workflow_template(
            template_name="auth-security-review",
            parameters={
                "user_query": "Review authentication implementation",
                "app_url": "https://app.example.com/login",
                "framework": "FastAPI"
            }
        )
    """
    result = mcp_orchestrator.get_workflow_template(
        template_name=template_name,
        parameters=parameters or {}
    )

    return json.dumps(result, indent=2)


@mcp.tool()
def list_mcp_workflow_templates() -> str:
    """
    List all available multi-MCP workflow templates.

    Returns a summary of pre-built workflows with their descriptions,
    required MCPs, cost estimates, and time estimates.

    Returns:
        JSON array of available workflow templates

    Example:
        # List all templates
        list_mcp_workflow_templates()

        # Returns: 7 templates (auth-security-review, performance-debug, etc.)
    """
    templates = mcp_orchestrator.list_workflow_templates()

    return json.dumps(templates, indent=2)


# ============================================================================
# v0.8.0 NEW TOOLS - Executable Demo Workflows
# ============================================================================

@mcp.tool()
def run_demo(
    demo_type: str,
    custom_params: dict = None,
    output_format: str = "markdown"
) -> str:
    """
    Execute a demonstration workflow that showcases multi-MCP orchestration.

    Runs a self-contained demo that combines Sensei + external MCPs (Context7,
    Tavily, Playwright) in realistic workflows. Perfect for:
    - Testing multi-MCP coordination
    - Generating example documentation
    - Demonstrating Sensei capabilities
    - Training and onboarding

    Args:
        demo_type: Type of demo to run
            Available demos:
            - "auth-review": Authentication security review (Sensei + Context7 + Tavily + Playwright)
            - "performance-debug": Performance debugging (Sensei + Playwright + Context7)
            - "cost-analysis": Cloud cost optimization (Sensei + Tavily)
            - "api-review": API design review (Sensei + Context7 + Tavily)

        custom_params: Optional custom parameters to override defaults
            Example for auth-review: {
                "user_query": "Review FastAPI authentication",
                "app_url": "https://myapp.com/login",
                "framework": "FastAPI"
            }

        output_format: Output format ("markdown", "json", "text")

    Returns:
        Comprehensive demo execution report showing:
        - Workflow steps and MCP coordination
        - Example findings from multi-MCP synthesis
        - Expected output structure
        - How to run the demo yourself

    Examples:
        # Run auth security review demo with defaults
        run_demo(demo_type="auth-review")

        # Run with custom parameters
        run_demo(
            demo_type="auth-review",
            custom_params={
                "user_query": "Review OAuth implementation",
                "framework": "Django"
            }
        )

        # Get JSON output
        run_demo(demo_type="performance-debug", output_format="json")
    """
    result = demo_executor.run_demo(
        demo_type=demo_type,
        custom_params=custom_params,
        output_format=output_format
    )

    # If there's an error, return it as plain text
    if "error" in result:
        return json.dumps(result, indent=2)

    # Return formatted report
    return result["formatted_report"]


@mcp.tool()
def list_demos() -> str:
    """
    List all available demonstration workflows.

    Returns a summary of executable demos that showcase multi-MCP orchestration
    capabilities.

    Returns:
        JSON array of available demos with descriptions and example parameters

    Example:
        # List all demos
        list_demos()

        # Returns: 4 demos (auth-review, performance-debug, cost-analysis, api-review)
    """
    demos = demo_executor.list_demos()

    return json.dumps(demos, indent=2)


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
