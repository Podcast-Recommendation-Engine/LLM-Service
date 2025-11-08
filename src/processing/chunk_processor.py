
from client.grpc_client import GrpcClient

class ChunkProcessor:
    def __init__(self, url: str, max_tokens: int, model_name: str) -> None:
        self.grpc_client = GrpcClient(url=url, max_tokens=max_tokens, model_name=model_name)
        

    def run_generate_chunk(self, chunk_content: str, order: int, is_last: bool) -> dict:
        metadata = self.grpc_client.generate_chunk(chunk_content= chunk_content, order= order, is_last= is_last)
        return metadata
    
    
