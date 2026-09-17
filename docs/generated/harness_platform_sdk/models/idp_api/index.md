Module harness_platform_sdk.models.idp_api
==========================================
Harness models for /v1/idp_api resources.

Domain-specific request and response models for IDP managers.

Sub-modules
-----------
* harness_platform_sdk.models.idp_api.catalog_custom_properties
* harness_platform_sdk.models.idp_api.entities
* harness_platform_sdk.models.idp_api.scores

Classes
-------

`CatalogCustomPropertyCreateRequest(**data: Any)`
:   CatalogCustomProperty creation request model.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.models.idp_api.catalog_custom_properties.CatalogCustomPropertyResponse
    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

`CatalogCustomPropertyResponse(**data: Any)`
:   CatalogCustomProperty resource response model.
    
    Used for both get() and list() item responses.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Descendants

    * harness_platform_sdk.models.idp_api.catalog_custom_properties.CatalogCustomPropertyCreateRequest

    ### Class variables

    `account_identifier: str`
    :   The type of the None singleton.

    `catalog_property: str`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `kind: str`
    :   The type of the None singleton.

    `mode: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `value: Any`
    :   The type of the None singleton.

`CatalogCustomPropertyResponseByEntity(**data: Any)`
:   CatalogCustomProperty resource response model.
    
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

    `identifier: str`
    :   The type of the None singleton.

    `kind: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `properties: list[dict]`
    :   The type of the None singleton.

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

`ScoreResponse(**data: Any)`
:   Score resource response model.
    
    Used for both list() and get_aggregated_scores() item responses.
    
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

    `identifier: str`
    :   The type of the None singleton.

    `kind: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `overall_score: int`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `scorecard_scores: list[dict] | None`
    :   The type of the None singleton.

`ScoreSummaryResponse(**data: Any)`
:   Score summary resource response model.
    
    Used for get() item response.
    
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

    `checks_statuses: list[dict] | None`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `kind: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `recalibrate_info: dict | None`
    :   The type of the None singleton.

    `scorecard_identifier: str`
    :   The type of the None singleton.

    `scorecard_name: str`
    :   The type of the None singleton.

    `timestamp: int`
    :   The type of the None singleton.