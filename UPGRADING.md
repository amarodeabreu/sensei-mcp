# Upgrading Sensei MCP

Guide for upgrading between versions of Sensei MCP.

---

## Quick Upgrade (TL;DR)

```bash
# For uvx installations (most common)
uvx --force sensei-mcp@latest

# For pip installations
pip install --upgrade sensei-mcp

# Then restart your MCP client (Claude Desktop, Cursor, etc.)
```

---

## Upgrading to v0.5.0 from v0.4.x

### What's New

v0.5.0 introduces **4 major features** and the **Database Architect persona** (23rd expert):

1. **Interactive Persona Discovery** 🔍
   - Enhanced `list_available_skills()` with 3 format modes (standard, detailed, quick)
   - CLI demo mode (`sensei-mcp --demo`) with 5 real-world scenarios
   - Intelligent context hints when <2 personas selected

2. **CI/CD Integration Pack** 🔧
   - GitHub Actions workflows for PR reviews and architecture checks
   - Pre-commit hooks (consistency, security, cost analysis)
   - GitLab CI pipeline with 3-stage validation
   - Enhanced `analyze_changes()` with persona suggestions

3. **Session Merge & Team Sync** 🤝
   - `merge_sessions()` tool with 4 conflict resolution strategies
   - `compare_sessions()` for side-by-side analysis
   - Attribution tracking for all decisions

4. **Database Architect Persona** 🗄️
   - 23rd specialized expert joins the team
   - Expertise: schema design, query optimization, migrations, scalability

### Breaking Changes

**✅ NONE** - v0.5.0 is fully backwards compatible with v0.4.x

All existing tools, workflows, and session files continue to work exactly as before.

### Upgrade Steps

Same as previous versions (see Quick Upgrade above).

### Using New v0.5.0 Features

**Try the CLI demo:**
```bash
sensei-mcp --demo
```

**Enhanced persona discovery:**
```python
# Detailed format with examples and metadata
list_available_skills(format="detailed")

# Quick format (names only)
list_available_skills(format="quick")
```

**Merge developer sessions:**
```python
merge_sessions(
  session_ids=["alice-frontend", "bob-backend"],
  target_session_id="sprint-23",
  conflict_strategy="latest"  # or "oldest", "all", "manual"
)

# Compare before merging
compare_sessions(
  session_a_id="alice-session",
  session_b_id="bob-session"
)
```

**Consult Database Architect:**
```python
consult_skill(
  skill_name="database-architect",
  query="Design a database schema for a multi-tenant SaaS application"
)

# Or auto-selected via orchestrator
get_engineering_guidance(
  query="How should I index this table for optimal read performance?"
)
```

**CI/CD Integration:**
- See `integrations/INTEGRATION_GUIDE.md` for GitHub Actions, GitLab CI, and pre-commit hook setup
- Templates available in `integrations/` directory

### Session Compatibility

**v0.4.x sessions work in v0.5.0:**
- All session data preserved
- No migration needed
- New merge functionality available immediately

---

## Upgrading to v0.3.0 from v0.2.x

### What's New

v0.3.0 introduces the **Multi-Persona Orchestrator** with 22 specialized AI skills:
- New primary tool: `get_engineering_guidance()` with multi-persona collaboration
- 3 new MCP tools total (get_engineering_guidance, consult_skill, list_available_skills)
- All v0.2.x tools still work (full backwards compatibility)
- Session memory now tracks persona consultations

### Breaking Changes

**✅ NONE** - v0.3.0 is fully backwards compatible with v0.2.x

All existing tools, workflows, and session files continue to work exactly as before.

### Upgrade Steps

#### For uvx Users (Recommended - Most Common)

**Claude Code / CLI:**
```bash
# Force update to latest version
uvx --force sensei-mcp@latest

# Or specify exact version
uvx --force sensei-mcp@0.3.0
```

**Claude Desktop / Cursor / Windsurf / Cline / Roo Code:**
```bash
# Update via uvx
uvx --force sensei-mcp@latest

# Then restart your editor/app
# No config changes needed - same command in config file
```

**Verify version:**
```bash
uvx sensei-mcp --version
# Should show: sensei-mcp 0.3.0
```

#### For pip Users

```bash
# Upgrade to latest
pip install --upgrade sensei-mcp

# Or specify exact version
pip install --upgrade sensei-mcp==0.3.0

# Verify
python -m sensei_mcp --version
```

#### For Editable Installs (Development)

```bash
cd /path/to/sensei-mcp
git pull origin main
pip install -e .
```

### After Upgrade

**Restart your MCP client:**
- **Claude Desktop:** Quit and reopen
- **Cursor:** Reload window (Cmd/Ctrl + Shift + P → "Reload Window")
- **Windsurf:** Restart application
- **Cline/Roo Code (VS Code):** Reload window
- **Zed:** Restart application
- **Claude Code:** No restart needed (uses uvx directly)

**Verify it works:**
1. Open your MCP client
2. Try listing available tools - you should see 11 tools (8 legacy + 3 new)
3. Test the new `get_engineering_guidance` tool with a simple query

### Using New v0.3.0 Features

**Try the multi-persona orchestrator:**
```python
# Get collaborative guidance (default mode)
get_engineering_guidance(
    query="Should we use microservices or a monolith?",
    mode="orchestrated",
    session_id="my-project"
)

# Quick mode - just Snarky Senior Engineer
get_engineering_guidance(
    query="How do I fix this bug?",
    mode="quick"
)

# Crisis mode - emergency response team
get_engineering_guidance(
    query="Production is down!",
    mode="crisis"
)

# Consult a specific expert
consult_skill(
    skill_name="security-sentinel",
    query="Review this authentication code"
)

# Discover all 22 personas
list_available_skills()
```

**Legacy mode (v0.2.x behavior):**
```python
# Old tool still works
get_engineering_context(
    operation="CREATE",
    file_paths=["api/users.py"]
)

# Or use new tool in standards mode
get_engineering_guidance(
    query="Creating API endpoint",
    mode="standards"
)
```

### Session Compatibility

**v0.2.x sessions work in v0.3.0:**
- Existing session files automatically gain a `consultations: []` field
- All decisions, constraints, and patterns preserved
- No migration needed

**v0.3.0 sessions in v0.2.x:**
- If you downgrade, consultation history won't be visible
- But all core data (decisions, constraints) still works
- No data loss

---

## Upgrading to v0.2.x from v0.1.x

### What Changed

v0.2.0 added:
- Team Sync via `.sensei` folder
- Git awareness with `analyze_changes()` tool
- Project-local session support

### Upgrade Steps

Same as v0.3.0 upgrade (see above).

### Breaking Changes

**✅ NONE** - v0.2.0 was fully backwards compatible with v0.1.x

---

## Version History

| Version | Release Date | Key Features |
|---------|--------------|--------------|
| **0.5.0** | 2025-01-23 | Enhanced Discovery, CI/CD Integration, Session Merge, Database Architect (23 personas), 2 new tools |
| **0.4.0** | 2025-01-23 | Session Analytics & Team Collaboration, 3 new tools |
| **0.3.0** | 2025-01-22 | Multi-Persona Orchestrator (22 skills), 3 new tools |
| **0.2.1** | 2025-01-15 | CI/CD fixes |
| **0.2.0** | 2025-01-14 | Team Sync, Git Awareness, Project Isolation |
| **0.1.0** | 2025-01-10 | Initial release with 7 MCP tools |

---

## Troubleshooting Upgrades

### "Command not found: uvx"

Install `uvx`:
```bash
pip install uvx
```

### "Old version still showing after upgrade"

Force clear uvx cache:
```bash
# Remove cached version
rm -rf ~/.local/share/uvx/sensei-mcp

# Reinstall
uvx sensei-mcp@latest
```

### "MCP client doesn't see new tools"

1. Verify version: `uvx sensei-mcp --version`
2. Restart MCP client completely (quit and reopen)
3. Check MCP server logs for errors
4. Try removing and re-adding server in config

### "Session file errors after upgrade"

This shouldn't happen (we maintain compatibility), but if it does:

```bash
# Backup sessions
cp -r ~/.sensei/sessions ~/.sensei/sessions.backup

# Or for project-local sessions
cp -r .sensei/sessions.json .sensei/sessions.json.backup

# Then try upgrade again
```

### "Performance seems slower"

v0.3.0 has excellent caching (0ms cached persona loads). If slow:

1. First query after restart takes ~20ms (loading personas)
2. Subsequent queries should be <200ms
3. Check if your `.sensei` folder has huge decision files
4. Report issue: https://github.com/amarodeabreu/sensei-mcp/issues

---

## Downgrading (Not Recommended)

If you need to downgrade:

```bash
# uvx
uvx --force sensei-mcp@0.2.1

# pip
pip install sensei-mcp==0.2.1
```

**Note:** Downgrading loses access to new features but preserves data.

---

## Getting Help

- **GitHub Issues:** https://github.com/amarodeabreu/sensei-mcp/issues
- **Documentation:** https://github.com/amarodeabreu/sensei-mcp
- **Changelog:** https://github.com/amarodeabreu/sensei-mcp/blob/main/CHANGELOG.md

---

## Auto-Update Behavior

### uvx (Recommended)

**By default, uvx does NOT auto-update.** It uses the version installed in its cache.

**To get latest version:**
```bash
uvx --force sensei-mcp@latest  # Force update
```

**Pin to specific version in MCP config:**
```json
{
  "mcpServers": {
    "sensei": {
      "command": "uvx",
      "args": ["sensei-mcp@0.3.0"]  // Pin to 0.3.0
    }
  }
}
```

### pip

**Manual updates only:**
```bash
pip install --upgrade sensei-mcp
```

---

Made with 🥋 by [amarodeabreu](https://github.com/amarodeabreu)
