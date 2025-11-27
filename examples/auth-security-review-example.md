# Authentication Security Review Demo
**Demo Execution Report**
*Generated: 2025-01-27T00:00:00Z*

---

## 📋 Overview

Demonstrates comprehensive auth security review using Sensei + Context7 + Tavily + Playwright

**Workflow Template:** `auth-security-review`
**MCPs Involved:** 4 servers
**Execution Steps:** 5 steps

## ⚙️ Parameters
```json
{
  "user_query": "Review authentication implementation for security vulnerabilities",
  "app_url": "https://example.com/login",
  "framework": "FastAPI"
}
```

## 🔄 Execution Plan
*Multi-MCP workflow coordination sequence:*

**Step 1:** Query Sensei for relevant expert personas
- **MCP:** `sensei`
- **Action:** `suggest_personas_for_query`
- **Params:** {"query": "Review authentication implementation for security vulnerabilities", "max_suggestions": 3}

**Step 2:** Fetch documentation from Context7
- **MCP:** `context7`
- **Action:** `get_library_docs`
- **Params:** {"libraries": ["owasp/asvs", "oauth", "framework-specific-auth"]}

**Step 3:** Search recent data and vulnerabilities via Tavily
- **MCP:** `tavily`
- **Action:** `tavily_search`
- **Params:** {"queries": ["FastAPI vulnerabilities 2025", "OAuth security 2025"]}

**Step 4:** Navigate to target URL with Playwright *(optional)*
- **MCP:** `playwright`
- **Action:** `browser_navigate`
- **Params:** {"url": "https://example.com/login"}

**Step 5:** Analyze network requests with Playwright *(optional)*
- **MCP:** `playwright`
- **Action:** `browser_network_requests`

## 🔍 Example Findings
*Simulated output showing multi-MCP coordination:*

### 🔴 Finding 1: Authentication
**Severity:** HIGH

**Finding:** No rate limiting on login endpoint

**Source:** `sensei:security-sentinel`

**Recommendation:** Implement exponential backoff rate limiting

### 🟡 Finding 2: Session Management
**Severity:** MEDIUM

**Finding:** Session tokens not rotated after privilege elevation

**Source:** `context7:owasp-asvs`

**Recommendation:** Rotate session IDs on authentication state changes

### ℹ️ Finding 3: Recent Vulnerabilities
**Severity:** INFO

**Finding:** FastAPI 0.104.0 has known OAuth vulnerability (CVE-2024-xxxx)

**Source:** `tavily:cve-search`

**Recommendation:** Upgrade to FastAPI 0.109.0+

## 🎯 Multi-MCP Coordination
1. Sensei selected relevant personas based on query context
1. Context7 provided up-to-date documentation and standards
1. Tavily searched for recent vulnerabilities and best practices
1. Playwright (if applicable) performed live system inspection
1. Sensei synthesized findings into actionable recommendations

## 📄 Expected Output Sections
*A real execution would include:*

- Executive Summary
- MCP Coordination
- Security Findings
- Persona Analysis
- Recommendations
- Next Steps

---
## 💡 How to Run This Demo

```python
# Using Sensei MCP tools:
run_demo(demo_type="auth-security-review")

# Or with custom parameters:
run_demo(
    demo_type="auth-security-review",
    custom_params={
        "user_query": "your-value"
    }
)
```

**Note:** This is a demonstration output. Real execution would fetch live data from Context7, Tavily, and Playwright.
