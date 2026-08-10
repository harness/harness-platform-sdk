import json

####################
# WorkspaceStates Tests
####################
print(f"{' WorkspaceStates ':#^40}")
# print(f"WorkspaceStates -> List")
# for list_workspace_states in [
#     elem for elem in client.workspace_states.list(pipeline_identifier=pipeline_identifier)
# ]:
#     print(f"\t \t -> : {list_workspace_states.identifier}")

workspace_states_request = WorkspaceStateCreateRequest(
    identifier="simple_test",
    terraform_version="1.10.0",
    lineage="avalue",
    resources=[
        {
            "mode": "data",
            "type": "harness_platform_organization",
            "name": "selected",
            "provider": 'provider["registry.opentofu.org/harness/harness"]',
            "instances": [
                {
                    "schema_version": 0,
                    "attributes": {
                        "description": "Centralized Harness Platform Management",
                        "id": "Harness_Platform_Management",
                        "identifier": "Harness_Platform_Management",
                        "name": "Harness Platform Management",
                        "tags": [
                            "created_by:Terraform",
                            "harnessSolutionsFactory:true",
                            "managedResource:true",
                        ],
                    },
                    "sensitive_attributes": [],
                }
            ],
        },
    ],
)

workspace_states = client.workspace_states.get(identifier=workspace_states_request.identifier)
if workspace_states:
    print(f"\t -> Get : { workspace_states.identifier}")
    workspace_states_request.description = "UPDATE from Existing"
    workspace_states = client.workspace_states.create(
        identifier=workspace_states_request.identifier, body=workspace_states_request
    )
    print(f"\t -> Updated : { workspace_states.identifier}")
else:
    workspace_states_request.description = "CREATE from New"
    workspace_states = client.workspace_states.create(
        identifier=workspace_states_request.identifier, body=workspace_states_request
    )
    print(f"\t -> Created : { workspace_states.identifier}")
# print(f"WorkspaceStates -> List")
# for list_workspace_states in [
#     elem for elem in client.workspace_states.list(pipeline_identifier=pipeline_identifier)
# ]:
#     print(f"\t \t -> : {list_workspace_states.identifier}")

# if unit_cleanup:
#     client.workspace_states.delete(
#         identifier=workspace_states.identifier, pipeline_identifier=pipeline_identifier
#     )
#     print(f"\t -> Delete : { workspace_states.identifier}")
