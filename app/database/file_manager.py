import json
import os
from typing import List, Dict, Any

class FileManager:
    """
    Utility class responsible for File I/O operations.
    Handles reading from and writing to JSON files securely.
    All methods are static as they manage pure data flow without needing object state.
    """
    
    # Base directory path where all data files will be stored
    DATA_DIR: str = os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def _get_file_path(filename: str) -> str:
        """
        Helper method to construct the full absolute path for a given filename.
        Keeps path generation logic centralized.
        """
        return os.path.join(FileManager.DATA_DIR, filename)

    @staticmethod
    def load_data(filename: str) -> List[Dict[str, Any]]:
        """
        Reads data from a specified JSON file.
        
        Returns:
            A list of dictionaries containing the parsed JSON data. 
            Returns an empty list if the file is missing or corrupted.
        """
        path = FileManager._get_file_path(filename)
        
        # Guard clause: Agar file exist nahi karti, toh empty list return karo
        if not os.path.exists(path):
            return []
        
        try:
            
            with open(path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):

            return []

    @staticmethod
    def save_data(filename: str, data: List[Dict[str, Any]]) -> bool:
        """
        Saves a list of dictionaries into a specified JSON file.
        Automatically creates the target directory if it does not exist.
        
        Returns:
            True if data is saved successfully, False if an error occurs.
        """
        path = FileManager._get_file_path(filename)
        
        
        if not os.path.exists(FileManager.DATA_DIR):
            os.makedirs(FileManager.DATA_DIR)

        try:

            with open(path, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as error:
            print(f">> ⚠️ Error saving data to {filename}. Details: {error}")
            return False

