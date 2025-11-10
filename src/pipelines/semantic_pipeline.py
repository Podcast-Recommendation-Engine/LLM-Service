from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import logging
import os
import time
from processing.chunk_processor import ChunkProcessor
from processing.episode_processor import EpisodeProcessor
from utils.chunker import SemanticChunkingManager
from utils.storage import StorageManager

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Pipeline:
    def __init__(self, full_episode: str, url: str, max_tokens: int, model_name: str, chunk_size: int, window_overlap: int, bronze_dir: str, silver_dir: str, gold_dir: str, max_wokers: int ) -> None:
        
        self.bronze_dir = bronze_dir
        self.silver_dir = silver_dir
        self.gold_dir = gold_dir
        self.max_workers = max_wokers

        self.semanticchunkermanager = SemanticChunkingManager(content=full_episode, chunk_size=chunk_size, window_overlap=window_overlap)
        self.storagemanager = StorageManager(bronze_dir=self.bronze_dir, silver_dir=self.silver_dir, gold_dir=self.gold_dir)
        self.chunkprocessor = ChunkProcessor(url=url, max_tokens=max_tokens, model_name=model_name)
        self.episodeprocessor = EpisodeProcessor(url=url, max_tokens=max_tokens, model_name=model_name)

    def chunk_threaded(self):
        data = self.semanticchunkermanager.chunk_content()
        self.storagemanager.save_to_layer(layer="silver", data=data, filename="test.json")

        metadata_chunked = []
        start = time.time()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all chunks as separate threads
            futures = {
                executor.submit(
                    self.chunkprocessor.run_generate_chunk,
                    chunk["content"],
                    chunk["order"],
                    chunk["is_last"]
                ): chunk["order"]
                for chunk in data
            }

            for future in as_completed(futures):
                order = futures[future]
                try:
                    metadata_chunked.append(future.result())
                except Exception as e:
                    log.error(f"Chunk {order} failed : {e}")

        elapsed = int(time.time() - start)
        log.info(f"Chunk processing finished in {elapsed}s. {len(metadata_chunked)}/{len(data)} chunks processed.")
        self.storagemanager.save_to_layer("silver", metadata_chunked, "chunkfromollama.json")
        return metadata_chunked

    def aggregate(self):
        metadata_chunked = self.chunk_threaded()
        episode_metadata = self.episodeprocessor.run_aggregate_chunks(content=metadata_chunked)
        return episode_metadata
