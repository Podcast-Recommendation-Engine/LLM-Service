import os
import json
import logging

log = logging.getLogger(__name__)

class StorageManager:

    def __init__(self, bronze_dir: str, silver_dir: str, gold_dir: str) -> None:
        self.bronze_dir = bronze_dir
        self.silver_dir = silver_dir
        self.gold_dir = gold_dir
        self._assert_exist()

    def save_to_layer(self, layer: str, data: list, filename: str) -> str:
        # Resolve layer path
        layer_path = self._get_layer_path(layer)
        file_path = os.path.join(layer_path, filename)

        # Load existing data if file exists
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as existed_file:
                existing_data = json.load(existed_file)
                existing_data.extend(data)        
        else:
            existing_data = data

        # Save back to JSON
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)

        log.info(f"Saved {len(data)} items to {file_path}")
        return file_path
    
    def load_from_layer(self, layer: str, filename: str) -> list:
        # Resolve layer path
        layer_path = self._get_layer_path(layer)
        file_path = os.path.join(layer_path, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(F"File {file_path} Not found a si ibrahim")
        # Load existing data if file exists
        else :
            with open(file_path, 'r', encoding='utf-8') as existed_file:
                existing_data = json.load(existed_file)         
            return existing_data
    
    def _assert_exist(self) -> None:
        """Ensure all directories exist; raise error if missing."""
        for dir in [self.bronze_dir, self.silver_dir, self.gold_dir]:
            if not os.path.isdir(dir):
                raise FileNotFoundError(f"Directory does not exist: {dir}")

    def _get_layer_path(self, layer: str) -> str:
        """Return the absolute path for the given layer name."""
        layer_map = {
            "bronze": self.bronze_dir,
            "silver": self.silver_dir,
            "gold": self.gold_dir
        }
        if layer not in layer_map:
            raise ValueError(f"Invalid layer '{layer}'. Expected one of {list(layer_map.keys())}")
        return layer_map[layer]
