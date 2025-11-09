from functools import lru_cache
from dotenv import load_dotenv
import os


@lru_cache(maxsize=1)
def get_config():
    """
    Load configuration from environment variables (.env) only once,
    and provide a globally shared config object across the entire app.
    This pattern behaves as a Singleton — one shared instance everywhere.
    """
    load_dotenv()
    class _Config:
        OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
        OLLAMA_PORT = int(os.getenv("OLLAMA_PORT", 11434))
        CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 8000))
        MAX_TOKENS = int(os.getenv("MAX_TOKENS", 1024))
        OVERLAP_SENTENCES = int(os.getenv("OVERLAP_SENTENCES", 2))
        MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:3b")
        
    # Return a single instance of the config class.
    # Due to @lru_cache, this instance will be cached in memory and reused.
    return _Config()
