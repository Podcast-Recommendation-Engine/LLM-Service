from processing.base_processor import BaseProcessor
from google.protobuf.json_format import MessageToDict

class EpisodeProcessor(BaseProcessor):
    def run_aggregate_chunks(self, content) -> dict:
        metadata = self.grpc_client.aggregate_chunks(content=content)
        return MessageToDict(metadata, preserving_proto_field_name=True)
