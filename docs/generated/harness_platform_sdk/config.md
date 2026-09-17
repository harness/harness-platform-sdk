Module harness_platform_sdk.config
==================================
Harness SDK configuration.

HarnessConfig holds all configuration needed for the SDK client.
API keys are never exposed in __repr__ or error messages.

Classes
-------

`HarnessConfig(**data: Any)`
:   Configuration for HarnessClient.
    
    Attributes:
        api_key: Harness API key for authentication.
        account_id: Harness account identifier.
        base_url: Base URL for Harness API (default: https://app.harness.io).
        timeout: Request timeout in seconds (default: 30.0).
        max_retries: Maximum number of connection retries (default: 3).
        retry_status_codes: HTTP status codes to retry on (default: [429, 503]).
        retry_enabled: Whether to retry failed requests (default: True).
        verify_ssl: Whether to verify SSL certificates (default: True).
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Class variables

    `account_id: str`
    :   The type of the None singleton.

    `api_key: str`
    :   The type of the None singleton.

    `base_url: str`
    :   The type of the None singleton.

    `max_retries: int`
    :   The type of the None singleton.

    `model_config`
    :   The type of the None singleton.

    `retry_enabled: bool`
    :   The type of the None singleton.

    `retry_status_codes: list[int]`
    :   The type of the None singleton.

    `timeout: float`
    :   The type of the None singleton.

    `verify_ssl: bool`
    :   The type of the None singleton.

    ### Methods

    `merge_duplicates(self, items, key='name')`
    :   Merge duplicate items by key, combining values.