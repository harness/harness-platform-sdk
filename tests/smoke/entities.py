import json

####################
# Entities Tests
####################
print(f"{' Entities ':#^40}")
pipeline_identifier = "simple_test"
print(f"Entities -> List")
for list_entities in [
    elem for elem in client.entities.list()
]:
    # client._display_payload(list_entities)
    print(f"\t \t -> : {list_entities.identifier}")

entities_request = EntityResourceCreateRequest(
    identifier="simple_test",
    name="Simple Test",
    description="a test",
    lifecycle="production",
    type="sdk_test",
    owner="test"
)

entities = client.entities.get(
    identifier=entities_request.identifier,
    kind=entities_request.kind
)
# client._display_payload(entities)
if entities:
    print(f"\t -> Get : { entities.identifier}")
    entities_request.description = "UPDATE from Existing"
    entities = client.entities.update(identifier=entities.identifier, kind=entities_request.kind, body=entities_request)
    print(f"\t -> Updated : { entities.identifier}")

else:
    entities_request.description = "CREATE from New"
    entities = client.entities.create(entities_request)
    # client._display_payload(entities)
    print(f"\t -> Created : { entities.identifier}")
    entities_request.description = "UPDATE after Creating"
    entities = client.entities.update(identifier=entities.identifier, kind=entities_request.kind, body=entities_request)
    print(f"\t -> Updated : { entities.identifier}")
print(f"Entities -> List")
for list_entities in [
    elem for elem in client.entities.list(pipeline_identifier=pipeline_identifier)
]:
    print(f"\t \t -> : {list_entities.identifier}")

if unit_cleanup:
    client.entities.delete(
        identifier=entities.identifier, kind=entities_request.kind
    )
    print(f"\t -> Delete : { entities.identifier}")
