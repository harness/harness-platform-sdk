####################
# Roles Tests
####################
print(f"{' Roles ':#^40}")
print(f"Roles -> List")
for role in [elem for elem in client.roles.list()]:
    print(f"\t \t -> : {role.identifier}")
# print(roles[0].identifier)
spec = {"roleManagerIdentifier": "harnessSecretManager", "valueType": "Inline", "value": "changeme"}
role_request = RoleCreateRequest(
    identifier="simple_test",
    name="Simple Test",
    description="Initial",
    allowed_scope_levels=["project"],
    permissions=["core_template_edit"],
)
role = client.roles.get(identifier=role_request.identifier)
if role:
    print(f"\t -> Get : {role_request.identifier}")
    role_request.description = "UPDATE from Existing"
    role = client.roles.update(identifier=role.identifier, body=role_request)
    print(f"\t -> Updated : {role.identifier}")
else:
    role_request.description = "CREATE from New"
    role = client.roles.create(role_request)
    print(f"\t -> Created : {role.identifier}")
    role = client.roles.update(identifier=role.identifier, body=role_request)
    # print(role)
    role.description = "UPDATE after Creating"
    print(f"\t -> Updated : {role.identifier}")
print(f"roles -> List")
for role in [elem for elem in client.roles.list()]:
    print(f"\t \t -> : {role.identifier}")

if cleanup:
    client.roles.delete(identifier=role.identifier)
    print(f"\t -> Delete : {role.identifier}")
