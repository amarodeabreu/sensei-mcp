# Changelog

All notable changes to Sensei MCP will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2025-01-23

### Added - Enhanced Discovery, CI/CD Integration, Team Collaboration & Database Expertise 🚀

#### Feature #1: Interactive Persona Discovery 🔍
- **Enhanced `list_available_skills()`** with format parameter:
  - `standard`: Default format with category grouping
  - `detailed`: Full metadata including examples, use_when, related_personas, quick_tip
  - `quick`: Condensed format showing only names and one-liners
- **CLI Demo Mode** (`sensei-mcp --demo`):
  - Interactive walkthrough of 5 real-world scenarios
  - Demonstrates multi-persona collaboration patterns
  - Scenarios: Architecture Decision, Production Crisis, Security Review, Cost Optimization, Code Quality
  - Colored terminal output for better readability
- **Context Hints in `get_engineering_guidance()`**:
  - Intelligent suggestions when <2 personas selected
  - Keyword-based detection across 10+ technology domains (database, api, security, frontend, mobile, ml, team)
  - Context-based fallback suggestions (SECURITY → security-sentinel, CRISIS → incident-commander)
  - Shows top 3 persona recommendations with usage examples

#### Feature #2: CI/CD Integration Pack 🔧
- **GitHub Actions Workflows** (2 templates):
  - `sensei-pr-review.yml`: Multi-persona PR analysis with architecture, security, and cost checks
  - `sensei-architecture-check.yml`: Architecture validation on pull requests
- **Pre-Commit Hooks** (3 Python scripts):
  - `sensei_consistency_check.py`: Validate changes against session decisions
  - `sensei_security_review.py`: Pattern-based security scanning (secrets, SQL injection, XSS)
  - `sensei_cost_check.py`: Cloud cost impact analysis (AWS, GCP, Azure service detection)
- **GitLab CI Configuration**:
  - 3-stage pipeline (validate, review, report)
  - Scheduled weekly architecture audits
  - Security and cost review jobs
- **Enhanced `analyze_changes()`** tool:
  - Diff statistics (files changed, lines added/removed)
  - Intelligent persona suggestions based on file patterns
  - File extension and path pattern detection
- **Comprehensive Integration Guide** (`integrations/INTEGRATION_GUIDE.md`):
  - 500+ lines of documentation
  - Setup instructions for all platforms
  - Configuration examples and best practices
  - Troubleshooting guide

#### Feature #3: Session Merge & Team Sync 🤝
- **SessionMerger class** with `merge_sessions()` functionality:
  - Merge decisions, constraints, patterns, and consultations from multiple sessions
  - 4 conflict resolution strategies:
    - `latest`: Prefer most recent item (default)
    - `oldest`: Prefer earliest item
    - `all`: Keep all items with source attribution
    - `manual`: Return conflicts for human resolution
  - Attribution tracking via timestamps and session IDs
  - Chronological sorting of merged consultations
- **Session comparison** via `compare_sessions()`:
  - Side-by-side diff of decisions, constraints, patterns
  - Markdown-formatted comparison reports
- **Conflict detection and reporting**:
  - MergeConflict dataclass with full metadata
  - Human-readable conflict descriptions
  - Resolution tracking
- **MergeResult data structure**:
  - Summary statistics (decisions merged, conflicts detected)
  - Error reporting
  - Markdown formatting helpers

#### Feature #4: Database Architect Persona (23rd Persona) 🗄️
- **New specialized persona**: `database-architect`
  - Category: specialized
  - Expertise areas: schema design, query optimization, indexing, migrations, scalability
  - Related personas: data-engineer, pragmatic-architect, site-reliability-engineer, finops-optimizer
- **11 comprehensive sections**:
  - Core Principles (The Database Commandments)
  - Personality & Tone
  - Schema Design & Normalization (1NF-BCNF)
  - Query Optimization & EXPLAIN Plans
  - Indexing Strategies (composite, covering, partial)
  - Migration Planning & Zero-Downtime Deployments
  - Scalability Patterns (partitioning, sharding, replication)
  - Multi-Tenancy Architecture
  - Database Selection Guidance (relational, document, graph, time-series)
  - Performance Monitoring & Anti-Pattern Detection
  - SQL Query Optimization Patterns
- **v0.4.0 metadata** included:
  - Examples: "Design a database schema for a multi-tenant SaaS application"
  - use_when: Database design, query performance, migration planning
  - quick_tip: "Consult for database schema design, query optimization, and scalability planning"
  - related_personas: Links to complementary expertise

#### New MCP Tools (2)
- `merge_sessions()` - Merge multiple developer sessions with conflict resolution
- `compare_sessions()` - Compare two sessions side-by-side

### Enhanced
- **PersonaRegistry**:
  - Added `category` property to ConcretePersona
  - Enhanced `search_by_expertise()` to accept string or list
  - Searches both expertise areas AND descriptions
  - database-architect added to specialized category
- **Demo Mode Integration**:
  - Added `--demo` CLI flag to `__main__.py`
  - Interactive scenario walkthrough
  - ANSI color codes for terminal formatting
- **Context Detection**:
  - New context hints system with keyword mapping
  - DATABASE context detection
  - Technology-specific keyword recognition (postgres, mongodb, graphql, vue, android, etc.)

### Testing
- Added `tests/test_merge.py` with 13 test cases:
  - SessionMerger initialization and functionality
  - All 4 conflict resolution strategies
  - Session comparison
  - Markdown formatting
  - Edge cases (empty sessions, nonexistent sessions)
  - Chronological consultation sorting
  - MergeConflict and MergeResult data structures
- Added `tests/test_context_hints.py` with 29 test cases:
  - Hint generation logic
  - Keyword detection across 10+ domains
  - Context-based fallback suggestions
  - Persona limit enforcement (max 3)
  - Case-insensitive matching
  - Edge cases (0 personas, no keyword match)
- Added `tests/test_database_architect.py` with 25 test cases:
  - File existence and loading
  - Metadata validation (name, description, expertise)
  - v0.4.0 metadata fields (quick_tip, examples, use_when, related_personas)
  - Content validation (principles, personality, sections)
  - Registry integration (category, searchability)
  - Database expertise validation
  - YAML frontmatter parsing
- **Total: 67 new tests, 100% passing**
- **Runtime: 0.34s**
- Created `V0.5.0_TESTING_SUMMARY.md` with comprehensive test report

### Documentation
- Created `V0.5.0_IMPLEMENTATION_STATUS.md` tracking implementation progress
- Created `V0.5.0_TESTING_SUMMARY.md` with detailed test results
- Created `integrations/INTEGRATION_GUIDE.md` (500+ lines)
- Updated tool count: 16 total MCP tools (2 new in v0.5.0)
- Updated persona count: 23 personas (22 → 23)

### Technical Details
- Added `src/sensei_mcp/demo.py` (~410 LOC):
  - Colors class for ANSI terminal formatting
  - 5 demo scenarios with expected personas
  - Interactive demo runner
- Added `src/sensei_mcp/merge.py` (~480 LOC):
  - SessionMerger class with merge_sessions()
  - compare_sessions() functionality
  - MergeConflict and MergeResult dataclasses
  - 4 conflict resolution strategies
- Added `src/sensei_mcp/personas/skills/database-architect.md` (~550 LOC):
  - Comprehensive database architecture expertise
  - 11 sections covering all database concerns
  - v0.4.0 metadata format
- Enhanced `src/sensei_mcp/server.py`:
  - Enhanced list_available_skills() with format parameter (~85 LOC)
  - Added _generate_context_hint() helper (~80 LOC)
  - Integrated context hints into get_engineering_guidance() (~10 LOC)
  - Enhanced analyze_changes() with persona suggestions (~140 LOC)
  - Added merge_sessions() and compare_sessions() tools (~100 LOC)
- Enhanced `src/sensei_mcp/personas/registry.py`:
  - Added category property to ConcretePersona (~24 LOC)
  - Enhanced search_by_expertise() (~38 LOC)
  - Added database-architect to CATEGORIES
- Enhanced `src/sensei_mcp/__main__.py`:
  - Added --demo flag and integration (~15 LOC)
- Created CI/CD integration files (~1,350 LOC):
  - 2 GitHub Actions workflows
  - 3 pre-commit hooks with Python scripts
  - 1 GitLab CI configuration
  - Comprehensive integration guide

### Files Added
- `src/sensei_mcp/demo.py`
- `src/sensei_mcp/merge.py`
- `src/sensei_mcp/personas/skills/database-architect.md`
- `integrations/github-actions/sensei-pr-review.yml`
- `integrations/github-actions/sensei-architecture-check.yml`
- `integrations/pre-commit/.pre-commit-config.yaml`
- `integrations/pre-commit/sensei_consistency_check.py`
- `integrations/pre-commit/sensei_security_review.py`
- `integrations/pre-commit/sensei_cost_check.py`
- `integrations/gitlab-ci/.gitlab-ci.yml`
- `integrations/INTEGRATION_GUIDE.md`
- `tests/test_merge.py`
- `tests/test_context_hints.py`
- `tests/test_database_architect.py`
- `V0.5.0_IMPLEMENTATION_STATUS.md`
- `V0.5.0_TESTING_SUMMARY.md`

### Bugs Fixed
- PersonaRegistry fixture missing skills_dir parameter
- Category attribute not exposed in ConcretePersona
- database-architect not in CATEGORIES['specialized']
- search_by_expertise() now accepts string or list
- Merge test expectations corrected for empty session behavior

### Backwards Compatibility
- ✅ All v0.4.x tools remain functional
- ✅ All v0.3.x tools remain functional
- ✅ All v0.2.x tools remain functional
- ✅ Session format compatible (no breaking changes)
- ✅ All existing workflows continue to function

### Known Issues
- 16 DeprecationWarnings for datetime.utcnow() usage (deferred to v0.5.1)

### Statistics
- **Total LOC Added**: ~4,064 (features + tests)
- **New Tests**: 67 (100% passing)
- **New Tools**: 2 MCP tools
- **New Personas**: 1 (database-architect)
- **New Integration Templates**: 7 files across 3 platforms
- **Documentation**: 3 new markdown files

---

## [0.4.0] - 2025-01-23

### Added - Analytics & Team Collaboration 📊

#### Session Analytics (`get_session_insights`)
- **Data-driven insights** into persona usage and consultation patterns
- **Time-based filtering**: last 7 days, last 30 days, all time
- **Persona statistics**:
  - Consultation counts and decision influence per persona
  - First/last consultation timestamps
  - Average synthesis length
  - Contexts where each persona was used
- **Context distribution**: track which engineering contexts (SECURITY, CRISIS, etc.) are most common
- **Decision metrics**:
  - Decision velocity (decisions per day)
  - Average time to decision (consultations per decision)
- **Session health**:
  - Session age in days
  - Active days count
  - Average consultations per day
- **Multiple output formats**: Markdown (reports), JSON (CI/CD), text (quick view)
- **Configurable filtering**: minimum consultations threshold for persona stats

#### Consultation Export (`export_consultation`)
- **Professional reports** for individual consultations
- **Metadata support**: consultation ID, timestamp, mode, context
- **Persona tracking**: which experts were consulted
- **Decision linking**: automatically links to decisions made from consultation
- **Multiple formats**: Markdown (human-readable), JSON (API integration), text (plain)
- **Optional metadata**: toggle metadata inclusion for cleaner reports

#### Session Summary Export (`export_session_summary`)
- **Architecture Decision Records (ADRs)**: comprehensive decision documentation
- **ADR format** includes:
  - Decision description and category
  - Rationale and timestamp
  - Associated constraints and patterns (from decision context dict)
  - Linked consultations
- **Consultation history**: recent consultations with personas and outcomes
- **Active constraints**: current project requirements and limitations
- **Agreed patterns**: architectural patterns the team has adopted
- **Configurable includes**: select which sections to include (decisions, consultations, constraints, patterns)
- **Configurable consultation limit**: control how many recent consultations to include
- **Multiple formats**: Markdown (documentation), JSON (tooling), text (summaries)
- **Team onboarding**: perfect for sharing engineering context with new team members

#### New MCP Tools (3)
- `get_session_insights()` - Analyze persona usage and decision patterns
- `export_consultation()` - Export individual consultations as reports
- `export_session_summary()` - Export comprehensive ADRs and session context

### Enhanced
- **Session persistence**: consultations now stored with full metadata
- **Decision context**: decisions track constraints and patterns in context dict
- **SessionState model**: added patterns_agreed field
- **Analytics module**: comprehensive session analysis engine
- **Export utilities**: flexible export system for consultations and sessions

### Testing
- Added `tests/test_analytics.py` with 17 test cases
  - PersonaStats and SessionInsights data classes
  - SessionAnalyzer with time-range filtering
  - Persona statistics calculation
  - Context and mode distribution analysis
  - Decision velocity calculations
  - Output formatting (markdown, JSON, text)
- Added `tests/test_exporter.py` with 17 test cases
  - ConsultationExporter in all formats
  - SessionExporter with configurable includes
  - ADR generation with constraint/pattern handling
  - Consultation truncation and metadata toggling
- All 34 new tests passing with 100% coverage

### Documentation
- Updated README.md with v0.4.0 features and tool examples
- Created comprehensive CHANGELOG.md entry
- Updated tool count: 14 total MCP tools (3 new in v0.4.0)
- Added analytics and export examples to usage section

### Technical Details
- Added `src/sensei_mcp/analytics.py` (~400 LOC)
  - PersonaStats dataclass for individual persona metrics
  - SessionInsights dataclass for comprehensive analytics
  - SessionAnalyzer with filtering and formatting
- Added `src/sensei_mcp/exporter.py` (~380 LOC)
  - ConsultationExporter for single consultation reports
  - SessionExporter for ADRs and session summaries
- Enhanced `src/sensei_mcp/server.py` with 3 new MCP tool exports
- Updated Decision model usage: constraints/patterns stored in context dict

### Backwards Compatibility
- ✅ All v0.3.x tools remain functional
- ✅ All v0.2.x tools remain functional
- ✅ Session format compatible (no breaking changes)
- ✅ All existing workflows continue to function

---

## [0.3.0] - 2025-01-22

### Added - Multi-Persona Orchestrator 🎭

#### New Core Capabilities
- **Skill Orchestrator**: Meta-persona coordinating 22 specialized AI skills for collaborative engineering guidance
- **Context Detection**: Intelligent query analysis across 8 context types (CRISIS, SECURITY, POLITICAL, ARCHITECTURAL, COST, TEAM, TECHNICAL, GENERAL)
- **22 Specialized Personas**:
  - **Core (3):** Snarky Senior Engineer, Pragmatic Architect, Legacy Archaeologist
  - **Specialized (8):** Security Sentinel, FinOps Optimizer, Performance Engineer, Product Engineering Lead, API Architect, Platform Builder, Staff+ Mentor, Tech Debt Wrangler
  - **Operations (4):** Incident Commander, Site Reliability Engineer, Executive Liaison, Compliance Guardian
  - **Additional (7):** DevX Advocate, Data Platform Engineer, Frontend Performance Specialist, Mobile Platform Engineer, Documentation Curator, ML/AI Infrastructure Specialist, Integration Specialist

#### New MCP Tools
- `get_engineering_guidance()` - **New primary tool** with multi-persona orchestration
  - Modes: `orchestrated` (default), `quick`, `crisis`, `standards` (legacy)
  - Auto-selects 2-5 relevant personas based on query context
  - Supports specific persona selection via `specific_personas` parameter
  - Multiple output formats: `standard`, `executive`, `technical`
- `consult_skill()` - Direct consultation with a single persona
- `list_available_skills()` - Discover all 22 personas by category

#### Enhanced Infrastructure
- **Personas Module**: Base classes, skill loader, and registry with lazy loading
- **Consultation Tracking**: Session memory now records which personas were consulted for each query
- **Conflict Resolution**: "Disagree and commit" synthesis combining multiple perspectives
- **Session Integration**: Personas receive constraints, patterns, and past decisions from session memory

### Changed
- `get_engineering_context()` is now legacy - internally delegates to `get_engineering_guidance(..., mode="standards")`
- Updated description: "Multi-persona engineering mentor with 22 specialized AI skills orchestrating collaborative guidance"
- Bumped version from 0.2.1 to 0.3.0

### Technical Details
- Added `src/sensei_mcp/personas/` module with base.py, loader.py, registry.py
- Added `src/sensei_mcp/context_detector.py` for query context analysis
- Added `src/sensei_mcp/orchestrator.py` for multi-persona coordination
- Enhanced `SessionState` with `Consultation` dataclass
- Added 22 SKILL.md persona definition files to `src/sensei_mcp/personas/skills/`
- Updated `pyproject.toml` to include personas/skills directory in package distribution

### Testing
- Added `tests/test_personas_smoke.py` - Verify all 22 personas load correctly
- Added `tests/test_orchestrator_integration.py` - Comprehensive orchestration testing
  - Context detection across all 8 types
  - Persona selection (auto, quick, crisis modes)
  - Session context integration
  - Specific persona selection
  - Output format validation
- All 102 tests passing

### Documentation
- Updated README.md with v0.3.0 multi-persona orchestrator features
- Added new example workflows showcasing persona collaboration
- Added crisis mode example for production incidents
- Updated tool count from 7 to 11 tools

### Backwards Compatibility
- ✅ All v0.2.x tools remain functional
- ✅ Legacy `get_engineering_context()` continues to work (delegates to standards mode)
- ✅ Session format compatible (added `consultations` field with default empty list)
- ✅ All existing workflows continue to function

---

## [0.2.1] - 2025-01-15

### Fixed
- CI/CD pipeline configuration for PyPI publishing
- Token authentication for package publishing

---

## [0.2.0] - 2025-01-14

### Added - Team Sync & Git Awareness

#### New Features
- **Team Sync**: Share decisions and rules via `.sensei` folder in your repo
  - Local project rules via `.sensei/rules.md`
  - Session decisions saved to `.sensei/decisions.md`
  - Commit to Git for team collaboration
- **Git Awareness**: `analyze_changes()` tool automatically infers context from staged files
- **Project Isolation**: Session states separated by project_root parameter

#### New MCP Tools
- `analyze_changes()` - Infer engineering context from git staged files

### Changed
- Session manager now supports both global sessions (`~/.sensei/sessions/`) and local project sessions (`.sensei/`)
- Context inference engine enhanced to detect project-local rules

### Documentation
- Added team sync documentation to README.md
- Added `.sensei` folder structure examples

---

## [0.1.0] - 2025-01-10

### Added - Initial Release

#### Core Features
- **Context-aware loading**: Only 5-15% of rulebook per request (87.5% token savings)
- **Session memory**: Persists architectural decisions across conversations
- **50+ file types**: Comprehensive tech stack coverage
- **Smart inference**: Automatically determines relevant standards
- **Zero configuration**: Works immediately after install

#### MCP Tools (7)
- `get_engineering_context()` - Smart context injection
- `record_decision()` - Save architectural decisions
- `validate_against_standards()` - Pre-implementation validation
- `get_session_summary()` - Review decisions and constraints
- `list_sessions()` - Manage multiple projects
- `query_specific_standard()` - Direct rulebook section access
- `check_consistency()` - Validate against past decisions

#### Supported File Types
- Programming languages (20+): Python, JS/TS, Go, Java, Kotlin, Swift, Ruby, Rust, PHP, C#, Scala, C/C++, Dart, Elixir, Clojure, Elm, Julia, R
- Frontend: React, Vue, Svelte, Astro, HTML, CSS/SCSS/SASS/LESS
- Infrastructure: Terraform, Docker, Kubernetes, nginx, Shell scripts, HCL
- Data: SQL, Prisma, GraphQL, Protobuf, Avro, CSV, XML, Jupyter
- Config: YAML, JSON, TOML, ESLint, Prettier, Jest, Playwright, Webpack, Vite
- CI/CD: GitHub Actions, GitLab CI, Jenkins, CircleCI, Azure Pipelines
- Mobile: Android, iOS
- Package managers: npm, gem, cargo, go.mod, pip, pipenv
- Monitoring: Prometheus, Grafana, Datadog, New Relic, Sentry

#### Context Inference
- **57 rulebook sections** mapped to **32 file patterns**
- File pattern detection (API, database, tests, infrastructure, etc.)
- Operation type detection (CREATE, REFACTOR, DEBUG, SECURITY, etc.)
- Keyword triggers (multi-tenant, payment, async, etc.)

---

[0.5.0]: https://github.com/amarodeabreu/sensei-mcp/releases/tag/v0.5.0
[0.4.0]: https://github.com/amarodeabreu/sensei-mcp/releases/tag/v0.4.0
[0.3.0]: https://github.com/amarodeabreu/sensei-mcp/releases/tag/v0.3.0
[0.2.1]: https://github.com/amarodeabreu/sensei-mcp/releases/tag/v0.2.1
[0.2.0]: https://github.com/amarodeabreu/sensei-mcp/releases/tag/v0.2.0
[0.1.0]: https://github.com/amarodeabreu/sensei-mcp/releases/tag/v0.1.0
