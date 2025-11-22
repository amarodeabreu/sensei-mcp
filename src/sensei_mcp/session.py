import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import asdict

from .models import SessionState, Decision

class SessionManager:
    """Manages session state persistence"""

    def __init__(self, global_session_dir: Path):
        self.global_session_dir = global_session_dir
        self.global_session_dir.mkdir(parents=True, exist_ok=True)
        self.current_session: Optional[SessionState] = None
        self.current_project_root: Optional[Path] = None

    def _get_session_path(self, session_id: str, project_root: Optional[str] = None) -> Path:
        """
        Determine where to store the session file.
        If project_root is provided and has a .sensei directory, use that.
        Otherwise use the global session directory.
        """
        if project_root:
            path = Path(project_root)
            if (path / ".sensei").exists():
                self.current_project_root = path
                return path / ".sensei" / f"{session_id}.json"
        
        self.current_project_root = None
        return self.global_session_dir / f"{session_id}.json"

    def get_or_create_session(self, session_id: str = "default", project_root: Optional[str] = None) -> SessionState:
        """Load existing session or create new one"""
        session_file = self._get_session_path(session_id, project_root)

        if session_file.exists():
            with open(session_file, 'r') as f:
                data = json.load(f)
                self.current_session = SessionState(
                    session_id=data['session_id'],
                    started_at=data['started_at'],
                    decisions=[Decision(**d) for d in data['decisions']],
                    active_constraints=data['active_constraints'],
                    patterns_agreed=data['patterns_agreed'],
                    last_updated=data['last_updated']
                )
        else:
            self.current_session = SessionState(
                session_id=session_id,
                started_at=datetime.now().isoformat(),
                decisions=[],
                active_constraints=[],
                patterns_agreed=[],
                last_updated=datetime.now().isoformat()
            )

        return self.current_session

    def save_session(self):
        """Persist current session to disk"""
        if not self.current_session:
            return

        # We need to know where to save. If get_or_create was called, we know the path.
        # But we might need to re-evaluate if project_root changed (unlikely in one tool call).
        # For now, we assume the path determined in get_or_create is valid.
        # Re-calculating path requires session_id and project_root.
        # We'll store the last used path or re-calculate if we store project_root in state.
        
        # Better approach: The session object doesn't know its path. 
        # We should probably store the path in the manager when we load it.
        # But for now, let's assume we are saving to the same place we loaded from.
        # To make this robust, let's just re-use the logic if we have the project root.
        
        session_file = self._get_session_path(self.current_session.session_id, str(self.current_project_root) if self.current_project_root else None)
        self.current_session.last_updated = datetime.now().isoformat()

        with open(session_file, 'w') as f:
            data = {
                'session_id': self.current_session.session_id,
                'started_at': self.current_session.started_at,
                'decisions': [asdict(d) for d in self.current_session.decisions],
                'active_constraints': self.current_session.active_constraints,
                'patterns_agreed': self.current_session.patterns_agreed,
                'last_updated': self.current_session.last_updated
            }
            json.dump(data, f, indent=2)
            
        # Also save decisions to Markdown if we are in a project
        if self.current_project_root:
            self._save_decisions_md(self.current_project_root / ".sensei" / "decisions.md")

    def _save_decisions_md(self, path: Path):
        """Save decisions to a human-readable Markdown file"""
        if not self.current_session or not self.current_session.decisions:
            return
            
        content = ["# Architectural Decisions Log\n"]
        content.append(f"*Last updated: {datetime.now().isoformat()}*\n\n")
        
        for dec in reversed(self.current_session.decisions):
            content.append(f"## {dec.id}: {dec.description}\n")
            content.append(f"- **Date:** {dec.timestamp}\n")
            content.append(f"- **Category:** {dec.category}\n")
            content.append(f"- **Rationale:** {dec.rationale}\n")
            if dec.context:
                content.append(f"- **Context:** {json.dumps(dec.context)}\n")
            content.append("\n---\n")
            
        with open(path, 'w') as f:
            f.write("".join(content))

    def add_decision(self, category: str, description: str, rationale: str,
                     context: Dict[str, Any] = None, project_root: Optional[str] = None):
        """Record a new decision"""
        if not self.current_session:
            self.get_or_create_session(project_root=project_root)

        decision = Decision(
            id=f"dec_{len(self.current_session.decisions) + 1}",
            timestamp=datetime.now().isoformat(),
            category=category,
            description=description,
            rationale=rationale,
            context=context or {}
        )

        self.current_session.decisions.append(decision)
        self.save_session()
        return decision
