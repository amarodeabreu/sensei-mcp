# Contributing to Sensei MCP

Thank you for your interest in contributing to Sensei MCP! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites
- Python 3.10 or higher
- `uv` or `pip` for package management

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/amarodeabreu/sensei-mcp.git
   cd sensei-mcp
   ```

2. **Install in development mode**
   ```bash
   pip install -e .
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   # or manually:
   pip install pytest pytest-cov black isort build twine
   ```

## Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=sensei_mcp tests/

# Run specific test file
pytest tests/test_server.py
```

## Code Style

We follow Python best practices:

- **Formatting**: Use `black` for code formatting
  ```bash
  black src/ tests/
  ```

- **Import sorting**: Use `isort`
  ```bash
  isort src/ tests/
  ```

- **Type hints**: Use type hints where appropriate
- **Docstrings**: Use clear docstrings for all public functions

## Making Changes

1. **Create a branch** for your feature or bugfix
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bugfix-name
   ```

2. **Make your changes** following the code style guidelines

3. **Add tests** for new functionality

4. **Run tests** to ensure everything works
   ```bash
   pytest tests/
   ```

5. **Commit your changes** with clear commit messages
   ```bash
   git commit -m "Add feature: description of feature"
   ```

## Submitting Changes

1. **Push your branch** to GitHub
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request** on GitHub with:
   - Clear description of changes
   - Any related issue numbers
   - Test results (if applicable)

3. **Wait for review** - maintainers will review your PR and may request changes

## Adding New File Type Support

To add support for new file types:

1. **Edit `src/sensei_mcp/server.py`**
2. **Add pattern to `FILE_PATTERNS`** in `ContextInferenceEngine` class
3. **Map to appropriate `ContextType` values**
4. **Add test case** in `tests/test_server.py`
5. **Document** in README.md under "Supported File Types"

Example:
```python
# In FILE_PATTERNS:
r'\.(your|new|extensions)': [
    ContextType.CODE_QUALITY,
    ContextType.CORE_PHILOSOPHY,
],
```

## Reporting Issues

- Use GitHub Issues for bug reports and feature requests
- Provide clear descriptions and reproduction steps
- Include Python version and installation method
- Tag appropriately (bug, feature, documentation, etc.)

## Questions?

Open a GitHub Discussion or Issue for:
- Questions about the codebase
- Design discussions
- Feature proposals

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on improving the project

Thank you for contributing! 🥋
