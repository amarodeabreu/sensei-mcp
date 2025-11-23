"""
Interactive Demo Mode for Sensei MCP v0.5.0

Provides an interactive walkthrough showcasing persona capabilities,
context detection, and multi-persona orchestration.
"""

import sys
from typing import List, Dict


# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print a colored header."""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{text}{Colors.ENDC}")


def print_section(text: str):
    """Print a colored section title."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{text}{Colors.ENDC}")


def print_success(text: str):
    """Print success message."""
    print(f"{Colors.GREEN}{text}{Colors.ENDC}")


def print_query(text: str):
    """Print a user query."""
    print(f"{Colors.YELLOW}Query: {text}{Colors.ENDC}")


def print_persona(text: str):
    """Print persona name."""
    print(f"{Colors.BLUE}{text}{Colors.ENDC}")


def wait_for_continue():
    """Wait for user to press Enter."""
    try:
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Demo interrupted. Goodbye!{Colors.ENDC}")
        sys.exit(0)


# Demo scenarios showcasing different persona combinations and contexts
DEMO_SCENARIOS = [
    {
        'title': "Scenario 1: Architecture Decision",
        'context': "ARCHITECTURAL",
        'query': "Should we migrate from a monolith to microservices?",
        'expected_personas': ["snarky-senior-engineer", "pragmatic-architect", "product-engineering-lead"],
        'explanation': """
This is a classic architecture decision that impacts:
- System complexity and maintainability
- Team structure and coordination
- Deployment and scaling patterns
- Business velocity and costs

Sensei detects this as an ARCHITECTURAL context and consults:
- Snarky Senior Engineer: Reality check on microservices hype
- Pragmatic Architect: Technical tradeoffs and evolution strategy
- Product Engineering Lead: Business impact and team readiness
        """,
        'synthesis_preview': """
🎭 MULTI-PERSONA SYNTHESIS:

**Consensus:**
Don't migrate to microservices just because it's trendy. Start by identifying:
1. Real pain points in the monolith (deployment coupling, scaling bottlenecks)
2. Team maturity (can you operate distributed systems?)
3. Business drivers (do you need independent service scaling?)

**Recommended Path:**
1. Extract 1-2 services for high-value use cases (e.g., billing, notifications)
2. Build operational maturity (observability, deployment automation)
3. Evaluate after 6 months: did it solve actual problems?

**Key Tensions:**
- Snarky warns: "Microservices trade complexity for independence"
- Pragmatic suggests: "Modular monolith first, extract services later"
- Product asks: "Does this accelerate feature delivery or slow it down?"
        """
    },
    {
        'title': "Scenario 2: Production Crisis",
        'context': "CRISIS",
        'query': "Production database is down! Users can't log in.",
        'expected_personas': ["incident-commander", "site-reliability-engineer", "executive-liaison"],
        'explanation': """
This is a CRISIS situation requiring immediate action and communication.

Sensei activates the Crisis Response Team:
- Incident Commander: Orchestrates response, assigns roles
- Site Reliability Engineer: Technical diagnosis and mitigation
- Executive Liaison: Stakeholder communication and impact assessment

Mode: CRISIS (emergency team, no time for lengthy analysis)
        """,
        'synthesis_preview': """
🚨 CRISIS MODE - IMMEDIATE ACTIONS:

**Incident Commander says:**
1. DECLARE INCIDENT - Severity 1 (user-facing outage)
2. ASSEMBLE WAR ROOM - Get SRE lead, on-call engineer, eng manager
3. ESTABLISH COMMAND - One person makes decisions, others execute
4. SET 15-MIN CHECK-INS - Regular status updates

**SRE says:**
Immediate triage:
- Check database health metrics (CPU, memory, connections)
- Review recent deployments (did we just push something?)
- Check logs for connection pool exhaustion
- Failover to read replica if needed

**Executive Liaison says:**
External communication:
- Status page update NOW: "Investigating login issues"
- Support team notification: canned response ready
- Escalation path: When to alert VP/CEO? (>30min outage or >10k users affected)

**Next 5 Minutes:**
Run diagnostics, establish incident channel, prepare status update.
        """
    },
    {
        'title': "Scenario 3: Security Review",
        'context': "SECURITY",
        'query': "Review this authentication implementation for security issues",
        'expected_personas': ["security-sentinel", "compliance-guardian", "api-platform-engineer"],
        'explanation': """
This is a SECURITY-focused consultation requiring multiple expert perspectives.

Sensei consults:
- Security Sentinel: Vulnerability detection, threat modeling
- Compliance Guardian: Regulatory requirements (GDPR, SOC2, etc.)
- API Platform Engineer: API security best practices

Security reviews benefit from paranoid thinking + compliance awareness.
        """,
        'synthesis_preview': """
🛡️ SECURITY REVIEW - MULTI-LAYERED ANALYSIS:

**Security Sentinel's Audit:**
⚠️ Critical Issues:
- No rate limiting on login endpoint (brute force risk)
- JWT tokens never expire (revocation impossible)
- Passwords stored with bcrypt rounds=10 (increase to 12+)

⚠️ Important Issues:
- No MFA support (add TOTP or WebAuthn)
- Session tokens in localStorage (use httpOnly cookies)
- No CSRF protection on state-changing endpoints

**Compliance Guardian's Check:**
📋 Regulatory Requirements:
- GDPR: Need consent for "remember me" (tracking cookies)
- SOC2: Require audit logging of authentication events
- Data retention: Define password hash retention policy

**API Platform Engineer's Input:**
🔧 Implementation Best Practices:
- Use OAuth2/OIDC instead of custom auth
- Implement refresh token rotation
- Add API key authentication for service-to-service

**Priority Actions:**
1. Add rate limiting TODAY (prevents brute force)
2. Implement JWT expiration (1 hour access, 7 day refresh)
3. Enable audit logging (compliance + incident response)
4. Plan MFA rollout (30-60 days)
        """
    },
    {
        'title': "Scenario 4: Cost Optimization",
        'context': "COST",
        'query': "Our AWS bill doubled this month. How do we reduce costs?",
        'expected_personas': ["finops-optimizer", "site-reliability-engineer", "pragmatic-architect"],
        'explanation': """
This is a COST optimization problem requiring financial + technical expertise.

Sensei consults:
- FinOps Optimizer: Cloud cost analysis and optimization strategies
- Site Reliability Engineer: Operational efficiency and resource usage
- Pragmatic Architect: Architectural cost implications

Cost problems often have architectural, operational, AND code-level solutions.
        """,
        'synthesis_preview': """
💰 COST OPTIMIZATION - SYSTEMATIC ANALYSIS:

**FinOps Optimizer's Breakdown:**
First, diagnose WHY costs doubled:
1. Check Cost Explorer for biggest deltas (EC2? RDS? Data transfer?)
2. Look for anomalies (did traffic 2x? New service launched?)
3. Review untagged resources (zombie instances?)

Quick wins (30% savings potential):
- Rightsiz

e over-provisioned instances (use AWS Compute Optimizer)
- Delete unused EBS volumes and snapshots
- Buy Reserved Instances for steady-state workloads
- Enable S3 lifecycle policies (move old data to Glacier)

**SRE's Operational Lens:**
Efficiency improvements:
- Audit autoscaling policies (are we scaling down?)
- Check connection pooling (are we reusing connections?)
- Review log retention (3 months of CloudWatch logs = $$)
- Optimize batch job scheduling (use spot instances)

**Pragmatic Architect's View:**
Architectural cost drivers:
- Are we over-indexing? (30 database indexes = slower writes, bigger storage)
- Caching strategy? (hit rate <80% = wasted Redis spend)
- N+1 queries? (1000 DB calls vs 1 = latency + cost)
- Data transfer? (cross-region = 10x cost vs same-region)

**Action Plan:**
Week 1: Identify top 3 cost drivers (FinOps analysis)
Week 2: Quick wins (rightsize, delete zombies)
Week 3: Operational improvements (autoscaling, pooling)
Week 4: Architectural review (caching, queries, data transfer)
        """
    },
    {
        'title': "Scenario 5: Code Quality Improvement",
        'context': "TECHNICAL",
        'query': "Our codebase is becoming unmaintainable. How do we improve quality?",
        'expected_personas': ["snarky-senior-engineer", "legacy-archaeologist", "empathetic-team-lead"],
        'explanation': """
This is a TECHNICAL + TEAM problem requiring code expertise + people skills.

Sensei consults:
- Snarky Senior Engineer: Pragmatic quality improvements
- Legacy Archaeologist: Incremental refactoring strategies
- Empathetic Team Lead: Team buy-in and sustainable pace

Quality improvements fail without team alignment and realistic expectations.
        """,
        'synthesis_preview': """
🔨 CODE QUALITY - PRAGMATIC IMPROVEMENT PATH:

**Snarky's Reality Check:**
"Unmaintainable" is vague. Define concrete pain points:
- Is it slow to add features? (coupling problems)
- Lots of bugs? (lack of tests)
- Hard to understand? (missing docs, poor naming)
- Scary to deploy? (no confidence in changes)

Don't rewrite. Don't add linters overnight. Start small.

**Legacy Archaeologist's Strategy:**
Incremental improvement ("Boy Scout Rule"):
1. Identify hotspots (files changed most often = highest ROI)
2. Add tests ONLY for hotspot files (not everything!)
3. Refactor incrementally during feature work
4. Document decisions (ADRs prevent re-litigation)

Tools:
- Code complexity metrics (identify hotspots)
- Test coverage for hotspots only
- Linting rules added gradually (1 per sprint)

**Empathetic Team Lead's Approach:**
Team sustainability:
- Don't blame: "Legacy code pays the bills"
- Reserve 20% time for quality (not 0%, not 50%)
- Celebrate improvements (shout-outs for refactoring)
- Set realistic expectations with product (quality takes time)

Avoid: "Quality sprint" (never ends), "Stop feature work" (unsustainable)

**6-Month Plan:**
Month 1-2: Identify hotspots, add tests to top 5 files
Month 3-4: Refactor hotspots incrementally
Month 5-6: Extract reusable modules, document patterns

Measure: Time to add features (should decrease), bug rate (should decrease)
        """
    }
]


def run_demo():
    """Run the interactive Sensei demo."""
    # Clear screen (works on Unix/Mac)
    print("\033[H\033[J")

    # Welcome
    print_header("=" * 70)
    print_header("🥋  WELCOME TO SENSEI MCP - INTERACTIVE DEMO  🥋")
    print_header("=" * 70)

    print(f"""
{Colors.BOLD}What is Sensei?{Colors.ENDC}
Sensei is your engineering mentor with 22 specialized AI personas that
collaborate to provide multi-perspective guidance on technical decisions.

{Colors.BOLD}What you'll see:{Colors.ENDC}
- 5 real-world scenarios showing persona collaboration
- Context detection (ARCHITECTURAL, CRISIS, SECURITY, COST, TECHNICAL)
- Multi-persona synthesis with consensus and tensions
- How different personas complement each other

{Colors.BOLD}How it works:{Colors.ENDC}
1. You ask an engineering question
2. Sensei detects the context (CRISIS, SECURITY, ARCHITECTURAL, etc.)
3. Relevant personas are consulted (2-5 experts)
4. Perspectives are synthesized with recommendations

Let's see it in action!
    """)

    wait_for_continue()

    # Run through scenarios
    for i, scenario in enumerate(DEMO_SCENARIOS, 1):
        # Clear screen
        print("\033[H\033[J")

        print_header("=" * 70)
        print_header(f"{scenario['title']} ({i}/{len(DEMO_SCENARIOS)})")
        print_header("=" * 70)

        print_section("📝 The Situation:")
        print_query(scenario['query'])

        print_section(f"\n🔍 Context Detected: {scenario['context']}")
        print(scenario['explanation'])

        print_section("\n🎭 Personas Consulted:")
        for persona in scenario['expected_personas']:
            print_persona(f"  • {persona.replace('-', ' ').title()}")

        wait_for_continue()

        # Show synthesis
        print_section("\n✨ Multi-Persona Synthesis:")
        print(scenario['synthesis_preview'])

        if i < len(DEMO_SCENARIOS):
            wait_for_continue()

    # Final screen
    print("\033[H\033[J")
    print_header("=" * 70)
    print_header("🎉  DEMO COMPLETE - YOU'VE SEEN SENSEI IN ACTION!  🎉")
    print_header("=" * 70)

    print(f"""
{Colors.BOLD}What you learned:{Colors.ENDC}
✅ Context detection automatically routes questions to relevant experts
✅ Multiple personas provide comprehensive, nuanced guidance
✅ Synthesis identifies consensus, tensions, and actionable recommendations
✅ Different modes (orchestrated, quick, crisis) for different needs

{Colors.BOLD}22 Available Personas:{Colors.ENDC}
- Core: Snarky Senior Engineer, Pragmatic Architect, Legacy Archaeologist
- Specialized: Security Sentinel, FinOps Optimizer, API Engineer, Data Engineer
- Operations: SRE, Incident Commander, Observability Engineer
- Leadership: Empathetic Team Lead, Product Lead, Executive Liaison
- ...and 10 more!

{Colors.BOLD}Getting Started:{Colors.ENDC}
1. Install: {Colors.CYAN}uvx sensei-mcp{Colors.ENDC}
2. Configure in your MCP client (Claude Desktop, Cursor, Windsurf, etc.)
3. Ask questions: {Colors.YELLOW}"Should we use PostgreSQL or MongoDB?"{Colors.ENDC}
4. Get multi-persona guidance with session memory

{Colors.BOLD}Key Features:{Colors.ENDC}
• Session Memory: Decisions persist across conversations
• Analytics: Track persona usage and decision velocity
• Team Collaboration: Export ADRs and share session context
• CI/CD Integration: Automate architecture reviews

{Colors.BOLD}Learn More:{Colors.ENDC}
- GitHub: {Colors.CYAN}https://github.com/amarodeabreu/sensei-mcp{Colors.ENDC}
- Docs: Run {Colors.CYAN}list_available_skills(){Colors.ENDC} to see all personas
- Examples: Check {Colors.CYAN}get_engineering_guidance(){Colors.ENDC} docstring

{Colors.BOLD}Try It Now:{Colors.ENDC}
• Standard mode: {Colors.CYAN}get_engineering_guidance(query="Your question"){Colors.ENDC}
• Quick mode: {Colors.CYAN}get_engineering_guidance(query="...", mode="quick"){Colors.ENDC}
• Specific personas: {Colors.CYAN}get_engineering_guidance(query="...", specific_personas=["security-sentinel"]){Colors.ENDC}

Thank you for trying Sensei! 🥋
    """)

    print_success("\n✨ May your code be boring, robust, and readable. ✨\n")


if __name__ == "__main__":
    run_demo()
