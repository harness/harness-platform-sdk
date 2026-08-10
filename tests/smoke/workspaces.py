import json

####################
# Workspaces Tests
####################
print(f"{' Workspaces ':#^40}")
pipeline_identifier = "simple_test"
print(f"Workspaces -> List")
for list_workspaces in [elem for elem in client.workspaces.list()]:
    print(f"\t \t -> : {list_workspaces.identifier}")

workspaces_request = WorkspaceCreateRequest(
    identifier="simple_test",
    name="Simple Test",
    description="a test",
    provisioner="opentofu",
    repository_branch="main",
)

workspaces = client.workspaces.get(
    identifier=workspaces_request.identifier,
)
if workspaces:
    print(f"\t -> Get : { workspaces.identifier}")
    workspaces_request.description = "UPDATE from Existing"
    workspaces = client.workspaces.update(identifier=workspaces.identifier, body=workspaces_request)
    print(f"\t -> Updated : { workspaces.identifier}")

else:
    workspaces_request.description = "CREATE from New"
    workspaces = client.workspaces.create(workspaces_request)
    print(f"\t -> Created : { workspaces.identifier}")
    workspaces_request.description = "UPDATE after Creating"
    workspaces = client.workspaces.update(identifier=workspaces.identifier, body=workspaces_request)
    print(f"\t -> Updated : { workspaces.identifier}")
print(f"Workspaces -> List")
for list_workspaces in [elem for elem in client.workspaces.list()]:
    print(f"\t \t -> : {list_workspaces.identifier}")

if unit_cleanup:
    client.workspaces.delete(
        identifier=workspaces.identifier,
    )
    print(f"\t -> Delete : { workspaces.identifier}")
