import json

####################
# EnvironmentsV2 Tests
####################
print(f"{' EnvironmentsV2 ':#^40}")
pipeline_identifier = "simple_test"
print(f"EnvironmentsV2 -> List")
for list_environments_v2 in [
    elem for elem in client.environments_v2.list(pipeline_identifier=pipeline_identifier)
]:
    # client._display_payload(list_environments_v2)
    print(f"\t \t -> : {list_environments_v2.identifier}")

environments_v2_request = EnvironmentV2CreateRequest(
    pipeline_identifier="simple_test",
    identifier="simple_test",
    name="Simple Test",
    description="a test",
    type="PreProduction",
)

environments_v2 = client.environments_v2.get(identifier=environments_v2_request.identifier)
# client._display_payload(environments_v2)
if environments_v2:
    print(f"\t -> Get : { environments_v2.identifier}")
    environments_v2_request.description = "UPDATE from Existing"
    environments_v2 = client.environments_v2.update(
        identifier=environments_v2.identifier, body=environments_v2_request
    )
    print(f"\t -> Updated : { environments_v2.identifier}")

else:
    environments_v2_request.description = "CREATE from New"
    environments_v2 = client.environments_v2.create(environments_v2_request)
    print(f"\t -> Created : { environments_v2.identifier}")
    environments_v2_request.description = "UPDATE after Creating"
    environments_v2 = client.environments_v2.update(
        identifier=environments_v2.identifier, body=environments_v2_request
    )
    print(f"\t -> Updated : { environments_v2.identifier}")
print(f"EnvironmentsV2 -> List")
for list_environments_v2 in [
    elem for elem in client.environments_v2.list(pipeline_identifier=pipeline_identifier)
]:
    print(f"\t \t -> : {list_environments_v2.identifier}")

if unit_cleanup:
    client.environments_v2.delete(identifier=environments_v2.identifier)
    print(f"\t -> Delete : { environments_v2.identifier}")
