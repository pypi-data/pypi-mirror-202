import importlib

connectorInterface = importlib.import_module("sm-search-connector-poc-interface")


class PocSearchConnector(connectorInterface.interface.ISearchConnector):
    def search(self, request: str) -> str:
        print(f"Connect me to Poc data source. Request: {request}")

    def getDetails(self):
        print("Get Details")

