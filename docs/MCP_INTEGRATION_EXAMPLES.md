# MCP Integration Examples: Real-World Workflows

**Version:** 0.8.0
**Last Updated:** 2025-01-27

This guide provides copy-paste workflows combining Sensei MCP with other MCP servers for common CTO scenarios.

---

## 🎯 Table of Contents

1. [Setup Instructions](#setup-instructions)
2. [Security Review Workflow](#security-review-workflow)
3. [Cost Optimization Workflow](#cost-optimization-workflow)
4. [Performance Analysis Workflow](#performance-analysis-workflow)
5. [Architecture Decision Workflow](#architecture-decision-workflow)
6. [Production Incident Workflow](#production-incident-workflow)
7. [Code Review Workflow](#code-review-workflow)

---

## Setup Instructions

### Install MCP Servers

```bash
# Sensei MCP (already installed if you're reading this)
# uvx sensei-mcp

# Context7 (library documentation)
npm install -g @upstash/context7-mcp

# Tavily (web search)
npm install -g @tavily/mcp-server

# Playwright (live system inspection)
npm install -g @playwright/mcp-server
```

### Configure Claude Code

```bash
# Add all MCP servers
claude mcp add sensei -- uvx sensei-mcp
claude mcp add context7 -- npx -y @upstash/context7-mcp
claude mcp add tavily -- npx -y @tavily/mcp-server
claude mcp add playwright -- npx -y @playwright/mcp-server
```

### Verify Installation

Ask Claude:
```
List all available MCP servers and their tools
```

Expected output should show tools from:
- ✅ sensei (20 tools)
- ✅ context7 (2 tools)
- ✅ tavily (2 tools)
- ✅ playwright (15+ tools)

---

## Security Review Workflow

### Scenario: Authentication Implementation Review

**Copy-paste this into Claude Code:**

```
SECURITY REVIEW WORKFLOW

Context: I need a comprehensive security review of our authentication implementation.

Step 1: Sensei, suggest relevant personas for this security review
Use: suggest_personas_for_query(query="security review of authentication implementation")

Step 2: Get full content for suggested personas
Use: get_persona_content() for each suggested persona

Step 3: Context7, fetch current security best practices
Use: resolve-library-id(libraryName="OWASP ASVS")
Then: get-library-docs() for OAuth 2.0 and JWT standards

Step 4: Tavily, search for recent authentication vulnerabilities
Use: tavily-search(query="OAuth JWT vulnerabilities 2025")

Step 5: Synthesize all perspectives
- Security expert analysis (Sensei personas)
- Current OWASP standards (Context7)
- Recent threat landscape (Tavily)

Step 6: Record the consultation
Use: record_consultation() to save this analysis to session

Provide:
1. Critical vulnerabilities to fix immediately
2. Medium-priority improvements
3. Good practices to keep
4. Implementation timeline
5. Success metrics
```

**Expected Output:**
- 3-5 security-related personas consulted
- Current OWASP ASVS and OAuth 2.0 docs
- Recent CVEs and security advisories
- Prioritized action plan with timeline

---

## Cost Optimization Workflow

### Scenario: AWS Bill Reduction

**Copy-paste this into Claude Code:**

```
COST OPTIMIZATION WORKFLOW

Context: Our AWS bill is $50K/month and we need to reduce it by 30%.

Step 1: Sensei, suggest relevant personas for cost optimization
Use: suggest_personas_for_query(query="reduce AWS cloud costs by 30%")

Step 2: Get session context for past decisions
Use: get_session_context(session_id="production-aws")

Step 3: Tavily, get current AWS pricing and cost optimization guides
Use: tavily-search(query="AWS cost optimization 2025 best practices")
Use: tavily-search(query="AWS reserved instances vs savings plans 2025")

Step 4: Get full content for suggested personas
Use: get_persona_content() for FinOps Optimizer, Cloud Architect, etc.

Step 5: Analyze current AWS usage (if available via API/exports)
Provide: EC2 instance types, RDS usage, S3 storage, data transfer costs

Step 6: Synthesize recommendations
- FinOps perspective (cost optimization strategies)
- Cloud Architect perspective (architecture changes)
- SRE perspective (reliability vs. cost trade-offs)
- Current AWS pricing (Tavily)
- Past cost decisions (session context)

Step 7: Record decisions
Use: record_decision() for approved cost optimization strategies

Provide:
1. Quick wins (implement this week) with $ savings
2. Medium-term optimizations (next month) with $ savings
3. Long-term architectural changes with $ savings
4. Total projected savings
5. Risk assessment for each change
```

**Expected Output:**
- Right-sizing recommendations
- Reserved instance/savings plan analysis
- S3 storage class optimization
- Data transfer reduction strategies
- $15K+ monthly savings plan

---

## Performance Analysis Workflow

### Scenario: Slow Checkout Page

**Copy-paste this into Claude Code:**

```
PERFORMANCE ANALYSIS WORKFLOW

Context: Our checkout page takes 8 seconds to load. Users are abandoning.

Step 1: Playwright, capture live performance data
Use: browser_navigate(url="https://app.example.com/checkout")
Use: browser_take_screenshot() to see current state
Use: browser_network_requests() to see waterfall

Step 2: Sensei, suggest relevant personas for performance analysis
Use: suggest_personas_for_query(query="optimize slow checkout page performance")

Step 3: Context7, fetch current web performance best practices
Use: resolve-library-id(libraryName="web.dev")
Then: get-library-docs() for Core Web Vitals, performance optimization

Step 4: Tavily, search for checkout optimization case studies
Use: tavily-search(query="e-commerce checkout performance optimization 2025")

Step 5: Get full content for suggested personas
Use: get_persona_content() for Performance Engineer, Frontend UX Specialist

Step 6: Synthesize analysis
- Live network waterfall (Playwright)
- Performance expert recommendations (Sensei)
- Core Web Vitals benchmarks (Context7)
- Industry case studies (Tavily)

Step 7: Record optimization plan
Use: record_decision() for approved performance changes

Provide:
1. Top 3 bottlenecks with impact (% of 8s)
2. Quick fixes (implement today) with expected improvement
3. Medium-term optimizations (this sprint)
4. Long-term architectural improvements
5. Target metrics: <2s load time, LCP <2.5s, CLS <0.1
```

**Expected Output:**
- Identified bottlenecks (large images, blocking JS, API latency)
- Prioritized optimization plan
- Expected improvement timeline
- Before/after metrics

---

## Architecture Decision Workflow

### Scenario: Microservices Migration Decision

**Copy-paste this into Claude Code:**

```
ARCHITECTURE DECISION WORKFLOW

Context: Should we migrate from monolith to microservices?
- Team size: 15 engineers
- Current users: 50K MAU
- Scaling pain: Deployments take 30 minutes, frequent conflicts

Step 1: Sensei, use orchestrated mode for multi-persona analysis
Use: get_engineering_guidance(
  query="Should we migrate from monolith to microservices? 15 engineers, 50K users",
  mode="orchestrated",
  session_id="architecture-decisions"
)

Step 2: Get session context for past architectural decisions
Use: get_session_context(session_id="architecture-decisions")

Step 3: Context7, fetch microservices patterns and best practices
Use: resolve-library-id(libraryName="microservices")
Then: get-library-docs() for service mesh, event-driven architecture

Step 4: Tavily, search for microservices case studies at similar scale
Use: tavily-search(query="microservices migration 15 engineers 50K users case study")

Step 5: Sequential Thinking (if available), explore trade-offs
Use chain-of-thought reasoning to evaluate:
- Migrate now vs. later vs. never
- Modular monolith vs. microservices
- Cost, complexity, team capacity

Step 6: Synthesize comprehensive recommendation
- Pragmatic Architect perspective
- Site Reliability Engineer perspective
- FinOps Optimizer perspective (cost impact)
- DevEx Champion perspective (developer experience)
- Current best practices (Context7)
- Real-world case studies (Tavily)
- Past decisions (session context)

Step 7: Record architectural decision
Use: record_decision(
  category="architecture",
  description="[Decision: Migrate/Stay/Modular Monolith]",
  rationale="[Full reasoning from synthesis]"
)

Provide:
1. Clear recommendation (Migrate / Stay / Modular Monolith)
2. Pros and cons of each option
3. Timeline and phases (if migrating)
4. Cost impact (infrastructure, team time)
5. Risk mitigation strategies
6. Success metrics and checkpoints
```

**Expected Output:**
- Data-driven recommendation
- 6-12 month migration plan (if applicable)
- Cost/benefit analysis
- Risk assessment
- Decision rationale documented

---

## Production Incident Workflow

### Scenario: Database Outage

**Copy-paste this into Claude Code:**

```
PRODUCTION INCIDENT WORKFLOW (CRISIS MODE)

Context: 🚨 PRODUCTION DATABASE IS DOWN. Users can't log in.
Time: 2:34 AM
Impact: 100% of users affected
Stakeholders: CEO is asking for updates

Step 1: Sensei, activate CRISIS mode
Use: get_engineering_guidance(
  query="Production database outage, users can't log in, need immediate triage",
  mode="crisis",
  session_id="production-incidents"
)
Expected personas: Incident Commander, SRE, Executive Liaison

Step 2: Tavily, search for recent similar incidents
Use: tavily-search(query="PostgreSQL outage root cause analysis 2025")

Step 3: Get full crisis response content
Use: get_persona_content() for:
- Incident Commander (triage and coordination)
- Site Reliability Engineer (technical diagnosis)
- Executive Liaison (stakeholder communication)

Step 4: Playwright (if accessible), check system status
Use: browser_navigate() to status pages, monitoring dashboards

Step 5: Immediate triage synthesis
- Incident Commander: Triage steps, communication plan
- SRE: Diagnosis checklist, recovery procedures
- Executive Liaison: Stakeholder messaging templates
- Recent incident learnings (Tavily)

Step 6: Execute and log actions
As actions are taken, use: record_consultation() to log timeline

Provide RIGHT NOW:
1. 🚨 Immediate triage steps (next 5 minutes)
2. 📊 Quick diagnosis checklist
3. 💬 Stakeholder message template (for CEO)
4. ⏱️ Recovery SLA estimate
5. 📞 Who to page/escalate to

Then provide:
6. 🔍 Root cause analysis framework
7. 📝 Post-mortem template
8. 🛡️ Prevention measures
```

**Expected Output:**
- Immediate 5-minute action plan
- Stakeholder communication template
- Technical diagnosis checklist
- Recovery procedures
- Post-mortem framework

---

## Code Review Workflow

### Scenario: Pull Request Architectural Review

**Copy-paste this into Claude Code:**

```
CODE REVIEW WORKFLOW

Context: Review PR #456 for architectural consistency and best practices.
PR: Adds new payment processing microservice

Step 1: GitHub MCP (if available), fetch PR context
Use: Get PR #456 diff, comments, CI status, linked issues

Step 2: Sensei, analyze git changes
Use: analyze_changes(project_root="/path/to/repo")

Step 3: Sensei, suggest relevant personas based on changes
Use: suggest_personas_for_query(
  query="review payment processing microservice PR",
  context_hint="ARCHITECTURAL"
)

Step 4: Get session context for past architectural decisions
Use: get_session_context(session_id="payment-service")

Step 5: Context7, fetch payment processing best practices
Use: resolve-library-id(libraryName="Stripe")
Then: get-library-docs() for payment APIs, PCI compliance

Step 6: Tavily, search for payment security best practices
Use: tavily-search(query="payment processing security PCI DSS 2025")

Step 7: Get full content for suggested personas
Use: get_persona_content() for suggested personas

Step 8: Check consistency with past decisions
Use: check_consistency(
  proposed_change="New payment microservice with Stripe integration",
  session_id="payment-service"
)

Step 9: Synthesize comprehensive review
- Architectural consistency (Pragmatic Architect)
- Security review (Security Sentinel)
- API design (API Platform Engineer)
- Compliance (Compliance Guardian)
- Current Stripe best practices (Context7)
- PCI-DSS requirements (Tavily)
- Past payment decisions (session context)

Step 10: Record review and decisions
Use: record_consultation() to save review

Provide:
1. ✅ Approvals (what's good)
2. 🔴 Blocking issues (must fix before merge)
3. 🟡 Suggestions (nice to have)
4. 📚 References (docs, standards)
5. 🎯 Testing recommendations
6. 📊 Compliance checklist (PCI-DSS)
```

**Expected Output:**
- Comprehensive architectural review
- Security and compliance checks
- Consistency with past decisions
- Actionable feedback with references

---

## 🎯 Tips for Effective Workflows

### 1. Always Use Session IDs
```python
# Bad
get_engineering_guidance(query="...")

# Good
get_engineering_guidance(
  query="...",
  session_id="project-name"
)
```

### 2. Combine Multiple MCP Servers
```
Best practices:
- Sensei for expert personas
- Context7 for current documentation
- Tavily for recent events/research
- Playwright for live system inspection
```

### 3. Record Everything
```python
# After every decision
record_decision(
  category="architecture",  # or "security", "cost", etc.
  description="...",
  rationale="...",
  session_id="project-name"
)

# After every consultation
record_consultation(
  query="...",
  personas_used=[...],
  synthesis="...",
  session_id="project-name"
)
```

### 4. Export for Team Sharing
```python
# Weekly team summary
export_session_summary(
  session_id="project-name",
  format="markdown",
  include=["decisions", "consultations", "constraints"]
)

# Share in Slack, Confluence, ADR repo
```

### 5. Use Analytics to Improve
```python
# Monthly review
get_session_insights(
  session_id="project-name",
  time_range="last_30_days",
  format="markdown"
)

# Questions to ask:
# - Which personas are most/least used?
# - Which contexts appear most often?
# - Where do we re-litigate decisions?
```

---

## 📚 Additional Resources

- **MCP Integration Architecture**: `docs/MCP_INTEGRATION_ARCHITECTURE.md`
- **Sensei MCP API Reference**: `docs/USAGE_GUIDE.md`
- **Context7 Documentation**: https://github.com/upstash/context7-mcp
- **Tavily Documentation**: https://tavily.com
- **Playwright MCP**: https://github.com/executeautomation/playwright-mcp-server

---

## 🤝 Contributing Workflows

Found a great workflow? Share it!

1. Fork the repo
2. Add your workflow to this file
3. Submit a PR with:
   - Workflow name and scenario
   - Step-by-step instructions
   - Expected output
   - Tips and gotchas

---

**Made with 🥋 by the Sensei MCP community**

*Combining 64 expert personas with real-time intelligence for CTO-level decisions*
