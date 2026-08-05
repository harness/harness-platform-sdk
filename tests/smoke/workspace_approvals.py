import json
import uuid

####################
# WorkspaceApprovals Tests
####################
print(f"{' WorkspaceApprovals ':#^40}")
workspace_identifier = "iacm_test"
print(f"WorkspaceApprovals -> List")
all_workspace_approvals = [
    elem
    for elem in client.workspace_approvals.list(
        workspace_identifier=workspace_identifier, status="pending"
    )
]
for list_workspace_approvals in all_workspace_approvals:
    # client._display_payload(list_workspace_approvals)
    print(f"\t \t -> : {list_workspace_approvals.identifier}")

if not all_workspace_approvals:
    import uuid

    approval_identifier = str(uuid)
else:
    approval_identifier = all_workspace_approvals[0].identifier
workspace_approvals_request = WorkspaceApprovalCreateRequest(
    identifier=approval_identifier,
    status="approved",
    actioned_by="Harness SCOE Team",
    actioned_by_email="harness_scoe@scoe.harness.lab",
)

workspace_approvals = client.workspace_approvals.get(
    identifier=approval_identifier,
)
# client._display_payload(workspace_approvals)
if workspace_approvals:
    print(f"\t -> Get : { workspace_approvals.identifier}")
    workspace_approvals_request.description = "UPDATE from Existing"
    workspace_approvals = client.workspace_approvals.update(
        identifier=workspace_approvals.identifier, body=workspace_approvals_request
    )
    print(f"\t -> Updated : { workspace_approvals.identifier}")
else:
    print(f"\t -> Skipped - no active approval for workspace : { workspace_identifier }")
print(f"WorkspaceApprovals -> List")
for list_workspace_approvals in [
    elem for elem in client.workspace_approvals.list(workspace_identifier=workspace_identifier)
]:
    print(f"\t \t -> : {list_workspace_approvals.identifier}")

if unit_cleanup:
    print(f"\t -> Delete Approval Skipped. Unsupported action")
