import asyncio
import logging
from pipelines.semantic_pipeline import Pipeline
from config import get_config
from utils.storage import StorageManager
import time

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    log.info("Starting pipeline *****************************************************************************")
    config = get_config()
    bronze_dir= "./data/bronze"
    silver_dir= "./data/silver"
    gold_dir= "./data/gold"

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
            gold_dir=gold_dir,
            max_wokers= config.MAX_WORKERS
        )
    
    init_timestamp = int(time.time())
    episode_metadata =  pipeline.aggregate()
    log.info(f"Time taken : {int(time.time()) - init_timestamp}  s")
    storagemanager.save_to_layer(layer="gold", data=[episode_metadata], filename='episode_data.json')

if __name__ == "__main__":
    main()
