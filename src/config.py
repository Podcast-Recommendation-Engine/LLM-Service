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
        OLLAMA_KEEP_ALIVE = os.getenv("OLLAMA_KEEP_ALIVE", "true").lower() in ("1", "true", "yes")
        OLLAMA_NUM_THREADS = int(os.getenv("OLLAMA_NUM_THREADS", 4))
        OLLAMA_MAX_LOADED_MODELS = int(os.getenv("OLLAMA_MAX_LOADED_MODELS", 2))
        CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 512))
        OVERLAP_SENTENCES = int(os.getenv("OVERLAP_SENTENCES", 2))
        MODEL_NAME = os.getenv("MODEL_NAME", "llama2")
        MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
        REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))
        BATCH_SIZE = int(os.getenv("BATCH_SIZE", 5))

    # Return a single instance of the config class.
    # Due to @lru_cache, this instance will be cached in memory and reused.
    return _Config()
