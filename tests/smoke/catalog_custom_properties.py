####################
# CatalogCustomProperty Tests
####################

# Test Suite Control CatalogCustomProperty
SUITE_NAME = "CatalogCustomProperty"
SUITE_TEST_ID = global_catalog_entity
SUITE_TEST_NAME = SUITE_TEST_ID.replace("_", " ").capitalize()
SUITE_TEST_CLASS = client.catalog_custom_properties
SUITE_CREATE_OBJECT = CatalogCustomPropertyCreateRequest(
    identifier=SUITE_TEST_ID,
    name=SUITE_TEST_NAME,
    kind="component",
    mode="replace",
    catalog_property="metadata.SDK_Validator",
    value="CREATED",
)

LIST_KWARGS = {}
GET_KWARGS = {"identifier": SUITE_TEST_ID, "kind": "component"}
UPDATE_KWARGS = {}
DELETE_KWARGS = {}

print(f"{f" {SUITE_NAME} ":#^40}")
print(f"{SUITE_NAME} -> List")
print(f"\t \t -> : No List Method")

print(f"{SUITE_NAME} -> Get Entities by a given property")
for list_catalog_custom_properties in [
    elem
    for elem in SUITE_TEST_CLASS.get_by_property(
        catalog_property=SUITE_CREATE_OBJECT.catalog_property
    )
]:
    print(
        f"\t \t -> : {list_catalog_custom_properties.identifier} = {list_catalog_custom_properties.value}"
    )

print(f"{SUITE_NAME} -> Get Properties for a given entity")
validation_object = SUITE_TEST_CLASS.get_by_entity(**GET_KWARGS)
if len(validation_object.properties) >= 1:
    print(f"\t Get -> {validation_object.identifier} has the following custom_properties:")
    for catalog_properties in validation_object.properties:
        print(
            f"\t\t: {catalog_properties["property"]} has the following custom_properties {catalog_properties["value"]}"
        )
    SUITE_CREATE_OBJECT.value = "UPDATED"
    validation_object = SUITE_TEST_CLASS.update(body=SUITE_CREATE_OBJECT, **UPDATE_KWARGS)
    print(
        f"\t -> Updated Entity {validation_object.identifier}: {validation_object.catalog_property} with value {validation_object.value}"
    )

else:
    print(f"\t -> {validation_object.identifier} has no custom_properties")
    validation_object = SUITE_TEST_CLASS.create(SUITE_CREATE_OBJECT)
    print(
        f"\t -> Created Entity {validation_object.identifier}: {validation_object.catalog_property} with value {validation_object.value}"
    )
    SUITE_CREATE_OBJECT.value = "RECENTLY_CREATED"
    validation_object = SUITE_TEST_CLASS.update(body=SUITE_CREATE_OBJECT, **UPDATE_KWARGS)
    print(
        f"\t -> Updated Entity {validation_object.identifier}: {validation_object.catalog_property} with value {validation_object.value}"
    )

print(f"{SUITE_NAME} -> Get Entities by a given property")
for list_catalog_custom_properties in [
    elem
    for elem in SUITE_TEST_CLASS.get_by_property(
        catalog_property=SUITE_CREATE_OBJECT.catalog_property
    )
]:
    print(
        f"\t \t -> : {list_catalog_custom_properties.identifier} = {list_catalog_custom_properties.value}"
    )

if cleanup:
    SUITE_TEST_CLASS.delete(body=SUITE_CREATE_OBJECT, **DELETE_KWARGS)
    print(
        f"\t -> Delete : CustomProperty {validation_object.catalog_property} from {validation_object.identifier}"
    )
