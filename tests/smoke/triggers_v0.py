import json

####################
# Trigger Tests
####################
print(f"{' Triggers ':#^40}")
pipeline_identifier = "simple_test"
print(f"Triggers -> List")
for list_trigger in [
    elem for elem in client.triggers_v0.list(pipeline_identifier=pipeline_identifier)
]:
    # client._display_payload(list_trigger)
    print(f"\t \t -> : {list_trigger.identifier}")

trigger_request = TriggerV0CreateRequest(
    pipeline_identifier="simple_test",
    identifier="simple_test",
    name="Simple Test",
    description="a test",
    source={
        "spec": {
            "spec": {
                "spec": {
                    "autoAbortPreviousExecutions": "false",
                    "connectorRef": "account.github",
                    "headerConditions": [],
                    "payloadConditions": [],
                    "repoName": "tmp"
                },
                "type": "Create"
            },
            "type": "Github"
        },
        "type": "Webhook"
    },
    inputs={
        "pipeline": {
            "identifier": "simple_test",
            "variables": [
                {
                    "name": "test",
                    "type": "String",
                    "value": "valueME"
                }
            ]
        }
    },
)

trigger = client.triggers_v0.get(
    identifier=trigger_request.identifier, pipeline_identifier=pipeline_identifier
)
# client._display_payload(trigger)
if trigger:
    print(f"\t -> Get : {trigger.identifier}")
    trigger_request.description = "UPDATE from Existing"
    trigger = client.triggers_v0.update(identifier=trigger.identifier, body=trigger_request)
    print(f"\t -> Updated : {trigger.identifier}")

else:
    trigger_request.description = "CREATE from New"
    trigger = client.triggers_v0.create(trigger_request)
    print(f"\t -> Created : {trigger.identifier}")
    trigger_request.description = "UPDATE after Creating"
    trigger = client.triggers_v0.update(identifier=trigger.identifier, body=trigger_request)
    print(f"\t -> Updated : {trigger.identifier}")
print(f"Triggers -> List")
for list_trigger in [
    elem for elem in client.triggers_v0.list(pipeline_identifier=pipeline_identifier)
]:
    print(f"\t \t -> : {list_trigger.identifier}")

if unit_cleanup:
    client.triggers_v0.delete(
        identifier=trigger.identifier, pipeline_identifier=pipeline_identifier
    )
    print(f"\t -> Delete : {trigger.identifier}")
