import json

from harness_platform_sdk.models.ng_api import *

####################
# Variables Tests
####################
print(f"{' Variables ':#^40}")
pipeline_identifier = "simple_test"
print(f"Variables -> List")
for list_variables in [elem for elem in client.variables.list()]:
    print(f"\t \t -> : {list_variables.identifier}")

variables_request = VariableCreateRequest(
    pipeline_identifier="simple_test",
    identifier="simple_test",
    name="Simple Test",
    description="a test",
    type="String",
    spec=VariableSpec(
        value_type="FIXED",
        type="string",
        fixed_value="changeme",
    ),
)

variables = client.variables.get(
    identifier=variables_request.identifier,
)
if variables:
    print(f"\t -> Get : { variables.identifier}")
    variables_request.description = "UPDATE from Existing"
    variables_request.spec.fixed_value = "UPDATED"
    variables = client.variables.update(identifier=variables.identifier, body=variables_request)
    print(f"\t -> Updated : { variables.identifier}")

else:
    variables_request.description = "CREATE from New"
    variables = client.variables.create(variables_request)
    print(f"\t -> Created : { variables.identifier}")
    variables_request.description = "UPDATE after Creating"
    variables = client.variables.update(identifier=variables.identifier, body=variables_request)
    print(f"\t -> Updated : { variables.identifier}")
print(f"Variables -> List")
for list_variables in [elem for elem in client.variables.list()]:
    print(f"\t \t -> : {list_variables.identifier}")

if unit_cleanup:
    client.variables.delete(
        identifier=variables.identifier,
    )
    print(f"\t -> Delete : { variables.identifier}")
