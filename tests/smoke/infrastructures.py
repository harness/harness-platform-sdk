import json

####################
# Infrastructures Tests
####################
print(f"{' Infrastructures ':#^40}")
environment_identifier = "simple_test"
print(f"Infrastructures -> List")
for list_infrastructures in [
    elem for elem in client.infrastructures.list(environment_identifier=environment_identifier)
]:
    # client._display_payload(list_infrastructures)
    print(f"\t \t -> : {list_infrastructures.identifier}")

infrastructures_request = InfrastructureCreateRequest(
    environment_identifier="simple_test",
    identifier="simple_test",
    name="Simple Test",
    description="a test",
    type="KubernetesDirect",
    deployment_type="Kubernetes",
    spec={
        "connectorRef": "<+input>",
        "namespace": "<+input>",
        "releaseName": "release-<+INFRA_KEY_SHORT_ID>",
    },
    allow_simultaneous_deployments=True,
)

infrastructures = client.infrastructures.get(
    identifier=infrastructures_request.identifier, environment_identifier=environment_identifier
)
# client._display_payload(infrastructures)
if infrastructures:
    print(f"\t -> Get : { infrastructures.identifier}")
    infrastructures_request.description = "UPDATE from Existing"
    infrastructures = client.infrastructures.update(
        identifier=infrastructures.identifier, body=infrastructures_request
    )
    print(f"\t -> Updated : { infrastructures.identifier}")

else:
    infrastructures_request.description = "CREATE from New"
    infrastructures = client.infrastructures.create(infrastructures_request)
    print(f"\t -> Created : { infrastructures.identifier}")
    infrastructures_request.description = "UPDATE after Creating"
    infrastructures = client.infrastructures.update(
        identifier=infrastructures.identifier, body=infrastructures_request
    )
    print(f"\t -> Updated : { infrastructures.identifier}")
print(f"Infrastructures -> List")
for list_infrastructures in [
    elem for elem in client.infrastructures.list(environment_identifier=environment_identifier)
]:
    print(f"\t \t -> : {list_infrastructures.identifier}")

if unit_cleanup:
    client.infrastructures.delete(
        identifier=infrastructures.identifier, environment_identifier=environment_identifier
    )
    print(f"\t -> Delete : { infrastructures.identifier}")
