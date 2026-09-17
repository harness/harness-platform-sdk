Module harness_platform_sdk.scope
=================================
Scope management for Harness SDK.

Scope is a frozen model representing the account/organization/project context
for API calls. Scopes are resolved once at the start of each request.

Classes
-------

`Scope(**data: Any)`
:   Represents the account/org/project scope for API requests.
    
    The scope is frozen — once created, it cannot be modified.
    The account_id is required; org and project are optional.
    
    Attributes:
        account_id: Harness account identifier (required).
        org: Harness organization identifier (optional).
        project: Harness project identifier (optional).
        pipeline: Harness pipeline identifier (optional).
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Class variables

    `account_id: str`
    :   The type of the None singleton.

    `model_config`
    :   The type of the None singleton.

    `org: str | None`
    :   The type of the None singleton.

    `pipeline: str | None`
    :   The type of the None singleton.

    `project: str | None`
    :   The type of the None singleton.