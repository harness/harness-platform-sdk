import json

####################
# workspace_default_pipelines Tests
####################
print(f"{' workspace_default_pipelines ':#^40}")
# Test Project Default Pipeline
print(f"workspace_default_pipelines -> Create Request Objects")
workspace_default_pipelines_request = WorkspaceDefaultPipelineCreateRequest(
    pipeline_identifier="iacm_provision", operation="plan", provisioner="opentofu"
)
# Test Workspace-only Default Pipeline
workspace_default_pipelines_request_by_ws = WorkspaceDefaultPipelineCreateRequest(
    workspace_identifier="iacm_test",
    pipeline_identifier="iacm_provision",
    operation="apply",
    provisioner="opentofu",
)

# Return all Default Pipelines by Project
print(f"workspace_default_pipelines -> List by Project")
for list_workspace_default_pipelines in [
    elem for elem in client.workspace_default_pipelines.list()
]:
    print(f"\t \t -> : {list_workspace_default_pipelines.operation}")

print(f"workspace_default_pipelines -> Get Default by operation")
project_default_pipelines = client.workspace_default_pipelines.get(
    operation=workspace_default_pipelines_request.operation
)

if project_default_pipelines:
    print(f"\t -> Get [Found]: { project_default_pipelines.operation}")
else:
    print(f"\t -> Get [NotFound]: { workspace_default_pipelines_request.operation.value}")
project_default_pipelines = client.workspace_default_pipelines.update(
    body=workspace_default_pipelines_request
)
print(
    f"\t -> Updated : - { project_default_pipelines.pipeline_identifier} - { project_default_pipelines.operation}"
)
######

# Return all Default Pipelines by Workspace
print(f"workspace_default_pipelines -> List by Workspace")
for get_workspace_default_pipelines in list(
    client.workspace_default_pipelines.get(
        workspace_identifier=workspace_default_pipelines_request_by_ws.workspace_identifier
    )
):
    print(f"\t \t -> : {get_workspace_default_pipelines.operation}")

workspace_default_pipelines = client.workspace_default_pipelines.get(
    workspace_identifier=workspace_default_pipelines_request_by_ws.workspace_identifier,
    operation=workspace_default_pipelines_request_by_ws.operation,
)
if workspace_default_pipelines:
    print(f"\t -> Get [Found]: { workspace_default_pipelines.operation}")
else:
    print(f"\t -> Get [NotFound]: { workspace_default_pipelines_request_by_ws.operation.value}")

workspace_default_pipelines = client.workspace_default_pipelines.update(
    body=workspace_default_pipelines_request_by_ws
)
print(
    f"\t -> Updated : { workspace_default_pipelines.workspace_identifier} - { workspace_default_pipelines.pipeline_identifier} - { workspace_default_pipelines.operation}"
)

print(f"workspace_default_pipelines -> List by Workspace")
for get_workspace_default_pipelines in list(
    client.workspace_default_pipelines.get(
        workspace_identifier=workspace_default_pipelines_request_by_ws.workspace_identifier
    )
):
    print(f"\t \t -> : {get_workspace_default_pipelines.operation}")

print(f"workspace_default_pipelines -> List by Project")
for list_workspace_default_pipelines in [
    elem for elem in client.workspace_default_pipelines.list()
]:
    print(f"\t \t -> : {list_workspace_default_pipelines.operation}")

if unit_cleanup:
    client.workspace_default_pipelines.delete(body=workspace_default_pipelines_request_by_ws)
    print(
        f"\t -> Delete : { workspace_default_pipelines_request_by_ws.workspace_identifier} -{ workspace_default_pipelines_request_by_ws.pipeline_identifier} -  { workspace_default_pipelines_request_by_ws.operation.value}"
    )
    client.workspace_default_pipelines.delete(body=workspace_default_pipelines_request)
    print(
        f"\t -> Delete : { workspace_default_pipelines_request.workspace_identifier} -{ workspace_default_pipelines_request_by_ws.pipeline_identifier} -  { workspace_default_pipelines_request.operation.value}"
    )
