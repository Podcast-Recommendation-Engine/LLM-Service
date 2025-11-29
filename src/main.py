import json
import logging
import re
import time
from pipelines.semantic_pipeline import Pipeline
from config import get_config
from utils.storage import StorageManager
from quixstreams import Application

# Global variables to be accessed in process_pipeline
raw_data: str = ""
processed_data: str = ""
aggregated_data: str = ""
storagemanager: StorageManager | None = None
cfg = get_config()

def process_pipeline(msg):
    full_episode = msg.get('transcription')
    filename = msg.get('title')
    # Sanitize filename: remove/replace illegal characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)  # Remove illegal chars
    # filename = filename.strip()  
    
    if not filename.endswith('.json'):
        filename = f"{filename}.json"

    pipeline = Pipeline( 
        full_episode, 
        filename,
        f"{cfg.OLLAMA_HOST}:{cfg.OLLAMA_PORT}", 
        cfg.MAX_TOKENS, 
        cfg.MODEL_NAME,
        cfg.CHUNK_SIZE, 
        cfg.OVERLAP_SENTENCES, 
        raw_data, 
        processed_data,
        aggregated_data,
        max_wokers=cfg.MAX_WORKERS
    )
    
    init_timestamp = int(time.time())
    episode_metadata = pipeline.aggregate()
    logging.info(f"Time taken : {int(time.time()) - init_timestamp}  s")
    
    if storagemanager is not None:
        storagemanager.save_to_layer(layer="gold", data=[episode_metadata], filename=filename)

    # Merge with the original message
    enriched_msg = msg.copy()
    enriched_msg["metadata"] = episode_metadata
    with open(f"data/gold/enriched_metadata/{filename}", "w", encoding="utf-8") as f:
        json.dump(enriched_msg, f, indent=2, ensure_ascii=False)
    return enriched_msg


def main(url: str, port: int, consumer_group: str, topic_in: str, topic_out: str):
    global raw_data, processed_data, aggregated_data, storagemanager
    
    raw_data = "./data/silver/transcripts"
    processed_data = "./data/gold/chunked_data"
    aggregated_data = "./data/gold/aggregated"
    storagemanager = StorageManager(bronze_dir=raw_data, silver_dir=processed_data, gold_dir=aggregated_data)

    app = Application(
        broker_address=f"{url}:{port}",
        auto_offset_reset='earliest',
        consumer_group=consumer_group
    )
    
    input_topic = app.topic(topic_in)
    output_topic = app.topic(topic_out)
    sdf = app.dataframe(input_topic)

    sdf = sdf.apply(process_pipeline)
    
    sdf = sdf.to_topic(output_topic)
    app.run()


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.Formatter.converter = time.gmtime
    
    main(
        url=cfg.KAFKA_URL,
        port=cfg.KAFKA_PORT,
        consumer_group=cfg.GROUP_ID,
        topic_in=cfg.TOPIC_TO_CONSUME,
        topic_out=cfg.TOPIC_TO_PRODUCE
    )
