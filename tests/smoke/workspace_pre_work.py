import json
import uuid

####################
# WorkspaceApprovals Tests
####################

# Preparation Work
#########################
spec = {
    "secretManagerIdentifier": "harnessSecretManager",
    "valueType": "Inline",
    "value": client._config.api_key,
}
secret_request = SecretCreateRequest(
    identifier="harness_api_key",
    name="Harness API Key",
    type="SecretText",
    description="Initial",
    spec=spec,
)
secret = client.secrets.get(identifier=secret_request.identifier)
if not secret:
    secret_request.description = "CREATE from New"
    secret = client.secrets.create(secret_request)
    print(f"\t -> Created : {secret.identifier}")

workspaces_request = WorkspaceCreateRequest(
    identifier="iacm_test",
    name="IACM Approval Test",
    description="a test",
    provisioner="opentofu",
    repository="goodrum-harness/terraform-provider-harness",
    repository_connector="account.github",
    repository_branch="main",
    repository_path="examples/resources/harness_platform_organization",
    environment_variables={
        "HARNESS_ACCOUNT_ID": {
            "key": "HARNESS_ACCOUNT_ID",
            "value": client._config.account_id,
            "value_type": "string",
        },
        "HARNESS_PLATFORM_API_KEY": {
            "key": "HARNESS_PLATFORM_API_KEY",
            "value": secret.identifier,
            "value_type": "secret",
        },
        "HARNESS_ENDPOINT": {
            "key": "HARNESS_ENDPOINT",
            "value": client._config.base_url,
            "value_type": "string",
        },
        # ""
    },
)

workspace = client.workspaces.get(
    identifier=workspaces_request.identifier,
)
if not workspace:
    workspace = client.workspaces.create(workspaces_request)
    print(f"\t -> Created : { workspace.identifier}")

pipeline_request = PipelineV0CreateRequest(
    identifier="iacm_provision",
    name="IACM Provision",
    description="a test for IACM",
    stages=[
        {
            "stage": {
                "name": "Provision",
                "identifier": "Provision",
                "description": "",
                "type": "IACM",
                "spec": {
                    "platform": {"os": "Linux", "arch": "Amd64"},
                    "runtime": {"type": "Cloud", "spec": {}},
                    "workspace": workspaces_request.identifier,
                    "execution": {
                        "steps": [
                            {
                                "step": {
                                    "type": "Run",
                                    "name": "Generate Provider file",
                                    "identifier": "Generate_Provider_file",
                                    "spec": {
                                        "shell": "Sh",
                                        "command": 'cd <+workspace.folderPath>\ncat << EOF > providers.tf\nterraform {\n  required_providers {\n    harness = {\n      source = "harness/harness"\n    }\n  }\n}\nprovider "harness" {}\nEOF\nls -l\n',
                                    },
                                }
                            },
                            {
                                "step": {
                                    "type": "IACMOpenTofuPlugin",
                                    "name": "init",
                                    "identifier": "init",
                                    "timeout": "10m",
                                    "spec": {"command": "init"},
                                }
                            },
                            {
                                "step": {
                                    "type": "IACMOpenTofuPlugin",
                                    "name": "plan",
                                    "identifier": "plan",
                                    "timeout": "10m",
                                    "spec": {"command": "plan"},
                                }
                            },
                            {
                                "step": {
                                    "type": "IACMApproval",
                                    "name": "IACMApproval_1",
                                    "identifier": "IACMApproval_1",
                                    "spec": {"autoApprove": "false"},
                                    "timeout": "1h",
                                }
                            },
                            {
                                "step": {
                                    "type": "IACMOpenTofuPlugin",
                                    "name": "apply",
                                    "identifier": "apply",
                                    "timeout": "10m",
                                    "spec": {"command": "apply"},
                                }
                            },
                            {
                                "step": {
                                    "type": "IACMOpenTofuPlugin",
                                    "name": "destroy",
                                    "identifier": "destroy",
                                    "timeout": "10m",
                                    "spec": {"command": "destroy"},
                                }
                            },
                        ]
                    },
                },
                "tags": {},
            }
        }
    ],
)

pipeline = client.pipelines_v0.get(identifier=pipeline_request.identifier)
if not pipeline:
    pipeline = client.pipelines_v0.create(pipeline_request)
    print(f"\t -> Created : {pipeline.identifier}")
#########################
