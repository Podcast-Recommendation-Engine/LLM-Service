import json
import logging
import os
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

        self.episodeprocessor = EpisodeProcessor(
            url=url,
            max_tokens=max_tokens,
            model_name=model_name
        )

    def chunk(self):
        data = self.semanticchunkermanager.chunk_content()
        metadata_chunked = []

        for chunk in data:
            try:
                chunk_metadata = self.chunkprocessor.run_generate_chunk(
                    chunk_content=chunk["content"],
                    order=chunk["order"],
                    is_last=chunk["is_last"]
                )
                metadata_chunked.append(chunk_metadata)

            except Exception as e:
                log.error(f"Failed to process chunk {chunk['order']}: {e}")
                continue

        return metadata_chunked
    

    def aggregate(self):
        metadata_chunked = self.chunk()
        episode_metadata = []

        episode_metadata = self.episodeprocessor.run_gaggregate_chunks(
                   content=metadata_chunked
                )

            # Save the processed metadata to silver layer
        self.storagemanager.save_to_layer(
            layer="gold", 
            data=episode_metadata, 
            filename="testwbaralelgold.json"
    )

        return episode_metadata

