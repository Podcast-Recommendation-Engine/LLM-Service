import logging
from processing.chunk_processor import ChunkProcessor
from processing.episode_processor import EpisodeProcessor
from utils.chunker import SemanticChunkingManager
from utils.storage import StorageManager

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Pipeline:
    def __init__(
        self,
        full_episode: str,
        url: str,
        max_tokens: int,
        model_name: str,
        chunk_size: int,
        window_overlap: int,
        bronze_dir: str,
        silver_dir: str,
        gold_dir: str
    ) -> None:
        self.bronze_dir = bronze_dir
        self.silver_dir = silver_dir
        self.gold_dir = gold_dir
        self.semanticchunkermanager = SemanticChunkingManager(
            content=full_episode,
            chunk_size=chunk_size,
            window_overlap=window_overlap
        )
        self.storagemanager = StorageManager(
            bronze_dir=self.bronze_dir,
            silver_dir=self.silver_dir,
            gold_dir=self.gold_dir
        )
        self.chunkprocessor = ChunkProcessor(
            url=url,
            max_tokens=max_tokens,
            model_name=model_name
        )

    def chunk(self):
        data = self.semanticchunkermanager.chunk_content()
        metadata_chunked = []

        for chunk in data:
            log.info(chunk["order"])
            log.info(chunk["is_last"])
            log.info(chunk)
            chunk_metadata = self.chunkprocessor.run_generate_chunk(
                chunk_content=chunk["content"],
                order=chunk["order"],
                is_last=chunk["is_last"]
            )
            # Debug line
            log.info(f"The type of chunk metadata is: {type(chunk_metadata)}")
            metadata_chunked.append(chunk_metadata) 

            data = self.storagemanager.save_to_layer(layer="silver", data=metadata_chunked, filename="testwbara.json")
            print("Allez si ibrahim")

        return metadata_chunked


# ---- Main entry point ----
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
    log.info(f"Pipeline completed with {len(result)} chunks.")


if __name__ == "__main__":
    main()
