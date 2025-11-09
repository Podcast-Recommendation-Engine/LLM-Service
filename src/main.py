import logging
from pipelines.semantic_pipeline import Pipeline
from config import get_config
log = logging.getLogger(__name__)
from utils.storage import StorageManager
logging.basicConfig(level=logging.INFO)


def main():
    log.info("Starting pipeline************************************************")
    config = get_config()

    bronze_dir= "./data/bronze"
    silver_dir= "./data/silver"
    gold_dir= "./data/gold"
    full_episode = "../data/bronze/transcript.txt"

    storagemanager = StorageManager(bronze_dir=bronze_dir, silver_dir=silver_dir, gold_dir=gold_dir)
    full_episode_data = storagemanager.load_from_layer(layer="bronze", filename="transcript.txt")
    pipeline = Pipeline(
            full_episode=full_episode_data,
            url=f"{config.OLLAMA_HOST}:{config.OLLAMA_PORT}",
            max_tokens=config.MAX_TOKENS,
            model_name=config.MODEL_NAME,
            chunk_size=config.CHUNK_SIZE,
            window_overlap=config.OVERLAP_SENTENCES,
            bronze_dir=bronze_dir,
            silver_dir=silver_dir,
            gold_dir=gold_dir
        )
    
    episode_metadata = pipeline.aggregate()

    # storagemanager.save_to_layer(layer="silver", data=chunks, filename='chunks_data.json')
    # Wrap episode_metadata in a list since it's a single dict
    storagemanager.save_to_layer(layer="gold", data=[episode_metadata], filename='episode_data.json')
    # log.info(f"Pipeline completed with {len(chunks)} chunks.")

if __name__ == "__main__":
    main()
