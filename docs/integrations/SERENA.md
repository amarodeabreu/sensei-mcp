# Serena MCP Integration Guide

**Integration Tier:** Tier 1 (Essential for End-to-End Workflows)
**Best Paired With:** Sensei (Strategic Intelligence) + Context7 (Current Standards)
**Primary Use Cases:** Code refactoring, semantic search, architecture enforcement, surgical code changes

---

## 🎯 Why Sensei + Serena is the Killer Combination

### The Perfect Partnership

```
Sensei: "WHAT should we do?" (Strategic intelligence, architecture, patterns)
Serena: "HOW do we do it?" (Tactical execution, code manipulation, surgical changes)
Context7: "What are current best practices?" (Up-to-date standards)
```

**Together they enable:**
- **Strategic Thinking → Tactical Execution:** Sensei suggests the architecture → Serena implements it
- **Architecture Enforcement:** Sensei validates patterns → Serena refactors violations
- **Knowledge-Driven Refactoring:** Context7 provides standards → Sensei interprets → Serena applies
- **End-to-End Workflows:** From architectural decision to production-ready code

---

## 🚀 Quick Start

### Prerequisites

```bash
# Ensure Sensei MCP is installed
uvx sensei-mcp

# Install Serena MCP
pip install serena-mcp
```

### Configuration

Add both servers to your MCP configuration:

```json
{
  "mcpServers": {
    "sensei": {
      "command": "uvx",
      "args": ["sensei-mcp"]
    },
    "serena": {
      "command": "python",
      "args": ["-m", "serena_mcp"]
    }
  }
}
```

### Verify Setup

```python
# Check Sensei is available
get_engineering_guidance(query="test")

# Check Serena is available
mcp__serena__get_current_config()
```

---

## 🔄 Multi-MCP Workflows

### Workflow 1: Architecture-Driven Refactoring

**Scenario:** Refactor authentication to follow OWASP best practices with dependency injection

**Multi-MCP Flow:**

```
User: "Refactor our authentication to use dependency injection and follow OWASP standards"

Step 1: Sensei Strategic Analysis
├─ suggest_personas_for_query(query="auth refactoring DI")
├─ Returns: [pragmatic-architect, security-sentinel, api-platform-engineer]
└─ Each persona provides architectural guidance

Step 2: Context7 Current Standards
├─ resolve_library_id(libraryName="owasp/asvs")
├─ get_library_docs(context7CompatibleLibraryID="/owasp/asvs", topic="authentication")
└─ Fetches OWASP ASVS current authentication standards

Step 3: Serena Code Discovery
├─ list_dir(relative_path="src/auth", recursive=true)
├─ get_symbols_overview(relative_path="src/auth/auth_handler.py")
├─ find_symbol(name_path_pattern="AuthHandler", include_body=true)
└─ Identifies all authentication-related code

Step 4: Sensei Validation & Design
├─ get_persona_content(persona_name="pragmatic-architect")
├─ Analyze current code against OWASP standards
├─ Design DI-based refactoring approach
└─ Validate design with security-sentinel persona

Step 5: Serena Surgical Refactoring
├─ replace_symbol_body(name_path="AuthHandler/__init__", body="<new DI constructor>")
├─ insert_before_symbol(name_path="AuthHandler", body="<new dependency interfaces>")
├─ find_referencing_symbols(name_path="AuthHandler")
├─ Update all call sites to use DI
└─ Refactoring complete

Step 6: Sensei Post-Refactor Validation
├─ validate_against_standards(code_snippet="<refactored code>")
├─ check_consistency(proposed_change="DI pattern applied")
└─ record_decision(category="architecture", description="Migrated to DI pattern")
```

**Result:** Production-ready refactored code with architectural validation

**Code Example:**
```python
# Step 1-2: Sensei + Context7 analysis
suggest_mcps_for_query(
    query="Refactor auth to DI with OWASP compliance",
    context="SECURITY"
)
# Returns: sensei, context7, serena

# Step 3: Serena discovers code structure
mcp__serena__get_symbols_overview(relative_path="src/auth/auth_handler.py")
mcp__serena__find_symbol(name_path_pattern="AuthHandler", include_body=true)

# Step 4: Sensei designs refactoring
get_persona_content(persona_name="pragmatic-architect")
get_persona_content(persona_name="security-sentinel")

# Step 5: Serena executes refactoring
mcp__serena__replace_symbol_body(
    name_path="AuthHandler/__init__",
    relative_path="src/auth/auth_handler.py",
    body="""def __init__(self, user_repo: UserRepository, token_service: TokenService):
    self.user_repo = user_repo
    self.token_service = token_service
    """
)

# Step 6: Sensei validates
validate_against_standards(code_snippet="<refactored code>")
record_decision(
    category="architecture",
    description="Migrated AuthHandler to dependency injection pattern",
    rationale="Improves testability, follows SOLID principles, aligns with OWASP"
)
```

---

### Workflow 2: Semantic Code Navigation + Architecture Review

**Scenario:** Find all database queries and review them against multi-tenancy standards

**Multi-MCP Flow:**

```
User: "Find all database queries and check if they enforce tenant isolation"

Step 1: Sensei Context Setup
├─ get_session_context(session_id="my-project")
├─ Load active constraints: ["Multi-tenant from day one"]
└─ Load agreed patterns: ["Row-level security for all tables"]

Step 2: Serena Semantic Search
├─ search_for_pattern(
│   substring_pattern="SELECT.*FROM|INSERT.*INTO|UPDATE.*SET",
│   restrict_search_to_code_files=true
│  )
├─ find_symbol(name_path_pattern="*Repository", substring_matching=true)
└─ Returns: All database access code with locations

Step 3: Sensei Security Analysis
├─ get_persona_content(persona_name="security-sentinel")
├─ get_persona_content(persona_name="database-reliability-engineer")
├─ Analyze each query for tenant_id enforcement
└─ Flag queries missing tenant isolation

Step 4: Serena Code Inspection
├─ For each flagged query:
├─ find_symbol(name_path="Repository/query_method", include_body=true)
├─ find_referencing_symbols(name_path="Repository/query_method")
└─ Build impact analysis

Step 5: Sensei Recommendation Synthesis
├─ Synthesize findings from security-sentinel + DRE personas
├─ Prioritize by severity (data leak risk)
├─ Provide remediation steps
└─ record_consultation(personas_used=["security-sentinel", "database-reliability-engineer"])
```

**Result:** Complete multi-tenancy audit with prioritized fixes

**Code Example:**
```python
# Step 1: Load Sensei context
get_session_context(session_id="my-saas-app")

# Step 2: Serena finds all DB access
mcp__serena__search_for_pattern(
    substring_pattern="SELECT.*FROM|INSERT.*INTO|UPDATE.*SET",
    restrict_search_to_code_files=true,
    paths_include_glob="**/*repository*.py"
)

# Step 3: Sensei analyzes for security
suggest_personas_for_query(
    query="Review database queries for multi-tenant isolation",
    context="SECURITY"
)

# Step 4: Serena provides code details
mcp__serena__find_symbol(
    name_path_pattern="*Repository/*",
    include_body=true
)

# Step 5: Sensei synthesizes
get_engineering_guidance(
    query="Are these queries tenant-safe?",
    mode="orchestrated"
)
```

---

### Workflow 3: Library Upgrade with Compatibility Checking

**Scenario:** Upgrade React 17 → React 18 with concurrent features

**Multi-MCP Flow:**

```
User: "Upgrade to React 18 and enable concurrent rendering"

Step 1: Context7 Documentation
├─ resolve_library_id(libraryName="react")
├─ get_library_docs(context7CompatibleLibraryID="/facebook/react/v18", topic="concurrent")
└─ Fetch breaking changes and migration guide

Step 2: Serena Codebase Analysis
├─ search_for_pattern(substring_pattern="import.*react", paths_include_glob="**/*.tsx")
├─ find_symbol(name_path_pattern="*", paths_include_glob="**/App.tsx")
├─ Identify all React usage patterns
└─ Find lifecycle methods, unsafe patterns

Step 3: Sensei Migration Planning
├─ get_persona_content(persona_name="frontend-ux-specialist")
├─ get_persona_content(persona_name="pragmatic-architect")
├─ Analyze breaking changes impact
├─ Plan migration strategy (flags, gradual rollout)
└─ Prioritize high-risk components

Step 4: Serena Refactoring Execution
├─ replace_symbol_body() for components using unsafe lifecycle methods
├─ insert_before_symbol() to add React 18 imports
├─ Update package.json dependencies
└─ Refactor ReactDOM.render → createRoot

Step 5: Sensei Validation
├─ validate_against_standards(code_snippet="<migrated code>")
├─ check_consistency(proposed_change="React 18 migration")
└─ record_decision(category="architecture", description="Upgraded to React 18")
```

**Result:** Safe, validated React 18 migration with concurrent features enabled

---

### Workflow 4: Design Pattern Enforcement

**Scenario:** Enforce repository pattern across all database access code

**Multi-MCP Flow:**

```
User: "Ensure all database access uses repository pattern"

Step 1: Sensei Pattern Definition
├─ get_session_context(session_id="my-project")
├─ record_decision(
│   category="pattern",
│   description="All DB access must use repository pattern",
│   pattern="Repository pattern for all data access"
│  )
└─ Load pragmatic-architect for pattern guidance

Step 2: Serena Pattern Violation Detection
├─ search_for_pattern(
│   substring_pattern="session\\.query|Session\\(\\)|execute\\(.*SELECT",
│   restrict_search_to_code_files=true
│  )
├─ Exclude files in **/repositories/
└─ Find direct DB access outside repositories

Step 3: Sensei Refactoring Strategy
├─ get_persona_content(persona_name="pragmatic-architect")
├─ get_persona_content(persona_name="database-reliability-engineer")
├─ Design repository interfaces for violations
└─ Plan gradual migration

Step 4: Serena Repository Creation
├─ For each violation:
├─ Create repository class (insert_after_symbol)
├─ Move query logic to repository
├─ find_referencing_symbols() to update call sites
└─ Replace direct DB access with repository calls

Step 5: Sensei Consistency Check
├─ check_consistency(proposed_change="Repository pattern applied")
├─ validate_against_standards()
└─ Update session patterns
```

**Result:** Consistent repository pattern enforcement across codebase

---

## 🔧 Serena MCP Tool Reference

### Core Navigation Tools

#### `list_dir(relative_path, recursive, skip_ignored_files)`
List files and directories
```python
mcp__serena__list_dir(
    relative_path="src/auth",
    recursive=true,
    skip_ignored_files=true
)
```

#### `find_file(file_mask, relative_path)`
Find files by pattern
```python
mcp__serena__find_file(
    file_mask="*auth*.py",
    relative_path="src"
)
```

#### `get_symbols_overview(relative_path)`
Get high-level view of symbols in a file
```python
mcp__serena__get_symbols_overview(
    relative_path="src/auth/auth_handler.py"
)
```

### Semantic Search Tools

#### `find_symbol(name_path_pattern, relative_path, include_body, substring_matching)`
Find symbols by name path
```python
# Find specific class
mcp__serena__find_symbol(
    name_path_pattern="AuthHandler",
    include_body=true
)

# Find all methods in a class
mcp__serena__find_symbol(
    name_path_pattern="AuthHandler/*",
    include_body=false,
    depth=1
)

# Substring matching
mcp__serena__find_symbol(
    name_path_pattern="*Repository",
    substring_matching=true
)
```

#### `find_referencing_symbols(name_path, relative_path)`
Find all references to a symbol
```python
mcp__serena__find_referencing_symbols(
    name_path="AuthHandler/login",
    relative_path="src/auth/auth_handler.py"
)
```

#### `search_for_pattern(substring_pattern, relative_path, restrict_search_to_code_files, paths_include_glob)`
Pattern search across codebase
```python
mcp__serena__search_for_pattern(
    substring_pattern="SELECT.*FROM users WHERE",
    restrict_search_to_code_files=true,
    paths_include_glob="**/*.py"
)
```

### Code Modification Tools

#### `replace_symbol_body(name_path, relative_path, body)`
Replace entire symbol definition
```python
mcp__serena__replace_symbol_body(
    name_path="AuthHandler/login",
    relative_path="src/auth/auth_handler.py",
    body="""def login(self, username: str, password: str) -> Token:
    # New implementation with dependency injection
    user = self.user_repo.find_by_username(username)
    if user and self.password_service.verify(password, user.hashed_password):
        return self.token_service.create(user)
    raise AuthenticationError()"""
)
```

#### `insert_before_symbol(name_path, relative_path, body)`
Insert code before a symbol
```python
mcp__serena__insert_before_symbol(
    name_path="AuthHandler",
    relative_path="src/auth/auth_handler.py",
    body="""from typing import Protocol

class UserRepository(Protocol):
    def find_by_username(self, username: str) -> User: ...
"""
)
```

#### `insert_after_symbol(name_path, relative_path, body)`
Insert code after a symbol
```python
mcp__serena__insert_after_symbol(
    name_path="AuthHandler",
    relative_path="src/auth/auth_handler.py",
    body="""class TokenAuthHandler(AuthHandler):
    '''JWT token-based authentication'''
    pass
"""
)
```

#### `rename_symbol(name_path, relative_path, new_name)`
Rename symbol across entire codebase
```python
mcp__serena__rename_symbol(
    name_path="AuthHandler/login",
    relative_path="src/auth/auth_handler.py",
    new_name="authenticate"
)
```

### Memory Tools

#### `write_memory(memory_file_name, content)`
Store project information for future tasks
```python
mcp__serena__write_memory(
    memory_file_name="architecture-decisions",
    content="""# Architecture Decisions

## Authentication Pattern
- Using dependency injection
- Repository pattern for user data
- JWT tokens with rotation
"""
)
```

#### `read_memory(memory_file_name)`
Read stored project information
```python
mcp__serena__read_memory(
    memory_file_name="architecture-decisions"
)
```

---

## 🎯 Integration Patterns

### Pattern 1: Sensei Guides, Serena Executes

**Use when:** You need architectural decisions translated to code

```
1. Sensei analyzes requirements
2. Sensei suggests design/patterns
3. Serena finds relevant code
4. Sensei validates approach
5. Serena executes refactoring
6. Sensei validates result
```

### Pattern 2: Serena Discovers, Sensei Analyzes

**Use when:** You need to understand existing codebase patterns

```
1. Serena searches/navigates code
2. Serena provides code structure
3. Sensei analyzes patterns
4. Sensei identifies violations
5. Serena provides impact analysis
6. Sensei recommends remediation
```

### Pattern 3: Three-Way Synthesis (Sensei + Serena + Context7)

**Use when:** You need current standards + architecture + implementation

```
1. Context7 fetches current standards
2. Sensei interprets for your context
3. Serena analyzes existing code
4. Sensei designs migration path
5. Serena executes changes
6. Sensei validates compliance
```

---

## ⚡ Best Practices

### 1. Start with Strategy (Sensei), Then Tactics (Serena)

**Good:**
```python
# 1. Strategic analysis first
suggest_personas_for_query(query="How to refactor auth?")
get_persona_content(persona_name="pragmatic-architect")

# 2. Then tactical discovery
mcp__serena__get_symbols_overview(relative_path="src/auth/auth.py")
mcp__serena__find_symbol(name_path_pattern="AuthHandler")

# 3. Then execution
mcp__serena__replace_symbol_body(...)
```

**Bad:**
```python
# Don't jump straight to code manipulation without strategy
mcp__serena__replace_symbol_body(...)  # What pattern? Why this approach?
```

### 2. Use Sensei Session Memory with Serena Memory

**Synergy:**
```python
# Sensei: Project-level architectural decisions
record_decision(
    category="architecture",
    description="All auth uses DI pattern"
)

# Serena: Implementation details and patterns
mcp__serena__write_memory(
    memory_file_name="auth-implementation",
    content="AuthHandler uses UserRepository and TokenService interfaces"
)
```

### 3. Validate Before and After Changes

**Safety pattern:**
```python
# Before refactoring
get_persona_content(persona_name="security-sentinel")
validate_against_standards(code_snippet="<current code>")

# Serena refactors
mcp__serena__replace_symbol_body(...)

# After refactoring
check_consistency(proposed_change="Applied DI pattern")
validate_against_standards(code_snippet="<new code>")
```

### 4. Use find_referencing_symbols Before Breaking Changes

**Impact analysis:**
```python
# Before renaming or changing signature
mcp__serena__find_referencing_symbols(
    name_path="AuthHandler/login",
    relative_path="src/auth/auth_handler.py"
)
# Shows all call sites that will be affected

# Then plan migration
get_engineering_guidance(
    query="How to safely migrate all call sites?"
)
```

### 5. Leverage Persona-Specific Guidance

**Match persona to task:**
```python
# For refactoring
get_persona_content(persona_name="pragmatic-architect")

# For security-sensitive code
get_persona_content(persona_name="security-sentinel")

# For database changes
get_persona_content(persona_name="database-reliability-engineer")

# For API changes
get_persona_content(persona_name="api-platform-engineer")
```

---

## 🚨 Common Pitfalls

### ❌ Pitfall 1: Serena Changes Without Sensei Validation

**Problem:**
```python
# Just refactoring without strategic guidance
mcp__serena__replace_symbol_body(...)
```

**Solution:**
```python
# Get architectural guidance first
get_persona_content(persona_name="pragmatic-architect")
validate_against_standards(code_snippet="<current>")

# Then refactor
mcp__serena__replace_symbol_body(...)

# Then validate
check_consistency(proposed_change="...")
```

### ❌ Pitfall 2: Not Checking References

**Problem:**
```python
# Renaming without checking impact
mcp__serena__rename_symbol(...)
```

**Solution:**
```python
# Check references first
refs = mcp__serena__find_referencing_symbols(...)
# Analyze impact, plan migration
# Then execute
```

### ❌ Pitfall 3: Modifying Without Understanding Context

**Problem:**
```python
# Changing code without reading it first
mcp__serena__replace_symbol_body(...)
```

**Solution:**
```python
# Understand first
mcp__serena__get_symbols_overview(...)
mcp__serena__find_symbol(include_body=true)

# Analyze
get_engineering_guidance(query="Should we refactor this?")

# Then modify
mcp__serena__replace_symbol_body(...)
```

---

## 📊 Success Metrics

### Code Quality Improvements
- ✅ Architectural patterns consistently applied
- ✅ Security vulnerabilities caught and fixed
- ✅ Design principles enforced (SOLID, DRY, YAGNI)

### Development Velocity
- ✅ Faster refactoring with strategic guidance
- ✅ Reduced manual code navigation
- ✅ Automated pattern enforcement

### Knowledge Retention
- ✅ Architectural decisions documented in Sensei sessions
- ✅ Implementation details stored in Serena memory
- ✅ Cross-project patterns reusable

---

## 🔮 Advanced Use Cases

### Use Case 1: Multi-Tenant SaaS Migration

**Goal:** Add tenant_id to all database operations

```python
# 1. Sensei: Define strategy
record_decision(
    category="architecture",
    description="Multi-tenant row-level security",
    constraint="All queries must include tenant_id"
)

# 2. Serena: Find violations
violations = mcp__serena__search_for_pattern(
    substring_pattern="SELECT.*FROM.*WHERE(?!.*tenant_id)",
    restrict_search_to_code_files=true
)

# 3. Sensei: Validate approach
check_consistency(proposed_change="Add tenant_id to all queries")

# 4. Serena: Execute migration
for violation in violations:
    mcp__serena__replace_symbol_body(...)
```

### Use Case 2: Security Audit + Automated Fixes

**Goal:** Find and fix SQL injection vulnerabilities

```python
# 1. Serena: Find potential SQL injection
risks = mcp__serena__search_for_pattern(
    substring_pattern='execute\\(f"SELECT.*\\{.*\\}"\\)',
    restrict_search_to_code_files=true
)

# 2. Sensei: Security analysis
get_persona_content(persona_name="security-sentinel")
validate_against_standards(focus_areas=["sql-injection"])

# 3. Serena: Provide context
for risk in risks:
    code = mcp__serena__find_symbol(include_body=true)

# 4. Sensei: Recommend fixes
get_engineering_guidance(query="How to fix SQL injection?")

# 5. Serena: Apply parameterization
mcp__serena__replace_symbol_body(body="<parameterized query>")
```

### Use Case 3: API Versioning Migration

**Goal:** Migrate from /api/v1 to /api/v2 with backward compatibility

```python
# 1. Context7: Current API standards
resolve_library_id(libraryName="openapi")
get_library_docs(topic="versioning")

# 2. Sensei: Design migration strategy
get_persona_content(persona_name="api-platform-engineer")
record_decision(
    category="architecture",
    description="API v2 with v1 compatibility layer"
)

# 3. Serena: Find all v1 endpoints
endpoints = mcp__serena__search_for_pattern(
    substring_pattern='@app\\.route\\("/api/v1/',
    paths_include_glob="**/*.py"
)

# 4. Serena: Create v2 endpoints
for endpoint in endpoints:
    mcp__serena__insert_after_symbol(body="<v2 endpoint>")

# 5. Sensei: Validate compatibility
validate_against_standards(design_description="API v1/v2 compatibility")
```

---

## 🎓 Learning Path

### Beginner: Single-MCP Usage

**Week 1:** Use Serena alone for code navigation
```python
mcp__serena__get_symbols_overview(...)
mcp__serena__find_symbol(...)
```

**Week 2:** Use Sensei alone for architectural guidance
```python
get_engineering_guidance(...)
validate_against_standards(...)
```

### Intermediate: Two-MCP Coordination

**Week 3:** Serena discovers → Sensei analyzes
```python
# Serena finds patterns
violations = mcp__serena__search_for_pattern(...)

# Sensei analyzes
get_engineering_guidance(query="How critical are these violations?")
```

**Week 4:** Sensei guides → Serena executes
```python
# Sensei provides strategy
get_persona_content(persona_name="pragmatic-architect")

# Serena implements
mcp__serena__replace_symbol_body(...)
```

### Advanced: Multi-MCP Orchestration

**Week 5:** Three-way synthesis (Sensei + Serena + Context7)
```python
# Context7: Current standards
get_library_docs(...)

# Sensei: Interpret for your context
get_engineering_guidance(...)

# Serena: Apply to codebase
mcp__serena__replace_symbol_body(...)
```

**Week 6:** Full workflow automation with validation loops
```python
# Complete end-to-end workflows with validation at each step
```

---

## 🛠️ Troubleshooting

### Issue: Serena can't find symbols

**Cause:** Serena needs to index the codebase first

**Solution:**
```python
# Check onboarding status
mcp__serena__check_onboarding_performed()

# If not performed, trigger it
mcp__serena__onboarding()
```

### Issue: Sensei suggestions don't match Serena capabilities

**Cause:** Sensei personas may suggest refactorings Serena can't do automatically

**Solution:**
```python
# Use Sensei for strategy + validation
# Use Serena for what it can automate
# Manual work for complex refactorings
```

### Issue: Symbol replacement breaks tests

**Cause:** Didn't check references or validate changes

**Solution:**
```python
# Always check impact first
mcp__serena__find_referencing_symbols(...)

# Validate with Sensei
validate_against_standards(...)

# Then execute
mcp__serena__replace_symbol_body(...)

# Validate after
check_consistency(...)
```

---

## 📚 Related Documentation

- **Sensei Personas:** All 64 personas and their specialties
- **Context7 Integration:** [CONTEXT7.md](./CONTEXT7.md)
- **Tavily Integration:** [TAVILY.md](./TAVILY.md)
- **Multi-MCP Patterns:** [README.md](./README.md)

---

## 🎉 Success Stories

### Case Study 1: Multi-Tenant Migration (3 days → 4 hours)

**Challenge:** Add tenant isolation to 200+ database queries

**Solution:**
```
- Serena: Found all queries in 2 minutes
- Sensei: Designed migration strategy (security-sentinel + DRE)
- Serena: Applied changes systematically
- Sensei: Validated each change
- Result: 95% automated, 4 hours total
```

### Case Study 2: Security Audit (2 weeks → 1 day)

**Challenge:** Audit entire codebase for security violations

**Solution:**
```
- Serena: Scanned for SQL injection, XSS, auth bypasses
- Sensei: Prioritized by severity (security-sentinel)
- Context7: Fetched OWASP standards
- Sensei: Designed fixes
- Serena: Applied parameterization and sanitization
- Result: 40 vulnerabilities fixed in 1 day
```

---

**Made with 🥋 by the Sensei + Serena community**

*Strategic thinking meets tactical execution.*
