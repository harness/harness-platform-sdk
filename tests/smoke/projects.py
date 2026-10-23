"""
Smoke test for Projects API (project CRUD operations).

Test Coverage:
  - List projects (org-scoped)
  - Get project by identifier
  - Create project
  - Update project
  - Delete project (if cleanup=True)

Scope: Organization-level (requires org_id)
Fixture Dependency: Organizations (Tier 0)
"""

print(f"{' Projects ':#^40}")
SUITE_NAME = "Projects"
SUITE_TEST_ID = "PLATFORM_SDK_FIXTURES_TEST_PROJECT"
SUITE_TEST_NAME = SUITE_TEST_ID.replace("_", " ").capitalize()
print(f"{SUITE_NAME} -> List")
for list_project in [elem for elem in client.projects.list()]:
    print(f"\t \t -> : {list_project.identifier}")

project_request = ProjectCreateRequest(
    identifier=SUITE_TEST_ID,
    name=SUITE_TEST_NAME,
    description="Smoke Test Validation - Create",
)

# Attempt to get existing project
project = client.projects.get(identifier=project_request.identifier)
if project:
    print(f"\t -> Get : {project.identifier}")
    project_request.description = "Smoke Test Validation - Update"
    project = client.projects.update(identifier=project.identifier, body=project_request)
    print(f"\t -> Updated : {project.identifier}")
else:
    # Create if not found
    project = client.projects.create(project_request)
    print(f"\t -> Created : {project.identifier}")
    project_request.description = "Smoke Test Validation - Update after create"
    project = client.projects.update(identifier=project.identifier, body=project_request)
    print(f"\t -> Updated : {project.identifier}")

print(f"{SUITE_NAME} -> List")
for list_project in [elem for elem in client.projects.list()]:
    print(f"\t \t -> : {list_project.identifier}")

if cleanup:
    client.projects.delete(identifier=SUITE_TEST_ID)
    print(f"\t -> Deleted : {SUITE_TEST_ID}")
