from client.grpc_client import GrpcClient
from google.protobuf.json_format import MessageToDict

class EpisodeProcessor:
    def __init__(self, url: str,  max_tokens: int, model_name: str) -> None:
        self.grpc_client = GrpcClient(url=url, max_tokens=max_tokens, model_name=model_name)
        

    def run_gaggregate_chunks(self, content) -> dict:
        metadata = self.grpc_client.aggregate_chunks(content= content)
        metadata_dict = MessageToDict(metadata, preserving_proto_field_name=True)
        return metadata_dict
    

