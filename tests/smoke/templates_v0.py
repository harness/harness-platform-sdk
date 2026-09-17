import json

####################
# TemplatesV0 Tests
####################
print(f"{' TemplatesV0 ':#^40}")
pipeline_identifier = "simple_test"
print(f"TemplatesV0 -> List")
for list_templates_v0 in [elem for elem in client.templates_v0.list()]:
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
            "source": {"spec": {"script": 'echo "hello"'}, "type": "Inline"},
        },
        "timeout": "10m",
        "type": "ShellScript",
    },
    version_label="v1",
)

templates_v0 = client.templates_v0.get(identifier=templates_v0_request.identifier)
if templates_v0:
    print(f"\t -> Get : { templates_v0.identifier}")
    templates_v0_request.description = "UPDATE from Existing"
    templates_v0 = client.templates_v0.update(
        identifier=templates_v0.identifier, body=templates_v0_request
    )
    print(f"\t -> Updated : { templates_v0.identifier}")

else:
    templates_v0_request.description = "CREATE from New"
    templates_v0 = client.templates_v0.create(templates_v0_request)
    print(f"\t -> Created : { templates_v0.identifier}")
    templates_v0_request.description = "UPDATE after Creating"
    templates_v0 = client.templates_v0.update(
        identifier=templates_v0.identifier, body=templates_v0_request
    )
    print(f"\t -> Updated : { templates_v0.identifier}")
print(f"TemplatesV0 -> List")
for list_templates_v0 in [elem for elem in client.templates_v0.list()]:
    print(f"\t \t -> : {list_templates_v0.identifier}")

print(f"TemplatesV0 -> GetEntityUsage")
try:
    usage = client.templates_v0.get_entity_usage(identifier=templates_v0.identifier)
    print(f"\t -> GetEntityUsage : {usage}")
except Exception as e:
    print(f"\t -> GetEntityUsage FAILED: {e}")

print(f"TemplatesV0 -> GetLabels")
try:
    labels = client.templates_v0.get_labels(identifier=templates_v0.identifier)
    print(f"\t -> GetLabels : {labels}")
except Exception as e:
    print(f"\t -> GetLabels FAILED: {e}")

print(f"TemplatesV0 -> RefreshAndGet")
try:
    refreshed = client.templates_v0.refresh_and_get(
        identifier=templates_v0.identifier, branch="main"
    )
    print(f"\t -> RefreshAndGet : {refreshed.identifier}")
except Exception as e:
    print(f"\t -> RefreshAndGet FAILED: {e}")

if unit_cleanup:
    client.templates_v0.delete(
        identifier=templates_v0.identifier, version_label=templates_v0_request.version_label
    )
    print(f"\t -> Delete : { templates_v0.identifier}")
