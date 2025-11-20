# Publishing Sensei MCP to PyPI

This guide covers how to build and publish Sensei MCP to PyPI.

## Prerequisites

```bash
pip install build twine
```

## Version Bumping

Sensei MCP follows [Semantic Versioning](https://semver.org/):
- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features, backward compatible
- **PATCH** (0.0.1): Bug fixes, backward compatible

To bump version:

1. **Update version in `pyproject.toml`**
   ```toml
   version = "0.2.0"  # Change this
   ```

2. **Update version in `src/sensei_mcp/__init__.py`**
   ```python
   __version__ = "0.2.0"  # Change this
   ```

3. **Commit the version bump**
   ```bash
   git add pyproject.toml src/sensei_mcp/__init__.py
   git commit -m "Bump version to 0.2.0"
   ```

## Building the Package

1. **Clean previous builds**
   ```bash
   rm -rf dist/ build/ *.egg-info
   ```

2. **Build wheel and source distribution**
   ```bash
   python -m build
   ```

   This creates:
   - `dist/sensei_mcp-0.1.0-py3-none-any.whl` (wheel)
   - `dist/sensei-mcp-0.1.0.tar.gz` (source)

3. **Verify the build**
   ```bash
   ls -lh dist/
   ```

## Testing Locally

Before publishing, test the package locally:

```bash
# Install from local build
pip install dist/sensei_mcp-0.1.0-py3-none-any.whl

# Test it works
sensei-mcp
# Or
uvx --from . sensei-mcp
```

## Publishing to PyPI

### First-time setup

1. **Create PyPI account** at https://pypi.org/account/register/
2. **Create API token** at https://pypi.org/manage/account/token/
3. **Configure token** in `~/.pypirc`:
   ```ini
   [pypi]
   username = __token__
   password = pypi-...your-token-here...
   ```

### Publishing

1. **Upload to PyPI**
   ```bash
   twine upload dist/*
   ```

2. **Verify upload** at https://pypi.org/project/sensei-mcp/

### Test PyPI (Optional)

Test on Test PyPI first:

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ sensei-mcp
```

## Creating GitHub Release

After publishing to PyPI:

1. **Tag the release**
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

2. **Create GitHub release**
   - Go to https://github.com/amarodeabreu/sensei-mcp/releases/new
   - Choose tag: `v0.1.0`
   - Release title: `Sensei MCP v0.1.0`
   - Description: Changelog and key features

## Release Checklist

- [ ] All tests pass (`pytest tests/`)
- [ ] Version bumped in `pyproject.toml` and `__init__.py`
- [ ] CHANGELOG.md updated (if you have one)
- [ ] Clean build (`rm -rf dist/ && python -m build`)
- [ ] Tested locally (`pip install dist/*.whl`)
- [ ] Published to PyPI (`twine upload dist/*`)
- [ ] Git tagged (`git tag v0.1.0 && git push origin v0.1.0`)
- [ ] GitHub release created
- [ ] Tested installation (`uvx sensei-mcp`)

## Troubleshooting

### Upload fails with "File already exists"
- You can't re-upload the same version
- Bump version number and rebuild

### Import errors after installation
- Check package structure in `dist/` wheel
- Verify `packages = ["src/sensei_mcp"]` in `pyproject.toml`

### uvx can't find the package
- Wait a few minutes for PyPI index to update
- Try with explicit version: `uvx sensei-mcp==0.1.0`

## Automation (Future)

Consider setting up GitHub Actions for:
- Automated testing on PR
- Automated PyPI publishing on tag push
- Automated changelog generation

Example workflow: `.github/workflows/publish.yml`
