####################
# Organization Tests
####################
print(f"{' Organizations ':#^40}")
default_org_id = "simple_test"
default_org_name = default_org_id.replace("_", " ").capitalize()
print(f"Organizations -> List")
for list_organization in [elem for elem in client.organizations.list()]:
    print(f"\t \t -> : {list_organization.identifier}")

organization_request = OrganizationCreateRequest(
    identifier=global_org_id or default_org_id,
    name=global_org_name or default_org_name,
    description="a test",
)
organization = client.organizations.get(identifier=organization_request.identifier)
# print(organization)
if organization:
    print(f"\t -> Get : {organization.identifier}")
    organization_request.description = "UPDATE from Existing"
    organization = client.organizations.update(
        identifier=organization.identifier, body=organization_request
    )
    print(f"\t -> Updated : {organization.identifier}")
else:
    organization_request.description = "CREATE from New"
    organization = client.organizations.create(organization_request)
    print(f"\t -> Created : {organization.identifier}")
    organization = client.organizations.update(
        identifier=organization.identifier, body=organization_request
    )
    organization_request.description = "UPDATE after Creating"
    print(f"\t -> Updated : {organization.identifier}")
print(f"Organizations -> List")
for list_organization in [elem for elem in client.organizations.list()]:
    print(f"\t \t -> : {list_organization.identifier}")
