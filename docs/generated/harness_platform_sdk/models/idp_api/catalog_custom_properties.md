Module harness_platform_sdk.models.idp_api.catalog_custom_properties
====================================================================
CatalogCustomProperty resource models for Harness SDK.

Defines request/response models for catalogcustomproperties CRUD operations.

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