from harness_platform_sdk.models.ng_api.service_overrides import ServiceOverrideCreateRequest

####################
# ServiceOverrides Tests
####################
print(f"{' ServiceOverrides ':#^40}")
environment_identifier = "simple_test"
print(f"ServiceOverrides -> List")
for list_service_overrides in [
    elem for elem in client.service_overrides.list(override_type="ENV_GLOBAL_OVERRIDE")
]:
    # client._display_payload(list_service_overrides)
    print(f"\t \t -> : {list_service_overrides.identifier}")

service_overrides_request = ServiceOverrideCreateRequest(
    environment_identifier="simple_test",
    variables=[{"name": "this", "type": "String", "value": "is_it"}],
    type="ENV_GLOBAL_OVERRIDE",
)

service_overrides = client.service_overrides.get(environment_identifier=environment_identifier)
# client._display_payload(service_overrides)
if service_overrides:
    print(f"\t -> Get : {service_overrides.identifier}")
    service_overrides.variables += [{"name": "jeremy", "value": "runs", "type": "String"}]
    service_overrides = client.service_overrides.update(
        identifier=service_overrides.identifier, body=service_overrides
    )
    print(f"\t -> Updated : {service_overrides.identifier}")

else:
    service_overrides = client.service_overrides.create(service_overrides_request)
    print(f"\t -> Created : {service_overrides.identifier}")
    service_overrides = client.service_overrides.update(
        identifier=service_overrides.identifier, body=service_overrides_request
    )
    print(f"\t -> Updated : {service_overrides.identifier}")
print(f"ServiceOverrides -> List")
for list_service_overrides in [
    elem for elem in client.service_overrides.list(override_type="ENV_GLOBAL_OVERRIDE")
]:
    print(f"\t \t -> : {list_service_overrides.identifier}")

if unit_cleanup:
    client.service_overrides.delete(identifier=service_overrides.identifier)
    print(f"\t -> Delete : {service_overrides.identifier}")
