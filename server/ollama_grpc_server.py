from concurrent import futures
import sys
import grpc
import requests
import json
import logging
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import llm_pb2_grpc
import llm_pb2

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class OllamaServicer(llm_pb2_grpc.OllamaServicer):
    
    def GenerateChunk(self, request, context):
        chunk_content = request.chunk.content
        chunk_order = request.chunk.order
        max_tokens = request.max_tokens
        model_name = request.model
        
        log.info(f"GenerateChunk: Processing chunk {chunk_order}")

        prompt = (
            "You are a text summarizer. "
            "Given the following text, return a JSON object with fields: "
            "`title`, `description`, `keywords` (list), and `topic`. "
            f"Text: {chunk_content}"
        )

        url = "http://ollama:11434/api/generate"
        payload = {
            "prompt": prompt,
            "model": model_name,
            "stream": False,
            "format": "json",
            "num_predict": max_tokens
        }

        try:
            response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
            response.raise_for_status()
            result_text = response.json().get("response", "")
            metadata_json = json.loads(result_text)
            
            # Debug logging - show the actual result
            log.info(f"GenerateChunk: Chunk {chunk_order} result: {metadata_json}")
            log.info(f"GenerateChunk: Chunk {chunk_order} completed successfully")
        except (requests.RequestException, json.JSONDecodeError) as e:
            log.error(f"GenerateChunk: Chunk {chunk_order} failed - {e}")
            metadata_json = {}

        metadata = llm_pb2.ChunkMetadata(
            order=chunk_order,
            title=metadata_json.get("title", ""),
            description=metadata_json.get("description", ""),
            keywords=metadata_json.get("keywords", []),
            topic=metadata_json.get("topic", "")
        )

        return llm_pb2.GenerateChunkResponse(metadata=metadata)

    def AggregateChunks(self, request, context):
        model_name = request.model
        chunk_metadata_list = request.chunk_metadata
        
        log.info(f"AggregateChunks: Aggregating {len(chunk_metadata_list)} chunks")

        meta_texts = [
            f"Chunk {m.order}: Title: {m.title}; Description: {m.description}; Keywords: {', '.join(m.keywords)}; Topic: {m.topic}"
            for m in chunk_metadata_list
        ]
        combined_meta = "\n".join(meta_texts)
        
        prompt = f"""You are an expert text aggregator.
Given the following chunk metadata, generate a single coherent summary for the entire episode.
Chunk metadata:
{combined_meta}
Return ONLY a valid JSON object with fields: title, description, keywords (list), topic."""

        url = "http://ollama:11434/api/generate"
        payload = {
            "prompt": prompt,
            "model": model_name,
            "stream": False,
            "format": "json"
        }

        try:
            response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
            response.raise_for_status()
            result_text = response.json().get("response", "")
            metadata_json = json.loads(result_text)
            
            # Debug logging - show the aggregation result
            log.info(f"AggregateChunks: Final result: {metadata_json}")
            log.info("AggregateChunks: Aggregation completed successfully")
        except (requests.RequestException, json.JSONDecodeError) as e:
            log.error(f"AggregateChunks: Aggregation failed - {e}")
            metadata_json = {}

        return llm_pb2.AggregateResponse(
            title=metadata_json.get("title", ""),
            description=metadata_json.get("description", ""),
            keywords=metadata_json.get("keywords", []),
            topic=metadata_json.get("topic", "")
        )

def serve():
    log.info("Starting gRPC server on port 50051...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    llm_pb2_grpc.add_OllamaServicer_to_server(OllamaServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    log.info("Server ready")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        log.info("Shutting down...")
        server.stop(0)

if __name__ == "__main__":
    serve()
