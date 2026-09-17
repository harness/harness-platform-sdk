Module harness_platform_sdk.exceptions
======================================
Harness SDK exception hierarchy.

All exceptions inherit from HarnessSdkError. API errors expose status_code,
body, and headers without exposing API keys.

Classes
-------

`ApiError(status_code: int, body: str, headers: dict[str, str], payload: dict | None = None)`
:   Raised for non-2xx API responses (other than 401/403).
    
    Exposes HTTP status code, response body, and headers without revealing
    API keys or other secrets.
    
    Attributes:
        status_code: HTTP status code from API response.
        body: Response body as string.
        headers: Response headers dictionary.
        payload: Parsed JSON payload (if response was JSON), else None.
    
    Initialize ApiError.
    
    Args:
        status_code: HTTP status code from failed request.
        body: Raw response body as string.
        headers: Response headers as dictionary.
        payload: Parsed JSON payload from response (optional).

    ### Ancestors (in MRO)

    * harness_platform_sdk.exceptions.HarnessSdkError
    * builtins.Exception
    * builtins.BaseException

    ### Descendants

    * harness_platform_sdk.exceptions.AuthError

`AuthError(status_code: int, body: str, headers: dict[str, str], payload: dict | None = None)`
:   Raised for 401 (Unauthorized) and 403 (Forbidden) responses.
    
    Indicates authentication or authorization failure. Typically means
    the API key is missing, invalid, expired, or lacks required permissions.
    
    Initialize ApiError.
    
    Args:
        status_code: HTTP status code from failed request.
        body: Raw response body as string.
        headers: Response headers as dictionary.
        payload: Parsed JSON payload from response (optional).

    ### Ancestors (in MRO)

    * harness_platform_sdk.exceptions.ApiError
    * harness_platform_sdk.exceptions.HarnessSdkError
    * builtins.Exception
    * builtins.BaseException

`HarnessSdkError(*args, **kwargs)`
:   Base exception for all Harness SDK errors.
    
    All SDK exceptions inherit from this class, allowing callers to catch
    any Harness-specific error with a single except clause.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

    ### Descendants

    * harness_platform_sdk.exceptions.ApiError
    * harness_platform_sdk.exceptions.ScopeNotSetError

`ScopeNotSetError(*args, **kwargs)`
:   Raised when required scope fields are not set or provided.
    
    Indicates that required scope fields (account_id, org, project, etc.)
    are missing and cannot be resolved from defaults.

    ### Ancestors (in MRO)

    * harness_platform_sdk.exceptions.HarnessSdkError
    * builtins.Exception
    * builtins.BaseException