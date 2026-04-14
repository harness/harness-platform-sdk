####################
# Secrets Tests
####################
print(f"{' Secrets ':#^40}")
print(f"Secrets -> List")
for secret in [elem for elem in client.secrets.list()]:
    print(f"\t \t -> : {secret.identifier}")
# print(secrets[0].identifier)
spec = {
    # "type": "SecretTextSpec1",
    "secretManagerIdentifier": "harnessSecretManager",
    "valueType": "Inline",
    "value": "changeme",
}
secret_request = SecretCreateRequest(
    identifier="simple_test",
    name="Simple Test",
    type="SecretText",
    description="Initial",
    spec=spec,
)
secret = client.secrets.get(identifier=secret_request.identifier)
# print(secret)
if secret:
    print(f"\t -> Get : {secret_request.identifier}")
    secret_request.description = "UPDATE from Existing"
    secret = client.secrets.update(identifier=secret.identifier, body=secret_request)
    print(f"\t -> Updated : {secret.identifier}")
else:
    secret_request.description = "CREATE from New"
    secret = client.secrets.create(secret_request)
    print(f"\t -> Created : {secret.identifier}")
    secret = client.secrets.update(identifier=secret.identifier, body=secret_request)
    # print(secret)
    secret.description = "UPDATE after Creating"
    print(f"\t -> Updated : {secret.identifier}")
print(f"secrets -> List")
for secret in [elem for elem in client.secrets.list()]:
    print(f"\t \t -> : {secret.identifier}")

if cleanup:
    client.secrets.delete(identifier=secret.identifier)
    print(f"\t -> Delete : {secret.identifier}")
