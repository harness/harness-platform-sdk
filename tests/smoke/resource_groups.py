####################
# ResourceGroups Tests
####################
print(f"{' ResourceGroups ':#^40}")
print(f"ResourceGroups -> List")
for resource_group in [elem for elem in client.resource_groups.list()]:
    print(f"\t \t -> : {resource_group.identifier}")
spec = {
    "resource_groupManagerIdentifier": "harnessSecretManager",
    "valueType": "Inline",
    "value": "changeme",
}
resource_group_request = ResourceGroupCreateRequest(
    identifier="simple_test",
    name="Simple Test",
    description="Initial",
    allowed_scope_levels=["project"],
    resource_filter={"resources": [], "includeAllResource": "true"},
    included_scopes=[{"filter": "EXCLUDING_CHILD_SCOPES"}],
)
resource_group = client.resource_groups.get(identifier=resource_group_request.identifier)
if resource_group:
    print(f"\t -> Get : {resource_group_request.identifier}")
    resource_group_request.description = "UPDATE from Existing"
    resource_group = client.resource_groups.update(
        identifier=resource_group.identifier, body=resource_group_request
    )
    print(f"\t -> Updated : {resource_group.identifier}")
else:
    resource_group_request.description = "CREATE from New"
    resource_group = client.resource_groups.create(resource_group_request)
    print(f"\t -> Created : {resource_group.identifier}")
    resource_group = client.resource_groups.update(
        identifier=resource_group.identifier, body=resource_group_request
    )
    # print(resource_group)
    resource_group.description = "UPDATE after Creating"
    print(f"\t -> Updated : {resource_group.identifier}")
print(f"resource_groups -> List")
for resource_group in [elem for elem in client.resource_groups.list()]:
    print(f"\t \t -> : {resource_group.identifier}")

if cleanup:
    client.resource_groups.delete(identifier=resource_group.identifier)
    print(f"\t -> Delete : {resource_group.identifier}")
