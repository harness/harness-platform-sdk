"""
Smoke test for Pipelines V0 API (pipeline CRUD operations).

Test Coverage:
  - List pipelines
  - Get pipeline by identifier
  - Create pipeline with stages and variables
  - Update pipeline (add stages)
  - Delete pipeline (if cleanup=True)

Scope: Project-level (requires org_id and project_id)
Fixture Dependency: Organizations, Projects (Tier 0-1)
"""

print(f"{' Pipelines ':#^40}")
SUITE_NAME = "Pipelines"
SUITE_TEST_ID = "SDK_Test_Pipeline"
SUITE_TEST_NAME = SUITE_TEST_ID.replace("_", " ").capitalize()
print(f"{SUITE_NAME} -> List")
for list_pipeline in [elem for elem in client.pipelines_v0.list()]:
    print(f"\t \t -> : {list_pipeline.identifier}")

pipeline_request = PipelineV0CreateRequest(
    identifier=SUITE_TEST_ID,
    name=SUITE_TEST_NAME,
    description="Smoke Test Validation - Create",
    stages=[
        {
            "stage": {
                "name": "test",
                "identifier": "test",
                "description": "",
                "type": "Custom",
                "spec": {
                    "execution": {
                        "steps": [
                            {
                                "step": {
                                    "type": "Wait",
                                    "name": "Wait_1",
                                    "identifier": "Wait_1",
                                    "spec": {"duration": "10m"},
                                }
                            }
                        ]
                    }
                },
                "tags": {},
            }
        }
    ],
    variables=[
        {
            "name": "test",
            "type": "String",
            "description": "",
            "required": False,
            "value": "<+input>",
        }
    ],
)
additional_stage = [
    {
        "stage": {
            "name": "test2",
            "identifier": "test2",
            "description": "",
            "type": "Custom",
            "spec": {
                "execution": {
                    "steps": [
                        {
                            "step": {
                                "type": "Wait",
                                "name": "Wait_1",
                                "identifier": "Wait_1",
                                "spec": {"duration": "10m"},
                            }
                        }
                    ]
                }
            },
            "tags": {},
        }
    }
]

# Attempt to get existing pipeline
pipeline = client.pipelines_v0.get(identifier=pipeline_request.identifier)
if pipeline:
    print(f"\t -> Get : {pipeline.identifier}")
    pipeline_request.description = "Smoke Test Validation - Update"
    pipeline_request.stages += additional_stage
    pipeline = client.pipelines_v0.update(identifier=pipeline.identifier, body=pipeline_request)
    print(f"\t -> Updated : {pipeline.identifier}")
else:
    # Create if not found
    pipeline = client.pipelines_v0.create(pipeline_request)
    print(f"\t -> Created : {pipeline.identifier}")
    pipeline_request.description = "Smoke Test Validation - Update after create"
    pipeline_request.stages += additional_stage
    pipeline = client.pipelines_v0.update(identifier=pipeline.identifier, body=pipeline_request)
    print(f"\t -> Updated : {pipeline.identifier}")

print(f"{SUITE_NAME} -> List")
for list_pipeline in [elem for elem in client.pipelines_v0.list()]:
    print(f"\t \t -> : {list_pipeline.identifier}")

if cleanup:
    client.pipelines_v0.delete(identifier=SUITE_TEST_ID)
    print(f"\t -> Deleted : {SUITE_TEST_ID}")
