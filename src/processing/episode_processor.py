from client.grpc_client import GrpcClient

class EpisodeProcessor:
    def __init__(self, url: str, chunk_content: str, max_tokens: int, order: int, is_last: bool, model_name: str) -> None:
        self.grpc_client = GrpcClient(url=url, max_tokens=max_tokens, model_name=model_name)
        

    def run_gaggregate_chunks(self, content) -> dict:
        metadata = self.grpc_client.aggregate_chunks(content= content)
        return metadata
    

