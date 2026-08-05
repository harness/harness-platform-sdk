import json

####################
# Service Tests
####################
print(f"{' Services ':#^40}")
pipeline_identifier = "simple_test"
print(f"Services -> List")
for list_service in [elem for elem in client.services.list()]:
    # client._display_payload(list_service)
    print(f"\t \t -> : {list_service.identifier}")

service_request = ServiceCreateRequest(
    pipeline_identifier="simple_test",
    identifier="simple_test",
    name="Simple Test",
    description="a test",
    type="NativeHelm",
    manifests=[
        {
            "manifest": {
                "identifier": "manifest",
                "type": "HelmChart",
                "spec": {
                    "store": {
                        "type": "Github",
                        "spec": {
                            "connectorRef": "account.github",
                            "gitFetchType": "Branch",
                            "folderPath": "/",
                            "repoName": "path-to-nowhere",
                            "branch": "main",
                        },
                    },
                    "subChartPath": '\\"\\"',
                    "optionalValuesYaml": False,
                    "skipResourceVersioning": False,
                    "enableDeclarativeRollback": False,
                    "helmVersion": "V3",
                    "fetchHelmChartMetadata": False,
                },
            }
        }
    ],
    artifacts={
        "primary": {
            "primaryArtifactRef": "<+input>",
            "sources": [
                {
                    "spec": {
                        "connectorRef": "account.harnessImage",
                        "imagePath": "nowhere",
                        "tag": "<+input>",
                        "digest": '\\"\\"',
                    },
                    "identifier": "primary",
                    "type": "DockerRegistry",
                }
            ],
        }
    },
)

service = client.services.get(identifier=service_request.identifier)
# client._display_payload(service)
if service:
    print(f"\t -> Get : { service.identifier}")
    service_request.description = "UPDATE from Existing"
    service = client.services.update(identifier=service.identifier, body=service_request)
    print(f"\t -> Updated : { service.identifier}")

else:
    service_request.description = "CREATE from New"
    service = client.services.create(service_request)
    print(f"\t -> Created : { service.identifier}")
    service_request.description = "UPDATE after Creating"
    service = client.services.update(identifier=service.identifier, body=service_request)
    print(f"\t -> Updated : { service.identifier}")
print(f"Services -> List")
for list_service in [elem for elem in client.services.list()]:
    print(f"\t \t -> : {list_service.identifier}")

if unit_cleanup:
    client.services.delete(identifier=service.identifier)
    print(f"\t -> Delete : { service.identifier}")
