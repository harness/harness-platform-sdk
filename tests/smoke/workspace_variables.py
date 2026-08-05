import json

####################
# WorkspaceVariables Tests
####################
print(f"{' WorkspaceVariables ':#^40}")
workspace_identifier = "iacm_test"
print(f"WorkspaceVariables -> List")
for list_workspace_variables in [
    elem for elem in client.workspace_variables.list(workspace_identifier=workspace_identifier)
]:
    # client._display_payload(list_workspace_variables)
    print(f"\t \t -> : {list_workspace_variables.identifier}")

workspace_variables_request = WorkspaceVariableCreateRequest(
    workspace_identifier="iacm_test",
    identifier="myvar",
    value="Simple Test",
    value_type="string",
    kind="tf",
)

workspace_variables = client.workspace_variables.get(
    workspace_identifier=workspace_variables_request.workspace_identifier,
    identifier=workspace_variables_request.identifier,
    kind=workspace_variables_request.kind,
)
# client._display_payload(workspace_variables)
if workspace_variables:
    print(f"\t -> Get : { workspace_variables.identifier}")
    workspace_variables_request.description = "UPDATE from Existing"
    workspace_variables = client.workspace_variables.update(
        identifier=workspace_variables.identifier, body=workspace_variables_request
    )
    print(f"\t -> Updated : { workspace_variables.identifier}")

else:
    workspace_variables = client.workspace_variables.create(workspace_variables_request)
    print(f"\t -> Created : { workspace_variables.identifier}")
    workspace_variables_request.description = "UPDATE after Creating"
    workspace_variables = client.workspace_variables.update(
        identifier=workspace_variables.identifier, body=workspace_variables_request
    )
    print(f"\t -> Updated : { workspace_variables.identifier}")
print(f"WorkspaceVariables -> List")
for list_workspace_variables in [
    elem for elem in client.workspace_variables.list(workspace_identifier=workspace_identifier)
]:
    print(f"\t \t -> : {list_workspace_variables.identifier}")

if unit_cleanup:
    client.workspace_variables.delete(
        identifier=workspace_variables_request.identifier,
        workspace_identifier=workspace_variables_request.workspace_identifier,
        kind=workspace_variables_request.kind,
    )
    print(f"\t -> Delete : { workspace_variables.identifier}")
