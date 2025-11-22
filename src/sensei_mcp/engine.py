import re
from pathlib import Path
from typing import Optional, Dict, List, Set

from .models import ContextType

class RulebookLoader:
    """Loads and manages rulebook content with section extraction"""

    def __init__(self, directives_path: Path):
        self.directives_path = directives_path
        self._full_content: Optional[str] = None
        self._section_cache: Dict[str, str] = {}
        self._local_rules: Optional[str] = None

    def _load_full_content(self) -> str:
        """Load full directives file"""
        if self._full_content is None:
            if not self.directives_path.exists():
                raise FileNotFoundError(f"Core directives not found at {self.directives_path}")
            self._full_content = self.directives_path.read_text()
        return self._full_content
        
    def load_local_rules(self, project_root: Optional[str]):
        """Load project-specific rules if they exist"""
        if not project_root:
            return
            
        local_rules_path = Path(project_root) / ".sensei" / "rules.md"
        if local_rules_path.exists():
            self._local_rules = local_rules_path.read_text()

    def extract_section(self, section_name: str) -> str:
        """Extract a specific section from the directives"""
        if section_name == "local_rules" and self._local_rules:
            return self._local_rules

        if section_name in self._section_cache:
            return self._section_cache[section_name]

        content = self._load_full_content()

        # Find section by HTML comment marker
        pattern = f"<!-- SECTION: {section_name} -->(.*?)(?=<!-- SECTION:|$)"
        match = re.search(pattern, content, re.DOTALL)

        if match:
            section_content = match.group(1).strip()
            self._section_cache[section_name] = section_content
            return section_content

        return f"Section '{section_name}' not found in directives."

    def extract_multiple_sections(self, section_names: List[str]) -> str:
        """Extract multiple sections and combine them"""
        sections = []
        for name in section_names:
            content = self.extract_section(name)
            if content and "not found" not in content:
                sections.append(content)
                
        # Append local rules if they exist and we are loading relevant sections
        # (For now, just append them if they exist, or maybe only if specific contexts are triggered?
        # Let's append them at the end if they exist, as they might override or add to any section)
        if self._local_rules:
             sections.append(f"\n\n# 🏠 Project Local Rules\n\n{self._local_rules}")

        return "\n\n---\n\n".join(sections)


class ContextInferenceEngine:
    """
    Analyzes file paths, operations, and context to determine which
    engineering standards sections are most relevant.
    """

    # File type patterns → Context sections
    FILE_PATTERNS = {
        # API Files
        r'(api|route|controller|handler|endpoint)': [
            ContextType.APIS_CONTRACTS,
            ContextType.SECURITY_PRIVACY,
            ContextType.MULTI_TENANCY,
            ContextType.ALWAYS_ON_DEFAULTS,
            ContextType.CONCURRENCY,
        ],
        # Database Files
        r'\.(sql|prisma)|migration|schema|query\.sql|seed\.(sql|js|ts)|knexfile|sequelize': [
            ContextType.DATA_PERSISTENCE,
            ContextType.SECURITY_PRIVACY,
            ContextType.MULTI_TENANCY,
            ContextType.ALWAYS_ON_DEFAULTS,
            ContextType.PERFORMANCE_UX,
        ],
        # Cloud/Infrastructure
        r'\.(tf|ya?ml)|dockerfile|k8s|cloud|terraform': [
            ContextType.CLOUD_PLATFORM,
            ContextType.COMPLIANCE,
            ContextType.COST_CAPACITY,
            ContextType.OBSERVABILITY,
        ],
        # Security Files
        r'(auth|security|permission|token)': [
            ContextType.SECURITY_PRIVACY,
            ContextType.MULTI_TENANCY,
            ContextType.AI_SAFETY,
            ContextType.ALWAYS_ON_DEFAULTS,
        ],
        # Test Files
        r'(test|spec|\._test\.|\.test\.|\.e2e\.|\.integration\.|\.unit\.)': [
            ContextType.TESTING,
            ContextType.CODE_QUALITY,
            ContextType.ANTI_PATTERNS,
            ContextType.TESTS_LINTERS,
        ],
        # Code Files
        r'\.(py|js|ts|go|java|rb|rs|php|cs|kt|kts|swift|scala|c|cpp|cc|cxx|h|hpp|dart|ex|exs|clj|cljs|elm|jl|r)': [
            ContextType.CODE_QUALITY,
            ContextType.CORE_PHILOSOPHY,
            ContextType.CONTEXT_AWARENESS,
        ],
        # Frontend Files
        r'\.(tsx|jsx|vue|svelte|astro|qwik|solid|html|htm|css|scss|sass|less|styl)': [
            ContextType.PERFORMANCE_UX,
            ContextType.I18N_A11Y,
            ContextType.SECURITY_PRIVACY,
            ContextType.FORMATTING,
        ],
        # Config Files
        r'\.(env|json|config|toml)': [
            ContextType.OBSERVABILITY,
            ContextType.AI_SAFETY,
        ],
        # Documentation
        r'\.(md|rst|adoc)': [
            ContextType.DOCUMENTATION,
            ContextType.COMMUNICATION,
            ContextType.FORMATTING,
        ],
        # Shell Scripts
        r'\.(sh|bash|zsh|fish)|Makefile|Rakefile|Justfile': [
            ContextType.CLOUD_PLATFORM,
            ContextType.DELIVERY,
            ContextType.OBSERVABILITY,
            ContextType.WORKSPACE_HYGIENE,
        ],
        # API Schema
        r'\.(graphql|gql|proto|avro)': [
            ContextType.APIS_CONTRACTS,
            ContextType.DOCUMENTATION,
            ContextType.SECURITY_PRIVACY,
        ],
        # Data Files
        r'\.(xml|csv|tsv|parquet)': [
            ContextType.DATA_PERSISTENCE,
            ContextType.ANALYTICS,
            ContextType.I18N_A11Y,
        ],
        # Notebooks
        r'\.(ipynb|rmd)': [
            ContextType.ANALYTICS,
            ContextType.OBSERVABILITY,
            ContextType.DATA_PERSISTENCE,
            ContextType.DOCUMENTATION,
        ],
        # Mobile
        r'(AndroidManifest\.xml|Info\.plist|build\.gradle|settings\.gradle|Podfile)': [
            ContextType.CLOUD_PLATFORM,
            ContextType.DEPENDENCIES,
            ContextType.COMPLIANCE,
            ContextType.SECURITY_PRIVACY,
        ],
        # IaC
        r'\.(hcl|nomad)': [
            ContextType.CLOUD_PLATFORM,
            ContextType.COMPLIANCE,
            ContextType.COST_CAPACITY,
            ContextType.OBSERVABILITY,
            ContextType.SECURITY_PRIVACY,
        ],
        # Containers
        r'(Dockerfile|docker-compose|\.dockerfile)': [
            ContextType.CLOUD_PLATFORM,
            ContextType.COST_CAPACITY,
            ContextType.OBSERVABILITY,
            ContextType.DELIVERY,
        ],
        # Web Server
        r'(nginx\.conf|apache\.conf|httpd\.conf|\.htaccess)': [
            ContextType.CLOUD_PLATFORM,
            ContextType.SECURITY_PRIVACY,
            ContextType.PERFORMANCE_UX,
        ],
        # CI/CD
        r'(\.github/workflows/.*\.ya?ml|\.gitlab-ci\.yml|Jenkinsfile|\.circleci/config\.yml|azure-pipelines\.yml)': [
            ContextType.DELIVERY,
            ContextType.CLOUD_PLATFORM,
            ContextType.TESTS_LINTERS,
            ContextType.OBSERVABILITY,
        ],
        # Linters
        r'(\.eslintrc.*|\.prettierrc.*|\.stylelintrc.*|\.editorconfig|pyproject\.toml|tox\.ini|setup\.cfg)': [
            ContextType.CODE_QUALITY,
            ContextType.FORMATTING,
            ContextType.TESTS_LINTERS,
            ContextType.WORKSPACE_HYGIENE,
        ],
        # Package Managers
        r'(package\.json|package-lock\.json|yarn\.lock|pnpm-lock\.yaml|Gemfile|Gemfile\.lock|requirements\.txt|Pipfile|Cargo\.toml|go\.mod|go\.sum)': [
            ContextType.DEPENDENCIES,
            ContextType.SECURITY_PRIVACY,
            ContextType.COST_CAPACITY,
        ],
        # Test Configs
        r'(jest\.config.*|vitest\.config.*|playwright\.config.*|cypress\.config.*|pytest\.ini|phpunit\.xml)': [
            ContextType.TESTING,
            ContextType.TESTS_LINTERS,
            ContextType.CODE_QUALITY,
        ],
        # Build Configs
        r'(webpack\.config.*|vite\.config.*|rollup\.config.*|esbuild\.config.*|tsconfig\.json|babel\.config.*)': [
            ContextType.CLOUD_PLATFORM,
            ContextType.PERFORMANCE_UX,
            ContextType.DEPENDENCIES,
        ],
        # Ignore Files
        r'(\.gitignore|\.dockerignore|\.npmignore|\.eslintignore)': [
            ContextType.WORKSPACE_HYGIENE,
            ContextType.SECURITY_PRIVACY,
        ],
        # Secrets
        r'(\.env.*|secrets.*|credentials.*|\.aws/|\.gcloud/)': [
            ContextType.SECURITY_PRIVACY,
            ContextType.AI_SAFETY,
            ContextType.CLOUD_PLATFORM,
        ],
        # License
        r'(LICENSE|COPYING|NOTICE|PATENTS)': [
            ContextType.COMPLIANCE,
            ContextType.DOCUMENTATION,
        ],
        # Monitoring
        r'(prometheus\.yml|grafana\.json|datadog\.ya?ml|newrelic\.yml|sentry\.config.*)': [
            ContextType.OBSERVABILITY,
            ContextType.CLOUD_PLATFORM,
            ContextType.COST_CAPACITY,
        ],
        # Email
        r'(templates/.*\.(html|txt)|emails/|notifications/)': [
            ContextType.I18N_A11Y,
            ContextType.SECURITY_PRIVACY,
            ContextType.COMMUNICATION,
        ],
    }

    # Operation types → Context sections
    OPERATION_PATTERNS = {
        'CREATE': [
            ContextType.CORE_PHILOSOPHY,
            ContextType.PROTOTYPE_MODE,
            ContextType.QUALITY_BAR,
        ],
        'REFACTOR': [
            ContextType.CORE_PHILOSOPHY,
            ContextType.CODE_QUALITY,
            ContextType.MANTRAS,
            ContextType.SELF_CONSISTENCY,
            ContextType.REFACTORING,
        ],
        'DEBUG': [
            ContextType.OBSERVABILITY,
            ContextType.CLAUDE_BEHAVIOR,
            ContextType.UNCERTAINTY,
            ContextType.TESTS_LINTERS,
        ],
        'DESIGN': [
            ContextType.CORE_PHILOSOPHY,
            ContextType.PRODUCT_ALIGNMENT,
            ContextType.ARCHITECTURE,
            ContextType.TASK_SHAPING,
        ],
        'REVIEW': [
            ContextType.CODE_QUALITY,
            ContextType.ANTI_PATTERNS,
            ContextType.SANITY_CHECKLIST,
            ContextType.CODE_REVIEW,
        ],
        'OPTIMIZE': [
            ContextType.COST_CAPACITY,
            ContextType.PERFORMANCE_UX,
            ContextType.DATA_PERSISTENCE,
        ],
        'SECURITY': [
            ContextType.SECURITY_PRIVACY,
            ContextType.MULTI_TENANCY,
            ContextType.AI_SAFETY,
            ContextType.COMPLIANCE,
        ],
        'DEPLOY': [
            ContextType.DELIVERY,
            ContextType.CLOUD_PLATFORM,
            ContextType.OBSERVABILITY,
        ],
        'TEST': [
            ContextType.TESTING,
            ContextType.TESTS_LINTERS,
        ],
        'DOCUMENTATION': [
            ContextType.DOCUMENTATION,
            ContextType.COMMUNICATION,
            ContextType.FORMATTING,
        ],
    }

    # Keyword triggers → Context sections
    KEYWORD_PATTERNS = {
        r'(tenant|multi.?tenant|isolation)': [
            ContextType.MULTI_TENANCY,
            ContextType.ALWAYS_ON_DEFAULTS,
        ],
        r'(payment|billing|charge)': [
            ContextType.SECURITY_PRIVACY,
            ContextType.CONCURRENCY,
            ContextType.AI_SAFETY,
        ],
        r'(async|queue|background|concurrent)': [
            ContextType.CONCURRENCY,
        ],
        r'(scale|performance|slow|latency)': [
            ContextType.COST_CAPACITY,
            ContextType.PERFORMANCE_UX,
        ],
        r'(junior|explain|help|teach)': [
            ContextType.PERSONALITY,
            ContextType.COMMUNICATION,
        ],
        r'(cost|expensive|bill)': [
            ContextType.COST_CAPACITY,
        ],
        r'(legacy|inherited|old.?code)': [
            ContextType.CONTEXT_AWARENESS,
            ContextType.DELIVERY,
        ],
        r'(prototype|spike|poc)': [
            ContextType.PROTOTYPE_MODE,
        ],
        r'(breaking.?change|migration)': [
            ContextType.APIS_CONTRACTS,
            ContextType.DOCUMENTATION,
        ],
    }

    @classmethod
    def infer_contexts(cls,
                      file_paths: Optional[List[str]] = None,
                      operation: Optional[str] = None,
                      description: Optional[str] = None) -> Set[ContextType]:
        """
        Infer which directive sections are relevant based on context.
        """
        contexts = set()

        # ALWAYS include core sections
        contexts.add(ContextType.CORE_PRINCIPLES)
        contexts.add(ContextType.PERSONALITY)

        # Analyze file paths
        if file_paths:
            for file_path in file_paths:
                file_lower = file_path.lower()
                for pattern, context_types in cls.FILE_PATTERNS.items():
                    if re.search(pattern, file_lower):
                        contexts.update(context_types)

        # Analyze operation
        if operation:
            op_upper = operation.upper()
            for op_keyword in cls.OPERATION_PATTERNS.keys():
                if op_keyword in op_upper:
                    contexts.update(cls.OPERATION_PATTERNS[op_keyword])

        # Analyze description for keywords
        if description:
            desc_lower = description.lower()
            for pattern, context_types in cls.KEYWORD_PATTERNS.items():
                if re.search(pattern, desc_lower):
                    contexts.update(context_types)

        return contexts
