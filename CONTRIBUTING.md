# Contributing to the Harness Platform SDK

Harness values the input and feedback from our community of users. This repository is open to fork and update via Pull Requests.

## Development Setup

The Harness Platform SDK is built with Python 3.11+ using Pydantic v2 and httpx. Follow the development workflow documented in the SDK.

## Directory Structure

- **`src/harness_platform_sdk/`** — Main SDK package
  - `client.py` — HarnessClient entry point
  - `*_api/` — Domain-organized API managers (ng_api, authz, pipeline_api, iacm_api, idp_api, template_api)
  - `models/` — Pydantic data models for requests/responses

- **`tests/`** — Test suite
  - `unit_tests/` — Unit tests for all APIs and models
  - `smoke/` — Smoke tests for production verification

- **`scripts/`** — Development tools
  - Build, testing, and documentation utilities

- **`docs/`** — Documentation
  - Generated API reference and style guides

## Contributor's Guides

### Adding a New Resource API

See [CONTRIBUTING_NEW_CLASSES.md](CONTRIBUTING_NEW_CLASSES.md) for the pattern used to implement new resource APIs.

## Style Guidelines

### Python Code Style

This project uses **Google-style docstrings** for all Python code. See [docs/DOCSTRING_STYLE.md](docs/DOCSTRING_STYLE.md) for the complete guide.

**Docstring Requirements:**
- All modules, classes, functions, and methods must have docstrings
- Use Google-style format with Args, Returns, Raises, and Example sections
- Docstring compliance is enforced via `ruff check --select D` in CI
- Examples in docstrings must be runnable and tested via doctest

**Quick Example:**
```python
def get_organization(self, org_id: str, scope: Scope | None = None) -> Organization:
    """Retrieve an organization by ID.

    Args:
        org_id: The organization identifier.
        scope: Scope for authentication (uses default if not provided).

    Returns:
        Organization object with full details.

    Raises:
        ScopeNotSetError: If scope cannot be resolved.
        ApiError: If the API request fails.

    Example:
        >>> client = HarnessClient(api_key="key", account_id="acct")
        >>> org = client.organizations.get_organization("my-org-id")
        >>> print(org.name)
    """
```

**Check locally before committing:**
```bash
# Lint docstrings
ruff check --select D src/harness_platform_sdk

# Run docstring examples
pytest --doctest-modules src/harness_platform_sdk -v
```

### Docstring Examples

**Requirements for examples in docstrings:**
- Must be executable (imports available, realistic parameters)
- Must use correct API (not pseudocode)
- Should demonstrate primary use case
- Can use `...` for output or long results

**Example:**
```python
>>> from harness_platform_sdk import HarnessClient
>>> client = HarnessClient(api_key="your_key", account_id="your_account")
>>> org = client.organizations.get_organization("org_id")
>>> print(org.name)  # doctest: +SKIP (requires real credentials)
```

**Note:** Use `# doctest: +SKIP` for examples requiring real credentials or external state

---

### General Style Guidelines

This project includes support for the auto-formatting tool known as [EditorConfig](https://EditorConfig.org) (File://.editorconfig). This is a plugin for most modern IDE platforms such as Visual Studio Code (preferred by the maintainers) and others. It is highly suggested to leverage this tool as part of your contributions as it will help ensure proper and clear spacing and formatting of files for consistency.

When contributing to this project, please adhere to the following guidelines:

- **Indentation:** 4 spaces for all Python files (enforced by ruff/black)
- **File endings:** Use linux-style line endings (`lf`) for all commits
- **Character set:** UTF-8 for all text files
- **Python formatting:** Run `ruff format` before committing

**Check locally before committing:**
```bash
# Format code
ruff format src/harness_platform_sdk tests

# Lint
ruff check src/harness_platform_sdk tests

# Type check
mypy src/harness_platform_sdk
```

## Code Quality

- **No external dependencies** without maintainer approval (keep the dependency tree minimal)
- **All code must be tested** — aim for ≥85% coverage
- **Type hints required** for all public APIs
- **Docstrings required** — use Google style (see `docs/DOCSTRING_STYLE.md`)

## Pull Request Process

1. Fork the repository and create a feature branch
2. Make your changes following the style guidelines
3. Write tests for new functionality
4. Run the full test suite: `pytest tests/ -v`
5. Ensure docstrings and type hints are complete
6. Submit a PR with a clear description of changes
7. Maintainers will review and merge when ready

## Questions?

If you have questions about contributing, please open an issue or reach out to the maintainers. We're here to help!
