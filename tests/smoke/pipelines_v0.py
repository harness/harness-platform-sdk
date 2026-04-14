####################
# Pipeline Tests
####################
print(f"{' Pipelines ':#^40}")
print(f"Pipelines -> List")
for list_pipeline in [elem for elem in client.pipelines_v0.list()]:
    print(f"\t \t -> : {list_pipeline.identifier}")

pipeline_request = PipelineV0CreateRequest(
    identifier="simple_test",
    name="Simple Test",
    description="a test",
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

pipeline = client.pipelines_v0.get(identifier=pipeline_request.identifier)
# print(pipeline)
if pipeline:
    print(f"\t -> Get : {pipeline.identifier}")
    pipeline_request.description = "UPDATE from Existing"
    pipeline_request.stages += additional_stage
    pipeline = client.pipelines_v0.update(identifier=pipeline.identifier, body=pipeline_request)
    print(f"\t -> Updated : {pipeline.identifier}")

else:
    pipeline_request.description = "CREATE from New"
    pipeline = client.pipelines_v0.create(pipeline_request)
    print(f"\t -> Created : {pipeline.identifier}")
    pipeline = client.pipelines_v0.update(identifier=pipeline.identifier, body=pipeline_request)
    pipeline_request.description = "UPDATE after Creating"
    print(f"\t -> Updated : {pipeline.identifier}")
print(f"Pipelines -> List")
for list_pipeline in [elem for elem in client.pipelines_v0.list()]:
    print(f"\t \t -> : {list_pipeline.identifier}")
