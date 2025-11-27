# Tavily MCP Integration Guide

**Version:** 0.8.0
**MCP Server:** [@tavily/mcp-server](https://github.com/tavily-ai/tavily-mcp)
**Purpose:** Real-time web search and intelligence gathering

---

## 🎯 What is Tavily?

Tavily provides AI-powered web search, giving Sensei personas access to:
- **Recent security vulnerabilities** (CVEs published this week)
- **Current cloud pricing** (AWS/GCP/Azure rate changes)
- **Incident postmortems** (recent outages and lessons learned)
- **Technology news** (framework releases, best practice updates)

### Why This Matters

When making decisions, you need **current** data, not just Claude's training cutoff:
- Security Sentinel: "Is Log4j still dangerous in 2025?" → Tavily finds latest CVEs
- FinOps Optimizer: "How much does GCP Cloud Run cost?" → Tavily finds current pricing
- SRE: "What caused the recent GitHub outage?" → Tavily finds incident report

---

## 🚀 Quick Start (5 Minutes)

### 1. Get Tavily API Key

Tavily requires an API key (free tier: 1,000 searches/month):

1. Visit: https://tavily.com/
2. Sign up for free account
3. Copy API key from dashboard

### 2. Install Tavily MCP

```bash
# Test if Tavily works
npx -y @tavily/mcp-server --version
```

### 3. Configure MCP Client

**Claude Code:**
```bash
# Set API key
export TAVILY_API_KEY="tvly-xxxxxxxxxxxxx"

# Add MCP server
claude mcp add tavily -- npx -y @tavily/mcp-server
```

**Claude Desktop (macOS):**
```json
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "sensei": {
      "command": "uvx",
      "args": ["sensei-mcp"]
    },
    "tavily": {
      "command": "npx",
      "args": ["-y", "@tavily/mcp-server"],
      "env": {
        "TAVILY_API_KEY": "tvly-xxxxxxxxxxxxx"
      }
    }
  }
}
```

**Claude Desktop (Windows):**
```json
// %APPDATA%\Claude\claude_desktop_config.json
{
  "mcpServers": {
    "sensei": {
      "command": "uvx",
      "args": ["sensei-mcp"]
    },
    "tavily": {
      "command": "npx",
      "args": ["-y", "@tavily/mcp-server"],
      "env": {
        "TAVILY_API_KEY": "tvly-xxxxxxxxxxxxx"
      }
    }
  }
}
```

### 4. Test Integration

Restart your MCP client and try:

```
You: "What are the latest security vulnerabilities in Node.js?"

Expected workflow:
1. Sensei suggests: [security-sentinel]
2. Tavily searches: "Node.js vulnerabilities 2025"
3. Claude synthesizes: Security expert perspective + recent CVE data
```

---

## 📚 How to Use Tavily with Sensei

### Pattern: Current Intelligence + Expert Analysis

**User Query:** "Should we use Log4j in our new Java microservice?"

**Sensei + Tavily Flow:**
1. **Sensei suggests:** `[security-sentinel, backend-distributed-systems-engineer]`
2. **Tavily searches:**
   - "Log4j vulnerabilities 2025"
   - "Log4j alternatives Java logging"
3. **Synthesis:**
   - Security Sentinel: CVE history, threat assessment
   - Backend Engineer: Alternative frameworks (Logback, SLF4J)
   - **Tavily results:** Recent security advisories, current best practices

**Output:**
```markdown
## Log4j Recommendation: DO NOT USE

### Security Assessment (Security Sentinel + Tavily)

**Recent Vulnerabilities (Tavily search: Jan 2025):**
- CVE-2021-44228 (Log4Shell): Still actively exploited
- CVE-2021-45046: Follow-up bypass discovered
- CVE-2023-XXXXX: New RCE found in Log4j 2.17.0

**Exploitation Stats (from Tavily sources):**
- 40% of attacks in Q4 2024 targeted Log4j (Cloudflare report)
- Average time to exploit: 15 minutes (CISA alert)

### Recommended Alternatives (Backend Engineer + Tavily)

**1. Logback (First Choice)**
- Used by Spring Boot by default
- Active maintenance (last release: 2 weeks ago)
- No critical CVEs in 5 years

**2. SLF4J + Logback**
- Abstraction layer (easy to swap implementations)
- Industry standard for Java logging

### Migration Path
```java
// Replace Log4j dependency
// OLD:
// <dependency>
//   <groupId>org.apache.logging.log4j</groupId>
//   <artifactId>log4j-core</artifactId>
// </dependency>

// NEW:
<dependency>
  <groupId>ch.qos.logback</groupId>
  <artifactId>logback-classic</artifactId>
  <version>1.4.14</version>
</dependency>
```
```

---

## 🔥 Example Workflows

### Workflow 1: Security Vulnerability Check

**Scenario:** Check if a dependency has recent vulnerabilities

```
You: "We're using FastAPI 0.100. Are there any recent security issues?"

Sensei + Tavily workflow:
1. Sensei suggests: [security-sentinel]
2. Tavily searches:
   - "FastAPI vulnerabilities 2025"
   - "FastAPI CVE 2024 2025"
   - "FastAPI security advisories"
3. Claude synthesizes: CVE data + Security Sentinel risk assessment
```

**Sample Output:**
```markdown
## FastAPI 0.100 Security Assessment

### 🟡 Medium Priority Upgrade Recommended

**Recent Vulnerabilities (Tavily - Jan 2025):**

1. **CVE-2024-XXXXX** (Severity: 7.5 HIGH)
   - Affects: FastAPI 0.95 - 0.103
   - Issue: Path traversal in static file serving
   - Fixed in: FastAPI 0.104.0
   - **Action:** Upgrade to 0.104.0+ this sprint

2. **CVE-2024-YYYYY** (Severity: 5.3 MEDIUM)
   - Affects: FastAPI 0.100 - 0.103
   - Issue: Open redirect in OAuth2 flow
   - Fixed in: FastAPI 0.104.1
   - **Action:** Review OAuth2 implementation

### Upgrade Plan (Security Sentinel)
**Week 1:**
- Upgrade FastAPI: `pip install fastapi==0.110.0` (latest)
- Run test suite
- Deploy to staging

**Week 2:**
- Security review of OAuth2 flows
- Deploy to production
```

---

### Workflow 2: Cloud Cost Intelligence

**Scenario:** Check current cloud pricing before making infrastructure decisions

```
You: "What's more cost-effective: AWS Lambda or GCP Cloud Run for our Python API?"

Sensei + Tavily workflow:
1. Sensei suggests: [finops-optimizer, cloud-architect]
2. Tavily searches:
   - "AWS Lambda pricing 2025"
   - "GCP Cloud Run pricing 2025"
   - "Lambda vs Cloud Run cost comparison"
3. Claude synthesizes: Current pricing + FinOps analysis
```

**Sample Output:**
```markdown
## Cost Comparison: AWS Lambda vs GCP Cloud Run

### Current Pricing (Tavily - Jan 2025)

**AWS Lambda:**
- Compute: $0.0000166667 per GB-second
- Requests: $0.20 per 1M requests
- Free tier: 1M requests/month, 400K GB-seconds

**GCP Cloud Run:**
- Compute: $0.000024 per vCPU-second + $0.0000025 per GB-second
- Requests: $0.40 per 1M requests
- Free tier: 2M requests/month, 360K vCPU-seconds

### Cost Analysis (FinOps Optimizer)

**Scenario 1: Low Traffic (100K req/month)**
- AWS Lambda: ~$0 (within free tier)
- GCP Cloud Run: ~$0 (within free tier)
- **Winner:** Tie

**Scenario 2: Medium Traffic (10M req/month)**
- AWS Lambda: ~$23/month ($2 compute + $1.80 requests)
- GCP Cloud Run: ~$28/month ($4 compute + $3.60 requests)
- **Winner:** AWS Lambda (19% cheaper)

**Scenario 3: High Traffic (100M req/month, 2s avg)**
- AWS Lambda: ~$360/month
- GCP Cloud Run: ~$410/month
- **Winner:** AWS Lambda (14% cheaper)

### Recommendation (Cloud Architect + FinOps)
- **Cost:** AWS Lambda wins across all scales
- **BUT:** GCP Cloud Run has better DX (longer timeouts, WebSocket support)
- **Decision:** If cost-sensitive, choose Lambda. If need WebSockets, choose Cloud Run.
```

---

### Workflow 3: Technology Due Diligence

**Scenario:** Evaluate if a new technology is production-ready

```
You: "Should we adopt Bun (JavaScript runtime) for our Node.js services?"

Sensei + Tavily workflow:
1. Sensei suggests: [pragmatic-architect, snarky-senior-engineer]
2. Tavily searches:
   - "Bun production ready 2025"
   - "Bun vs Node.js benchmarks"
   - "Bun stability issues"
3. Claude synthesizes: Current status + expert recommendations
```

**Sample Output:**
```markdown
## Bun Adoption Analysis

### Current Status (Tavily - Jan 2025)

**Positive Signals:**
- Bun 1.1 released (Dec 2024) - marked "production ready"
- Companies using: Vercel (internal tools), Railway (build system)
- Performance: 3x faster than Node.js (V8) for I/O-heavy tasks

**Concerns:**
- NPM compatibility: 95% (some native modules fail)
- Community: 50K GitHub stars vs Node.js 100K+
- Job market: Few "Bun expertise" requirements yet

### Expert Assessment

**Pragmatic Architect:**
> "Bun is promising but still early. For new greenfield services with
> no legacy dependencies, worth experimenting. For critical production
> systems with large dependency trees, wait 12 months."

**Snarky Senior Engineer:**
> "Bun is fast. You know what's faster? Not rewriting your entire stack
> because a native module broke. Node.js 20 with proper async patterns
> is fast enough for 99% of use cases."

### Recommendation
- ✅ **Experiment:** Use Bun for CLI tools, build scripts, dev tooling
- ⚠️ **Caution:** Pilot in 1 non-critical service, measure stability
- ❌ **Avoid:** Don't rewrite existing production services yet

**Revisit in:** Q3 2025 (when Bun 2.0 ships)
```

---

### Workflow 4: Incident Intelligence

**Scenario:** Learn from recent outages

```
You: "What caused the recent AWS S3 outage? How can we prevent similar issues?"

Sensei + Tavily workflow:
1. Sensei suggests: [site-reliability-engineer, incident-commander]
2. Tavily searches:
   - "AWS S3 outage 2025"
   - "AWS S3 postmortem"
   - "S3 resilience best practices"
3. Claude synthesizes: Incident details + SRE recommendations
```

**Sample Output:**
```markdown
## AWS S3 Outage Analysis & Prevention

### Incident Summary (Tavily - Jan 2025)

**What Happened:**
- Date: Jan 15, 2025
- Duration: 4 hours 23 minutes
- Affected: us-east-1 region (S3 + CloudFront)
- Root cause: Authentication service capacity exceeded

**Impact (from AWS postmortem):**
- 2.4% of PUT/GET requests failed
- 12% of customers experienced errors
- $10M+ in lost revenue across customers

### SRE Analysis

**Root Cause (Site Reliability Engineer):**
> "Classic capacity planning failure. AWS authentication service couldn't
> handle peak traffic spike (3x normal). Cascading failures took down
> S3 API, then CloudFront."

**Prevention Strategies:**

1. **Multi-Region Architecture** (Critical)
   ```
   Primary: us-east-1
   Failover: us-west-2
   Replication: Cross-region async (S3 CRR)
   ```

2. **Circuit Breakers** (High Priority)
   ```python
   # Don't retry forever on S3 errors
   @retry(
       stop=stop_after_attempt(3),
       wait=wait_exponential(multiplier=1, min=4, max=10),
       retry=retry_if_exception_type(S3Error)
   )
   def upload_to_s3(file):
       # If S3 down, fallback to local disk queue
       pass
   ```

3. **Health Checks** (Medium Priority)
   - Monitor S3 API latency (alert if p99 > 500ms)
   - Synthetic checks every 60s from multiple regions

### Immediate Actions (Incident Commander)
- [ ] Implement S3 cross-region replication (Week 1)
- [ ] Add circuit breakers to S3 upload paths (Week 2)
- [ ] Document failover runbook (Week 2)
- [ ] Test failover in staging (Week 3)
```

---

## 🔍 Tavily MCP Tools Reference

### `tavily-search`
Perform AI-powered web search:

```javascript
tavily_search({
  query: "FastAPI security vulnerabilities 2025",
  search_depth: "advanced",  // "basic" or "advanced"
  topic: "general",  // "general" or "news"
  max_results: 10,
  include_raw_content: false
})
```

**Parameters:**
- `query`: Search query (required)
- `search_depth`: "basic" (faster, $0.005) or "advanced" (deeper, $0.01)
- `topic`: "general" or "news" (news searches last 7 days by default)
- `max_results`: 5-20 results
- `include_raw_content`: Include full page HTML (verbose)
- `time_range`: "day", "week", "month", "year" (for general topic)
- `days`: Number of days for news searches (default: 3)

**Cost:**
- Basic search: $0.005 per search
- Advanced search: $0.01 per search
- Free tier: 1,000 searches/month

### `tavily-extract`
Extract content from specific URLs:

```javascript
tavily_extract({
  urls: [
    "https://github.com/tiangolo/fastapi/security/advisories/GHSA-xxxx",
    "https://nvd.nist.gov/vuln/detail/CVE-2024-XXXX"
  ],
  extract_depth: "basic"  // or "advanced"
})
```

---

## 💡 Best Practices

### 1. Use Time-Specific Queries

Tavily shines for recent data. Be explicit about timeframe:

**❌ Vague:**
```
Tavily: "React vulnerabilities"
// Returns results from 2019-2025
```

**✅ Specific:**
```
Tavily: "React vulnerabilities 2025"
// Returns only recent CVEs
```

### 2. Combine Topic Filters

For security/incident queries, use `topic="news"`:

```javascript
tavily_search({
  query: "AWS outage",
  topic: "news",  // ← Only recent news articles
  days: 7  // Last 7 days
})
```

### 3. Cache Expensive Searches

Tavily costs $0.005-0.01 per search. Cache results in session memory:

```
1. First consultation: Tavily search "GCP pricing"
2. Record in Sensei session memory
3. Second consultation (same session): Use cached pricing (10 min TTL)
```

### 4. Use `search_depth` Strategically

**Basic ($0.005):** Quick checks, known topics
```
"What's the latest Python version?" → basic
```

**Advanced ($0.01):** Research, rare topics, incident postmortems
```
"Why did the Jan 15 AWS outage happen?" → advanced
```

### 5. Pair with Context7 for Best Results

- **Context7:** Official documentation (API reference, guides)
- **Tavily:** Recent news, incidents, CVEs, pricing changes

**Example:**
```
User: "Review our React authentication"

1. Context7: React official docs (hooks, best practices)
2. Tavily: Recent React security advisories (CVEs)
3. Sensei: Security Sentinel synthesizes both
```

---

## 💸 Cost Management

### Understanding Tavily Pricing

| Plan | Monthly Cost | Searches | Cost per Search |
|------|--------------|----------|-----------------|
| Free | $0 | 1,000 | $0 |
| Pro | $29 | 5,000 | $0.0058 |
| Enterprise | Custom | Unlimited | $0.005-0.01 |

**Cost per Consultation:**
- Simple query: 1 search = $0.005-0.01
- Complex query: 3-5 searches = $0.015-0.05
- Full security review: 10 searches = $0.05-0.10

### Cost Optimization Strategies

**1. Rate Limiting**
```python
# Limit Tavily searches per session
MAX_TAVILY_SEARCHES_PER_SESSION = 10

if session.tavily_count >= MAX_TAVILY_SEARCHES_PER_SESSION:
    log.warning("Tavily quota exceeded for session. Using cached data.")
    # Fall back to Context7 or Claude training data
```

**2. Caching**
```python
# Cache Tavily results for 1 hour
TAVILY_CACHE_TTL = 3600  # seconds

cache_key = f"tavily:{query_hash}"
if cached_result := redis.get(cache_key):
    return cached_result

result = tavily_search(query)
redis.setex(cache_key, TAVILY_CACHE_TTL, result)
```

**3. Budget Alerts**
```python
# Track monthly spend
if monthly_tavily_cost > 50:  # $50 threshold
    notify_finops_team(f"Tavily spend: ${monthly_tavily_cost}")
```

### Cost Dashboard

Track Tavily usage with Sensei analytics:

```python
get_session_insights(session_id="my-project")

# Returns:
{
  "mcp_usage": {
    "tavily": {
      "total_searches": 127,
      "cost_estimate": "$1.27",  # Basic searches only
      "avg_searches_per_consultation": 2.1
    }
  }
}
```

---

## 🐛 Troubleshooting

### Issue: "TAVILY_API_KEY not set"

**Cause:** API key missing or not passed to MCP server

**Solution:**
1. Check env var: `echo $TAVILY_API_KEY`
2. If empty, set it:
   ```bash
   export TAVILY_API_KEY="tvly-xxxxxxxxxxxxx"
   ```
3. Verify MCP config includes `env` section (see Quick Start)

---

### Issue: "Rate limit exceeded"

**Cause:** Exceeded free tier (1,000 searches/month)

**Solution:**
1. Check usage: https://tavily.com/dashboard
2. Options:
   - Wait until next month (free tier resets)
   - Upgrade to Pro plan ($29/month, 5,000 searches)
   - Implement caching (see Cost Management)

---

### Issue: "No results found"

**Cause:** Query too specific or recent (topic not indexed yet)

**Solution:**
1. Broaden query:
   ```
   "FastAPI CVE-2024-12345" → "FastAPI security 2024"
   ```

2. Try `search_depth="advanced"`:
   ```javascript
   tavily_search({
     query: "obscure-library vulnerabilities",
     search_depth: "advanced"  // ← Deeper search
   })
   ```

3. Fallback to Context7 or Google:
   ```
   Tavily failed → Try Context7 for official docs
   ```

---

### Issue: "Stale data returned"

**Cause:** Tavily caches results for ~1 hour

**Solution:**
1. For breaking news, use `topic="news"` + `days=1`:
   ```javascript
   tavily_search({
     query: "AWS outage",
     topic: "news",
     days: 1  // Last 24 hours only
   })
   ```

2. Cross-reference with official sources:
   ```
   Tavily: Search AWS outage
   Then: tavily_extract("https://aws.amazon.com/status")
   ```

---

## 🎯 Success Metrics

Track Tavily ROI:

```python
get_session_insights(session_id="my-project")

# Good indicators:
{
  "mcp_usage": {
    "tavily": {
      "total_searches": 89,
      "cost_estimate": "$0.89",
      "value_added": "high"  # From user feedback
    }
  },
  "consultations_with_current_data": 67,  # 67% included recent data
  "avg_decision_confidence": 4.7/5  # User ratings
}
```

**Success Criteria:**
- ✅ Tavily used in 30%+ of consultations
- ✅ Cost per consultation <$0.10
- ✅ "Is this current?" follow-ups reduced by 50%

---

## 📖 Related Resources

- [Tavily API Docs](https://docs.tavily.com/)
- [Tavily MCP GitHub](https://github.com/tavily-ai/tavily-mcp)
- [Sensei MCP Integration Architecture](../MCP_INTEGRATION_ARCHITECTURE.md)
- [Context7 Integration Guide](./CONTEXT7.md) (for official docs)
- [Multi-MCP Workflow Examples](../MCP_INTEGRATION_EXAMPLES.md)

---

## 🤝 Contributing

Found a great Tavily + Sensei workflow? Share it!

1. Open issue: https://github.com/amarodeabreu/sensei-mcp/issues
2. Add your workflow to this doc via PR
3. Tag with `integration-example`

---

**Made with 🥋 by the Sensei MCP community**

*Current data. Better decisions.*
