import json

####################
# InputSet Tests
####################
print(f"{' InputSets ':#^40}")
pipeline_identifier = "simple_test"
print(f"InputSets -> List")
for list_input_set in [
    elem for elem in client.input_sets_v0.list(pipeline_identifier=pipeline_identifier)
]:
    # print(f"\t \t -> : {json.dumps(dict(list_input_set), indent=4, sort_keys=True)}")
    print(f"\t \t -> : {list_input_set.identifier}")

input_set_request = InputSetV0CreateRequest(
    pipeline_identifier="simple_test",
    identifier="simple_test",
    name="Simple Test",
    description="a test",
    variables=[
        {
            "name": "test",
            "type": "String",
            "description": "",
            "required": False,
            "value": "<+input>",
        }
    ],
)

input_set = client.input_sets_v0.get(
    identifier=input_set_request.identifier, pipeline_identifier=pipeline_identifier
)
# print(input_set)
if input_set:
    print(f"\t -> Get : {input_set.identifier}")
    input_set_request.description = "UPDATE from Existing"
    input_set = client.input_sets_v0.update(identifier=input_set.identifier, body=input_set_request)
    print(f"\t -> Updated : {input_set.identifier}")

else:
    input_set_request.description = "CREATE from New"
    input_set = client.input_sets_v0.create(input_set_request)
    print(f"\t -> Created : {input_set.identifier}")
    input_set_request.description = "UPDATE after Creating"
    input_set = client.input_sets_v0.update(identifier=input_set.identifier, body=input_set_request)
    print(f"\t -> Updated : {input_set.identifier}")
print(f"InputSets -> List")
for list_input_set in [
    elem for elem in client.input_sets_v0.list(pipeline_identifier=pipeline_identifier)
]:
    print(f"\t \t -> : {list_input_set.identifier}")

if cleanup:
    client.input_sets_v0.delete(
        identifier=input_set.identifier, pipeline_identifier=pipeline_identifier
    )
    print(f"\t -> Delete : {input_set.identifier}")
