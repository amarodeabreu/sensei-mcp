# Architecture-Driven Refactoring Demo
**Demo Execution Report**
*Generated: 2025-01-27T00:00:00Z*

---

## 📋 Overview

Demonstrates refactoring code with Sensei architectural guidance + Serena surgical execution

**Workflow Template:** `architecture-refactoring`
**MCPs Involved:** 3 servers
**Execution Steps:** 7 steps

## ⚙️ Parameters
```json
{
  "user_query": "Refactor authentication to use dependency injection",
  "target_file": "src/auth/auth_handler.py",
  "pattern_type": "dependency injection"
}
```

## 🔄 Execution Plan
*Multi-MCP workflow coordination sequence:*

**Step 1:** Query Sensei for relevant expert personas
- **MCP:** `sensei`
- **Action:** `suggest_personas_for_query`
- **Params:** {"query": "Refactor authentication to use dependency injection", "max_suggestions": 2}

**Step 2:** Fetch documentation from Context7 *(optional)*
- **MCP:** `context7`
- **Action:** `get_library_docs`
- **Params:** {"topic": "dependency injection"}

**Step 3:** Analyze code structure with Serena
- **MCP:** `serena`
- **Action:** `get_symbols_overview`
- **Params:** {"relative_path": "src/auth/auth_handler.py"}

**Step 4:** Locate code symbols with Serena
- **MCP:** `serena`
- **Action:** `find_symbol`
- **Params:** {"name_path_pattern": "{symbol_pattern}", "include_body": true}

**Step 5:** Validate with Sensei standards
- **MCP:** `sensei`
- **Action:** `validate_against_standards`
- **Params:** {"code_snippet": "{current_code}"}

**Step 6:** Refactor code with Serena
- **MCP:** `serena`
- **Action:** `replace_symbol_body`
- **Params:** {"name_path": "{symbol_name}", "relative_path": "src/auth/auth_handler.py", "body": "{refactored_code}"}

**Step 7:** Check consistency with Sensei
- **MCP:** `sensei`
- **Action:** `check_consistency`
- **Params:** {"proposed_change": "Applied dependency injection pattern"}

## 🔍 Example Findings
*Simulated output showing multi-MCP coordination:*

### 🟡 Finding 1: Architecture
**Severity:** MEDIUM

**Finding:** Direct database access in auth handler violates separation of concerns

**Source:** `sensei:pragmatic-architect`

**Recommendation:** Inject UserRepository interface for testability

### ℹ️ Finding 2: Code Structure
**Severity:** INFO

**Finding:** AuthHandler has 8 dependencies instantiated in constructor

**Source:** `serena:code-analysis`

**Recommendation:** Apply constructor injection pattern

### ℹ️ Finding 3: Best Practices
**Severity:** INFO

**Finding:** SOLID principles documentation updated for 2025

**Source:** `context7:solid-principles`

**Recommendation:** Follow Interface Segregation Principle for repositories

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

- Refactoring Summary
- Architecture Analysis
- Code Changes
- Validation Results

---
## 💡 How to Run This Demo

```python
# Using Sensei MCP tools:
run_demo(demo_type="architecture-refactoring")

# Or with custom parameters:
run_demo(
    demo_type="architecture-refactoring",
    custom_params={
        "user_query": "your-value"
    }
)
```

**Note:** This is a demonstration output. Real execution would fetch live data from Context7, Tavily, and Playwright.
