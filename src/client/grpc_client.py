import os
import sys
import grpc
import logging
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import llm_pb2, llm_pb2_grpc


logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)
log = logging.getLogger(__name__)

class GrpcClient:
    def __init__(self, url: str, max_tokens: int, model_name: str) -> None:
        self.url = url
        self.max_tokens = max_tokens
        self.model_name = model_name
        self.stub = self.open_channel(self.url)

    def generate_chunk(self, chunk_content: str, order: int, is_last: bool):
        try:
            chunk = llm_pb2.TextChunk(
                content=chunk_content,
                order= order,
                is_last= is_last
            )
            request = llm_pb2.GenerateChunkRequest(
                model=self.model_name,
                chunk=chunk,
                max_tokens=self.max_tokens
            )
            response = self.stub.GenerateChunk(request)
            return response.metadata
        except grpc.RpcError as e:
            log.error(f"gRPC error during GenerateChunk: {e.code()} - {e.details()}")
            raise

    def aggregate_chunks(self, content: str):
        try:
            request = llm_pb2.AggregateRequest(
                model=self.model_name,
                chunk_metadata=content,
                max_tokens=self.max_tokens
            )
            response = self.stub.AggregateChunks(request)
            return response
        except grpc.RpcError as e:
            log.error(f"gRPC error during AggregateChunks: {e.code()} - {e.details()}")
            raise

    @staticmethod
    def open_channel(url):
        channel = grpc.insecure_channel(url)
        stub = llm_pb2_grpc.OllamaStub(channel)
        return stub
