# Product Requirements Document: Sensei MCP "Next Level"

## 1. Introduction
This document outlines the "Next Level" features for Sensei MCP, transforming it from a passive context engine into an active Engineering Sensei.

## 2. Features

### 2.1 RAG-Powered Context
**Problem**: Regex-based context inference is brittle and misses semantic nuance.
**Solution**: Use local embeddings to index the rulebook.
**Requirements**:
- Integrate a lightweight embedding model (e.g., `sentence-transformers` or an API if allowed).
- Index `core-directives.md` and local `rules.md` into a vector store (e.g., `chromadb` or in-memory FAISS).
- **Tool**: `query_knowledge_base(query: str)` returns semantically relevant sections.

### 2.2 Active Validation (Linter Integration)
**Problem**: `validate_against_standards` relies on LLM hallucination/reasoning, not ground truth.
**Solution**: Execute real validation tools.
**Requirements**:
- Allow configuring "validators" in `.sensei/config.json`.
- Example: `"validators": {"python": "flake8", "javascript": "npm run lint"}`.
- **Tool**: `run_validation(files: List[str])` executes the configured commands and returns stdout/stderr.

### 2.3 CTO Mode Dashboard
**Problem**: Visibility into project health and standard adherence is low.
**Solution**: A visual dashboard or CLI summary.
**Requirements**:
- **CLI**: `sensei-mcp status` command.
- **Web UI**: Simple local server showing:
    - Compliance Score (based on linter results).
    - Recent Decisions log.
    - Active Constraints.
    - "Debt" tracker (conflicts logged but ignored).

### 2.4 Semantic Consistency Checks
**Problem**: Keyword matching for consistency is easily fooled.
**Solution**: Use an LLM call (if available) to check consistency.
**Requirements**:
- If an API key is present, use a small model (e.g., Gemini Flash, Claude Haiku) to compare "Proposed Change" vs "Agreed Decisions" and return a structured conflict report.

## 3. Roadmap
- **Phase 1 (Current)**: Refactor, Git Awareness, Team Sync.
- **Phase 2**: RAG Context & Semantic Search.
- **Phase 3**: Active Validation Hooks.
- **Phase 4**: Dashboard & Reporting.
