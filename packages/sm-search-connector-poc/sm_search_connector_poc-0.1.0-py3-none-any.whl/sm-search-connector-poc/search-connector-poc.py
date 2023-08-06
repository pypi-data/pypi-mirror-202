from sm-search-connector-poc-interface import ISearchConnector

class PocSearchConnector(ISearchConnector):
    def search(self, request: str) -> str:
        print(f"Connect me to Poc data source. Request: {request}")