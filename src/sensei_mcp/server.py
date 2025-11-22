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


@mcp.tool()
def analyze_changes(project_root: str) -> str:
    """
    Analyze staged git changes to identify relevant engineering contexts.
    
    Args:
        project_root: Absolute path to the project root
        
    Returns:
        Summary of changed files and their inferred context types
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
            
        # Infer context for these files
        contexts = ContextInferenceEngine.infer_contexts(file_paths=files)
        section_names = [ctx.value for ctx in contexts]
        
        report = ["# 🕵️ Git Change Analysis\n"]
        report.append(f"**Analyzed {len(files)} changed files:**\n")
        for f in files[:10]: # Limit to 10 files
            report.append(f"- `{f}`\n")
        if len(files) > 10:
            report.append(f"...and {len(files)-10} more\n")
            
        report.append(f"\n**Inferred Contexts ({len(contexts)}):**\n")
        for ctx in section_names:
            report.append(f"- {ctx}\n")
            
        report.append("\n**Recommendation:**\n")
        report.append(f"Run `get_engineering_context(file_paths={files[:5]})` to load these standards.")
        
        return "".join(report)
        
    except Exception as e:
        return f"❌ Error running git analysis: {str(e)}"


# ============================================================================
# v0.3.0 NEW TOOLS - Multi-Persona Orchestration
# ============================================================================

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

    return result['synthesis']


@mcp.tool()
def consult_skill(
    skill_name: str,
    query: str,
    session_id: str = "default",
    project_root: str = None
) -> str:
    """
    Consult a single skill persona directly.

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
def list_available_skills(category: str = None) -> str:
    """
    List all available skill personas.

    Args:
        category: Optional filter (core, specialized, operations, security, platform, cost, leadership, meta)

    Returns:
        Formatted list of available personas with descriptions
    """
    if category:
        if category not in persona_registry.get_categories():
            available_categories = ", ".join(persona_registry.get_categories().keys())
            return f"❌ Category '{category}' not found.\n\nAvailable categories: {available_categories}"

        personas = persona_registry.get_by_category(category)
        result = [f"# 🎭 {category.title()} Personas\n"]
    else:
        personas = persona_registry.get_all().values()
        result = [f"# 🎭 All Available Personas ({len(personas)} total)\n"]

    for persona in personas:
        result.append(f"\n## {persona.name.replace('-', ' ').title()}")
        result.append(f"{persona.description}\n")
        if persona.expertise_areas:
            result.append(f"**Expertise:** {', '.join(persona.expertise_areas[:5])}\n")

    result.append("\n---\n")
    result.append("**Usage:** `consult_skill(skill_name=\"...\", query=\"...\")` or `get_engineering_guidance(specific_personas=[\"...\"])`\n")

    return "".join(result)


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
