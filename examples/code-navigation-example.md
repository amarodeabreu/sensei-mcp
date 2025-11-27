# Semantic Code Navigation Demo
**Demo Execution Report**
*Generated: 2025-01-27T00:00:00Z*

---

## 📋 Overview

Demonstrates code discovery with Serena + architectural analysis with Sensei

**Workflow Template:** `code-pattern-enforcement`
**MCPs Involved:** 2 servers
**Execution Steps:** 6 steps

## ⚙️ Parameters
```json
{
  "user_query": "Find all database queries and check tenant isolation",
  "violation_pattern": "SELECT.*FROM|INSERT.*INTO",
  "session_id": "multi-tenant-audit"
}
```

## 🔄 Execution Plan
*Multi-MCP workflow coordination sequence:*

**Step 1:** Load session context from Sensei
- **MCP:** `sensei`
- **Action:** `get_session_context`
- **Params:** {"session_id": "multi-tenant-audit"}

**Step 2:** Search codebase patterns with Serena
- **MCP:** `serena`
- **Action:** `search_for_pattern`
- **Params:** {"substring_pattern": "SELECT.*FROM|INSERT.*INTO", "restrict_search_to_code_files": true}

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
- **Params:** {"category": "pattern", "description": "Enforced {pattern_name} pattern"}

## 🔍 Example Findings
*Simulated output showing multi-MCP coordination:*

### 🔴 Finding 1: Multi-Tenancy
**Severity:** HIGH

**Finding:** Query in UserRepository.find_by_email missing tenant_id filter

**Source:** `serena:semantic-search`

**Recommendation:** Add WHERE tenant_id = ? to all queries

### 🔴 Finding 2: Security
**Severity:** HIGH

**Finding:** 15 database queries missing tenant isolation

**Source:** `sensei:security-sentinel`

**Recommendation:** Enforce row-level security pattern across all repositories

### 🟡 Finding 3: Impact Analysis
**Severity:** MEDIUM

**Finding:** UserRepository referenced in 23 locations

**Source:** `serena:find-references`

**Recommendation:** Update all call sites to pass tenant context

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

- Discovery Summary
- Pattern Violations
- Security Analysis
- Remediation Plan

---
## 💡 How to Run This Demo

```python
# Using Sensei MCP tools:
run_demo(demo_type="code-navigation")

# Or with custom parameters:
run_demo(
    demo_type="code-navigation",
    custom_params={
        "user_query": "your-value"
    }
)
```

**Note:** This is a demonstration output. Real execution would use Serena to scan your actual codebase and Sensei to provide multi-tenant security analysis.
