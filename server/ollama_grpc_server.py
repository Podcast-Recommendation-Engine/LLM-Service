from concurrent import futures
import time
import grpc
import requests
import json
import logging

# Import the generated modules
import llm_pb2
import llm_pb2_grpc

log = logging.getLogger(__name__)


class OllamaServicer(llm_pb2_grpc.OllamaServicer):
    """Ollama gRPC service implementation"""

    def GenerateChunk(self, request, context):
        """Generate metadata for a text chunk using Ollama LLM"""
        # Step 1: Get info from request
        chunk_content = request.chunk.content
        chunk_order = request.chunk.order

        # Step 2: Prepare data for Ollama
        prompt = (
            "You are a text summarizer. "
            "Given the following text, return a JSON object with fields: "
            "`title`, `description`, `keywords` (list), and `topic`. "
            f"Text: {chunk_content}"
        )

        url = "http://ollama:11434/api/generate"
        payload = {
            "prompt": prompt,
            "model": "llama3.2:3b",
            "stream": False
        }

        headers = {"Content-Type": "application/json"}
        data = json.dumps(payload)
        # Step 3: Call Ollama
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
        except requests.RequestException as e:
            log.error(f"Ollama request failed for chunk {chunk_order}: {e}")
            return llm_pb2.GenerateChunkResponse(
                metadata=llm_pb2.ChunkMetadata(order=chunk_order)
            )

        # Step 4: Parse Ollama response
        data = response.json()
        result_text = data.get("response", "")

        try:
            metadata_json = json.loads(result_text)
        except json.JSONDecodeError:
            log.error("Failed to parse JSON from Ollama output")
            metadata_json = {}

        # Step 5: Build response metadata
        metadata = llm_pb2.ChunkMetadata(
            order=chunk_order,
            title=metadata_json.get("title", ""),
            description=metadata_json.get("description", ""),
            keywords=metadata_json.get("keywords", []),
            topic=metadata_json.get("topic", "")
        )

        return llm_pb2.GenerateChunkResponse(metadata=metadata)

    def AggregateChunks(self, request, context):
        # Step 1: Extract relevaant info
        model_name = request.model
        chunk_metadata_list = request.chunk_metadata
        max_tokens = request.max_tokens

        # Step 2: Build an aggregated text prompt
    # Convert each chunk metadata into readable text for the model
        meta_texts = []
        for m in chunk_metadata_list:
            meta_texts.append(
                f"Chunk {m.order}: "
                f"Title: {m.title}; "
                f"Description: {m.description}; "
                f"Keywords: {', '.join(m.keywords)}; "
                f"Topic: {m.topic}"
            )

        combined_meta = "\n".join(meta_texts)

        prompt = f"""
            You are an expert text aggregator.
            Given the following chunk metadata, generate a single coherent summary for the entire episode.

            Chunk metadata:
            {combined_meta}

            Return ONLY a valid JSON object with the following fields:
            - title
            - description
            - keywords (list of strings)
            - topic
        """
         
        url = "http://ollama:11434/api/generate"
        payload = {
            "prompt": prompt,
            "model": model_name,
            "stream": False
        }

        headers = {"Content-Type": "application/json"}
        data = json.dumps(payload)
        # Step 3: Call Ollama
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
        except requests.RequestException as e:
            log.error(f"Ollama aggregation failed for model {model_name}: {e}")

            return llm_pb2.AggregateResponse(
            title="", description="", keywords=[], topic=""
            )

        # Step 4: Parse Ollama response
        data = response.json()
        result_text = data.get("response", "")

        try:
            metadata_json = json.loads(result_text)
        except json.JSONDecodeError:
            log.error("Failed to parse JSON from Ollama output")
            metadata_json = {}
       
        return llm_pb2.AggregateResponse(
            title=metadata_json.get("title", ""),
            description=metadata_json.get("description", ""),
            keywords=metadata_json.get("keywords", []),
            topic=metadata_json.get("topic", "")
        )
    




def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    llm_pb2_grpc.add_OllamaServicer_to_server(OllamaServicer(), server)
    server.add_insecure_port("[::]:50051")  # listen on all interfaces
    log.info(" Ollama gRPC server is starting on port 50051...")
    server.start()
    try:
        while True:
            server.wait_for_termination()
    except KeyboardInterrupt:
        log.info(" Shutting down server gracefully...")
        server.stop(0)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    serve()