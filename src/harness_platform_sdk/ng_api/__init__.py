"""Next Generation API resources.

Provides APIs for managing organizations, projects, connectors, secrets,
services, user groups, and other resources under the /ng/ path root.
"""

from .connectors import ConnectorsApi
from .environments_v2 import EnvironmentsV2Api
from .infrastructures import InfrastructuresApi
from .organizations import OrganizationsApi
from .projects import ProjectsApi
from .secrets import SecretsApi
from .service_overrides import ServiceOverridesApi
from .services import ServicesApi
from .user_groups import UserGroupsApi
from .variables import VariablesApi

__all__ = [
    "OrganizationsApi",
    "ProjectsApi",
    "ServicesApi",
    "ConnectorsApi",
    "SecretsApi",
    "EnvironmentsV2Api",
    "InfrastructuresApi",
    "UserGroupsApi",
    "VariablesApi",
    "ServiceOverridesApi",
]
