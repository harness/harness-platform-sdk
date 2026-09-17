# Docstring Style Guide

**Standard:** Google-style docstrings (PEP 257 + Google conventions)

This guide ensures consistent, LLM-friendly documentation across the Harness Platform SDK.

---

## Quick Examples

### Module-Level Docstring
```python
"""Harness SDK configuration management.

This module provides the HarnessConfig class for SDK initialization,
handling authentication, timeouts, retries, and SSL verification.
"""
```

### Class Docstring
```python
class HarnessClient:
    """Main SDK client for interacting with Harness APIs.

    Supports both context manager and explicit close() patterns.
    Handles HTTP requests, scope resolution, pagination, and error handling.

    Attributes:
        account_id: The Harness account identifier.
        base_url: Base URL for Harness API calls.
    """
```

### Function/Method Docstring
```python
def get_organization(
    self,
    org_id: str,
    scope: Scope | None = None,
) -> Organization:
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
        >>> client = HarnessClient(api_key="...", account_id="...")
        >>> org = client.get_organization("my-org-id")
        >>> print(org.name)
    """
```

---

## Detailed Format

### 1. Module Docstrings

**Required for:** All `.py` files  
**Location:** First statement in the file, before imports

**Format:**
```python
"""One-line summary of module purpose.

Longer description explaining what this module does, what classes/functions
it exports, and any important context for users.
"""
```

**Rules:**
- Start with one-line summary (under 80 chars, no period)
- Add blank line, then longer description if needed
- Mention main classes/functions if not obvious from name
- Include any prerequisites or setup requirements

---

### 2. Class Docstrings

**Required for:** All public classes  
**Location:** Immediately after `class` statement

**Format:**
```python
class MyClass:
    """One-line summary of class purpose.

    Longer description of what this class does, its role, usage patterns.
    Mention important methods if not obvious.

    Attributes:
        attr1: Description of first attribute.
        attr2: Description of second attribute.

    Example:
        >>> obj = MyClass(param="value")
        >>> result = obj.method()
    """
```

**Rules:**
- Start with one-line summary
- Add blank line, then longer description
- **Attributes section:** List all public attributes with type and description
- **Example section:** Include at least one runnable example for entry points

---

### 3. Function/Method Docstrings

**Required for:** All public functions and methods  
**Location:** Immediately after `def` statement

**Format:**
```python
def my_function(param1: str, param2: int | None = None) -> dict:
    """One-line summary of function purpose.

    Longer description of what the function does, its behavior,
    any side effects, or important implementation details.

    Args:
        param1: Description of first parameter.
        param2: Description of second parameter. Defaults to None.

    Returns:
        Description of return value, including its type and structure.

    Raises:
        ValueError: When param1 is empty.
        RuntimeError: When internal operation fails.

    Example:
        >>> result = my_function("hello", 42)
        >>> print(result)
        {'status': 'ok'}
    """
```

**Rules:**
- Start with one-line summary
- Add blank line, then longer description (optional but recommended)
- **Args section:**
  - List every parameter (even if has default)
  - Include type in description if not obvious from annotation
  - Note defaults: "Defaults to None." or similar
  - Mark optional params: "Optional. Defaults to X."
- **Returns section:**
  - Describe the return value and its structure
  - Include important context about what it represents
- **Raises section:**
  - List all exceptions that function can raise
  - Include condition when exception is raised
  - Do NOT list generic base exceptions (Exception, BaseException)
- **Example section:**
  - Include for all public entry points
  - Make examples copy-paste-ready (no placeholders)
  - Show realistic use case

---

### 4. Property Docstrings

```python
@property
def my_property(self) -> str:
    """One-line description of what property returns.

    Longer description if behavior is non-obvious or has side effects.
    """
```

**Rules:**
- Treat like method; describe return value (no Args/Returns sections)
- Keep brief; properties should be self-explanatory

---

### 5. Exception Class Docstrings

```python
class MyError(Exception):
    """Raised when specific error condition occurs.

    This exception is raised when X happens. Typically indicates Y.
    """

    def __init__(self, message: str, code: int):
        """Initialize MyError.

        Args:
            message: Error message.
            code: HTTP status code or error code.
        """
        super().__init__(message)
        self.code = code
```

**Rules:**
- Describe when/why exception is raised
- Document all `__init__` parameters in Args section
- Reference common scenarios or root causes if helpful

---

## Style Rules

### Section Order
1. One-line summary
2. Blank line
3. Longer description (optional)
4. Blank line (if has sections below)
5. Attributes / Args / Returns / Raises / Example sections (in this order)

### Formatting
- Use **backticks** for code: `` `variable_name` ``
- Use **bold** for emphasis: `**important concept**`
- Use bullet points for lists (see example below)
- Keep line length ≤ 88 characters (matches black formatter)
- Indent continuation lines by 4 spaces

### Common Patterns

#### Describing Optional Parameters
```
param: Description. Defaults to None.
```

#### Describing Enums
```python
mode: Execution mode; one of 'sync', 'async', 'streaming'. Defaults to 'sync'.
```

#### Describing Return Type (when complex)
```python
dict: Response object with keys: 'id' (str), 'status' (str), 'data' (list).
```

#### Describing Exceptions with Context
```python
ApiError: If the API request fails. Includes HTTP status and error message.
ScopeNotSetError: If scope cannot be resolved from parameters or defaults.
```

---

## LLM-Ready Best Practices

These docstrings are designed to be parseable by language models and documentation tools:

1. **Self-Contained:** Each docstring reads as standalone; no "see above" references
2. **Explicit Types:** Type hints in code, types described in docstring
3. **Complete Args/Returns:** Every parameter and return value documented
4. **Runnable Examples:** Copy-paste-ready code blocks (no pseudocode)
5. **Error Context:** Why exceptions are raised, not just what they are
6. **Clear Hierarchy:** Summary → details → sections, never buried

---

## Enforcement

This style is enforced via ruff linting rules:

**Rules enabled:**
- `D100`: Module docstring required
- `D101`: Class docstring required
- `D102`: Public method docstring required
- `D103`: Function docstring required
- `D104`: Package docstring required
- `D105`: Magic method docstring (exempt for common methods)
- `D107`: Function docstring required (private)

**Run locally:**
```bash
ruff check --select D src/harness_platform_sdk
```

**CI Enforcement:**
Every commit must pass: `ruff check --select D`

---

## When Exceptions Are OK

These are NOT required to have docstrings:

- `__init__`, `__repr__`, `__str__` (if trivial)
- `__enter__`, `__exit__` (standard context manager patterns)
- Inherited methods that are unchanged

Use judgment: if behavior is non-obvious, add a docstring anyway.

---

## Examples from SDK

### Good: Complete Docstring
[See: src/harness_platform_sdk/client.py — HarnessClient class]

```python
class HarnessClient:
    """Main SDK client for interacting with Harness APIs.

    The client supports keyword argument construction for convenience:
        client = HarnessClient(api_key="...", account_id="...")

    Or via explicit config:
        config = HarnessConfig(api_key="...", account_id="...")
        client = HarnessClient(config=config)

    Supports both context manager and explicit close():
        with HarnessClient(...) as client:
            ...

        client = HarnessClient(...)
        try:
            ...
        finally:
            client.close()
    """
```

### Good: Method with Full Documentation
[See: src/harness_platform_sdk/client.py — _get method]

```python
def _get(
    self,
    endpoint: str,
    response_type: type[T],
    **kwargs: Any,
) -> T:
    """Execute a GET request and deserialize response.

    Args:
        endpoint: API endpoint path (e.g., '/organizations').
        response_type: Pydantic model class for deserialization.
        **kwargs: Additional arguments passed to _request (e.g., params, headers).

    Returns:
        Deserialized response object of type response_type.

    Raises:
        ScopeNotSetError: If scope cannot be resolved from kwargs.
        ApiError: If API request fails.
    """
```

---

## References

- [PEP 257: Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- [Ruff Docstring Rules](https://docs.astral.sh/ruff/rules/#pydocstyle-d)

