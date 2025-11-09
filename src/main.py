
# ---- Main entry point ----
import logging
from pipelines.semantic_pipeline import Pipeline

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



def main():
    log.info("Starting pipeline...")

    # Example data (replace with real values)
    full_episode = "../data/bronze/transcript.txt."
    with open (full_episode, "r", encoding="utf-8") as file:
        data = file.read()

    url = "localhost:50051"
    max_tokens = 512
    model_name = "llama3.2:3b"
    chunk_size = 1000
    window_overlap = 200
    bronze_dir = "../data/bronze"
    silver_dir = "../data/silver"
    gold_dir = "../data/gold"

    pipeline = Pipeline(
        full_episode=data,
        url=url,
        max_tokens=max_tokens,
        model_name=model_name,
        chunk_size=chunk_size,
        window_overlap=window_overlap,
        bronze_dir=bronze_dir,
        silver_dir=silver_dir,
        gold_dir=gold_dir
    )

    result = pipeline.chunk()
    episode = pipeline.aggregate()
    log.info(f"Pipeline completed with {len(result)} chunks.")


if __name__ == "__main__":
    main()
