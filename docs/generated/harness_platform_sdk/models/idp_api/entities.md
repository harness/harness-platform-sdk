Module harness_platform_sdk.models.idp_api.entities
===================================================
Entity resource models for Harness SDK.

Defines request/response models for entities CRUD operations.

Classes
-------

`EntityComponentCreateRequest(**data: Any)`
:   Component Specific Spec.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.models.idp_api.entities.EntityCreateRequest
    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `kind: str`
    :   The type of the None singleton.

    `lifecycle: str`
    :   The type of the None singleton.

    `metadata: dict | None`
    :   The type of the None singleton.

`EntityCreateRequest(**data: Any)`
:   Entity creation request model.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Descendants

    * harness_platform_sdk.models.idp_api.entities.EntityComponentCreateRequest
    * harness_platform_sdk.models.idp_api.entities.EntityResourceCreateRequest
    * harness_platform_sdk.models.idp_api.entities.EntitySystemCreateRequest
    * harness_platform_sdk.models.idp_api.entities.EntityWorkflowCreateRequest

    ### Class variables

    `account_identifier: str`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `owner: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `tags: list[str, str] | None`
    :   The type of the None singleton.

    `type: str`
    :   The type of the None singleton.

`EntityResourceCreateRequest(**data: Any)`
:   Resource Specific Spec.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.models.idp_api.entities.EntityCreateRequest
    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `kind: str`
    :   The type of the None singleton.

    `lifecycle: str`
    :   The type of the None singleton.

    `metadata: dict | None`
    :   The type of the None singleton.

`EntityResponse(**data: Any)`
:   Entity resource response model.
    
    Used for both get() and list() item responses.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `account_identifier: str`
    :   The type of the None singleton.

    `created_at: int`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str | None`
    :   The type of the None singleton.

    `project_identifier: str | None`
    :   The type of the None singleton.

    `tags: list[str, str] | None`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

`EntitySystemCreateRequest(**data: Any)`
:   System Specific Spec.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.models.idp_api.entities.EntityCreateRequest
    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `kind: str`
    :   The type of the None singleton.

    `lifecycle: str`
    :   The type of the None singleton.

    `metadata: dict | None`
    :   The type of the None singleton.

`EntityWorkflowCreateRequest(**data: Any)`
:   Workflow Specific Spec.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.models.idp_api.entities.EntityCreateRequest
    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `kind: str`
    :   The type of the None singleton.

    `links: list[dict, dict]`
    :   The type of the None singleton.

    `outputs: list[dict, dict]`
    :   The type of the None singleton.

    `parameters: list[dict, dict]`
    :   The type of the None singleton.

    `steps: list[dict, dict]`
    :   The type of the None singleton.