# Pagination Inventory: Harness API Endpoints

Generated: 2026-04-01 16:44:40

Total endpoints analyzed: 940


## Summary


| Domain | Total Endpoints | OFFSET | CURSOR | UNKNOWN |

|--------|-----------------|--------|--------|----------|
| access_control | 15 | 1 | 0 | 14 |
| audit | 8 | 1 | 0 | 7 |
| cloud | 5 | 0 | 0 | 5 |
| connectors | 22 | 1 | 0 | 21 |
| cost | 84 | 6 | 0 | 78 |
| environments | 11 | 5 | 0 | 6 |
| governance | 4 | 4 | 0 | 0 |
| infrastructure | 15 | 6 | 0 | 9 |
| organizations | 17 | 0 | 0 | 17 |
| other | 583 | 113 | 0 | 470 |
| pipelines | 47 | 14 | 0 | 33 |
| projects | 123 | 24 | 0 | 99 |
| secrets | 6 | 0 | 0 | 6 |


---

## Access Control


| Endpoint / OperationId | Path | Method | Pagination Style | Evidence |

|------------------------|------|--------|------------------|----------|

| getPermissionList | /authz/api/permissions | GET | UNKNOWN | No pagination fields detected |
| getPermissionResourceTypesList | /authz/api/permissions/resourcetypes | GET | UNKNOWN | No pagination fields detected |
| getRoleList | /authz/api/roles | GET | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getUserGroupList | /ng/api/user-groups | GET | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getBatchUsersGroupList | /ng/api/user-groups/batch | POST | UNKNOWN | No pagination fields detected |
| getFilteredUserGroupsList | /ng/api/user-groups/filter | POST | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getInheritingChildScopeList | /ng/api/user-groups/{identifier}/scopes | GET | UNKNOWN | No pagination fields detected |
| getUserListInUserGroup | /ng/api/user-groups/{identifier}/users | POST | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| users#listActiveUsers | /v1/org/users/list | POST | UNKNOWN | No pagination fields detected |
| contributors#getSchema | /v1/org/users/schema | GET | UNKNOWN | No pagination fields detected |
| contributors#getActiveVersions | /v1/org/users/versions | GET | OFFSET | page, page_size |
| list-roles-project | /v1/orgs/{org}/projects/{project}/roles | GET | UNKNOWN | No pagination fields detected |
| list-roles-org | /v1/orgs/{org}/roles | GET | UNKNOWN | No pagination fields detected |
| list-roles-acc | /v1/roles | GET | UNKNOWN | No pagination fields detected |
| get-roles-count | /v1/roles/count | GET | UNKNOWN | No pagination fields detected |


---

## Audit


| Endpoint / OperationId | Path | Method | Pagination Style | Evidence |

|------------------------|------|--------|------------------|----------|

| getAuditFilterList | /audit/api/auditFilters | GET | OFFSET | pageSize, pageIndex |
| updateAuditFilter | /audit/api/auditFilters | PUT | UNKNOWN | No pagination fields detected |
| postAuditFilter | /audit/api/auditFilters | POST | UNKNOWN | No pagination fields detected |
| getAuditFilter | /audit/api/auditFilters/{identifier} | GET | UNKNOWN | No pagination fields detected |
| deleteAuditFilter | /audit/api/auditFilters/{identifier} | DELETE | UNKNOWN | No pagination fields detected |
| getYamlDiff | /audit/api/auditYaml | GET | UNKNOWN | No pagination fields detected |
| getAuditEventList | /audit/api/audits/list | POST | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getAuditEventListV2 | /audit/api/audits/listV2 | POST | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |


---

## Cloud


| Endpoint / OperationId | Path | Method | Pagination Style | Evidence |

|------------------------|------|--------|------------------|----------|

| getLegacyKubernetesChaosInfraStats | /gateway/chaos/manager/api/rest/kubernetes/infra/stats | GET | UNKNOWN | No pagination fields detected |
| getLegacyKubernetesChaosInfraVersionDetails | /gateway/chaos/manager/api/rest/kubernetes/infra/version | GET | UNKNOWN | No pagination fields detected |
| listLegacyKubernetesChaosInfra | /gateway/chaos/manager/api/rest/kubernetes/infras | POST | UNKNOWN | No pagination fields detected |
| k8sCmdFlags | /ng/api/servicesV2/k8s/command-flags | GET | UNKNOWN | No pagination fields detected |
| get-v1-releaseDetails | /v1/kubernetes/releases/service-mapping | GET | UNKNOWN | No pagination fields detected |


---

## Connectors


| Endpoint / OperationId | Path | Method | Pagination Style | Evidence |

|------------------------|------|--------|------------------|----------|

| getConnectorForInfra | /gateway/chaos/manager/api/rest/v2/infrastructure/{identity}/connector | GET | UNKNOWN | No pagination fields detected |
| module-registry#list-connectors | /iacm/api/modules/connectors | GET | UNKNOWN | No pagination fields detected |
| getConnectorList | /ng/api/connectors | GET | OFFSET | pageSize, pageIndex |
| getConnectorCatalogue | /ng/api/connectors/catalogue | GET | UNKNOWN | No pagination fields detected |
| getCCMK8SConnectorList | /ng/api/connectors/ccmK8sList | POST | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getAllAllowedFieldValues | /ng/api/connectors/fieldValues | GET | UNKNOWN | No pagination fields detected |
| getConnectorListV2 | /ng/api/connectors/listV2 | POST | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| listConnectorByFQN | /ng/api/connectors/listbyfqn | POST | UNKNOWN | No pagination fields detected |
| getConnectorStatistics | /ng/api/connectors/stats | GET | UNKNOWN | No pagination fields detected |
| validateTheIdentifierIsUnique | /ng/api/connectors/validateUniqueIdentifier | GET | UNKNOWN | No pagination fields detected |
| getGcpProjects | /ng/api/connectors/{connectorRef}/gcp-projects | GET | UNKNOWN | No pagination fields detected |
| get-connector-info | /v1/connector-info | GET | UNKNOWN | No pagination fields detected |
| get-account-scoped-connectors | /v1/connectors | GET | UNKNOWN | No pagination fields detected |
| get-connectors-info | /v1/connectors-info | GET | UNKNOWN | No pagination fields detected |
| test-account-scoped-connector | /v1/connectors/{connector}/test-connection | GET | UNKNOWN | No pagination fields detected |
| get-org-scoped-connectors | /v1/orgs/{org}/connectors | GET | UNKNOWN | No pagination fields detected |
| test-org-scoped-connector | /v1/orgs/{org}/connectors/{connector}/test-connection | GET | UNKNOWN | No pagination fields detected |
| get-project-scoped-connectors | /v1/orgs/{org}/projects/{project}/connectors | GET | UNKNOWN | No pagination fields detected |
| test-project-scoped-connector | /v1/orgs/{org}/projects/{project}/connectors/{connector}/test-connection | GET | UNKNOWN | No pagination fields detected |
| list-project-scoped-rancher-clusters-using-connector | /v1/orgs/{org}/projects/{project}/rancher/connectors/{connector}/clusters | GET | UNKNOWN | No pagination fields detected |
| list-org-scoped-rancher-clusters-using-connector | /v1/orgs/{org}/rancher/connectors/{connector}/clusters | GET | UNKNOWN | No pagination fields detected |
| list-account-scoped-rancher-clusters-using-connector | /v1/rancher/connectors/{connector}/clusters | GET | UNKNOWN | No pagination fields detected |


---

## Cost


| Endpoint / OperationId | Path | Method | Pagination Style | Evidence |

|------------------------|------|--------|------------------|----------|

| listAnomalies | /ccm/api/anomaly | POST | UNKNOWN | No pagination fields detected |
| anomalyFilterValues | /ccm/api/anomaly/filter-values | POST | UNKNOWN | No pagination fields detected |
| listIgnoredAnomalies | /ccm/api/anomaly/listIgnoredAnomalies | POST | UNKNOWN | No pagination fields detected |
| listPerspectiveAnomalies | /ccm/api/anomaly/perspective/{perspectiveId} | POST | UNKNOWN | No pagination fields detected |
| listAnomalyComments | /ccm/api/anomaly/v2/comment | GET | UNKNOWN | No pagination fields detected |
| getAnomalyDetails | /ccm/api/anomaly/v2/drill-down | GET | UNKNOWN | No pagination fields detected |
| getAnomalyCostTimeSeriesData | /ccm/api/anomaly/v2/drill-down/cost/time-series | GET | UNKNOWN | No pagination fields detected |
| getAnomalyForecastCostTimeSeriesData | /ccm/api/anomaly/v2/drill-down/forecast/cost/time-series | GET | UNKNOWN | No pagination fields detected |
| getAnomalyResourceList | /ccm/api/anomaly/v2/drill-down/list | GET | UNKNOWN | No pagination fields detected |
| getAnomalyResourceCostTimeSeriesData | /ccm/api/anomaly/v2/drill-down/resource/cost/time-series | GET | UNKNOWN | No pagination fields detected |
| getAnomaliesList | /ccm/api/anomaly/v2/list | POST | UNKNOWN | No pagination fields detected |
| listBIDashboards | /ccm/api/bi-dashboards | GET | UNKNOWN | No pagination fields detected |
| listBudgetGroups | /ccm/api/budgetGroups | GET | UNKNOWN | No pagination fields detected |
| getBudgetAndBudgetGroupsList | /ccm/api/budgetGroups/summary | GET | UNKNOWN | No pagination fields detected |
| listBudgets | /ccm/api/budgets | GET | UNKNOWN | No pagination fields detected |
| checkBulkBudgetJobStatus | /ccm/api/budgets/bulk/check-job-status | GET | UNKNOWN | No pagination fields detected |
| budgetFilterValues | /ccm/api/budgets/filter-values | POST | UNKNOWN | No pagination fields detected |
| listBudgetsForPerspective | /ccm/api/budgets/perspectiveBudgets | GET | UNKNOWN | No pagination fields detected |
| listBudgetAlertThresholds | /ccm/api/budgets/subscribe/list | GET | UNKNOWN | No pagination fields detected |
| getCostDetails | /ccm/api/budgets/{id}/costDetails | GET | UNKNOWN | No pagination fields detected |
| getBusinessMappingList | /ccm/api/business-mapping | GET | OFFSET | offset, limit |
| getBusinessMappingForFilterPanel | /ccm/api/business-mapping/filter-panel | GET | UNKNOWN | No pagination fields detected |
| getCostSettings | /ccm/api/cost-settings | GET | UNKNOWN | No pagination fields detected |
| listProvidersFileInfo | /ccm/api/externaldata/provider/filesinfo | POST | UNKNOWN | No pagination fields detected |
| getSignedUrl | /ccm/api/externaldata/signedurl | GET | UNKNOWN | No pagination fields detected |
| CcmgetFilterList | /ccm/api/filters | GET | OFFSET | pageSize, pageIndex |
| CcmupdateFilter | /ccm/api/filters | PUT | UNKNOWN | No pagination fields detected |
| CcmpostFilter | /ccm/api/filters | POST | UNKNOWN | No pagination fields detected |
| CcmgetFilter | /ccm/api/filters/{identifier} | GET | UNKNOWN | No pagination fields detected |
| CcmdeleteFilter | /ccm/api/filters/{identifier} | DELETE | UNKNOWN | No pagination fields detected |
| GovernanceAlertRules | /ccm/api/governance/alert/list | GET | UNKNOWN | No pagination fields detected |
| GovernanceResourceTypes | /ccm/api/governance/alert/resourceTypes | GET | UNKNOWN | No pagination fields detected |
| enforcementDetails | /ccm/api/governance/enforcement/details | GET | UNKNOWN | No pagination fields detected |
| getRuleEnforcement | /ccm/api/governance/enforcement/list | GET | OFFSET | pageSize, page |
| enforcementRecommendationDetails | /ccm/api/governance/enforcementRecommendation/details | GET | UNKNOWN | No pagination fields detected |
| ruleEnforcementRecommendations | /ccm/api/governance/enforcementRecommendation/list | GET | OFFSET | pageSize, page |
| getRuleExecutionsFilterValues | /ccm/api/governance/execution/filter-value | GET | UNKNOWN | No pagination fields detected |
| getRuleExecutionTagFilterValues | /ccm/api/governance/execution/filter-value/tags | POST | UNKNOWN | No pagination fields detected |
| governanceTargetList | /ccm/api/governance/governanceTargetList | GET | UNKNOWN | No pagination fields detected |
| totalActiveEnforcements | /ccm/api/governance/overview/totalActiveEnforcements | GET | UNKNOWN | No pagination fields detected |
| totalEvaluations | /ccm/api/governance/overview/totalEvaluations | GET | UNKNOWN | No pagination fields detected |
| totalNewEnforcementRecommendations | /ccm/api/governance/overview/totalNewEnforcementRecommendations | GET | UNKNOWN | No pagination fields detected |
| totalRealisedSavingsGrouped | /ccm/api/governance/overview/totalRealisedSavingsGrouped | GET | UNKNOWN | No pagination fields detected |
| getPromptResources | /ccm/api/governance/promptResources | GET | UNKNOWN | No pagination fields detected |
| getPromptRules | /ccm/api/governance/promptRules | GET | UNKNOWN | No pagination fields detected |
| recommendationHealth | /ccm/api/governance/recommendationHealth | GET | UNKNOWN | No pagination fields detected |
| listGovernanceRecommendationHealth | /ccm/api/governance/recommendationHealth/list | POST | UNKNOWN | No pagination fields detected |
| regions | /ccm/api/governance/regions | GET | UNKNOWN | No pagination fields detected |
| costCoRelationSupportedResources | /ccm/api/governance/rule/costCoRelationSupportedResources | GET | UNKNOWN | No pagination fields detected |
| getPotentialRulesForRecommendation | /ccm/api/governance/rule/potentialRulesForRecommendation | GET | UNKNOWN | No pagination fields detected |
| governanceRuleSchema | /ccm/api/governance/ruleSchema | GET | UNKNOWN | No pagination fields detected |
| listRuleSets | /ccm/api/governance/ruleSet/list | POST | UNKNOWN | No pagination fields detected |
| listNotificationSettingsV2 | /ccm/api/notificationSetting/v2 | GET | UNKNOWN | No pagination fields detected |
| getCCMOverview | /ccm/api/overview | GET | UNKNOWN | No pagination fields detected |
| getPerspective | /ccm/api/perspective | GET | UNKNOWN | No pagination fields detected |
| getAllPerspectives | /ccm/api/perspective/getAllPerspectives | GET | OFFSET | pageSize, pageNo |
| getLastPeriodCost_1 | /ccm/api/perspective/lastPeriodCost | GET | UNKNOWN | No pagination fields detected |
| getLastYearMonthlyCost | /ccm/api/perspective/lastYearMonthlyCost | GET | UNKNOWN | No pagination fields detected |
| getFolders | /ccm/api/perspectiveFolders | GET | UNKNOWN | No pagination fields detected |
| getAllFolderPerspectives | /ccm/api/perspectiveFolders/{folderId}/perspectives | GET | UNKNOWN | No pagination fields detected |
| getAllReports | /ccm/api/perspectiveReport/getAllReports | POST | UNKNOWN | No pagination fields detected |
| listCostCategoryJiraMapping | /ccm/api/recommendation/cost-category/jira-mapping | GET | UNKNOWN | No pagination fields detected |
| azureVmRecommendationDetail | /ccm/api/recommendation/details/azure-vm | GET | UNKNOWN | No pagination fields detected |
| ec2RecommendationDetail | /ccm/api/recommendation/details/ec2-instance | GET | UNKNOWN | No pagination fields detected |
| ecsRecommendationDetail | /ccm/api/recommendation/details/ecs-service | GET | UNKNOWN | No pagination fields detected |
| nodeRecommendationDetail | /ccm/api/recommendation/details/node-pool | GET | UNKNOWN | No pagination fields detected |
| workloadRecommendationDetail | /ccm/api/recommendation/details/workload | GET | UNKNOWN | No pagination fields detected |
| getRecommendationsIgnoreList | /ccm/api/recommendation/ignore-list | GET | UNKNOWN | No pagination fields detected |
| addRecommendationsIgnoreList | /ccm/api/recommendation/ignore-list/add | POST | UNKNOWN | No pagination fields detected |
| removeRecommendationsIgnoreList | /ccm/api/recommendation/ignore-list/remove | POST | UNKNOWN | No pagination fields detected |
| getMappedProjects | /ccm/api/recommendation/jira/mapped-projects | GET | UNKNOWN | No pagination fields detected |
| getResolutionCodes | /ccm/api/recommendation/jira/resolution-code | GET | UNKNOWN | No pagination fields detected |
| getJiraStatuses | /ccm/api/recommendation/jira/statuses | GET | UNKNOWN | No pagination fields detected |
| recommendationFilterValues | /ccm/api/recommendation/overview/filter-values | POST | UNKNOWN | No pagination fields detected |
| listRecommendations | /ccm/api/recommendation/overview/list | POST | UNKNOWN | No pagination fields detected |
| getRecommendationPreferences | /ccm/api/recommendation/preference | GET | UNKNOWN | No pagination fields detected |
| getRecommendationPresets | /ccm/api/recommendation/preset | GET | UNKNOWN | No pagination fields detected |
| getServiceNowServiceRequestFields | /ccm/api/recommendation/servicenow/serviceRequestFields | GET | UNKNOWN | No pagination fields detected |
| getRecommendationTags | /ccm/api/recommendation/tags | GET | UNKNOWN | No pagination fields detected |
| getTagsForFilterPanel | /ccm/api/recommendation/tags/filter-panel | GET | OFFSET | offset, limit |
| getUnitMetric | /ccm/api/unit-metric | GET | UNKNOWN | No pagination fields detected |
| CcmgetCDLicenseUsageForServiceInstances | /ccm/api/usage/CD/serviceInstancesLicense | GET | UNKNOWN | No pagination fields detected |
| CcmgetCDLicenseUsageForServices | /ccm/api/usage/CD/servicesLicense | GET | UNKNOWN | No pagination fields detected |
| CcmdownloadActiveServiceCSVReport | /ccm/api/usage/cd/active-services/csv/download | GET | UNKNOWN | No pagination fields detected |


---

## Environments


| Endpoint / OperationId | Path | Method | Pagination Style | Evidence |

|------------------------|------|--------|------------------|----------|

| Environment#Schemas | /api/environments/schemas | GET | UNKNOWN | No pagination fields detected |
| getEnvironments | /cv/api/monitored-service/environments | GET | UNKNOWN | No pagination fields detected |
| getSLOAssociatedEnvironmentIdentifiers | /cv/api/slo-dashboard/environment-identifiers | GET | OFFSET | pageNumber, pageSize |
| getEnvironmentGroupList | /ng/api/environmentGroup/list | POST | OFFSET | size, page |
| getEnvironmentList | /ng/api/environmentsV2 | GET | OFFSET | size, page |
| getEnvironmentAccessList | /ng/api/environmentsV2/list/access | GET | OFFSET | size, page |
| getServiceOverridesList | /ng/api/environmentsV2/serviceOverrides | GET | OFFSET | size, page |
| get-account-scoped-environments | /v1/environments | GET | UNKNOWN | No pagination fields detected |
| get-org-scoped-environments | /v1/orgs/{org}/environments | GET | UNKNOWN | No pagination fields detected |
| get-environments | /v1/orgs/{org}/projects/{project}/environments | GET | UNKNOWN | No pagination fields detected |
| getEnvironmentListForRemediation | /v1/orgs/{org}/projects/{project}/remediations/{remediation}/artifacts/{artifact}/environments | GET | UNKNOWN | No pagination fields detected |


---

## Governance


| Endpoint / OperationId | Path | Method | Pagination Style | Evidence |

|------------------------|------|--------|------------------|----------|

| policies#list | /pm/api/v1/policies | GET | OFFSET | per_page, page |
| policies#list_policy_sets | /pm/api/v1/policies/{identifier}/policysets | GET | OFFSET | per_page, page |
| policysets#list | /pm/api/v1/policysets | GET | OFFSET | per_page, page |
| policysets#listall | /pm/api/v1/policysets/all | GET | OFFSET | per_page, page |


---

## Infrastructure


| Endpoint / OperationId | Path | Method | Pagination Style | Evidence |

|------------------------|------|--------|------------------|----------|

| Infrastructure#List | /api/infrastructures | GET | OFFSET | offset, limit |
| Infrastructure#ListExecutions | /api/infrastructures/{id}/executions | GET | OFFSET | offset, limit |
| Infrastructure#ListSpecs | /api/infrastructures/{id}/specs | GET | OFFSET | offset, limit |
| listInfraV2 | /gateway/chaos/manager/api/rest/v2/infrastructures | POST | OFFSET | limit, page |
| listChaosEnabledInfraV2 | /gateway/chaos/manager/api/rest/v2/infrastructures/chaos-enabled | POST | OFFSET | limit, page |
| listApplication | /gateway/chaos/manager/api/rest/v2/infrastructures/{infrastructureIdentity}/applications | GET | UNKNOWN | No pagination fields detected |
| listFunction | /gateway/chaos/manager/api/rest/v2/infrastructures/{infrastructureIdentity}/applications/{applicationIdentity}/functions | GET | UNKNOWN | No pagination fields detected |
| getInfraToken | /gateway/chaos/manager/api/rest/v2/infrastructures/{infrastructureIdentity}/token | GET | UNKNOWN | No pagination fields detected |
| getInfrastructureList | /ng/api/infrastructures | GET | OFFSET | size, page |
| get-account-scoped-infrastructures | /v1/environments/{environment}/infrastructures | GET | UNKNOWN | No pagination fields detected |
| get-org-scoped-infrastructures | /v1/orgs/{org}/environments/{environment}/infrastructures | GET | UNKNOWN | No pagination fields detected |
| get-infrastructures | /v1/orgs/{org}/projects/{project}/environments/{environment}/infrastructures | GET | UNKNOWN | No pagination fields detected |
| list-project-scoped-rancher-clusters-using-env-and-infra | /v1/orgs/{org}/projects/{project}/rancher/environments/{environment}/infrastructure-definitions/{infrastructure-definition}/clusters | GET | UNKNOWN | No pagination fields detected |
| list-org-scoped-rancher-clusters-using-env-and-infra | /v1/orgs/{org}/rancher/environments/{environment}/infrastructure-definitions/{infrastructure-definition}/clusters | GET | UNKNOWN | No pagination fields detected |
| list-account-scoped-rancher-clusters-using-env-and-infra | /v1/rancher/environments/{environment}/infrastructure-definitions/{infrastructure-definition}/clusters | GET | UNKNOWN | No pagination fields detected |


---

## Organizations


| Endpoint / OperationId | Path | Method | Pagination Style | Evidence |

|------------------------|------|--------|------------------|----------|

| variable_sets#list-variable-set-references-org-level | /iacm/api/orgs/{org}/variable-set/{identifier}/references | GET | UNKNOWN | No pagination fields detected |
| variable_sets#list-variable-sets-org-level | /iacm/api/orgs/{org}/variable-sets | GET | UNKNOWN | No pagination fields detected |
| getOrganizationList | /ng/api/organizations | GET | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getTasOrganizations | /ng/api/tas/organizations | GET | UNKNOWN | No pagination fields detected |
| get-organizations | /v1/orgs | GET | UNKNOWN | No pagination fields detected |
| get-org-scoped-certificates | /v1/orgs/{org}/certificates | GET | UNKNOWN | No pagination fields detected |
| list-org-gitx-webhook-events | /v1/orgs/{org}/gitx-webhook-events | GET | UNKNOWN | No pagination fields detected |
| list-org-gitx-webhooks | /v1/orgs/{org}/gitx-webhooks | GET | UNKNOWN | No pagination fields detected |
| list-notification-channels-org | /v1/orgs/{org}/notification-channels | GET | UNKNOWN | No pagination fields detected |
| list-notification-rules-org | /v1/orgs/{org}/notification-rules | GET | UNKNOWN | No pagination fields detected |
| list-resource-groups-org | /v1/orgs/{org}/resource-groups | GET | UNKNOWN | No pagination fields detected |
| get-org-scoped-role-assignments | /v1/orgs/{org}/role-assignments | GET | UNKNOWN | No pagination fields detected |
| get-org-scoped-services | /v1/orgs/{org}/services | GET | UNKNOWN | No pagination fields detected |
| get-org-scoped-primary-manifests | /v1/orgs/{org}/services/{service}/primary-manifests | GET | UNKNOWN | No pagination fields detected |
| get-templates-list-org | /v1/orgs/{org}/templates | GET | UNKNOWN | No pagination fields detected |
| get-org-templates-inputs-schema | /v1/orgs/{org}/templates/{template}/versions/{version}/inputs-schema | GET | UNKNOWN | No pagination fields detected |
| list-org-webhooks | /v1/orgs/{org}/webhooks/list | POST | UNKNOWN | No pagination fields detected |


---

## Other


| Endpoint / OperationId | Path | Method | Pagination Style | Evidence |

|------------------------|------|--------|------------------|----------|

| Instance#List | /api/instances | GET | OFFSET | offset, limit |
| Instance#ListEvents | /api/instances/events | GET | OFFSET | offset, limit |
| getAccessControlList | /authz/api/acl | POST | UNKNOWN | No pagination fields detected |
| getAclCount | /authz/api/acl/get-acl-count | GET | UNKNOWN | No pagination fields detected |
| getResourceTypes | /authz/api/resourcetype | GET | UNKNOWN | No pagination fields detected |
| getRoleAssignmentList | /authz/api/roleassignments | GET | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getRoleAssignmentAggregateList | /authz/api/roleassignments/aggregate | POST | UNKNOWN | No pagination fields detected |
| getFilteredRoleAssignmentList | /authz/api/roleassignments/filter | POST | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getFilteredRoleAssignmentByScopeList | /authz/api/roleassignments/v2/filter | POST | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getResourceGroupListV2 | /authz/api/v2/resourcegroup | GET | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getFilterResourceGroupListV2 | /authz/api/v2/resourcegroup/filter | POST | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getCoveoToken | /authz/api/zendesk/token | GET | UNKNOWN | No pagination fields detected |
| GetAllAPIKeys | /cf/admin/apikey | GET | UNKNOWN | No pagination fields detected |
| GetAttributes | /cf/admin/attributes | GET | UNKNOWN | No pagination fields detected |
| GetAllFeatures | /cf/admin/features | GET | UNKNOWN | No pagination fields detected |
| GetDependentFeatures | /cf/admin/features/{identifier}/dependants | GET | UNKNOWN | No pagination fields detected |
| GetProxyKeys | /cf/admin/proxy/keys | GET | UNKNOWN | No pagination fields detected |
| GetAllSegments | /cf/admin/segments | GET | UNKNOWN | No pagination fields detected |
| GetAvailableFlagsForSegment | /cf/admin/segments/{identifier}/available_flags | GET | UNKNOWN | No pagination fields detected |
| GetSegmentFlags | /cf/admin/segments/{identifier}/flags | GET | UNKNOWN | No pagination fields detected |
| GetAllTags | /cf/admin/tags | GET | UNKNOWN | No pagination fields detected |
| GetAllTargets | /cf/admin/targets | GET | UNKNOWN | No pagination fields detected |
| GetTargetSegments | /cf/admin/targets/{identifier}/segments | GET | UNKNOWN | No pagination fields detected |
| listStatusCheckRecentSpace | /code/api/v1/checks/recent | GET | UNKNOWN | No pagination fields detected |
| listSpaceLabels | /code/api/v1/labels | GET | OFFSET | limit, page |
| listSpaceLabelValues | /code/api/v1/labels/{key}/values | GET | UNKNOWN | No pagination fields detected |
| listPrincipals | /code/api/v1/principals | GET | OFFSET | limit, page |
| listPullReqSpace | /code/api/v1/pullreq | GET | OFFSET | limit |
| countPullReqSpace | /code/api/v1/pullreq/count | GET | UNKNOWN | No pagination fields detected |
| listRepos | /code/api/v1/repos | GET | OFFSET | limit, page |
| listBranches | /code/api/v1/repos/{repo_identifier}/branches | GET | OFFSET | limit, page |
| listStatusCheckResults | /code/api/v1/repos/{repo_identifier}/checks/commits/{commit_sha} | GET | OFFSET | limit, page |
| listStatusCheckRecent | /code/api/v1/repos/{repo_identifier}/checks/recent | GET | UNKNOWN | No pagination fields detected |
| codeOwnersValidate | /code/api/v1/repos/{repo_identifier}/codeowners/validate | GET | UNKNOWN | No pagination fields detected |
| listCommits | /code/api/v1/repos/{repo_identifier}/commits | GET | OFFSET | limit, page |
| getCommitDiff | /code/api/v1/repos/{repo_identifier}/commits/{commit_sha}/diff | GET | UNKNOWN | No pagination fields detected |
| listRepoLabels | /code/api/v1/repos/{repo_identifier}/labels | GET | OFFSET | limit, page |
| listRepoLabelValues | /code/api/v1/repos/{repo_identifier}/labels/{key}/values | GET | UNKNOWN | No pagination fields detected |
| getRepoLanguages | /code/api/v1/repos/{repo_identifier}/languages | GET | UNKNOWN | No pagination fields detected |
| listPaths | /code/api/v1/repos/{repo_identifier}/paths | GET | UNKNOWN | No pagination fields detected |
| listPullReq | /code/api/v1/repos/{repo_identifier}/pullreq | GET | OFFSET | limit, page |
| prCandidates | /code/api/v1/repos/{repo_identifier}/pullreq/candidates | GET | OFFSET | limit |
| listPullReqActivities | /code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/activities | GET | OFFSET | limit |
| prAutoMergeGet | /code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/automerge | GET | UNKNOWN | No pagination fields detected |
| checksPullReq | /code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/checks | GET | UNKNOWN | No pagination fields detected |
| codeownersPullReq | /code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/codeowners | GET | UNKNOWN | No pagination fields detected |
| listPullReqCommits | /code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/commits | GET | OFFSET | limit, page |
| diffPullReq | /code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/diff | GET | UNKNOWN | No pagination fields detected |
| fileViewListPullReq | /code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/file-views | GET | UNKNOWN | No pagination fields detected |
| listPullReqLabels | /code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/labels | GET | OFFSET | limit, page |
| pullReqMetaData | /code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/metadata | GET | UNKNOWN | No pagination fields detected |
| reviewerListPullReq | /code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/reviewers | GET | UNKNOWN | No pagination fields detected |
| reviewerCombinedListPullReq | /code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/reviewers/combined | GET | UNKNOWN | No pagination fields detected |
| repoRuleList | /code/api/v1/repos/{repo_identifier}/rules | GET | OFFSET | limit, page |
| findGeneralSettings | /code/api/v1/repos/{repo_identifier}/settings/general | GET | UNKNOWN | No pagination fields detected |
| findSecuritySettings | /code/api/v1/repos/{repo_identifier}/settings/security | GET | UNKNOWN | No pagination fields detected |
| summary | /code/api/v1/repos/{repo_identifier}/summary | GET | UNKNOWN | No pagination fields detected |
| listTags | /code/api/v1/repos/{repo_identifier}/tags | GET | OFFSET | limit, page |
| listRepoWebhooks | /code/api/v1/repos/{repo_identifier}/webhooks | GET | OFFSET | limit, page |
| listRepoWebhookExecutions | /code/api/v1/repos/{repo_identifier}/webhooks/{webhook_identifier}/executions | GET | OFFSET | limit, page |
| listGitignore | /code/api/v1/resources/gitignore | GET | UNKNOWN | No pagination fields detected |
| listLicenses | /code/api/v1/resources/license | GET | UNKNOWN | No pagination fields detected |
| spaceRuleList | /code/api/v1/rules | GET | OFFSET | limit, page |
| listUsergroups | /code/api/v1/usergroups | GET | OFFSET | limit, page |
| listSpaceWebhooks | /code/api/v1/webhooks | GET | OFFSET | limit, page |
| listSpaceWebhookExecutions | /code/api/v1/webhooks/{webhook_identifier}/executions | GET | OFFSET | limit, page |
| listHealthSources | /cv/api/health-sources | GET | UNKNOWN | No pagination fields detected |
| list | /cv/api/monitored-service | GET | OFFSET | offset, pageSize |
| getAllMonitoredServicesWithHealthSources | /cv/api/monitored-service/all/time-series-health-sources | GET | UNKNOWN | No pagination fields detected |
| getCountOfServices | /cv/api/monitored-service/count-of-services | GET | UNKNOWN | No pagination fields detected |
| getHealthSources | /cv/api/monitored-service/health-sources | GET | UNKNOWN | No pagination fields detected |
| getList | /cv/api/monitored-service/list | GET | OFFSET | offset, pageSize |
| getListV2 | /cv/api/monitored-service/platform/list | GET | OFFSET | offset, pageSize |
| isReconciliationRequiredForMonitoredServices | /cv/api/monitored-service/reconciliation-required | GET | UNKNOWN | No pagination fields detected |
| getMonitoredServiceReconciliationStatuses | /cv/api/monitored-service/reconciliation-status | GET | OFFSET | pageNumber, pageSize |
| getMSSecondaryEventsDetails | /cv/api/monitored-service/secondary-events-details | GET | UNKNOWN | No pagination fields detected |
| getMonitoredServiceDetails_1 | /cv/api/monitored-service/service-details | GET | UNKNOWN | No pagination fields detected |
| getMonitoredServiceFromServiceAndEnvironment | /cv/api/monitored-service/service-environment | GET | UNKNOWN | No pagination fields detected |
| getServices | /cv/api/monitored-service/services | GET | UNKNOWN | No pagination fields detected |
| yamlTemplate | /cv/api/monitored-service/yaml-template | GET | UNKNOWN | No pagination fields detected |
| CvgetAnomaliesSummary | /cv/api/monitored-service/{identifier}/anomaliesCount | GET | UNKNOWN | No pagination fields detected |
| getNotificationRulesForMonitoredService | /cv/api/monitored-service/{identifier}/notification-rules | GET | OFFSET | pageNumber, pageSize |
| getOverAllHealthScore | /cv/api/monitored-service/{identifier}/overall-health-score | GET | UNKNOWN | No pagination fields detected |
| getMonitoredServiceResolvedTemplateInputs | /cv/api/monitored-service/{identifier}/resolved-template-inputs | GET | UNKNOWN | No pagination fields detected |
| getMonitoredServiceScore | /cv/api/monitored-service/{identifier}/scores | GET | UNKNOWN | No pagination fields detected |
| getMSSecondaryEvents | /cv/api/monitored-service/{identifier}/secondary-events | GET | UNKNOWN | No pagination fields detected |
| getMonitoredServiceChangeDetails | /cv/api/monitored-service/{monitoredServiceIdentifier}/change-details | GET | UNKNOWN | No pagination fields detected |
| getSloMetrics | /cv/api/monitored-service/{monitoredServiceIdentifier}/health-source/{healthSourceIdentifier}/slo-metrics | GET | UNKNOWN | No pagination fields detected |
| getHealthSourcesForMonitoredServiceIdentifier | /cv/api/monitored-service/{monitoredServiceIdentifier}/health-sources | GET | UNKNOWN | No pagination fields detected |
| getMonitoredServiceLogs | /cv/api/monitored-service/{monitoredServiceIdentifier}/logs | GET | OFFSET | pageNumber, pageSize |
| getMonitoredServiceDetails | /cv/api/monitored-service/{monitoredServiceIdentifier}/service-details | GET | UNKNOWN | No pagination fields detected |
| getNotificationRuleData_1 | /cv/api/notification-rule | GET | OFFSET | pageNumber, pageSize |
| getSLOAssociatedMonitoredServices | /cv/api/slo-dashboard/monitored-services | GET | OFFSET | pageNumber, pageSize |
| getServiceLevelObjectivesRiskCount | /cv/api/slo-dashboard/risk-count | GET | UNKNOWN | No pagination fields detected |
| getSecondaryEventDetails | /cv/api/slo-dashboard/secondary-events-details | GET | UNKNOWN | No pagination fields detected |
| getSloConsumptionBreakdownView | /cv/api/slo-dashboard/widget/{identifier}/consumption | GET | UNKNOWN | No pagination fields detected |
| getSLOHealthListView | /cv/api/slo-dashboard/widgets/list | GET | OFFSET | pageNumber, pageSize |
| getSLOHealthListViewV2 | /cv/api/slo-dashboard/widgets/list | POST | OFFSET | pageNumber, pageSize |
| getErrorBudgetResetHistory | /cv/api/slo/{identifier}/errorBudgetResetHistory | GET | UNKNOWN | No pagination fields detected |
| getServiceLevelObjectiveLogs | /cv/api/slo/{identifier}/logs | GET | OFFSET | pageNumber, pageSize |
| getNotificationRulesForSLO | /cv/api/slo/{identifier}/notification-rules | GET | OFFSET | pageNumber, pageSize |
| CvgetLicenseUsage | /cv/api/usage/CV | GET | UNKNOWN | No pagination fields detected |
| getSRMLicenseUsage | /cv/api/usage/SRM | GET | UNKNOWN | No pagination fields detected |
| listSRMActiveMonitoredServices | /cv/api/usage/SRM/active-monitored-services | POST | OFFSET | size, page |
| downloadActiveMonitoredServiceCSVReport | /cv/api/usage/SRM/active-monitored-services/csv/download | GET | UNKNOWN | No pagination fields detected |
| downloadActiveServiceMonitoredCSVReport | /cv/api/usage/SRM/active-services-monitored/csv/download | GET | UNKNOWN | No pagination fields detected |
| get_dashboard_data | /dashboard/api/dashboards/{dashboard_id}/download | GET | UNKNOWN | No pagination fields detected |
| get_dashboard_elements | /dashboard/dashboards/{dashboard_id}/elements | GET | UNKNOWN | No pagination fields detected |
| get_dashboard_filters | /dashboard/dashboards/{dashboard_id}/filters | GET | UNKNOWN | No pagination fields detected |
| update_dashboard_filter | /dashboard/dashboards/{dashboard_id}/filters/{filter_id} | PATCH | UNKNOWN | No pagination fields detected |
| get_dashboard_download_csv | /dashboard/download/dashboards/{dashboard_id}/csv | GET | UNKNOWN | No pagination fields detected |
| get_dashboard_download_pdf | /dashboard/download/dashboards/{dashboard_id}/pdf | GET | OFFSET | paper_size |
| getExperimentHelperImageVersion | /gateway/chaos/manager/api/experimentHelperImageVersion | GET | UNKNOWN | No pagination fields detected |
| listActions | /gateway/chaos/manager/api/rest/actions | GET | OFFSET | limit, page |
| listExperimentTemplate | /gateway/chaos/manager/api/rest/experimenttemplates | GET | OFFSET | limit, page |
| compareExperimentTemplateRevisions | /gateway/chaos/manager/api/rest/experimenttemplates/{identity}/compare | GET | UNKNOWN | No pagination fields detected |
| getExperimentTemplateRevisions | /gateway/chaos/manager/api/rest/experimenttemplates/{identity}/revisions | GET | OFFSET | limit, page |
| getExperimentTemplateVariables | /gateway/chaos/manager/api/rest/experimenttemplates/{identity}/variables | GET | UNKNOWN | No pagination fields detected |
| getExperimentTemplateYaml | /gateway/chaos/manager/api/rest/experimenttemplates/{identity}/yaml | GET | UNKNOWN | No pagination fields detected |
| listFaultv2 | /gateway/chaos/manager/api/rest/faults | GET | OFFSET | limit, page |
| listExperimentRunsOfFault | /gateway/chaos/manager/api/rest/faults/{identity}/experimentruns | GET | OFFSET | limit, page |
| getFaultVariables | /gateway/chaos/manager/api/rest/faults/{identity}/variables | GET | UNKNOWN | No pagination fields detected |
| getFaultYaml | /gateway/chaos/manager/api/rest/faults/{identity}/yaml | GET | UNKNOWN | No pagination fields detected |
| listFaultTemplate | /gateway/chaos/manager/api/rest/faulttemplates | GET | OFFSET | limit, page |
| compareFaultTemplateRevisions | /gateway/chaos/manager/api/rest/faulttemplates/{identity}/compare | GET | UNKNOWN | No pagination fields detected |
| getFaultTemplateRevisions | /gateway/chaos/manager/api/rest/faulttemplates/{identity}/revisions | GET | OFFSET | limit, page |
| getFaultTemplateVariables | /gateway/chaos/manager/api/rest/faulttemplates/{identity}/variables | GET | UNKNOWN | No pagination fields detected |
| getFaultTemplateYaml | /gateway/chaos/manager/api/rest/faulttemplates/{identity}/yaml | GET | UNKNOWN | No pagination fields detected |
| listChaosHub | /gateway/chaos/manager/api/rest/hubs | GET | OFFSET | limit, page |
| listFault | /gateway/chaos/manager/api/rest/hubs/faults | GET | OFFSET | limit, page |
| getImageRegistry | /gateway/chaos/manager/api/rest/imageRegistry | GET | UNKNOWN | No pagination fields detected |
| getMachineChaosInfraVersionDetails | /gateway/chaos/manager/api/rest/machine/infra/version | GET | UNKNOWN | No pagination fields detected |
| listMachineChaosInfra | /gateway/chaos/manager/api/rest/machine/infras | POST | OFFSET | limit, page |
| getExperimentRunsOverviewStats | /gateway/chaos/manager/api/rest/overview/experiment-stats | GET | UNKNOWN | No pagination fields detected |
| getRecommendation | /gateway/chaos/manager/api/rest/recommendations | GET | UNKNOWN | No pagination fields detected |
| listRecommendations1 | /gateway/chaos/manager/api/rest/recommendations | POST | OFFSET | limit, page |
| listActionTemplate | /gateway/chaos/manager/api/rest/templates/actions | GET | OFFSET | limit, page |
| getActionTemplateRevisionDifference | /gateway/chaos/manager/api/rest/templates/actions/{identity}/compare | GET | UNKNOWN | No pagination fields detected |
| listActionTemplateRevisions | /gateway/chaos/manager/api/rest/templates/actions/{identity}/revisions | GET | OFFSET | limit, page |
| listVariablesInActionTemplate | /gateway/chaos/manager/api/rest/templates/actions/{identity}/variables | GET | UNKNOWN | No pagination fields detected |
| listProbeTemplate | /gateway/chaos/manager/api/rest/templates/probes | GET | OFFSET | limit, page |
| listVariablesInProbeTemplate | /gateway/chaos/manager/api/rest/templates/probes/{identity}/variables | GET | UNKNOWN | No pagination fields detected |
| getResourceUsage | /gateway/chaos/manager/api/rest/usage | GET | UNKNOWN | No pagination fields detected |
| listTargetNetworkMaps | /gateway/chaos/manager/api/rest/v2/applicationmaps | POST | OFFSET | limit, page |
| canRetryExperimentCreation | /gateway/chaos/manager/api/rest/v2/applicationmaps/{applicationmapid}/canretry | GET | UNKNOWN | No pagination fields detected |
| listService | /gateway/chaos/manager/api/rest/v2/applicationmaps/{applicationmapid}/targetservices | GET | OFFSET | limit, page |
| listChaosV2Experiment | /gateway/chaos/manager/api/rest/v2/experiment | GET | OFFSET | limit, page |
| listExperiments | /gateway/chaos/manager/api/rest/v2/experiments | POST | OFFSET | limit, page |
| listInputSet1 | /gateway/chaos/manager/api/rest/v2/experiments/{experimentId}/inputsets | GET | OFFSET | limit, page |
| getChaosV2ExperimentRun | /gateway/chaos/manager/api/rest/v2/experiments/{experimentId}/run | GET | UNKNOWN | No pagination fields detected |
| getChaosV2ExperimentVariables | /gateway/chaos/manager/api/rest/v2/experiments/{experimentId}/variables | GET | UNKNOWN | No pagination fields detected |
| listHarnessInfra | /gateway/chaos/manager/api/rest/v2/harness-infrastructures | GET | OFFSET | limit, page |
| getNote | /gateway/chaos/manager/api/rest/v2/notes | GET | UNKNOWN | No pagination fields detected |
| listV2Onboarding | /gateway/chaos/manager/api/rest/v2/onboarding | GET | OFFSET | limit, page |
| getOnboardingExperiments | /gateway/chaos/manager/api/rest/v2/onboarding/{onboardingid}/experiments | GET | OFFSET | limit, page |
| listProbes | /gateway/chaos/manager/api/rest/v2/probes | GET | OFFSET | limit, page |
| listExperimentsWithActiveInfrasMinimalNotification | /gateway/chaos/manager/api/v1/notification-experiments | GET | OFFSET | limit, page |
| listActionMetadata | /gateway/chaos/manager/api/v3/actions/list-metadata | POST | OFFSET | limit, page |
| listCondition | /gateway/chaos/manager/api/v3/chaosguard-conditions | GET | OFFSET | limit, page |
| listRule | /gateway/chaos/manager/api/v3/chaosguard-rules | GET | OFFSET | limit, page |
| listDRTests | /gateway/chaos/manager/api/v3/dr-tests | GET | OFFSET | limit, page |
| listExperimentMetadata | /gateway/chaos/manager/api/v3/experiments/list-metadata | POST | OFFSET | limit, page |
| listFaultMetadata | /gateway/chaos/manager/api/v3/faults/list-metadata | POST | OFFSET | limit, page |
| healthCheckV3 | /gateway/chaos/manager/api/v3/health | GET | UNKNOWN | No pagination fields detected |
| listHubMetadata | /gateway/chaos/manager/api/v3/hubs/list-metadata | POST | OFFSET | limit, page |
| getChaosComponentVariable | /gateway/chaos/manager/api/v3/integrations/get-chaos-component-variable | GET | UNKNOWN | No pagination fields detected |
| getExperimentOrTemplateVariable | /gateway/chaos/manager/api/v3/integrations/get-experiment-or-template-variable | GET | UNKNOWN | No pagination fields detected |
| listExperimentOrTemplate | /gateway/chaos/manager/api/v3/integrations/list-experiment-or-template | GET | OFFSET | limit, page |
| listProbeMetadata | /gateway/chaos/manager/api/v3/probes/list-metadata | POST | OFFSET | limit, page |
| listRisks | /gateway/chaos/manager/api/v3/risks | GET | OFFSET | limit, page |
| listProbeExecutions | /gateway/chaos/manager/api/v3/risks/{identity}/active-risks | GET | OFFSET | limit, page |
| ListLoadBalancers | /gateway/lw/api/accounts/{account_id}/autostopping/loadbalancers | GET | UNKNOWN | No pagination fields detected |
| LoadBalancerActivity | /gateway/lw/api/accounts/{account_id}/autostopping/loadbalancers/{lb_id}/last_active_at | GET | UNKNOWN | No pagination fields detected |
| AccessPointRules | /gateway/lw/api/accounts/{account_id}/autostopping/loadbalancers/{lb_id}/rules | GET | UNKNOWN | No pagination fields detected |
| ListAutoStoppingRules | /gateway/lw/api/accounts/{account_id}/autostopping/rules | GET | UNKNOWN | No pagination fields detected |
| CumulativeAutoStoppingSavings | /gateway/lw/api/accounts/{account_id}/autostopping/rules/savings/cumulative | GET | UNKNOWN | No pagination fields detected |
| GetAutoStoppingCoolDownMeta | /gateway/lw/api/accounts/{account_id}/autostopping/rules/{rule_id}/cooldown_meta | GET | UNKNOWN | No pagination fields detected |
| GetAutoStoppingDiagnostics | /gateway/lw/api/accounts/{account_id}/autostopping/rules/{rule_id}/diagnostics | GET | UNKNOWN | No pagination fields detected |
| HealthOfAutoStoppingRule | /gateway/lw/api/accounts/{account_id}/autostopping/rules/{rule_id}/health | GET | UNKNOWN | No pagination fields detected |
| AllAutoStoppingResources | /gateway/lw/api/accounts/{account_id}/autostopping/rules/{rule_id}/resources | GET | UNKNOWN | No pagination fields detected |
| SavingsFromAutoStoppingRule | /gateway/lw/api/accounts/{account_id}/autostopping/rules/{rule_id}/savings | GET | UNKNOWN | No pagination fields detected |
| listConnectedKubernetesClusters | /gateway/lw/api/accounts/{account_id}/clusters | GET | UNKNOWN | No pagination fields detected |
| listAutoStoppingSchedules | /gateway/lw/api/accounts/{account_id}/schedules | GET | UNKNOWN | No pagination fields detected |
| ApprovalsList | /gateway/lw/api/accounts/{account_id}/v1/approvals/list | POST | UNKNOWN | No pagination fields detected |
| GetCommitmentUtilizationDetails | /gateway/lw/api/accounts/{account_id}/v1/detail/commitment_utilisation | GET | UNKNOWN | No pagination fields detected |
| GetFilters | /gateway/lw/api/accounts/{account_id}/v1/filters | POST | UNKNOWN | No pagination fields detected |
| GetInstanceFamilyFilters | /gateway/lw/api/accounts/{account_id}/v1/filters/instancefamilies | POST | UNKNOWN | No pagination fields detected |
| GetProviderAccountFilters | /gateway/lw/api/accounts/{account_id}/v1/filters/provideraccounts | POST | UNKNOWN | No pagination fields detected |
| GetRegionFilters | /gateway/lw/api/accounts/{account_id}/v1/filters/regions | POST | UNKNOWN | No pagination fields detected |
| ListSetups | /gateway/lw/api/accounts/{account_id}/v1/setup/list | GET | UNKNOWN | No pagination fields detected |
| ListMasters | /gateway/lw/api/accounts/{account_id}/v1/setup/listMasterAccounts | POST | UNKNOWN | No pagination fields detected |
| ListAccounts | /gateway/lw/api/accounts/{account_id}/v1/setup/{cloud_account_id}/child_accounts | GET | UNKNOWN | No pagination fields detected |
| ApprovalsListV2 | /gateway/lw/api/accounts/{account_id}/v2/approvals/list | POST | UNKNOWN | No pagination fields detected |
| GetRIFilterOptions | /gateway/lw/api/accounts/{account_id}/v2/filters/ri | GET | UNKNOWN | No pagination fields detected |
| GetSPFilterOptions | /gateway/lw/api/accounts/{account_id}/v2/filters/sp | GET | UNKNOWN | No pagination fields detected |
| ListReservedInstances | /gateway/lw/api/accounts/{account_id}/v2/inventory/ri/list | POST | UNKNOWN | No pagination fields detected |
| GetReservedInstanceDetails | /gateway/lw/api/accounts/{account_id}/v2/inventory/ri/{riId}/detail | GET | UNKNOWN | No pagination fields detected |
| ListSavingsPlans | /gateway/lw/api/accounts/{account_id}/v2/inventory/sp/list | POST | UNKNOWN | No pagination fields detected |
| GetSavingsPlanDetails | /gateway/lw/api/accounts/{account_id}/v2/inventory/sp/{spId}/detail | GET | UNKNOWN | No pagination fields detected |
| LandingPageHandler | /gateway/lw/api/accounts/{account_id}/v2/landing | GET | UNKNOWN | No pagination fields detected |
| FilterService_List | /gitops/api/filters | GET | OFFSET | pageIndex, pageSize |
| FilterService_Create | /gitops/api/filters | POST | UNKNOWN | No pagination fields detected |
| FilterService_Update | /gitops/api/filters | PUT | UNKNOWN | No pagination fields detected |
| FilterService_Get | /gitops/api/filters/{identifier} | GET | UNKNOWN | No pagination fields detected |
| FilterService_Delete | /gitops/api/filters/{identifier} | DELETE | UNKNOWN | No pagination fields detected |
| AgentServiceForServer_List | /gitops/api/v1/agents | GET | OFFSET | pageIndex, pageSize |
| AgentServiceForServer_ListNamespaces | /gitops/api/v1/agents/ns | GET | OFFSET | pageIndex, pageSize |
| AgentServiceForServer_Search | /gitops/api/v1/agents/search | POST | UNKNOWN | No pagination fields detected |
| AgentServiceForServer_ListTags | /gitops/api/v1/agents/tags | GET | OFFSET | pageIndex, pageSize |
| AgentServiceForServer_ListVersions | /gitops/api/v1/agents/versions | GET | OFFSET | pageIndex, pageSize |
| AgentApplicationService_List | /gitops/api/v1/agents/{agentIdentifier}/applications | GET | UNKNOWN | No pagination fields detected |
| AgentApplicationService_ManagedResources | /gitops/api/v1/agents/{agentIdentifier}/applications/{query.applicationName}/managed-resources | GET | UNKNOWN | No pagination fields detected |
| AgentApplicationService_ResourceTree | /gitops/api/v1/agents/{agentIdentifier}/applications/{query.applicationName}/resource-tree | GET | UNKNOWN | No pagination fields detected |
| AgentApplicationService_ListResourceEvents | /gitops/api/v1/agents/{agentIdentifier}/applications/{query.name}/events | GET | UNKNOWN | No pagination fields detected |
| AgentApplicationService_PodLogs2 | /gitops/api/v1/agents/{agentIdentifier}/applications/{query.name}/logs | GET | UNKNOWN | No pagination fields detected |
| AgentApplicationService_PodLogsBatch2 | /gitops/api/v1/agents/{agentIdentifier}/applications/{query.name}/logs/batch | GET | UNKNOWN | No pagination fields detected |
| AgentApplicationService_GetManifests | /gitops/api/v1/agents/{agentIdentifier}/applications/{query.name}/manifests | GET | UNKNOWN | No pagination fields detected |
| AgentApplicationService_PodLogs | /gitops/api/v1/agents/{agentIdentifier}/applications/{query.name}/pods/{query.podName}/logs | GET | UNKNOWN | No pagination fields detected |
| AgentApplicationService_PodLogsBatch | /gitops/api/v1/agents/{agentIdentifier}/applications/{query.name}/pods/{query.podName}/logs/batch | GET | UNKNOWN | No pagination fields detected |
| AgentApplicationService_RevisionMetadata | /gitops/api/v1/agents/{agentIdentifier}/applications/{query.name}/revisions/{query.revision}/metadata | GET | UNKNOWN | No pagination fields detected |
| AgentApplicationService_GetApplicationSyncWindows | /gitops/api/v1/agents/{agentIdentifier}/applications/{query.name}/syncwindows | GET | UNKNOWN | No pagination fields detected |
| AgentApplicationService_GetResource | /gitops/api/v1/agents/{agentIdentifier}/applications/{request.name}/resource | GET | UNKNOWN | No pagination fields detected |
| AgentApplicationService_ListResourceActions | /gitops/api/v1/agents/{agentIdentifier}/applications/{request.name}/resource/actions | GET | UNKNOWN | No pagination fields detected |
| RolloutsService_GetRolloutStatus | /gitops/api/v1/agents/{agentIdentifier}/applications/{request.name}/rollouts/status | GET | UNKNOWN | No pagination fields detected |
| AppProjectMappingService_GetAppProjectMappingListByAgent | /gitops/api/v1/agents/{agentIdentifier}/appprojectsmapping | GET | UNKNOWN | No pagination fields detected |
| ReconcilerService_ListAutoCreateLogs | /gitops/api/v1/agents/{agentIdentifier}/autocreate-logs | GET | OFFSET | limit |
| AgentCertificateService_List | /gitops/api/v1/agents/{agentIdentifier}/certificates | GET | UNKNOWN | No pagination fields detected |
| AgentClusterService_GetByName | /gitops/api/v1/agents/{agentIdentifier}/cluster_byname | GET | UNKNOWN | No pagination fields detected |
| AgentClusterService_GetByUrl | /gitops/api/v1/agents/{agentIdentifier}/cluster_byurl | GET | UNKNOWN | No pagination fields detected |
| AgentClusterService_List | /gitops/api/v1/agents/{agentIdentifier}/clusters | GET | UNKNOWN | No pagination fields detected |
| AgentServiceForServer_GetDeployYaml | /gitops/api/v1/agents/{agentIdentifier}/deploy.yaml | GET | UNKNOWN | No pagination fields detected |
| AgentGPGKeyService_List | /gitops/api/v1/agents/{agentIdentifier}/gpgkeys | GET | UNKNOWN | No pagination fields detected |
| AgentServiceForServer_GetDeployHelmChart | /gitops/api/v1/agents/{agentIdentifier}/helm-chart | GET | UNKNOWN | No pagination fields detected |
| AgentServiceForServer_GetDeployOverrides | /gitops/api/v1/agents/{agentIdentifier}/helm-overrides | GET | UNKNOWN | No pagination fields detected |
| AgentServiceForServer_GetOperatorYaml | /gitops/api/v1/agents/{agentIdentifier}/operator/yaml | GET | UNKNOWN | No pagination fields detected |
| AgentRepositoryService_ListRepositories | /gitops/api/v1/agents/{agentIdentifier}/repositories | GET | UNKNOWN | No pagination fields detected |
| AgentRepositoryService_CheckExternalSecretsOperator | /gitops/api/v1/agents/{agentIdentifier}/repositories/eso/check | GET | UNKNOWN | No pagination fields detected |
| AgentRepositoryService_ListESOGenerators | /gitops/api/v1/agents/{agentIdentifier}/repositories/eso/generators | GET | UNKNOWN | No pagination fields detected |
| AgentRepositoryService_GetAppDetails | /gitops/api/v1/agents/{agentIdentifier}/repositories/{identifier}/appdetails | GET | UNKNOWN | No pagination fields detected |
| AgentRepositoryService_ListApps | /gitops/api/v1/agents/{agentIdentifier}/repositories/{identifier}/apps | GET | UNKNOWN | No pagination fields detected |
| AgentRepositoryService_GetHelmCharts | /gitops/api/v1/agents/{agentIdentifier}/repositories/{identifier}/helmcharts | GET | UNKNOWN | No pagination fields detected |
| AgentRepositoryService_ListRefs | /gitops/api/v1/agents/{agentIdentifier}/repositories/{identifier}/refs | GET | UNKNOWN | No pagination fields detected |
| AgentRepositoryService_GetAppDetailsByUrl | /gitops/api/v1/agents/{agentIdentifier}/repositories_byurl/appdetails | GET | UNKNOWN | No pagination fields detected |
| AgentRepositoryService_ListAppsByUrl | /gitops/api/v1/agents/{agentIdentifier}/repositories_byurl/apps | GET | UNKNOWN | No pagination fields detected |
| AgentRepositoryService_GetHelmChartsByUrl | /gitops/api/v1/agents/{agentIdentifier}/repositories_byurl/helmcharts | GET | UNKNOWN | No pagination fields detected |
| AgentRepositoryService_ListRefsByUrl | /gitops/api/v1/agents/{agentIdentifier}/repositories_byurl/refs | GET | UNKNOWN | No pagination fields detected |
| AgentRepositoryService_GetByUrl | /gitops/api/v1/agents/{agentIdentifier}/repository_byurl | GET | UNKNOWN | No pagination fields detected |
| AgentApplicationService_Watch | /gitops/api/v1/agents/{agentIdentifier}/stream/applications | GET | UNKNOWN | No pagination fields detected |
| AgentApplicationService_WatchResourceTree | /gitops/api/v1/agents/{agentIdentifier}/stream/applications/{query.applicationName}/resource-tree | GET | UNKNOWN | No pagination fields detected |
| AgentServiceForServer_GetSyncAllowed | /gitops/api/v1/agents/{agentIdentifier}/sync-allowed | GET | UNKNOWN | No pagination fields detected |
| AgentServiceForServer_Unique | /gitops/api/v1/agents/{identifier}/unique | GET | OFFSET | pageIndex, pageSize |
| ApplicationService_ListApps | /gitops/api/v1/applications | POST | UNKNOWN | No pagination fields detected |
| ApplicationService_ListAttributes | /gitops/api/v1/applications/attributes | GET | UNKNOWN | No pagination fields detected |
| ApplicationService_ListNs | /gitops/api/v1/applications/ns | POST | UNKNOWN | No pagination fields detected |
| ApplicationService_ListAppSets | /gitops/api/v1/applications/sets | GET | OFFSET | pageIndex, pageSize |
| ApplicationService_ListAppSync | /gitops/api/v1/applications/sync | POST | UNKNOWN | No pagination fields detected |
| ApplicationService_Exists | /gitops/api/v1/applications/{name}/exists | GET | UNKNOWN | No pagination fields detected |
| ApplicationSetService_ListApplicationSetGenerators | /gitops/api/v1/applicationset/generators | GET | UNKNOWN | No pagination fields detected |
| ApplicationSetService_ResourceTree | /gitops/api/v1/applicationset/{identifier}/resource-tree | GET | UNKNOWN | No pagination fields detected |
| ApplicationSetService_List | /gitops/api/v1/applicationsets | POST | UNKNOWN | No pagination fields detected |
| AppProjectMappingService_GetAppProjectMappingList | /gitops/api/v1/appprojectsmapping | GET | UNKNOWN | No pagination fields detected |
| CertificateService_ListCerts | /gitops/api/v1/certificates | GET | OFFSET | pageIndex, pageSize |
| ClusterService_ListClusters | /gitops/api/v1/clusters | POST | UNKNOWN | No pagination fields detected |
| ClusterService_Exists | /gitops/api/v1/clusters/exists | GET | UNKNOWN | No pagination fields detected |
| DashboardService_RecentlyCreatedCounts | /gitops/api/v1/dashboard/counts | GET | UNKNOWN | No pagination fields detected |
| DashboardService_GetDashboardOverview | /gitops/api/v1/dashboard/overview | GET | UNKNOWN | No pagination fields detected |
| DashboardService_TopApplicationPhaseStats | /gitops/api/v1/dashboard/topapps | GET | OFFSET | limit |
| GnuPGKeyService_ListGPGKeys | /gitops/api/v1/gpgkeys | GET | OFFSET | pageIndex, pageSize |
| AgentRepositoryCredentialsService_ListRepositoryCredentials | /gitops/api/v1/repocreds | POST | UNKNOWN | No pagination fields detected |
| RepositoryService_ListRepositoriesByRepositoryCredentialTemplate | /gitops/api/v1/repositories | GET | OFFSET | pageIndex, pageSize |
| RepositoryService_ListRepositories | /gitops/api/v1/repositories | POST | UNKNOWN | No pagination fields detected |
| RepositoryService_Exists | /gitops/api/v1/repositories/exists | GET | UNKNOWN | No pagination fields detected |
| AppProjectMappingService_GetAppProjectMappingsListByAgentV2 | /gitops/api/v2/agents/{agentIdentifier}/appprojectsmappings | GET | UNKNOWN | No pagination fields detected |
| AppProjectMappingService_ListAppProjectMappings | /gitops/api/v2/appprojectsmapping | GET | OFFSET | pageIndex, pageSize |
| VersionUpgradeService_UpgradeAvailableV2 | /gitops/api/v2/versions/agents/upgrade-available | GET | UNKNOWN | No pagination fields detected |
| RedirectHarnessArtifact | /har/api/v1/registry/{registry_identifier}/artifact/{artifact}/redirect | GET | UNKNOWN | No pagination fields detected |
| ListArtifactLabels | /har/api/v1/registry/{registry_ref}/artifact/labels | GET | UNKNOWN | No pagination fields detected |
| GetArtifactStatsForRegistry | /har/api/v1/registry/{registry_ref}/artifact/stats | GET | UNKNOWN | No pagination fields detected |
| GetArtifactStats | /har/api/v1/registry/{registry_ref}/artifact/{artifact}/stats | GET | UNKNOWN | No pagination fields detected |
| GetArtifactSummary | /har/api/v1/registry/{registry_ref}/artifact/{artifact}/summary | GET | UNKNOWN | No pagination fields detected |
| GetOciArtifactTags | /har/api/v1/registry/{registry_ref}/artifact/{artifact}/tags | GET | UNKNOWN | No pagination fields detected |
| CreateBulkDownloadRequestV1 | /har/api/v1/registry/{registry_ref}/artifact/{artifact}/version/{version}/bulk-download | GET | UNKNOWN | No pagination fields detected |
| GetArtifactDeployments | /har/api/v1/registry/{registry_ref}/artifact/{artifact}/version/{version}/deploymentdetails | GET | UNKNOWN | No pagination fields detected |
| GetArtifactDetails | /har/api/v1/registry/{registry_ref}/artifact/{artifact}/version/{version}/details | GET | UNKNOWN | No pagination fields detected |
| GetDockerArtifactDetails | /har/api/v1/registry/{registry_ref}/artifact/{artifact}/version/{version}/docker/details | GET | UNKNOWN | No pagination fields detected |
| GetDockerArtifactIntegrationDetails | /har/api/v1/registry/{registry_ref}/artifact/{artifact}/version/{version}/docker/integrationdetails | GET | UNKNOWN | No pagination fields detected |
| GetDockerArtifactLayers | /har/api/v1/registry/{registry_ref}/artifact/{artifact}/version/{version}/docker/layers | GET | UNKNOWN | No pagination fields detected |
| GetDockerArtifactManifest | /har/api/v1/registry/{registry_ref}/artifact/{artifact}/version/{version}/docker/manifest | GET | UNKNOWN | No pagination fields detected |
| GetDockerArtifactManifests | /har/api/v1/registry/{registry_ref}/artifact/{artifact}/version/{version}/docker/manifests | GET | UNKNOWN | No pagination fields detected |
| GetArtifactFiles | /har/api/v1/registry/{registry_ref}/artifact/{artifact}/version/{version}/files | GET | UNKNOWN | No pagination fields detected |
| GetHelmArtifactDetails | /har/api/v1/registry/{registry_ref}/artifact/{artifact}/version/{version}/helm/details | GET | UNKNOWN | No pagination fields detected |
| GetHelmArtifactManifest | /har/api/v1/registry/{registry_ref}/artifact/{artifact}/version/{version}/helm/manifest | GET | UNKNOWN | No pagination fields detected |
| GetArtifactVersionSummary | /har/api/v1/registry/{registry_ref}/artifact/{artifact}/version/{version}/summary | GET | UNKNOWN | No pagination fields detected |
| GetAllArtifactVersions | /har/api/v1/registry/{registry_ref}/artifact/{artifact}/versions | GET | UNKNOWN | No pagination fields detected |
| GetAllArtifactsByRegistry | /har/api/v1/registry/{registry_ref}/artifacts | GET | UNKNOWN | No pagination fields detected |
| GetClientSetupDetails | /har/api/v1/registry/{registry_ref}/client-setup-details | GET | UNKNOWN | No pagination fields detected |
| ListWebhooks | /har/api/v1/registry/{registry_ref}/webhooks | GET | UNKNOWN | No pagination fields detected |
| ListWebhookExecutions | /har/api/v1/registry/{registry_ref}/webhooks/{webhook_identifier}/executions | GET | UNKNOWN | No pagination fields detected |
| ReTriggerWebhookExecution | /har/api/v1/registry/{registry_ref}/webhooks/{webhook_identifier}/executions/{webhook_execution_id}/retrigger | GET | UNKNOWN | No pagination fields detected |
| listReplicationRules | /har/api/v1/replication/rules | GET | UNKNOWN | No pagination fields detected |
| listMigrationImages | /har/api/v1/replication/rules/{id}/migration/images | GET | UNKNOWN | No pagination fields detected |
| getMigrationLogsForImage | /har/api/v1/replication/rules/{id}/migration/images/{image_id}/logs | GET | UNKNOWN | No pagination fields detected |
| GetArtifactStatsForSpace | /har/api/v1/spaces/{space_ref}/artifact/stats | GET | UNKNOWN | No pagination fields detected |
| GetAllHarnessArtifacts | /har/api/v1/spaces/{space_ref}/artifacts | GET | UNKNOWN | No pagination fields detected |
| GetStorageDetails | /har/api/v1/spaces/{space_ref}/details | GET | UNKNOWN | No pagination fields detected |
| RegistrylistSpaceLabels | /har/api/v1/spaces/{space_ref}/labels | GET | OFFSET | limit, page |
| RegistrylistSpaceLabelValues | /har/api/v1/spaces/{space_ref}/labels/{key}/values | GET | UNKNOWN | No pagination fields detected |
| GetAllRegistries | /har/api/v1/spaces/{space_ref}/registries | GET | UNKNOWN | No pagination fields detected |
| ListVersions | /har/api/v2/artifacts | GET | UNKNOWN | No pagination fields detected |
| SearchFiles | /har/api/v2/files/search | GET | UNKNOWN | No pagination fields detected |
| GetMetadata | /har/api/v2/metadata | GET | UNKNOWN | No pagination fields detected |
| GetMetadataKeys | /har/api/v2/metadata/keys | GET | UNKNOWN | No pagination fields detected |
| GetMetadataValues | /har/api/v2/metadata/values | GET | UNKNOWN | No pagination fields detected |
| ListPackages | /har/api/v2/packages | GET | UNKNOWN | No pagination fields detected |
| ListRegistries | /har/api/v2/registries | GET | UNKNOWN | No pagination fields detected |
| ListFilesV3 | /har/api/v3/files | GET | UNKNOWN | No pagination fields detected |
| GetFileV3 | /har/api/v3/files/{id}/content | GET | UNKNOWN | No pagination fields detected |
| GetFileMetadataV3 | /har/api/v3/files/{id}/metadata | GET | UNKNOWN | No pagination fields detected |
| GetMetadataKeysV3 | /har/api/v3/metadata/keys | GET | UNKNOWN | No pagination fields detected |
| GetMetadataValuesV3 | /har/api/v3/metadata/values | GET | UNKNOWN | No pagination fields detected |
| ListPackagesV3 | /har/api/v3/packages | GET | UNKNOWN | No pagination fields detected |
| GetPackageMetadataV3 | /har/api/v3/packages/{id}/metadata | GET | UNKNOWN | No pagination fields detected |
| ListRegistriesV3 | /har/api/v3/registries | GET | UNKNOWN | No pagination fields detected |
| GetRegistryMetadataV3 | /har/api/v3/registries/{id}/metadata | GET | UNKNOWN | No pagination fields detected |
| GetArtifactScansV3 | /har/api/v3/scans | GET | UNKNOWN | No pagination fields detected |
| GetArtifactScanDetailsV3 | /har/api/v3/scans/{id}/details | GET | UNKNOWN | No pagination fields detected |
| GetSystemInfoV3 | /har/api/v3/system/info | GET | UNKNOWN | No pagination fields detected |
| ListVersionsV3 | /har/api/v3/versions | GET | UNKNOWN | No pagination fields detected |
| GetVersionMetadataV3 | /har/api/v3/versions/{id}/metadata | GET | UNKNOWN | No pagination fields detected |
| IaCMsystem#health | /iacm/api/health | GET | UNKNOWN | No pagination fields detected |
| module-registry#list_modules-by-account | /iacm/api/modules | GET | OFFSET | limit, page |
| module-registry#list-modules-by-id | /iacm/api/modules/{id} | GET | UNKNOWN | No pagination fields detected |
| module-registry#list-module-tags-by-id | /iacm/api/modules/{id}/tags | GET | UNKNOWN | No pagination fields detected |
| module-registry#list-module-executions-id | /iacm/api/modules/{moduleId}/executions | GET | OFFSET | limit, page |
| module-registry#list-metadata-by-module | /iacm/api/modules/{module_id}/metadata | GET | UNKNOWN | No pagination fields detected |
| module-registry#list-readme-by-id | /iacm/api/modules/{module_id}/readme | GET | UNKNOWN | No pagination fields detected |
| provider-registry#list-providers | /iacm/api/providers | GET | OFFSET | limit, page |
| provider-registry#get-provider-domain | /iacm/api/providers/get-provider-domain | GET | UNKNOWN | No pagination fields detected |
| provider-registry#list-signing-keys | /iacm/api/providers/keys | GET | OFFSET | limit, page |
| system#list-supported-provisioner-versions | /iacm/api/provisioners/supported/{provisioner} | GET | UNKNOWN | No pagination fields detected |
| system#get-provisioner-config | /iacm/api/provisioners/{provisioner}/config | GET | UNKNOWN | No pagination fields detected |
| usage#checkLicence | /iacm/api/usage/check-licence | GET | UNKNOWN | No pagination fields detected |
| variable_sets#list-variable-set-references-account-level | /iacm/api/variable-set/{identifier}/references | GET | UNKNOWN | No pagination fields detected |
| variable_sets#list-variable-sets-account-level | /iacm/api/variable-sets | GET | UNKNOWN | No pagination fields detected |
| IaCMsystem#version | /iacm/api/version | GET | UNKNOWN | No pagination fields detected |
| workspaces#list-associated-workspaces | /iacm/api/workspace/templates/{template_id} | GET | UNKNOWN | No pagination fields detected |
| provider-registry#list-provider-versions | /iacm/provider/account/{account}/{type}/versions | GET | UNKNOWN | No pagination fields detected |
| module-registry#list-versions | /iacm/registry/account/{namespace}/{name}/{system}/versions | GET | UNKNOWN | No pagination fields detected |
| module-registry#download | /iacm/registry/account/{namespace}/{name}/{system}/{version}/download | GET | UNKNOWN | No pagination fields detected |
| module-registry#getModule | /iacm/registry/account/{namespace}/{name}/{system}/{version}/download/file | GET | UNKNOWN | No pagination fields detected |
| getAccountSetting | /ng/api/account-setting | GET | UNKNOWN | No pagination fields detected |
| listAccountSetting | /ng/api/account-setting/list | GET | UNKNOWN | No pagination fields detected |
| isImmutableDelegateEnabled | /ng/api/accounts/{accountIdentifier}/immutable-delegate-enabled | GET | UNKNOWN | No pagination fields detected |
| checkAgentMtlsEndpointDomainPrefixAvailability | /ng/api/agent/mtls/check-availability | GET | UNKNOWN | No pagination fields detected |
| getAgentMtlsEndpointForAccount | /ng/api/agent/mtls/endpoint | GET | UNKNOWN | No pagination fields detected |
| listApiKeys_1 | /ng/api/apikey | GET | UNKNOWN | No pagination fields detected |
| listApiKeys | /ng/api/apikey/aggregate | GET | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getAuthenticationSettings | /ng/api/authentication-settings | GET | UNKNOWN | No pagination fields detected |
| getLdapSettings | /ng/api/authentication-settings/ldap/settings | GET | UNKNOWN | No pagination fields detected |
| getPasswordStrengthSettings | /ng/api/authentication-settings/login-settings/password-strength | GET | UNKNOWN | No pagination fields detected |
| getSamlLoginTest | /ng/api/authentication-settings/saml-login-test | GET | UNKNOWN | No pagination fields detected |
| getAuthenticationSettingsV2 | /ng/api/authentication-settings/v2 | GET | UNKNOWN | No pagination fields detected |
| updateWhitelistedDomains | /ng/api/authentication-settings/whitelisted-domains | PUT | UNKNOWN | No pagination fields detected |
| getCannyBoards | /ng/api/canny/boards | GET | UNKNOWN | No pagination fields detected |
| getCannyBoards_1 | /ng/api/canny/categories | GET | UNKNOWN | No pagination fields detected |
| pipelineExecutionCount | /ng/api/dashboard/getPipelineExecutionCount | GET | UNKNOWN | No pagination fields detected |
| listDelegateGroupsUsingTags | /ng/api/delegate-group-tags/delegate-groups | POST | UNKNOWN | No pagination fields detected |
| listTagsForDelegateGroup | /ng/api/delegate-group-tags/{groupIdentifier} | GET | UNKNOWN | No pagination fields detected |
| generateTerraformModule | /ng/api/delegate-setup/delegate-terraform-module-file | GET | UNKNOWN | No pagination fields detected |
| publishedDelegateVersion | /ng/api/delegate-setup/latest-supported-version | GET | UNKNOWN | No pagination fields detected |
| listDelegates | /ng/api/delegate-setup/listDelegates | POST | UNKNOWN | No pagination fields detected |
| listOverrideDelegateImageTag | /ng/api/delegate-setup/override-delegate-tag | GET | UNKNOWN | No pagination fields detected |
| getCgDelegateTokens | /ng/api/delegate-token-ng | GET | UNKNOWN | No pagination fields detected |
| getDelegateGroupsUsingToken | /ng/api/delegate-token-ng/delegate-groups | GET | UNKNOWN | No pagination fields detected |
| listFilesAndFolders | /ng/api/file-store | GET | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getCreatedByList | /ng/api/file-store/files/createdBy | GET | UNKNOWN | No pagination fields detected |
| listFilesWithFilter | /ng/api/file-store/files/filter | POST | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| downloadFile | /ng/api/file-store/files/{identifier}/download | GET | UNKNOWN | No pagination fields detected |
| getFileContentUsingScopedFilePath | /ng/api/file-store/files/{scopedFilePath}/content | GET | UNKNOWN | No pagination fields detected |
| getEntityTypes | /ng/api/file-store/supported-entity-types | GET | UNKNOWN | No pagination fields detected |
| getReferencedBy | /ng/api/file-store/{identifier}/referenced-by | GET | OFFSET | pageSize, pageIndex |
| getFilterList | /ng/api/filters | GET | OFFSET | pageSize, pageIndex |
| updateFilter | /ng/api/filters | PUT | UNKNOWN | No pagination fields detected |
| postFilter | /ng/api/filters | POST | UNKNOWN | No pagination fields detected |
| getFilter | /ng/api/filters/{identifier} | GET | UNKNOWN | No pagination fields detected |
| deleteFilter | /ng/api/filters/{identifier} | DELETE | UNKNOWN | No pagination fields detected |
| getFrozenExecutionDetails | /ng/api/freeze/getFrozenExecutionDetails | GET | UNKNOWN | No pagination fields detected |
| getGlobalFreeze | /ng/api/freeze/getGlobalFreeze | GET | UNKNOWN | No pagination fields detected |
| getFreezeList | /ng/api/freeze/list | POST | OFFSET | size, page |
| getGitFullSyncConfig | /ng/api/git-full-sync/config | GET | UNKNOWN | No pagination fields detected |
| listFullSyncFiles | /ng/api/git-full-sync/files | POST | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getGitSyncConfigList | /ng/api/git-sync | GET | UNKNOWN | No pagination fields detected |
| getListOfBranchesWithStatus | /ng/api/git-sync-branch/listBranchesWithStatus | GET | OFFSET | size, page |
| listGitSyncErrors | /ng/api/git-sync-errors | GET | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| listGitToHarnessErrorsGroupedByCommits | /ng/api/git-sync-errors/aggregate | GET | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| listGitToHarnessErrorForCommit | /ng/api/git-sync-errors/commits/{commitId} | GET | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getGitSyncErrorsCount | /ng/api/git-sync-errors/count | GET | UNKNOWN | No pagination fields detected |
| getGitSyncSettings | /ng/api/git-sync-settings | GET | UNKNOWN | No pagination fields detected |
| isGitSyncEnabled | /ng/api/git-sync/git-sync-enabled | GET | UNKNOWN | No pagination fields detected |
| getClusterList | /ng/api/gitops/clusters | GET | OFFSET | size, page |
| getGcpRegions | /ng/api/google-secret-manager-connector/gcp-regions | GET | UNKNOWN | No pagination fields detected |
| filterHostsByConnector | /ng/api/hosts/filter | POST | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getInvites | /ng/api/invites | GET | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getInvite | /ng/api/invites/invite | GET | UNKNOWN | No pagination fields detected |
| ListAggregatedKeys | /ng/api/keys | GET | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getNgLdapSettings | /ng/api/ldap/ngLdapSettings | GET | UNKNOWN | No pagination fields detected |
| searchLdapGroups | /ng/api/ldap/{ldapId}/search/group | GET | UNKNOWN | No pagination fields detected |
| downloadCDUsageCSVReport | /ng/api/license-usage-cd/v2/{usageType}/csv/download | GET | UNKNOWN | No pagination fields detected |
| getHarnessOpenIdConfig_1 | /ng/api/oidc/account/{accountId}/.well-known/openid-configuration | GET | UNKNOWN | No pagination fields detected |
| getHarnessOpenIdConfig | /ng/api/oidc/account/{accountId}/.wellknown/jwks | GET | UNKNOWN | No pagination fields detected |
| getProviderList | /ng/api/provider | GET | UNKNOWN | No pagination fields detected |
| listServiceAccount | /ng/api/serviceaccount | GET | UNKNOWN | No pagination fields detected |
| listAggregatedServiceAccounts | /ng/api/serviceaccount/aggregate | GET | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getInheritingChildScopeListForServiceAccount | /ng/api/serviceaccount/{identifier}/scopes | GET | UNKNOWN | No pagination fields detected |
| getServiceList | /ng/api/servicesV2 | GET | OFFSET | size, page |
| hookActions | /ng/api/servicesV2/hooks/actions | GET | UNKNOWN | No pagination fields detected |
| kustomizeCmdFlags | /ng/api/servicesV2/kustomize/command-flags | GET | UNKNOWN | No pagination fields detected |
| getServiceAccessList | /ng/api/servicesV2/list/access | GET | OFFSET | size, page |
| getPluginInfo | /ng/api/servicesV2/plugin-info | GET | UNKNOWN | No pagination fields detected |
| getSettingsList | /ng/api/settings | GET | UNKNOWN | No pagination fields detected |
| getSmtpConfig | /ng/api/smtpConfig | GET | UNKNOWN | No pagination fields detected |
| getSourceCodeManagers | /ng/api/source-code-manager | GET | UNKNOWN | No pagination fields detected |
| getTasSpaces | /ng/api/tas/space | GET | UNKNOWN | No pagination fields detected |
| getTasSpacesV2 | /ng/api/tas/v2/space | GET | UNKNOWN | No pagination fields detected |
| listAggregatedTokens | /ng/api/token/aggregate | GET | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getCDLicenseUsageForServiceInstances | /ng/api/usage/CD/serviceInstancesLicense | GET | UNKNOWN | No pagination fields detected |
| getCDLicenseUsageForServices | /ng/api/usage/CD/servicesLicense | GET | UNKNOWN | No pagination fields detected |
| downloadActiveServiceCSVReport | /ng/api/usage/cd/active-services/csv/download | GET | UNKNOWN | No pagination fields detected |
| getUserSettingsList | /ng/api/user-settings | GET | UNKNOWN | No pagination fields detected |
| getUserPreferencesList | /ng/api/user-settings/get-user-preferences | GET | UNKNOWN | No pagination fields detected |
| getCurrentUserInfo | /ng/api/user/currentUser | GET | UNKNOWN | No pagination fields detected |
| checkIfLastAdmin | /ng/api/user/last-admin | GET | UNKNOWN | No pagination fields detected |
| getVariableList | /ng/api/variables | GET | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| listVariable | /ng/api/variables/list | POST | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| dashboard#metrics | /pm/api/v1/dashboard | GET | UNKNOWN | No pagination fields detected |
| evaluations#list | /pm/api/v1/evaluations | GET | OFFSET | per_page, page |
| evaluations#getYaml | /pm/api/v1/evaluations/getYaml | GET | UNKNOWN | No pagination fields detected |
| examples#list | /pm/api/v1/examples | GET | UNKNOWN | No pagination fields detected |
| system#health | /pm/api/v1/system/health | GET | UNKNOWN | No pagination fields detected |
| system#version | /pm/api/v1/system/version | GET | UNKNOWN | No pagination fields detected |
| Usage#ReportUsage | /sto/api/usage | GET | UNKNOWN | No pagination fields detected |
| Usage#UsageAllAccounts | /sto/api/usage/all-accounts | GET | UNKNOWN | No pagination fields detected |
| Exemptions#ListExemptions | /sto/api/v2/exemptions | GET | OFFSET | pageSize, page |
| Frontend#AllIssuesFilters | /sto/api/v2/frontend/all-issues/filters | GET | UNKNOWN | No pagination fields detected |
| Frontend#AllIssuesList | /sto/api/v2/frontend/all-issues/issues | GET | OFFSET | pageSize, page |
| Frontend#IssueSeverityChange | /sto/api/v2/frontend/exemption/{exemptionId}/issue-severity-change | GET | UNKNOWN | No pagination fields detected |
| Frontend#ImpactedTargetsForExemption | /sto/api/v2/frontend/exemption/{exemptionId}/targets | GET | OFFSET | pageSize, page |
| Frontend#ExemptionsFilters | /sto/api/v2/frontend/exemptions/filters | POST | UNKNOWN | No pagination fields detected |
| Frontend#ExecutionIssueCounts | /sto/api/v2/frontend/issue-counts | GET | UNKNOWN | No pagination fields detected |
| Frontend#OccurrenceDataflow | /sto/api/v2/frontend/issues/{issueId}/occurrence/{occurrenceInternalId}/dataflow | GET | UNKNOWN | No pagination fields detected |
| Frontend#QwietLicenseUsage | /sto/api/v2/frontend/metrics/licenseUsage | GET | UNKNOWN | No pagination fields detected |
| Frontend#OverviewBaselines | /sto/api/v2/frontend/overview/baselines | GET | UNKNOWN | No pagination fields detected |
| Frontend#OverviewHistoricalCounts | /sto/api/v2/frontend/overview/historical-counts | GET | UNKNOWN | No pagination fields detected |
| Frontend#SecurityReview | /sto/api/v2/frontend/security-review | GET | OFFSET | pageSize, page |
| Frontend#TestTargets | /sto/api/v2/frontend/test-targets | GET | OFFSET | pageSize, page |
| Issues#ListIssues | /sto/api/v2/issues | GET | OFFSET | pageSize, page |
| Overrides#ListOverrides | /sto/api/v2/overrides | GET | OFFSET | pageSize, page |
| Products#ListProducts | /sto/api/v2/products | GET | OFFSET | pageSize, page |
| Pull Requests#ListPullRequests | /sto/api/v2/pull-requests/repositories | GET | UNKNOWN | No pagination fields detected |
| Pull Requests#FindPullRequestByID | /sto/api/v2/pull-requests/repositories/pulls | GET | UNKNOWN | No pagination fields detected |
| Pull Requests#GetPullRequestCorrelation | /sto/api/v2/pull-requests/repositories/pulls/correlation | GET | UNKNOWN | No pagination fields detected |
| Qwiet#GetToken | /sto/api/v2/qwiet/token | GET | UNKNOWN | No pagination fields detected |
| Scans#ListScans | /sto/api/v2/scans | GET | OFFSET | pageSize, page |
| Scans#ScanIssueOccurrences | /sto/api/v2/scans/{id}/issue/{issueId}/occurrences | GET | OFFSET | pageSize, page |
| Scans#ScanIssues | /sto/api/v2/scans/{id}/issues | GET | UNKNOWN | No pagination fields detected |
| Scans#ScanIssueCounts | /sto/api/v2/scans/{id}/issues/counts | GET | UNKNOWN | No pagination fields detected |
| STO Data Frontend#AllIssuesList | /sto/api/v2/sto-data-frontend/all-issues/issues | POST | UNKNOWN | No pagination fields detected |
| System#health | /sto/api/v2/system/health | GET | UNKNOWN | No pagination fields detected |
| System#version | /sto/api/v2/system/version | GET | UNKNOWN | No pagination fields detected |
| Targets#ListTargets | /sto/api/v2/targets | GET | OFFSET | pageSize, page |
| Target Variants#ListTargetVariants | /sto/api/v2/targets/{targetId}/variants | GET | OFFSET | pageSize, page |
| Token#IssueToken | /sto/api/v2/token | GET | UNKNOWN | No pagination fields detected |
| TemplategetFilterList | /template/api/filters | GET | OFFSET | pageSize, pageIndex |
| TemplateupdateFilter | /template/api/filters | PUT | UNKNOWN | No pagination fields detected |
| TemplatepostFilter | /template/api/filters | POST | UNKNOWN | No pagination fields detected |
| TemplategetFilter | /template/api/filters/{identifier} | GET | UNKNOWN | No pagination fields detected |
| TemplatedeleteFilter | /template/api/filters/{identifier} | DELETE | UNKNOWN | No pagination fields detected |
| TemplatevalidateTemplateInputs | /template/api/refresh-template/validate-template-inputs | GET | UNKNOWN | No pagination fields detected |
| listTemplateUsage | /template/api/templates/entitySetupUsage/{templateIdentifier} | GET | OFFSET | pageSize, pageIndex |
| getTemplateMetadataList | /template/api/templates/list-metadata | POST | OFFSET | size, page |
| get-aggregation-rules | /v1/aggregation-rules | GET | UNKNOWN | No pagination fields detected |
| get-allow-list | /v1/allow-list | GET | UNKNOWN | No pagination fields detected |
| save-allow-list | /v1/allow-list | POST | UNKNOWN | No pagination fields detected |
| get-backstage-env-variables | /v1/backstage-env-variables | GET | UNKNOWN | No pagination fields detected |
| resolve-backstage-env-variables | /v1/backstage-env-variables/resolve | GET | UNKNOWN | No pagination fields detected |
| get-backstage-permissions | /v1/backstage-permissions | GET | UNKNOWN | No pagination fields detected |
| get-backstage-plugins | /v1/backstage-plugins-info | GET | UNKNOWN | No pagination fields detected |
| get-account-scoped-banners | /v1/banners | GET | UNKNOWN | No pagination fields detected |
| get-account-scoped-active-banners | /v1/banners/active | GET | UNKNOWN | No pagination fields detected |
| banners-allowed | /v1/banners/allowed | GET | UNKNOWN | No pagination fields detected |
| get-catalog-custom-properties-by-entity | /v1/catalog/custom-properties/entity | GET | UNKNOWN | No pagination fields detected |
| get-entities-by-catalog-custom-property | /v1/catalog/custom-properties/property | GET | UNKNOWN | No pagination fields detected |
| get-account-scoped-certificates | /v1/certificates | GET | UNKNOWN | No pagination fields detected |
| get-checks | /v1/checks | GET | UNKNOWN | No pagination fields detected |
| get-check-graph | /v1/checks/{check-id}/graph | GET | UNKNOWN | No pagination fields detected |
| get-check-stats | /v1/checks/{check-id}/stats | GET | UNKNOWN | No pagination fields detected |
| getComplianceStandardsFilters | /v1/compliance-standards/filters | GET | UNKNOWN | No pagination fields detected |
| get-v1-dailyModuleAccountAccess | /v1/dailyModuleAccountAccess | GET | UNKNOWN | No pagination fields detected |
| get-all-datasources-for-account | /v1/data-sources | GET | UNKNOWN | No pagination fields detected |
| get-data-sources-data-points-map | /v1/data-sources/data-points/map | GET | UNKNOWN | No pagination fields detected |
| get-data-points-for-data-source | /v1/data-sources/{data-source}/datapoints | GET | UNKNOWN | No pagination fields detected |
| V1ListDatabaseSchema | /v1/dbops/dbschema | GET | UNKNOWN | No pagination fields detected |
| V1GetCustomerConfig | /v1/dbops/execution-config/get-customer-config | GET | UNKNOWN | No pagination fields detected |
| V1GetDefaultConfig | /v1/dbops/execution-config/get-default-config | GET | UNKNOWN | No pagination fields detected |
| get-v1-devSubscriptions | /v1/devSubscriptions | GET | UNKNOWN | No pagination fields detected |
| get-entities | /v1/entities | GET | UNKNOWN | No pagination fields detected |
| get-entities-filters | /v1/entities/filters | GET | UNKNOWN | No pagination fields detected |
| get-entities-filters-by-query | /v1/entities/filters | POST | UNKNOWN | No pagination fields detected |
| get-entities-groups | /v1/entities/groups | GET | UNKNOWN | No pagination fields detected |
| get-json-schema | /v1/entities/json-schema | GET | UNKNOWN | No pagination fields detected |
| get-entities-kinds | /v1/entities/kinds | GET | UNKNOWN | No pagination fields detected |
| get-entity-facets | /v1/entity-facets | GET | UNKNOWN | No pagination fields detected |
| validate-eula-sign | /v1/eula/validate-sign | GET | UNKNOWN | No pagination fields detected |
| list-gitx-webhook-events | /v1/gitx-webhook-events | GET | UNKNOWN | No pagination fields detected |
| list-webhook-event-branches | /v1/gitx-webhook-events/list-branches | GET | UNKNOWN | No pagination fields detected |
| gitx-webhook-event-file-validation | /v1/gitx-webhook-events/{gitx-webhook-event}/validation-info | GET | UNKNOWN | No pagination fields detected |
| list-gitx-webhooks | /v1/gitx-webhooks | GET | UNKNOWN | No pagination fields detected |
| get-all-groups-for-account | /v1/groups | GET | UNKNOWN | No pagination fields detected |
| get-workflows-for-account | /v1/groups/workflows | GET | UNKNOWN | No pagination fields detected |
| get-groups-yaml | /v1/groups/yaml | GET | UNKNOWN | No pagination fields detected |
| get-home-page-layout-info | /v1/home-page-layout | GET | UNKNOWN | No pagination fields detected |
| get-yaml-for-home-page-layout | /v1/home-page-layout/yaml | GET | UNKNOWN | No pagination fields detected |
| getIntegrationsConfig | /v1/integrations/config | GET | UNKNOWN | No pagination fields detected |
| discover-entities | /v1/integrations/{integration-id}/discover/entities | GET | UNKNOWN | No pagination fields detected |
| create-ip-allowlist-config | /v1/ip-allowlist | POST | UNKNOWN | No pagination fields detected |
| get-ip-allowlist-configs | /v1/ip-allowlist | GET | UNKNOWN | No pagination fields detected |
| allowed-ip-address | /v1/ip-allowlist/allowed/ip-address | GET | UNKNOWN | No pagination fields detected |
| validate-unique-ip-allowlist-config-identifier | /v1/ip-allowlist/validate-unique-identifier/{ip-config-identifier} | GET | UNKNOWN | No pagination fields detected |
| validate-ip-address-allowlisted-or-not | /v1/ip-allowlist/validate/ip-address | GET | UNKNOWN | No pagination fields detected |
| get-ip-allowlist-config | /v1/ip-allowlist/{ip-config-identifier} | GET | UNKNOWN | No pagination fields detected |
| update-ip-allowlist-config | /v1/ip-allowlist/{ip-config-identifier} | PUT | UNKNOWN | No pagination fields detected |
| delete-ip-allowlist-config | /v1/ip-allowlist/{ip-config-identifier} | DELETE | UNKNOWN | No pagination fields detected |
| get-all-layouts | /v1/layout | GET | UNKNOWN | No pagination fields detected |
| get-layout-health | /v1/layout/health | GET | UNKNOWN | No pagination fields detected |
| get-account-ldap-settings | /v1/ldap-settings | GET | UNKNOWN | No pagination fields detected |
| ldap-settings-search-group | /v1/ldap-settings/search-group/{group-id} | GET | UNKNOWN | No pagination fields detected |
| get-account-licensed-modules | /v1/licensedModules | GET | UNKNOWN | No pagination fields detected |
| get-v1-listPrincipalsWithAccess | /v1/listPrincipalsWithAccess | GET | UNKNOWN | No pagination fields detected |
| post-v1-listPrincipalsWithAccess | /v1/listPrincipalsWithAccess | POST | UNKNOWN | No pagination fields detected |
| get-merged-plugins-config | /v1/merged-plugins-config | GET | UNKNOWN | No pagination fields detected |
| list-module-versions | /v1/module-versions | GET | UNKNOWN | No pagination fields detected |
| get-v1-moduleAccess | /v1/moduleAccess | GET | UNKNOWN | No pagination fields detected |
| get-v1-moduleLicenseUtilization | /v1/moduleLicenseUtilization | GET | UNKNOWN | No pagination fields detected |
| get-namespace-info | /v1/namespace-info | GET | UNKNOWN | No pagination fields detected |
| list-notification-channels-account | /v1/notification-channels | GET | UNKNOWN | No pagination fields detected |
| notification-resource-list | /v1/notification-resource-list | GET | UNKNOWN | No pagination fields detected |
| list-notification-rules-account | /v1/notification-rules | GET | UNKNOWN | No pagination fields detected |
| confluenceOauthTokenGenerate | /v1/oauth/confluence | GET | UNKNOWN | No pagination fields detected |
| msTeamsOauthTokenGenerate | /v1/oauth/msteams | GET | UNKNOWN | No pagination fields detected |
| slackOauthTokenGenerate | /v1/oauth/slack | GET | UNKNOWN | No pagination fields detected |
| zoomOauthTokenGenerate | /v1/oauth/zoom | GET | UNKNOWN | No pagination fields detected |
| list-oidc-provider | /v1/oidc-provider | GET | UNKNOWN | No pagination fields detected |
| get-oidc-provider-internal | /v1/oidc-provider/{providerIdentifier}/decrypt | GET | UNKNOWN | No pagination fields detected |
| get-harness-entities | /v1/onboarding/harness-entities | GET | UNKNOWN | No pagination fields detected |
| get-harness-entities-count | /v1/onboarding/harness-entities-count | GET | UNKNOWN | No pagination fields detected |
| collections#listCollections | /v1/org/units/list | POST | UNKNOWN | No pagination fields detected |
| categories#listCategories | /v1/org/workspaces/units/list | POST | UNKNOWN | No pagination fields detected |
| get-plugin-request | /v1/plugin/request | GET | UNKNOWN | No pagination fields detected |
| get-plugins | /v1/plugins-info | GET | UNKNOWN | No pagination fields detected |
| list-resource-groups-acc | /v1/resource-groups | GET | UNKNOWN | No pagination fields detected |
| filter-resource-groups | /v1/resource-groups/filter | POST | UNKNOWN | No pagination fields detected |
| get-account-scoped-role-assignments | /v1/role-assignments | GET | UNKNOWN | No pagination fields detected |
| get-role-assignments-count | /v1/role-assignments/count | GET | UNKNOWN | No pagination fields detected |
| get-scorecards | /v1/scorecards | GET | UNKNOWN | No pagination fields detected |
| get-scorecard-stats | /v1/scorecards/{scorecard-id}/stats | GET | UNKNOWN | No pagination fields detected |
| get-scorecards-scores-overview | /v1/scores | GET | UNKNOWN | No pagination fields detected |
| get-scorecards-graphs-score-summary | /v1/scores/graph | GET | UNKNOWN | No pagination fields detected |
| get-scores-recalibrate-status | /v1/scores/recalibrate/status | GET | UNKNOWN | No pagination fields detected |
| get-all-scorecard-summary | /v1/scores/summary | GET | UNKNOWN | No pagination fields detected |
| seiContributors#listContributors | /v1/sei_contributor/list | POST | UNKNOWN | No pagination fields detected |
| get-account-scoped-services | /v1/services | GET | UNKNOWN | No pagination fields detected |
| get-account-scoped-primary-manifests | /v1/services/{service}/primary-manifests | GET | UNKNOWN | No pagination fields detected |
| V1StepFlywayMigrationScripts | /v1/step/flyway/migrationscripts | GET | UNKNOWN | No pagination fields detected |
| get-streaming-destinations | /v1/streaming-destinations | GET | UNKNOWN | No pagination fields detected |
| getStreamingDestinationsAggregate | /v1/streaming-destinations/aggregate | GET | UNKNOWN | No pagination fields detected |
| get-streaming-destinations-cards | /v1/streaming-destinations/cards | GET | UNKNOWN | No pagination fields detected |
| validateUniqueIdentifier | /v1/streaming-destinations/{streaming-destination}/validate-unique-identifier | GET | UNKNOWN | No pagination fields detected |
| get-template-schema | /v1/template-schema/individual-schema | GET | UNKNOWN | No pagination fields detected |
| get-templates-list-acc | /v1/templates | GET | UNKNOWN | No pagination fields detected |
| get-acc-templates-inputs-schema | /v1/templates/{template}/versions/{version}/inputs-schema | GET | UNKNOWN | No pagination fields detected |
| Token#IssueToken1 | /v1/token | GET | UNKNOWN | No pagination fields detected |
| getVersion | /v1/version | GET | UNKNOWN | No pagination fields detected |
| list-account-webhooks | /v1/webhooks/list | POST | UNKNOWN | No pagination fields detected |


---

## Pipelines


| Endpoint / OperationId | Path | Method | Pagination Style | Evidence |

|------------------------|------|--------|------------------|----------|

| listPipelineOnboarding | /gateway/chaos/manager/api/rest/pipeline-onboarding | GET | UNKNOWN | No pagination fields detected |
| pipelineCanOnboardChaos | /gateway/chaos/manager/api/rest/pipeline-onboarding/{identity}/can-onboard-chaos | GET | UNKNOWN | No pagination fields detected |
| pipelineOnboardChaosStatus | /gateway/chaos/manager/api/rest/pipeline-onboarding/{identity}/status | GET | UNKNOWN | No pagination fields detected |
| verifyChaosStageInPipelineRun | /gateway/chaos/manager/api/rest/v2/pipeline/verify/runs | GET | UNKNOWN | No pagination fields detected |
| workspaces#list-pipelines | /iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/pipelines | GET | OFFSET | limit, page |
| PipelinegetFilterList | /pipeline/api/filters | GET | OFFSET | pageSize, pageIndex |
| PipelineupdateFilter | /pipeline/api/filters | PUT | UNKNOWN | No pagination fields detected |
| PipelinepostFilter | /pipeline/api/filters | POST | UNKNOWN | No pagination fields detected |
| PipelinegetFilter | /pipeline/api/filters/{identifier} | GET | UNKNOWN | No pagination fields detected |
| PipelinedeleteFilter | /pipeline/api/filters/{identifier} | DELETE | UNKNOWN | No pagination fields detected |
| downloadFileUsingFilePath | /pipeline/api/input-file/download-file | GET | UNKNOWN | No pagination fields detected |
| listInputSet | /pipeline/api/inputSets | GET | OFFSET | pageSize, pageIndex |
| postPipelineExecuteWithInputSetList | /pipeline/api/pipeline/execute/{identifier}/inputSetList | POST | UNKNOWN | No pagination fields detected |
| getListOfExecutionIdentifier | /pipeline/api/pipelines/execution/executionSummary | POST | OFFSET | size, page |
| getListOfExecutions | /pipeline/api/pipelines/execution/summary | POST | OFFSET | size, page |
| getListOfExecutionsOutline | /pipeline/api/pipelines/execution/summary/outline | POST | OFFSET | size |
| getPipelineExecutionAnnotations | /pipeline/api/pipelines/execution/{planExecutionId}/annotations | GET | UNKNOWN | No pagination fields detected |
| getAnnotationFullContent | /pipeline/api/pipelines/execution/{planExecutionId}/annotations/{contextId}/content | GET | UNKNOWN | No pagination fields detected |
| getInputsetYamlV2 | /pipeline/api/pipelines/execution/{planExecutionId}/inputsetV2 | GET | UNKNOWN | No pagination fields detected |
| getExecutionData | /pipeline/api/pipelines/execution/{planExecutionId}/metadata | GET | UNKNOWN | No pagination fields detected |
| getNotesForExecution | /pipeline/api/pipelines/execution/{planExecutionId}/notes | GET | UNKNOWN | No pagination fields detected |
| getPpolicyEvaluation | /pipeline/api/pipelines/execution/{planExecutionId}/policy-evaluation | GET | OFFSET | size, page |
| getWorkflowGraph | /pipeline/api/pipelines/execution/{planExecutionId}/workflow-graph | GET | UNKNOWN | No pagination fields detected |
| getPipelineList | /pipeline/api/pipelines/list | POST | OFFSET | size, page |
| getPipelineExecution | /pipeline/api/pipelines/pipelineExecution | GET | UNKNOWN | No pagination fields detected |
| listBranchSequences | /pipeline/api/pipelines/{pipelineIdentifier}/branch-sequences | GET | UNKNOWN | No pagination fields detected |
| getBranchSequence | /pipeline/api/pipelines/{pipelineIdentifier}/branch-sequences/current | GET | UNKNOWN | No pagination fields detected |
| validateTemplateInputs | /pipeline/api/refresh-template/validate-template-inputs | GET | UNKNOWN | No pagination fields detected |
| getListForTarget | /pipeline/api/triggers | GET | OFFSET | size, page |
| getTriggerCatalog | /pipeline/api/triggers/catalog | GET | UNKNOWN | No pagination fields detected |
| triggerEventHistoryBuildSourceType | /pipeline/api/triggers/eventHistory/artifact-manifest-info | GET | OFFSET | size, page |
| triggerEventHistoryUsingFilters | /pipeline/api/triggers/eventHistory/events | GET | OFFSET | size, page |
| getTriggerDetails | /pipeline/api/triggers/{triggerIdentifier}/details | GET | UNKNOWN | No pagination fields detected |
| triggerEventHistory | /pipeline/api/triggers/{triggerIdentifier}/eventHistory | GET | OFFSET | size, page |
| fetchWebhookDetails | /pipeline/api/webhook/triggerProcessingDetails | GET | UNKNOWN | No pagination fields detected |
| Frontend#PipelineSecurityIssues | /sto/api/v2/frontend/pipeline-security/issues | GET | OFFSET | pageExisting, pageSizeNew, pageSizeExisting, pageNew |
| Frontend#PipelineSecurityIssuesCSV | /sto/api/v2/frontend/pipeline-security/issues/csv | GET | OFFSET | pageExisting, pageSizeNew, pageSizeExisting, pageNew |
| Frontend#PipelineSecuritySteps | /sto/api/v2/frontend/pipeline-security/steps | GET | UNKNOWN | No pagination fields detected |
| pipeline-security#ExportPipelineSecurityIssuesCSV | /sto/api/v2/pipeline-security/issues/csv | GET | UNKNOWN | No pagination fields detected |
| V1GetPipelineExecutionStatus | /v1/orgs/{org}/projects/{project}/pipeline/{pipelineIdentifier}/status | GET | UNKNOWN | No pagination fields detected |
| list-pipelines | /v1/orgs/{org}/projects/{project}/pipelines | GET | UNKNOWN | No pagination fields detected |
| get-stages-execution-list | /v1/orgs/{org}/projects/{project}/pipelines/{pipeline}/execute/stages-execution-list | GET | UNKNOWN | No pagination fields detected |
| getPipelineArtifactList | /v1/orgs/{org}/projects/{project}/pipelines/{pipeline}/executions/{execution}/artifacts | POST | UNKNOWN | No pagination fields detected |
| getSSCASummary | /v1/orgs/{org}/projects/{project}/pipelines/{pipeline}/executions/{execution}/ssca-summary | GET | UNKNOWN | No pagination fields detected |
| get-pipeline-inputs | /v1/orgs/{org}/projects/{project}/pipelines/{pipeline}/inputs | GET | UNKNOWN | No pagination fields detected |
| get-inputs-schema-details | /v1/orgs/{org}/projects/{project}/pipelines/{pipeline}/inputs-schema | GET | UNKNOWN | No pagination fields detected |
| get-individual-static-schema | /v1/pipeline-schema/individual-schema | GET | UNKNOWN | No pagination fields detected |


---

## Projects


| Endpoint / OperationId | Path | Method | Pagination Style | Evidence |

|------------------------|------|--------|------------------|----------|

| getHistory | /cv/api/account/{accountIdentifier}/org/{orgIdentifier}/project/{projectIdentifier}/downtime/history | GET | OFFSET | pageNumber, pageSize |
| listDowntimes | /cv/api/account/{accountIdentifier}/org/{orgIdentifier}/project/{projectIdentifier}/downtime/list | GET | OFFSET | pageNumber, pageSize |
| getDowntimeAssociatedMonitoredServices | /cv/api/account/{accountIdentifier}/org/{orgIdentifier}/project/{projectIdentifier}/downtime/monitored-services | GET | OFFSET | pageNumber, pageSize |
| getServiceLevelObjectivesNg | /cv/api/account/{accountIdentifier}/org/{orgIdentifier}/project/{projectIdentifier}/slo/v2 | GET | OFFSET | offset, pageSize |
| getSLOHealthListViewNg | /cv/api/account/{accountIdentifier}/org/{orgIdentifier}/project/{projectIdentifier}/slo/v2/status-list | POST | OFFSET | pageNumber, pageSize |
| listSlo | /cv/api/v1/orgs/{org}/projects/{project}/slo | GET | OFFSET | limit, page |
| listIntegrations | /gateway/ssca-manager/v1/orgs/{org}/projects/{project}/integration | GET | UNKNOWN | No pagination fields detected |
| GetIntegration | /gateway/ssca-manager/v1/orgs/{org}/projects/{project}/integration/integration-summary | GET | UNKNOWN | No pagination fields detected |
| getIntegrationRepos | /gateway/ssca-manager/v1/orgs/{org}/projects/{project}/integration/{integration}/repos | GET | UNKNOWN | No pagination fields detected |
| queryAttestationsGraphQL | /gateway/ssca-manager/v2/orgs/{org}/projects/{project}/attestations/query | POST | UNKNOWN | No pagination fields detected |
| AgentProjectService_List | /gitops/api/v1/agents/{agentIdentifier}/projects | GET | UNKNOWN | No pagination fields detected |
| activities#list-activities | /iacm/api/orgs/{org}/projects/{project}/activities | GET | OFFSET | limit, page |
| activities#list-activity-resource-changes | /iacm/api/orgs/{org}/projects/{project}/activities/{id}/resource-changes | GET | UNKNOWN | No pagination fields detected |
| ansible#list-ansible-activities | /iacm/api/orgs/{org}/projects/{project}/ansible/activities | GET | OFFSET | limit, page |
| ansible#list-data | /iacm/api/orgs/{org}/projects/{project}/ansible/data | GET | OFFSET | limit, page |
| ansible#get-file | /iacm/api/orgs/{org}/projects/{project}/ansible/file | GET | UNKNOWN | No pagination fields detected |
| ansible#list-hosts | /iacm/api/orgs/{org}/projects/{project}/ansible/hosts | GET | OFFSET | limit, page |
| ansible#list-host-activities | /iacm/api/orgs/{org}/projects/{project}/ansible/hosts/{id}/activities | GET | OFFSET | limit, page |
| ansible#get-host-stats | /iacm/api/orgs/{org}/projects/{project}/ansible/hosts/{id}/stats | GET | UNKNOWN | No pagination fields detected |
| ansible#list-inventory | /iacm/api/orgs/{org}/projects/{project}/ansible/inventory | GET | OFFSET | limit, page |
| ansible#show-inventory-as-ansible | /iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{identifier}/ansible | GET | UNKNOWN | No pagination fields detected |
| ansible#show-inventory-groups | /iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{identifier}/groups | GET | OFFSET | limit, page |
| ansible#show-inventory-hosts | /iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{identifier}/hosts | GET | OFFSET | limit, page |
| ansible#show-inventory-vars | /iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{identifier}/vars | GET | OFFSET | limit, page |
| ansible#list-playbooks | /iacm/api/orgs/{org}/projects/{project}/ansible/playbook | GET | OFFSET | limit, page |
| ansible#show-playbook-vars | /iacm/api/orgs/{org}/projects/{project}/ansible/playbook/{identifier}/vars | GET | OFFSET | limit, page |
| approvals#list-approvals | /iacm/api/orgs/{org}/projects/{project}/approvals | GET | OFFSET | limit, page |
| costs#list-costs | /iacm/api/orgs/{org}/projects/{project}/costs | GET | OFFSET | limit, page |
| costs#list-costs-per-workspace | /iacm/api/orgs/{org}/projects/{project}/costs/{workspace} | GET | OFFSET | limit, page |
| executions#list-executions | /iacm/api/orgs/{org}/projects/{project}/executions | GET | OFFSET | limit, page |
| executions#list-cost-changes | /iacm/api/orgs/{org}/projects/{project}/executions/{pipeline_execution_id}/cost-changes | GET | UNKNOWN | No pagination fields detected |
| executions#list-cost-changes-all-stages | /iacm/api/orgs/{org}/projects/{project}/executions/{pipeline_execution_id}/cost-changes-all-stages | GET | UNKNOWN | No pagination fields detected |
| executions#list-cost-changes-all-stages-by-modules | /iacm/api/orgs/{org}/projects/{project}/executions/{pipeline_execution_id}/cost-changes-all-stages-by-modules | GET | UNKNOWN | No pagination fields detected |
| executions#list-resource-changes | /iacm/api/orgs/{org}/projects/{project}/executions/{pipeline_execution_id}/resource-changes | GET | UNKNOWN | No pagination fields detected |
| executions#list-resource-changes-all-stages | /iacm/api/orgs/{org}/projects/{project}/executions/{pipeline_execution_id}/resource-changes-all-stages | GET | UNKNOWN | No pagination fields detected |
| settings#list-default-pipelines | /iacm/api/orgs/{org}/projects/{project}/settings/default-pipelines | GET | UNKNOWN | No pagination fields detected |
| settings#check-push-data | /iacm/api/orgs/{org}/projects/{project}/settings/disabled | GET | UNKNOWN | No pagination fields detected |
| workspaces#list-all-workspace-tags | /iacm/api/orgs/{org}/projects/{project}/tags | GET | UNKNOWN | No pagination fields detected |
| variable_sets#list-variable-set-references-proj-level | /iacm/api/orgs/{org}/projects/{project}/variable-set/{identifier}/references | GET | UNKNOWN | No pagination fields detected |
| variable_sets#list-variable-sets-proj-level | /iacm/api/orgs/{org}/projects/{project}/variable-sets | GET | UNKNOWN | No pagination fields detected |
| workspaces#show-workspace-metrics | /iacm/api/orgs/{org}/projects/{project}/workspace-metrics | GET | UNKNOWN | No pagination fields detected |
| workspace_templates#get-workspace-template-reconciliation-diff | /iacm/api/orgs/{org}/projects/{project}/workspace/template/{workspace_id}/yaml-diff | GET | UNKNOWN | No pagination fields detected |
| workspaces#list-workspaces | /iacm/api/orgs/{org}/projects/{project}/workspaces | GET | OFFSET | limit, page |
| workspaces#list-provisioners-ratio | /iacm/api/orgs/{org}/projects/{project}/workspaces/provisioners-ratio | GET | UNKNOWN | No pagination fields detected |
| workspaces#list-workspace-modules | /iacm/api/orgs/{org}/projects/{project}/workspaces/{identifier}/modules | GET | UNKNOWN | No pagination fields detected |
| workspaces#list-resources | /iacm/api/orgs/{org}/projects/{project}/workspaces/{identifier}/resources | GET | OFFSET | limit, page |
| workspaces#search-resources | /iacm/api/orgs/{org}/projects/{project}/workspaces/{identifier}/resources/search | POST | UNKNOWN | No pagination fields detected |
| workspaces#list-data | /iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/data | GET | OFFSET | limit, page |
| workspaces#evaluate-data | /iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/data/{id}/evaluate-policy | GET | UNKNOWN | No pagination fields detected |
| workspaces#download-remote-execution | /iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/remote-executions/{id}/download | GET | UNKNOWN | No pagination fields detected |
| workspaces#list-workspace-resource-types | /iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/resource-types | GET | UNKNOWN | No pagination fields detected |
| workspaces#list-workspace-resource-types-and-attributes | /iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/resource-types-and-attributes | GET | UNKNOWN | No pagination fields detected |
| workspaces#list-workspace-resource-type-attributes | /iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/resource-types/{resource_type}/attributes | GET | UNKNOWN | No pagination fields detected |
| tf-standard-backend#pull-terraform-state | /iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/terraform-backend | GET | UNKNOWN | No pagination fields detected |
| variables#list-variables | /iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/variables | GET | UNKNOWN | No pagination fields detected |
| variables#get-variables-and-providers | /iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/variables/merged | GET | UNKNOWN | No pagination fields detected |
| getProjectList | /ng/api/projects | GET | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getProjectListWithMultiOrgFilter | /ng/api/projects/list | GET | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| getArtifactDetails | /v1/org/{org}/project/{project}/artifact/{artifact}/tag/{tag}/details | GET | UNKNOWN | No pagination fields detected |
| listArtifacts | /v1/org/{org}/project/{project}/artifacts | POST | UNKNOWN | No pagination fields detected |
| getPolicyViolations | /v1/org/{org}/project/{project}/enforcement/{enforcement-id}/policy-violations | GET | UNKNOWN | No pagination fields detected |
| getEnforcementSummary | /v1/org/{org}/project/{project}/enforcement/{enforcement-id}/summary | GET | UNKNOWN | No pagination fields detected |
| listLatestArtifacts | /v1/org/{org}/project/{project}/grouped-artifacts | POST | UNKNOWN | No pagination fields detected |
| downloadSbom | /v1/org/{org}/project/{project}/orchestration/{orchestration-id}/sbom-download | GET | UNKNOWN | No pagination fields detected |
| getSbomScorecard | /v1/org/{org}/project/{project}/orchestration/{orchestration-id}/sbom-scorecard | GET | UNKNOWN | No pagination fields detected |
| getOrchestrationSummary | /v1/org/{org}/project/{project}/orchestration/{orchestration-id}/summary | GET | UNKNOWN | No pagination fields detected |
| listConfigs | /v1/org/{org}/project/{project}/ssca-config | GET | UNKNOWN | No pagination fields detected |
| get-org-scoped-projects | /v1/orgs/{org}/projects | GET | UNKNOWN | No pagination fields detected |
| getArtifactV2OverviewByName | /v1/orgs/{org}/projects/{project}/artifact-overview | GET | UNKNOWN | No pagination fields detected |
| listArtifactSources | /v1/orgs/{org}/projects/{project}/artifact-sources | POST | UNKNOWN | No pagination fields detected |
| artifactListV2 | /v1/orgs/{org}/projects/{project}/artifact-sources/{source}/artifacts | POST | UNKNOWN | No pagination fields detected |
| getArtifactV2Overview | /v1/orgs/{org}/projects/{project}/artifact-sources/{source}/artifacts/{artifact}/overview | GET | UNKNOWN | No pagination fields detected |
| getBaselineForArtifact | /v1/orgs/{org}/projects/{project}/artifact/{artifact}/baseline | GET | UNKNOWN | No pagination fields detected |
| artifactList | /v1/orgs/{org}/projects/{project}/artifacts | POST | UNKNOWN | No pagination fields detected |
| getArtifactV2ChainOfCustody | /v1/orgs/{org}/projects/{project}/artifacts/{artifact}/chain-of-custody | GET | UNKNOWN | No pagination fields detected |
| get-project-scoped-certificates | /v1/orgs/{org}/projects/{project}/certificates | GET | UNKNOWN | No pagination fields detected |
| getCICDWorkflowsList | /v1/orgs/{org}/projects/{project}/ci-cd/list | POST | UNKNOWN | No pagination fields detected |
| getCICDWorkflowsSummary | /v1/orgs/{org}/projects/{project}/ci-cd/summary | GET | UNKNOWN | No pagination fields detected |
| getCICDOverview | /v1/orgs/{org}/projects/{project}/ci-cd/{workflow}/overview | GET | UNKNOWN | No pagination fields detected |
| fetchPluginsForWorkflow | /v1/orgs/{org}/projects/{project}/ci-cd/{workflow}/plugins | GET | UNKNOWN | No pagination fields detected |
| getCICDRulesEvaluationTrend | /v1/orgs/{org}/projects/{project}/ci-cd/{workflow}/rules/evalution-trend | GET | UNKNOWN | No pagination fields detected |
| codeRepositoriesList | /v1/orgs/{org}/projects/{project}/code-repos/list | POST | UNKNOWN | No pagination fields detected |
| getAllRepositoriesSummary | /v1/orgs/{org}/projects/{project}/code-repos/summary | GET | UNKNOWN | No pagination fields detected |
| getCodeRepositoryOverview | /v1/orgs/{org}/projects/{project}/code-repos/{code-repo}/overview | GET | UNKNOWN | No pagination fields detected |
| getRepoRulesEvaluationTrend | /v1/orgs/{org}/projects/{project}/code-repos/{code-repo}/rules/evalution-trend | GET | UNKNOWN | No pagination fields detected |
| fetchComplianceResultsByComplianceId | /v1/orgs/{org}/projects/{project}/compliance-results/compliances/{compliance}/artifacts | GET | UNKNOWN | No pagination fields detected |
| getComponents | /v1/orgs/{org}/projects/{project}/components | GET | UNKNOWN | No pagination fields detected |
| V2ListProjDbInstances | /v1/orgs/{org}/projects/{project}/dbinstancelist | POST | UNKNOWN | No pagination fields detected |
| V1ListProjDbSchema | /v1/orgs/{org}/projects/{project}/dbschema | GET | UNKNOWN | No pagination fields detected |
| V1GetDbOverview | /v1/orgs/{org}/projects/{project}/dbschema/overview | GET | UNKNOWN | No pagination fields detected |
| V1ChangesetYamlProjDbInstance | /v1/orgs/{org}/projects/{project}/dbschema/{dbschema}/dbinstance/{dbinstance}/changeset/yaml | GET | UNKNOWN | No pagination fields detected |
| V1ChangesetmetadataProjDbInstance | /v1/orgs/{org}/projects/{project}/dbschema/{dbschema}/dbinstance/{dbinstance}/changesetmetadata | GET | UNKNOWN | No pagination fields detected |
| V1MigrationStateFlywayInstance | /v1/orgs/{org}/projects/{project}/dbschema/{dbschema}/dbinstance/{dbinstance}/flyway/migrationstate | GET | UNKNOWN | No pagination fields detected |
| V1FetchMigrationScriptSql | /v1/orgs/{org}/projects/{project}/dbschema/{dbschema}/dbinstance/{dbinstance}/migration/scripts | GET | UNKNOWN | No pagination fields detected |
| V1MigrationStateProjDbInstance | /v1/orgs/{org}/projects/{project}/dbschema/{dbschema}/dbinstance/{dbinstance}/migrationstate | GET | UNKNOWN | No pagination fields detected |
| V1GetSnapshotObjectNames | /v1/orgs/{org}/projects/{project}/dbschema/{dbschema}/dbinstance/{dbinstance}/snapshot-object-names | GET | UNKNOWN | No pagination fields detected |
| V1ListProjDbSchemaInstance | /v1/orgs/{org}/projects/{project}/dbschema/{dbschema}/instancelist | POST | UNKNOWN | No pagination fields detected |
| V2ListProjDbSchema | /v1/orgs/{org}/projects/{project}/dbschemalist | POST | UNKNOWN | No pagination fields detected |
| V1DefaultLlmPipeline | /v1/orgs/{org}/projects/{project}/default-llm-pipeline | GET | UNKNOWN | No pagination fields detected |
| listExemptionsForProject | /v1/orgs/{org}/projects/{project}/exemptions | GET | UNKNOWN | No pagination fields detected |
| list-project-gitx-webhook-events | /v1/orgs/{org}/projects/{project}/gitx-webhook-events | GET | UNKNOWN | No pagination fields detected |
| list-project-gitx-webhook | /v1/orgs/{org}/projects/{project}/gitx-webhooks | GET | UNKNOWN | No pagination fields detected |
| list-input-sets | /v1/orgs/{org}/projects/{project}/input-sets | GET | UNKNOWN | No pagination fields detected |
| getHarnessPipelineIntegration | /v1/orgs/{org}/projects/{project}/integration/harness-pipeline | GET | UNKNOWN | No pagination fields detected |
| fetchReposInIntegration | /v1/orgs/{org}/projects/{project}/integration/{integration}/fetch-repos | GET | UNKNOWN | No pagination fields detected |
| list-notification-channels | /v1/orgs/{org}/projects/{project}/notification-channels | GET | UNKNOWN | No pagination fields detected |
| list-notification-rules | /v1/orgs/{org}/projects/{project}/notification-rules | GET | UNKNOWN | No pagination fields detected |
| listRemediations | /v1/orgs/{org}/projects/{project}/remediations/list | POST | UNKNOWN | No pagination fields detected |
| getOverallSummary | /v1/orgs/{org}/projects/{project}/remediations/overall-summary | GET | UNKNOWN | No pagination fields detected |
| getArtifactListForRemediation | /v1/orgs/{org}/projects/{project}/remediations/{remediation}/artifacts | POST | UNKNOWN | No pagination fields detected |
| getDeploymentsListForArtifactInRemediation | /v1/orgs/{org}/projects/{project}/remediations/{remediation}/artifacts/{artifact}/deployments | POST | UNKNOWN | No pagination fields detected |
| getArtifactInRemediationDetails | /v1/orgs/{org}/projects/{project}/remediations/{remediation}/artifacts/{artifact}/details | GET | UNKNOWN | No pagination fields detected |
| getRemediationDetails | /v1/orgs/{org}/projects/{project}/remediations/{remediation}/details | GET | UNKNOWN | No pagination fields detected |
| list-resource-groups-project | /v1/orgs/{org}/projects/{project}/resource-groups | GET | UNKNOWN | No pagination fields detected |
| get-project-scoped-role-assignments | /v1/orgs/{org}/projects/{project}/role-assignments | GET | UNKNOWN | No pagination fields detected |
| getComponentDrift | /v1/orgs/{org}/projects/{project}/sbom-drift/{drift}/components | GET | UNKNOWN | No pagination fields detected |
| getLicenseDrift | /v1/orgs/{org}/projects/{project}/sbom-drift/{drift}/licenses | GET | UNKNOWN | No pagination fields detected |
| get-services | /v1/orgs/{org}/projects/{project}/services | GET | UNKNOWN | No pagination fields detected |
| get-primary-manifests | /v1/orgs/{org}/projects/{project}/services/{service}/primary-manifests | GET | UNKNOWN | No pagination fields detected |
| get-templates-list-project | /v1/orgs/{org}/projects/{project}/templates | GET | UNKNOWN | No pagination fields detected |
| get-project-templates-inputs-schema | /v1/orgs/{org}/projects/{project}/templates/{template}/versions/{version}/inputs-schema | GET | UNKNOWN | No pagination fields detected |
| list-project-webhooks | /v1/orgs/{org}/projects/{project}/webhooks/list | POST | UNKNOWN | No pagination fields detected |
| getArtifactChainOfCustodyV2 | /v2/orgs/{org}/projects/{project}/artifacts/{artifact}/chain-of-custody | GET | UNKNOWN | No pagination fields detected |


---

## Secrets


| Endpoint / OperationId | Path | Method | Pagination Style | Evidence |

|------------------------|------|--------|------------------|----------|

| listSecretsV2 | /ng/api/v2/secrets | GET | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| listSecretsV3 | /ng/api/v2/secrets/list | POST | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| listSecretsV4 | /ng/api/v2/secrets/list/secrets | POST | UNKNOWN | Both styles detected: offset=pageSize,pageIndex,pageToken... |
| get-project-scoped-secrets | /v1/orgs/{org}/projects/{project}/secrets | GET | UNKNOWN | No pagination fields detected |
| get-org-scoped-secrets | /v1/orgs/{org}/secrets | GET | UNKNOWN | No pagination fields detected |
| get-account-scoped-secrets | /v1/secrets | GET | UNKNOWN | No pagination fields detected |


---

## Detection Logic


**OFFSET**: Response or parameters contain `pageIndex`, `pageSize`, `totalItems`, `totalPages`, `page`, `size`, `offset`, or `limit`


**CURSOR**: Response or parameters contain `nextPageToken`, `pageToken`, `cursor`, `nextCursor`, or `continuationToken`


**UNKNOWN**: No clear pagination pattern detected, or both styles present (ambiguous)


## Usage


This inventory is used in Branch 4 (domain API implementation) to determine the correct pagination 
implementation for each `list()` method. Each domain API file should reference this inventory to 
implement the appropriate pagination strategy for its list operations.
