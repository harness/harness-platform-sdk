"""Harness Platform SDK.

A Python SDK for interacting with the Harness Platform API.
Provides unified access to all Harness APIs (Organizations, Projects,
Pipelines, Connectors, Secrets, and more) with built-in authentication,
scope management, pagination, and retry handling.
"""

from .authz import *
from .client import HarnessClient
from .config import HarnessConfig
from .exceptions import ApiError, AuthError, HarnessSdkError, ScopeNotSetError
from .iacm_api import *
from .idp_api import *
from .ng_api import *
from .pipeline_api import *
from .scope import Scope
from .template_api import *

__version__ = "1.0.0"

__all__ = [
    "HarnessClient",
    "HarnessConfig",
    "Scope",
    "HarnessSdkError",
    "ScopeNotSetError",
    "ApiError",
    "AuthError",
    "OrganizationsApi",
    "ProjectsApi",
    "ServicesApi",
    "RolesApi",
    "ResourceGroupsApi",
    "RoleAssignmentsApi",
    "ConnectorsApi",
    "SecretsApi",
    "InfrastructuresApi",
    "UserGroupsApi",
    "PipelinesV0Api",
    "InputSetsV0Api",
    "TriggersV0Api",
    "TemplatesV0Api",
    "VariablesApi",
    "ServiceOverridesApi",
    # Infrastructure as Code
    "WorkspacesApi",
    "WorkspaceApprovalsApi",
    "WorkspaceDefaultPipelinesApi",
    "WorkspaceStatesApi",
    "WorkspaceVariablesApi",
    # Internal Developer Portal
    "CatalogCustomPropertyApi",
    "EntityApi",
    "ScoreApi",
]
