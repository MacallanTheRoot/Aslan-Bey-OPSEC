from abc import ABC, abstractmethod
import os
import shutil

class BaseHandler(ABC):
    """
    Abstract Base Class for all file handlers.
    """
    def __init__(self, logger):
        self.logger = logger

    @abstractmethod
    def process(self, input_path, output_path):
        """
        Process the file to remove metadata.
        Args:
            input_path (str): Path to the source file.
            output_path (str): Path where the cleaned file should be saved.
        Returns:
            list: List of cleaned metadata fields/keys.
            bool: True if successful, False otherwise.
        """
        pass

    def _copy_file(self, src, dst):
        """
        Helper to copy file, ensuring permissions are handled.
        """
        shutil.copy2(src, dst)
