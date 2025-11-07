import grpc
import logging
import llm_pb2, llm_pb2_grpc

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)
log = logging.getLogger(__name__)


def run_generate_chunk(url: str, chunk_content: str, max_tokens: int, order: int, is_last: bool, model_name: str):

    stub = open_grpc_channel(url)
    chunk = llm_pb2.TextChunk(  # type: ignore
        content=chunk_content,
        order=order,
        is_last=is_last
    )
    request = llm_pb2.GenerateChunkRequest(  # type: ignore
        model=model_name,
        chunk=chunk,
        max_tokens=max_tokens
    )
    # Step 3: Send the request and receive the response
    try:
        response = stub.GenerateChunk(request)
        metadata = response.metadata
        return metadata
    except grpc.RpcError as e:
        log.exception(f"gRPC call failed: {e.details()} (code: {e.code()})")
    

def run_aggregate_chunks(url: str, chunks_metadata: list, max_tokens: int, model_name: str):

    stub = open_grpc_channel(url)
    request = llm_pb2.AggregateRequest(  # type: ignore
        model=model_name,
        chunk_metadata=chunks_metadata,
        max_tokens=max_tokens
    )
    # Step 3: Send the request and receive the response
    try:
        response = stub.AggregateChunks(request)
        return response
    except grpc.RpcError as e:
        log.exception(f"gRPC call failed: {e.details()} (code: {e.code()})")


def open_grpc_channel(url):
    channel = grpc.insecure_channel(url)
    stub = llm_pb2_grpc.OllamaStub(channel)
    return stub


# ---- Main Test Runner ----

if __name__ == "__main__":
    url = "localhost:50051"
    model_name = "llama3.2:3b"

    # 1. Test GenerateChunk
    print("\n--- Testing GenerateChunk ---")

    long_text = (
        "The Joe Rogan Experience has become one of the most influential podcasts in the world, "
        "featuring long-form discussions with guests from a wide range of backgrounds — including "
        "scientists, athletes, authors, and entrepreneurs. In recent years, the podcast has hosted "
        "many experts in artificial intelligence, such as Elon Musk, Lex Fridman, and Sam Altman. "
        "These conversations have sparked global interest in AI ethics, automation, and the future "
        "of human creativity in an age dominated by algorithms.\n\n"
        "Rogan’s approach — an informal, conversational tone combined with deep curiosity — allows "
        "complex topics like neural networks, consciousness, and machine learning to be explored in "
        "an accessible way. Many listeners credit the show for introducing them to modern AI trends "
        "and the challenges of regulating powerful technologies.\n\n"
        "The intersection of entertainment and technology continues to grow. Podcasts like this serve "
        "as an educational bridge between experts and the general public, helping demystify AI while "
        "also raising awareness about its potential risks. As artificial intelligence advances, public "
        "discourse through accessible media becomes increasingly vital."
    )

    metadata = run_generate_chunk(
        url=url,
        chunk_content=long_text,
        max_tokens=512,
        order=1,
        is_last=True,
        model_name=model_name
    )

    if metadata:
        print("Received metadata:")
        print(metadata)
    else:
        print("No metadata received.")

    # 2. Test AggregateChunks
    print("\n--- Testing AggregateChunks ---")

    # Mock metadata for testing
    chunk1 = llm_pb2.ChunkMetadata(
        order=1,
        title="The Rise of AI Discussions in Podcasts",
        description="Explores how the Joe Rogan Experience popularized long-form AI discussions with influential guests.",
        keywords=["AI", "Podcast", "Joe Rogan", "Technology", "Ethics"],
        topic="Artificial Intelligence in Media"
    )
    chunk2 = llm_pb2.ChunkMetadata(
        order=2,
        title="Public Engagement with Artificial Intelligence",
        description="Examines how conversational podcasts bridge the gap between AI experts and the general audience.",
        keywords=["AI", "Education", "Communication", "Society"],
        topic="AI Awareness"
    )

    response = run_aggregate_chunks(
        url=url,
        chunks_metadata=[chunk1, chunk2],
        max_tokens=512,
        model_name=model_name
    )

    if response:
        print("Aggregated metadata:")
        print(response)
    else:
        print("No response received.")
