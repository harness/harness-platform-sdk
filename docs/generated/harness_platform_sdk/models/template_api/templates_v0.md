Module harness_platform_sdk.models.template_api.templates_v0
============================================================
TemplateV0 resource models for Harness SDK.

Defines request/response models for template CRUD operations.

Classes
-------

`TemplateV0Core(**data: Any)`
:   Model for TemplateV0Core.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Descendants

    * harness_platform_sdk.models.template_api.templates_v0.TemplateV0CreateRequest
    * harness_platform_sdk.models.template_api.templates_v0.TemplateV0Response

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

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

`TemplateV0CreateRequest(**data: Any)`
:   TemplateV0 creation request model.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.models.template_api.templates_v0.TemplateV0Core
    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `git_details: dict`
    :   The type of the None singleton.

    `store_type: str`
    :   The type of the None singleton.

    `template_entity_type: str`
    :   The type of the None singleton.

    `template_spec: dict`
    :   The type of the None singleton.

    `version_label: str`
    :   The type of the None singleton.

`TemplateV0Response(**data: Any)`
:   TemplateV0 resource response model.
    
    Used for both get() and list() item responses.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.models.template_api.templates_v0.TemplateV0Core
    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `child_type: str`
    :   The type of the None singleton.

    `entity_validity_details: dict`
    :   The type of the None singleton.

    `git_details: dict`
    :   The type of the None singleton.

    `is_inline_hc_entity: bool`
    :   The type of the None singleton.

    `stable_template: bool`
    :   The type of the None singleton.

    `store_type: str`
    :   The type of the None singleton.

    `template_entity_type: str`
    :   The type of the None singleton.

    `template_scope: str`
    :   The type of the None singleton.

    `template_spec: dict`
    :   The type of the None singleton.

    `version: int`
    :   The type of the None singleton.

    `version_label: str`
    :   The type of the None singleton.

    `yaml_version: int`
    :   The type of the None singleton.