from singular_client.endpoints._bases import _Endpoint
from singular_client.documents import *

class GraphQL(_Endpoint[dict]):
    endpoint = "graphql/graphql"
    data_path = ["data"]
    res_type = dict
    returns_collection = False
    method = "POST"

    def request(self, query: str):
        return super().request(
            data=query,
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }
        )



