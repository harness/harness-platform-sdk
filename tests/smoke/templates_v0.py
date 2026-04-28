import json

####################
# TemplatesV0 Tests
####################
print(f"{' TemplatesV0 ':#^40}")
pipeline_identifier = "simple_test"
print(f"TemplatesV0 -> List")
for list_templates_v0 in [
    elem for elem in client.templates_v0.list()
]:
    # client._display_payload(list_templates_v0)
    print(f"\t \t -> : {list_templates_v0.identifier}")

templates_v0_request = TemplateV0CreateRequest(
    pipeline_identifier="simple_test",
    identifier="simple_test",
    name="Simple Test",
    description="a test",
    template_entity_type="Step",
    template_spec={
        "spec": {
            "delegateSelectors": [],
            "environmentVariables": [],
            "executionTarget": {},
            "outputVariables": [],
            "shell": "Bash",
            "source": {
                "spec": {
                    "script": "echo \"hello\""
                },
                "type": "Inline"
            }
        },
        "timeout": "10m",
        "type": "ShellScript"
    },
    version_label="v1"
)

templates_v0 = client.templates_v0.get(
    identifier=templates_v0_request.identifier
)
# client._display_payload(templates_v0)
if templates_v0:
    print(f"\t -> Get : { templates_v0.identifier}")
    templates_v0_request.description = "UPDATE from Existing"
    templates_v0 = client.templates_v0.update(identifier=templates_v0.identifier, body=templates_v0_request)
    # client._display_payload(templates_v0)
    print(f"\t -> Updated : { templates_v0.identifier}")

else:
    templates_v0_request.description = "CREATE from New"
    templates_v0 = client.templates_v0.create(templates_v0_request)
    # client._display_payload(templates_v0)
    print(f"\t -> Created : { templates_v0.identifier}")
    templates_v0_request.description = "UPDATE after Creating"
    templates_v0 = client.templates_v0.update(identifier=templates_v0.identifier, body=templates_v0_request)
    print(f"\t -> Updated : { templates_v0.identifier}")
print(f"TemplatesV0 -> List")
for list_templates_v0 in [
    elem for elem in client.templates_v0.list()
]:
    print(f"\t \t -> : {list_templates_v0.identifier}")

if unit_cleanup:
    client.templates_v0.delete(
        identifier=templates_v0.identifier,
        version_label=templates_v0_request.version_label
    )
    print(f"\t -> Delete : { templates_v0.identifier}")
