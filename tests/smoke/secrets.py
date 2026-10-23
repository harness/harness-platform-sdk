####################
# Secrets Tests
####################

# Test Suite Control Secrets
SUITE_NAME = "Secrets"
SUITE_TEST_ID = "SDK_Test_Secret"
SUITE_TEST_NAME = SUITE_TEST_ID.replace("_", " ").capitalize()
SUITE_TEST_CLASS = client.secrets
SUITE_CREATE_OBJECT = SecretCreateRequest(
    identifier=SUITE_TEST_ID,
    name=SUITE_TEST_NAME,
    type="SecretText",
    description="Initial",
    spec={
        "secretManagerIdentifier": "harnessSecretManager",
        "valueType": "Inline",
        "value": "changeme",
    },
)

print(f"{f" {SUITE_NAME} ":#^40}")
print(f"{SUITE_NAME} -> List")
for validate_method_list in [elem for elem in SUITE_TEST_CLASS.list()]:
    print(f"\t \t -> : {validate_method_list.identifier}")

test_create_request = SUITE_CREATE_OBJECT
validation_object = SUITE_TEST_CLASS.get(identifier=test_create_request.identifier)
if validation_object:
    print(f"\t -> Get : {validation_object.identifier}")
    test_create_request.description = "Smoke Test Validation - Update"
    validation_object = SUITE_TEST_CLASS.update(
        identifier=validation_object.identifier, body=test_create_request
    )
    print(f"\t -> Updated : {validation_object.identifier}")

else:
    validation_object = SUITE_TEST_CLASS.create(test_create_request)
    print(f"\t -> Created : {validation_object.identifier}")
    validation_object.description = "Smoke Test Validation - Update after create"
    validation_object = SUITE_TEST_CLASS.update(
        identifier=validation_object.identifier, body=test_create_request
    )
    print(f"\t -> Updated : {validation_object.identifier}")
print(f"{SUITE_NAME} -> List")
for validate_method_list in [elem for elem in SUITE_TEST_CLASS.list()]:
    print(f"\t \t -> : {validate_method_list.identifier}")

if cleanup:
    SUITE_TEST_CLASS.delete(identifier=validation_object.identifier)
    print(f"\t -> Delete : {validation_object.identifier}")
