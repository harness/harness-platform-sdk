# import json

# ####################
# # CatalogCustomProperty Tests
# ####################
print(f"{' CatalogCustomProperty ':#^40}")
default_identifier = "lab"
default_kind = "resource"
default_scope = client._default_scope
default_scope = Scope(
    account_id=client.account_id, org="Harness_Platform_Management", project="Solutions_Factory"
)
print(f"CatalogCustomProperty -> Get Entities by a given property")
for list_catalog_custom_properties in [
    elem
    for elem in client.catalog_custom_properties.get_by_property(
        catalog_property="metadata.hsf.is_drifted", scope=default_scope
    )
]:
    # client._display_payload(list_catalog_custom_properties)
    print(
        f"\t \t -> : {list_catalog_custom_properties.identifier} = {list_catalog_custom_properties.value}"
    )
print(f"CatalogCustomProperty -> Get Properties for a given entity")
list_catalog_custom_properties = client.catalog_custom_properties.get_by_entity(
    identifier=default_identifier, kind=default_kind, scope=default_scope
)
# client._display_payload(list_catalog_custom_properties)
print(
    f"\t \t -> : {list_catalog_custom_properties.identifier} = {list_catalog_custom_properties.properties}"
)

catalog_custom_properties_request = CatalogCustomPropertyCreateRequest(
    identifier=default_identifier,
    kind=default_kind,
    mode="replace",
    catalog_property="metadata.hsf.is_drifted",
    value=True,
)
catalog_custom_properties = client.catalog_custom_properties.create(
    catalog_custom_properties_request, scope=default_scope
)
print(
    f"\t -> Created : { catalog_custom_properties.identifier} = { catalog_custom_properties.value}"
)
catalog_custom_properties_request.value = False
catalog_custom_properties = client.catalog_custom_properties.update(
    catalog_custom_properties_request, scope=default_scope
)
print(
    f"\t -> Created : { catalog_custom_properties.identifier} = { catalog_custom_properties.value}"
)
list_catalog_custom_properties = client.catalog_custom_properties.get_by_entity(
    identifier=default_identifier, kind=default_kind, scope=default_scope
)
print(
    f"\t \t -> : {list_catalog_custom_properties.identifier} = {list_catalog_custom_properties.properties}"
)

if unit_cleanup:
    client.catalog_custom_properties.delete(catalog_custom_properties_request, scope=default_scope)
    print(f"\t -> Delete : { catalog_custom_properties.identifier}")
