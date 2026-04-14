####################
# UserGroup Tests
####################
print(f"{' UserGroups ':#^40}")
print(f"UserGroups -> List")
for list_user_group in [elem for elem in client.user_groups.list()]:
    print(f"\t \t -> : {list_user_group.identifier}")

user_group_request = UserGroupCreateRequest(identifier="simple_test", name="Simple Test")
user_group = client.user_groups.get(identifier=user_group_request.identifier)
# print(user_group)
if user_group:
    print(f"\t -> Get : {user_group.identifier}")
    user_group_request.description = "UPDATE from Existing"
    user_group = client.user_groups.update(
        identifier=user_group.identifier, body=user_group_request
    )
    print(f"\t -> Updated : {user_group.identifier}")

else:
    user_group_request.description = "CREATE from New"
    user_group = client.user_groups.create(user_group_request)
    print(f"\t -> Created : {user_group.identifier}")
    user_group = client.user_groups.update(
        identifier=user_group.identifier, body=user_group_request
    )
    user_group_request.description = "UPDATE after Creating"
    print(f"\t -> Updated : {user_group.identifier}")
print(f"UserGroups -> List")
for list_user_group in [elem for elem in client.user_groups.list()]:
    print(f"\t \t -> : {list_user_group.identifier}")

if cleanup:
    client.user_groups.delete(identifier=user_group.identifier)
    print(f"\t -> Delete : {user_group.identifier}")
