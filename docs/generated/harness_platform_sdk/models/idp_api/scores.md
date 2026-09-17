Module harness_platform_sdk.models.idp_api.scores
=================================================
Score resource models for Harness SDK.

Defines request/response models for scores CRUD operations.

Classes
-------

`ScoreCreateRequest(**data: Any)`
:   Score creation request model.
    
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