"""Template Management API resources.

Provides APIs for managing Harness templates under the /template/ path root.
"""

from .templates_v0 import TemplatesV0Api

__all__ = [
    "TemplatesV0Api",
]
