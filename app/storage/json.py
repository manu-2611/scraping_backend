import json
import logging
from typing import Dict, Any
from storage.storage import StorageClass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JsonStorage(StorageClass):
    def __init__(self, file_path: str):
        self.file_path = file_path


    def get(self) -> Dict[str, Any]:
        """Reads data from a JSON file and returns it as a dictionary."""

        try:
            with open(self.file_path, 'r') as json_file:
                data = json.load(json_file)
            logger.info(f"Data read from {self.file_path} successfully.")
            return data
        
        except FileNotFoundError:
            logger.warning(f"File not found: {self.file_path}")
            return {}
        
        except json.JSONDecodeError:
            logger.error("Error decoding JSON. The file may be corrupted.")
            return {}
        
        except Exception as e:
            logger.error(f"Failed to read data from JSON: {e}")
            return {}
        
    def create(self, data: Dict[str, Any]) -> None:
        """Saves a dictionary to a JSON file."""

        try:
            with open(self.file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            logger.info(f"Data saved to {self.file_path} successfully.")
            
        except Exception as e:
            logger.error(f"Failed to save data to JSON: {e}")