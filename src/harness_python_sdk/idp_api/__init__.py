"""
Harness API resources under /authz/ path root.

"""

from .catalog_custom_properties import CatalogCustomPropertyApi
from .entities import EntityApi
from .scores import ScoreApi

__all__ = [
    "CatalogCustomPropertyApi",
    "EntityApi",
    "ScoreApi",
]
