"""
Smoke test for Services API (service CRUD operations).

Test Coverage:
  - List services
  - Get service by identifier
  - Create service with manifests and artifacts
  - Update service
  - Delete service (if cleanup=True)

Scope: Project-level (requires org_id and project_id)
Fixture Dependency: Organizations, Projects (Tier 0-1)
"""

SUITE_NAME = "Services"
SUITE_TEST_ID = "SDK_Test_Services"
SUITE_TEST_NAME = SUITE_TEST_ID.replace("_", " ").capitalize()
SUITE_TEST_CLASS = client.services
SUITE_CREATE_OBJECT = ServiceCreateRequest(
    identifier=SUITE_TEST_ID,
    name=SUITE_TEST_NAME,
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

print(f"{f' {SUITE_NAME} ':#^40}")
print(f"{SUITE_NAME} -> List")
for list_service in [elem for elem in SUITE_TEST_CLASS.list()]:
    print(f"\t \t -> : {list_service.identifier}")

# Attempt to get existing service
test_create_request = SUITE_CREATE_OBJECT
service = SUITE_TEST_CLASS.get(identifier=test_create_request.identifier)
if service:
    print(f"\t -> Get : {service.identifier}")
    test_create_request.description = "Smoke Test Validation - Update"
    service = SUITE_TEST_CLASS.update(identifier=service.identifier, body=test_create_request)
    print(f"\t -> Updated : {service.identifier}")
else:
    # Create if not found
    service = SUITE_TEST_CLASS.create(test_create_request)
    print(f"\t -> Created : {service.identifier}")
    test_create_request.description = "Smoke Test Validation - Update after create"
    service = SUITE_TEST_CLASS.update(identifier=service.identifier, body=test_create_request)
    print(f"\t -> Updated : {service.identifier}")

print(f"{SUITE_NAME} -> List")
for list_service in [elem for elem in SUITE_TEST_CLASS.list()]:
    print(f"\t \t -> : {list_service.identifier}")

if cleanup:
    SUITE_TEST_CLASS.delete(identifier=service.identifier)
    print(f"\t -> Delete : {service.identifier}")
