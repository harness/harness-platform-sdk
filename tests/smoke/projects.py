####################
# Project Tests
####################
print(f"{' Projects ':#^40}")
default_project_id = "simple_test"
default_project_name = default_project_id.replace("_", " ").capitalize()
print(f"Projects -> List")
for list_project in [elem for elem in client.projects.list()]:
    print(f"\t \t -> : {list_project.identifier}")

project_request = ProjectCreateRequest(
    identifier=global_project_id or default_project_id,
    name=global_project_name or default_project_name,
    description="a test",
)
project = client.projects.get(identifier=project_request.identifier)
# print(project)
if project:
    print(f"\t -> Get : {project.identifier}")
    project_request.description = "UPDATE from Existing"
    project = client.projects.update(identifier=project.identifier, body=project_request)
    print(f"\t -> Updated : {project.identifier}")
else:
    project_request.description = "CREATE from New"
    project = client.projects.create(project_request)
    print(f"\t -> Created : {project.identifier}")
    project = client.projects.update(identifier=project.identifier, body=project_request)
    project_request.description = "UPDATE after Creating"
    print(f"\t -> Updated : {project.identifier}")
print(f"Projects -> List")
for list_project in [elem for elem in client.projects.list()]:
    print(f"\t \t -> : {list_project.identifier}")
