"""
Base model for all Harness SDK domain models.

HarnessModel is the base class for all request/response models in the SDK.
It allows extra fields and populates by name or alias.
"""

from pydantic import BaseModel, ConfigDict, Field, AliasChoices


class HarnessModel(BaseModel):
    """Base model for Harness SDK domain models.

    Allows extra fields (for forward compatibility) and supports
    population by field name or alias.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)
