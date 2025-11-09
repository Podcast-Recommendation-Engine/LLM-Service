from processing.base_processor import BaseProcessor
from google.protobuf.json_format import MessageToDict

class ChunkProcessor(BaseProcessor):
    def run_generate_chunk(self, chunk_content: str, order: int, is_last: bool) -> dict:
        metadata = self.grpc_client.generate_chunk(
            chunk_content=chunk_content, order=order, is_last=is_last
        )
        return MessageToDict(metadata, preserving_proto_field_name=True)


