"""Internal Developer Portal (IDP) API resources.

Provides APIs for managing catalog entities, scores, and custom properties
under the /idp/ path root.
"""

from .catalog_custom_properties import CatalogCustomPropertyApi
from .entities import EntityApi
from .scores import ScoreApi

__all__ = [
    "CatalogCustomPropertyApi",
    "EntityApi",
    "ScoreApi",
]
