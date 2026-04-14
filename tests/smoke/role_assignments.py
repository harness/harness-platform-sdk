####################
# RoleAssignment Tests
####################
print(f"{' RoleAssignments ':#^40}")
print(f"RoleAssignments -> List")
for list_role_assignment in [elem for elem in client.role_assignments.list()]:
    print(f"\t \t -> : {list_role_assignment.identifier}")

role_assignment_request = RoleAssignmentCreateRequest(
    identifier="simple_test",
    name="Simple Test",
    role_identifier="_project_admin",
    resource_group_identifier="_all_project_level_resources",
    principal={"identifier": "_project_all_users", "type": "USER_GROUP"},
    role_reference={"identifier": "simple_test", "scopeLevel": "project"},
)
role_assignment = client.role_assignments.get(identifier=role_assignment_request.identifier)
# print(role_assignment)
if role_assignment:
    print(f"\t -> Get : {role_assignment.identifier}")
    role_assignment_request.description = "UPDATE from Existing"
    role_assignment = client.role_assignments.update(
        identifier=role_assignment.identifier, body=role_assignment_request
    )
    print(f"\t -> Updated : {role_assignment.identifier}")

else:
    role_assignment_request.description = "CREATE from New"
    role_assignment = client.role_assignments.create(role_assignment_request)
    print(f"\t -> Created : {role_assignment.identifier}")
    role_assignment = client.role_assignments.update(
        identifier=role_assignment.identifier, body=role_assignment_request
    )
    role_assignment_request.description = "UPDATE after Creating"
    print(f"\t -> Updated : {role_assignment.identifier}")
print(f"RoleAssignments -> List")
for list_role_assignment in [elem for elem in client.role_assignments.list()]:
    print(f"\t \t -> : {list_role_assignment.identifier}")

if cleanup:
    client.role_assignments.delete(identifier=role_assignment.identifier)
    print(f"\t -> Delete : {role_assignment.identifier}")
