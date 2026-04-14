####################
# Connector Tests
####################
print(f"{' Connectors ':#^40}")
print(f"Connectors -> List")
for list_connector in [elem for elem in client.connectors.list()]:
    print(f"\t \t -> : {list_connector.identifier}")

connector_request = ConnectorCreateRequest(
    identifier="simple_test",
    name="Simple Test",
    description="a test",
    type="K8sCluster",
    spec={
        "connectorType": "KubernetesClusterConfig",
        "credential": {"type": "InheritFromDelegate"},
        "delegateSelectors": ["build-farm"],
    },
)

connector = client.connectors.get(identifier=connector_request.identifier)
# print(connector)
if connector:
    print(f"\t -> Get : {connector.identifier}")
    connector_request.description = "UPDATE from Existing"
    connector = client.connectors.update(identifier=connector.identifier, body=connector_request)
    print(f"\t -> Updated : {connector.identifier}")

else:
    connector_request.description = "CREATE from New"
    connector = client.connectors.create(connector_request)
    print(f"\t -> Created : {connector.identifier}")
    connector = client.connectors.update(identifier=connector.identifier, body=connector_request)
    connector_request.description = "UPDATE after Creating"
    print(f"\t -> Updated : {connector.identifier}")
print(f"Connectors -> List")
for list_connector in [elem for elem in client.connectors.list()]:
    print(f"\t \t -> : {list_connector.identifier}")

if cleanup:
    client.connectors.delete(identifier=connector.identifier)
    print(f"\t -> Delete : {connector.identifier}")
