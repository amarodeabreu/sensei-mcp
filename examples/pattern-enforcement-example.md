# Code Pattern Enforcement Demo
**Demo Execution Report**
*Generated: 2025-01-27T00:00:00Z*

---

## 📋 Overview

Demonstrates finding and fixing pattern violations with Serena + Sensei validation

**Workflow Template:** `code-pattern-enforcement`
**MCPs Involved:** 2 servers
**Execution Steps:** 6 steps

## ⚙️ Parameters
```json
{
  "user_query": "Ensure all API responses use consistent error format",
  "violation_pattern": "return.*\\{.*error.*\\}",
  "pattern_name": "RFC 7807 Problem Details"
}
```

## 🔄 Execution Plan
*Multi-MCP workflow coordination sequence:*

**Step 1:** Load session context from Sensei
- **MCP:** `sensei`
- **Action:** `get_session_context`
- **Params:** {"session_id": "{session_id}"}

**Step 2:** Search codebase patterns with Serena
- **MCP:** `serena`
- **Action:** `search_for_pattern`
- **Params:** {"substring_pattern": "return.*\\{.*error.*\\}", "restrict_search_to_code_files": true}

**Step 3:** Query Sensei for relevant expert personas
- **MCP:** `sensei`
- **Action:** `suggest_personas_for_query`
- **Params:** {"query": "Review pattern violations", "max_suggestions": 2}

**Step 4:** Locate code symbols with Serena
- **MCP:** `serena`
- **Action:** `find_symbol`
- **Params:** {"name_path_pattern": "{symbol_pattern}", "include_body": true}

**Step 5:** Refactor code with Serena
- **MCP:** `serena`
- **Action:** `replace_symbol_body`
- **Params:** {"name_path": "{symbol_name}", "relative_path": "{file_path}", "body": "{corrected_code}"}

**Step 6:** Record architectural decision in Sensei
- **MCP:** `sensei`
- **Action:** `record_decision`
- **Params:** {"category": "pattern", "description": "Enforced RFC 7807 Problem Details pattern"}

## 🔍 Example Findings
*Simulated output showing multi-MCP coordination:*

### 🟡 Finding 1: API Consistency
**Severity:** MEDIUM

**Finding:** 12 endpoints return custom error format instead of RFC 7807

**Source:** `serena:pattern-search`

**Recommendation:** Standardize on ProblemDetails class

### 🟡 Finding 2: API Design
**Severity:** MEDIUM

**Finding:** Inconsistent error responses violate API contract

**Source:** `sensei:api-platform-engineer`

**Recommendation:** Create ErrorResponse base class with RFC 7807 schema

### ℹ️ Finding 3: Standards
**Severity:** INFO

**Finding:** RFC 7807 Problem Details spec provides standard error format

**Source:** `context7:rfc-7807`

**Recommendation:** Include type, title, status, detail fields in all errors

## 🎯 Multi-MCP Coordination
1. Sensei selected relevant personas based on query context
1. Context7 provided up-to-date documentation and standards
1. Serena (if applicable) analyzed code structure and patterns
1. Tavily searched for recent vulnerabilities and best practices
1. Playwright (if applicable) performed live system inspection
1. Serena (if applicable) performed surgical code refactoring
1. Sensei synthesized findings into actionable recommendations

## 📄 Expected Output Sections
*A real execution would include:*

- Pattern Analysis
- Violations Found
- Refactoring Applied
- Consistency Check

---
## 💡 How to Run This Demo

```python
# Using Sensei MCP tools:
run_demo(demo_type="pattern-enforcement")

# Or with custom parameters:
run_demo(
    demo_type="pattern-enforcement",
    custom_params={
        "user_query": "your-value"
    }
)
```

**Note:** This is a demonstration output. Real execution would scan your actual API endpoints and enforce RFC 7807 pattern automatically.
