# Context7 MCP Integration Guide

**Version:** 0.8.0
**MCP Server:** [@upstash/context7-mcp](https://github.com/upstash/context7)
**Purpose:** Fetch up-to-date documentation for libraries and frameworks

---

## 🎯 What is Context7?

Context7 provides real-time access to library documentation, ensuring your Sensei personas always reference **current** best practices, not just Claude's training data.

### Why This Matters

When Security Sentinel reviews your authentication code, it can reference:
- **OWASP ASVS 2025** (not 2023)
- **OAuth 2.0 Security BCP** (latest RFC)
- **Your specific framework's current version** (FastAPI 0.110, React 19, etc.)

---

## 🚀 Quick Start (5 Minutes)

### 1. Install Context7 MCP

Context7 is npm-based and works with any MCP client:

```bash
# Test if npx works
npx -y @upstash/context7-mcp --version

# Should see Context7 MCP server start
```

### 2. Configure MCP Client

**Claude Code:**
```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp
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
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
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
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

### 3. Test Integration

Restart your MCP client and try:

```
You: "Explain React 19's new hooks with latest documentation"

Expected workflow:
1. Sensei suggests: [frontend-ux-specialist]
2. Context7 fetches: /facebook/react (React 19 docs)
3. Claude synthesizes: Frontend expert perspective + current React 19 docs
```

---

## 📚 How to Use Context7 with Sensei

### Pattern: Library Recommendation + Current Docs

**User Query:** "What's the best Python library for JWT handling?"

**Sensei + Context7 Flow:**
1. **Sensei suggests:** `[api-platform-engineer, security-sentinel]`
2. **Claude asks Context7:** Fetch docs for `/python-jose/python-jose` and `/jpadilla/pyjwt`
3. **Synthesis:**
   - API Platform Engineer: Design patterns for JWT in REST APIs
   - Security Sentinel: Security considerations (secret rotation, algorithm choice)
   - **Context7 docs:** Current API reference, best practices from 2025

**Output:**
```markdown
## JWT Library Recommendation

### Recommended: PyJWT (jpadilla/pyjwt)

**Rationale (Security Sentinel):**
- More actively maintained (last commit: 2 weeks ago)
- Better algorithm support (RS256, ES256, PS256)
- Strong security defaults

**Current Best Practices (Context7 docs):**
```python
import jwt
from datetime import datetime, timedelta

# From PyJWT 2.8+ docs
payload = {
    'user_id': 123,
    'exp': datetime.utcnow() + timedelta(hours=1),
    'iat': datetime.utcnow(),
    'iss': 'your-app.com'
}

token = jwt.encode(
    payload,
    SECRET_KEY,
    algorithm='RS256'  # Use RSA, not HS256
)
```

**Security Considerations:**
- Rotate keys monthly (Security Sentinel + OWASP ASVS 2.9.3)
- Use RS256 for production (Context7 current docs)
- Validate all claims: exp, iat, iss, aud
```

---

## 🔥 Example Workflows

### Workflow 1: Security Review with Current Standards

**Scenario:** Review authentication implementation against latest OWASP standards

```
You: "Review our FastAPI authentication for security issues"

Sensei + Context7 workflow:
1. suggest_personas_for_query("Review FastAPI authentication for security")
   → Returns: ["security-sentinel", "api-platform-engineer", "privacy-engineer"]

2. Context7 fetches:
   - /owasp/asvs (Application Security Verification Standard)
   - /tiangolo/fastapi (FastAPI current docs)
   - /python-jose/python-jose (JWT library docs)

3. Claude synthesizes with 3 personas + current docs:
   - Security Sentinel: OWASP ASVS compliance check
   - API Platform Engineer: REST API security patterns
   - Privacy Engineer: GDPR Article 32 requirements
   - All using CURRENT documentation (not 2023 training data)
```

**Sample Output:**
```markdown
## Security Review: FastAPI Authentication

### 🔴 Critical Issues

1. **JWT Secret Rotation** (Security Sentinel + OWASP ASVS 2.9.3)
   - Current: Single static secret in env var
   - Risk: If compromised, all tokens valid forever
   - Fix: Implement key versioning

   **From OWASP ASVS 2025 (Context7):**
   > "Cryptographic keys must be rotated at least annually and immediately
   > upon suspected compromise." (Section 6.2.1)

2. **Password Hashing** (Security Sentinel)
   - Current: bcrypt (cost=10)
   - Recommended: Argon2id (OWASP winner)

   **From FastAPI docs (Context7):**
   ```python
   from passlib.context import CryptContext

   pwd_context = CryptContext(
       schemes=["argon2"],
       deprecated="auto"
   )
   ```
```

---

### Workflow 2: Framework Upgrade Decision

**Scenario:** Should we upgrade to React 19?

```
You: "We're on React 18. Should we upgrade to React 19? What are the breaking changes?"

Sensei + Context7 workflow:
1. Sensei suggests: [frontend-ux-specialist, pragmatic-architect]
2. Context7 fetches: /facebook/react (React 19 docs, migration guide)
3. Claude synthesizes:
   - Frontend UX Specialist: New hooks impact on UX patterns
   - Pragmatic Architect: Migration effort, breaking changes, timeline
   - React 19 official docs: Actions, useOptimistic, useFormStatus
```

**Sample Output:**
```markdown
## React 19 Upgrade Analysis

### TL;DR
✅ **Recommend upgrade** in Q2 (3-4 week effort)

### New Features (from React 19 docs via Context7)
1. **Actions**: Async transitions built-in
2. **useOptimistic**: Optimistic UI updates
3. **useFormStatus**: Form submission state

### Breaking Changes
- `ReactDOM.render` removed (use `createRoot`)
- Suspense behavior changed (SSR impact)
- Deprecated lifecycle methods removed

### Migration Plan (Pragmatic Architect)
**Week 1-2:** Update tooling (Webpack/Vite, TypeScript, ESLint)
**Week 3:** Convert ReactDOM.render → createRoot (automated codemod)
**Week 4:** Manual fixes for Suspense SSR changes
**Week 5:** Testing & QA

### UX Impact (Frontend UX Specialist)
- **Positive:** Actions reduce boilerplate for forms by 40%
- **Risk:** Suspense changes may cause loading state flicker
- **Mitigation:** Test critical user flows (checkout, signup)
```

---

### Workflow 3: Library Comparison

**Scenario:** Choose between two libraries

```
You: "Should we use Pydantic v2 or msgspec for API validation?"

Sensei + Context7 workflow:
1. Sensei suggests: [api-platform-engineer, performance-engineer]
2. Context7 fetches:
   - /pydantic/pydantic (Pydantic v2 docs)
   - /jcrist/msgspec (msgspec docs)
3. Claude synthesizes:
   - API Platform Engineer: API design patterns, validation clarity
   - Performance Engineer: Benchmarks, memory usage
   - Current docs for both libraries
```

**Sample Output:**
```markdown
## Library Comparison: Pydantic v2 vs msgspec

### Benchmark (Performance Engineer + Context7 docs)
| Metric | Pydantic v2 | msgspec |
|--------|-------------|---------|
| Parse speed | 1.0x | **3.2x faster** |
| Serialize | 1.0x | **5.1x faster** |
| Memory | 1.0x | **40% less** |

### Developer Experience (API Platform Engineer)
**Pydantic v2:**
- ✅ Rich ecosystem (FastAPI, SQLModel)
- ✅ Excellent error messages
- ✅ 10M+ downloads/month

**msgspec:**
- ⚠️ Smaller ecosystem
- ✅ Simpler API
- ⚠️ 100K downloads/month

### Recommendation
- **Existing FastAPI projects:** Stick with Pydantic v2 (ecosystem lock-in)
- **New high-throughput services:** msgspec (3-5x speedup matters at scale)
- **Hybrid approach:** Use msgspec for data layer, Pydantic for API layer
```

---

## 🔍 Context7 MCP Tools Reference

### `resolve-library-id`
Find the Context7-compatible library ID:

```
Input: "fastapi"
Output: {
  "id": "/tiangolo/fastapi",
  "name": "FastAPI",
  "description": "Modern Python web framework",
  "versions": ["0.110.0", "0.109.0", ...]
}
```

### `get-library-docs`
Fetch documentation for a library:

```
Input: {
  "context7CompatibleLibraryID": "/tiangolo/fastapi",
  "topic": "authentication",
  "mode": "code"
}

Output: {
  "docs": "...", // Markdown documentation
  "codeSnippets": [...],
  "apiReference": [...]
}
```

**Parameters:**
- `context7CompatibleLibraryID`: Library ID from `resolve-library-id`
- `topic` (optional): Narrow down to specific topic (e.g., "authentication", "database")
- `mode`: "code" for API reference, "info" for conceptual guides
- `page`: Pagination (1-10)

---

## 💡 Best Practices

### 1. Let Sensei Guide Library Selection

**❌ Don't:**
```
You: "Fetch React docs"
```

**✅ Do:**
```
You: "I need to build a form with complex validation. What React library should I use?"

// Sensei will suggest: [frontend-ux-specialist]
// Specialist will recommend: React Hook Form or Formik
// Then Context7 fetches docs for recommended library
```

### 2. Use `topic` Parameter to Narrow Results

Context7 returns a lot of docs. Use `topic` to focus:

```
get-library-docs(
  context7CompatibleLibraryID="/tiangolo/fastapi",
  topic="authentication",  // ← Narrows to auth-related docs only
  mode="code"
)
```

### 3. Combine with Tavily for "Is This Maintained?"

Context7 shows docs, but not activity. Combine with Tavily:

```
1. Context7: Fetch library docs
2. Tavily: Search "python-jose github activity 2025"
3. Sensei synthesizes: Docs + maintenance status
```

### 4. Cache Context7 Results in Session Memory

If you're iterating on the same library, avoid redundant fetches:

```
# First consultation
1. Fetch FastAPI docs via Context7
2. Sensei records in session memory

# Second consultation (same session)
1. Check session memory for FastAPI docs (cache hit)
2. Skip Context7 call → faster response
```

---

## 🐛 Troubleshooting

### Issue: "Context7 MCP server not found"

**Cause:** MCP server not installed or config error

**Solution:**
1. Test if Context7 works standalone:
   ```bash
   npx -y @upstash/context7-mcp
   ```

2. Check MCP config file syntax (JSON must be valid)

3. Restart MCP client after config changes

---

### Issue: "Library not found in Context7"

**Cause:** Library not indexed by Context7

**Fallback Strategy:**
1. Try alternate names:
   - `python-jose` → `/python-jose/python-jose`
   - `pyjwt` → `/jpadilla/pyjwt`

2. If library truly not in Context7:
   - Use Tavily to search official docs
   - Ask Claude to reference training data (mark as "may be outdated")

**Example:**
```markdown
## Library Recommendation

Note: XYZ library not available in Context7. Analysis based on:
- Claude training data (Jan 2025 cutoff)
- Tavily search for recent changes
```

---

### Issue: "Context7 docs are too long / truncated"

**Cause:** `get-library-docs` returns paginated results

**Solution:**
1. Use `topic` parameter to narrow scope
2. Use `page=2`, `page=3` for more results
3. Focus on most relevant sections first

**Example:**
```
# Instead of fetching ALL React docs:
get-library-docs(
  context7CompatibleLibraryID="/facebook/react",
  topic="hooks"  // ← Just hooks documentation
)
```

---

### Issue: "Context7 returns old version docs"

**Cause:** Context7 may cache older versions

**Solution:**
1. Specify version in library ID:
   ```
   /facebook/react/v19.0.0  // ← Specific version
   ```

2. Use Tavily to verify latest version:
   ```
   Tavily: "react latest version 2025"
   ```

3. Cross-reference with official changelog

---

## 🎯 Success Metrics

Track Context7 effectiveness:

```python
# Using Sensei's analytics
get_session_insights(session_id="my-project")

# Look for:
- "mcp_usage": {
    "context7": 45,  # Context7 used in 45 consultations
    "avg_quality_score": 4.6/5  # User feedback
  }
```

**Good indicators:**
- ✅ Context7 used in 60%+ of consultations
- ✅ Quality score >4.0/5
- ✅ Reduced "is this current?" follow-up questions

---

## 📖 Related Resources

- [Context7 GitHub](https://github.com/upstash/context7)
- [Sensei MCP Integration Architecture](../MCP_INTEGRATION_ARCHITECTURE.md)
- [Tavily Integration Guide](./TAVILY.md) (for recent news, CVEs)
- [Multi-MCP Workflow Examples](../MCP_INTEGRATION_EXAMPLES.md)

---

## 🤝 Contributing

Found a great Context7 + Sensei workflow? Share it!

1. Open issue: https://github.com/amarodeabreu/sensei-mcp/issues
2. Add your workflow to this doc via PR
3. Tag with `integration-example`

---

**Made with 🥋 by the Sensei MCP community**

*Always current. Never outdated.*
