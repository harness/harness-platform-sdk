"""
Smoke test for Organizations API (organization CRUD operations).

Test Coverage:
  - List organizations
  - Get organization by identifier
  - Create organization
  - Update organization
  - Delete organization (if cleanup=True)

Scope: Account-level (no org/project required)
Fixture Dependency: None (foundation test)
"""

print(f"{' Organizations ':#^40}")
SUITE_NAME = "Organizations"
SUITE_TEST_ID = "PLATFORM_SDK_FIXTURES_TEST_ORG"
SUITE_TEST_NAME = SUITE_TEST_ID.replace("_", " ").capitalize()
print(f"{SUITE_NAME} -> List")
for list_org in [elem for elem in client.organizations.list()]:
    print(f"\t \t -> : {list_org.identifier}")

organization_request = OrganizationCreateRequest(
    identifier=SUITE_TEST_ID,
    name=SUITE_TEST_NAME,
    description="Smoke Test Validation - Create",
)

# Attempt to get existing organization
organization = client.organizations.get(identifier=organization_request.identifier)
if organization:
    print(f"\t -> Get : {organization.identifier}")
    organization_request.description = "Smoke Test Validation - Update"
    organization = client.organizations.update(
        identifier=organization.identifier, body=organization_request
    )
    print(f"\t -> Updated : {organization.identifier}")
else:
    # Create if not found
    organization = client.organizations.create(organization_request)
    print(f"\t -> Created : {organization.identifier}")
    organization_request.description = "Smoke Test Validation - Update after create"
    organization = client.organizations.update(
        identifier=organization.identifier, body=organization_request
    )
    print(f"\t -> Updated : {organization.identifier}")

print(f"{SUITE_NAME} -> List")
for list_org in [elem for elem in client.organizations.list()]:
    print(f"\t \t -> : {list_org.identifier}")

if cleanup:
    client.organizations.delete(identifier=SUITE_TEST_ID)
    print(f"\t -> Deleted : {SUITE_TEST_ID}")
