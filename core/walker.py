import os
from pathlib import Path

class DirectoryWalker:
    """
    Robust directory walker that handles nested folders and symlinks safely.
    """
    def __init__(self, root_path, ignore_hidden=True, follow_symlinks=False):
        self.root_path = Path(root_path).resolve()
        self.ignore_hidden = ignore_hidden
        self.follow_symlinks = follow_symlinks

    def walk(self):
        """
        Yields valid file paths for processing.
        """
        if not self.root_path.exists():
            return

        if self.root_path.is_file():
            yield self.root_path
            return

        for root, dirs, files in os.walk(self.root_path, followlinks=self.follow_symlinks):
            # Modify dirs in-place to skip hidden directories
            if self.ignore_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if self.ignore_hidden and file.startswith('.'):
                    continue
                
                full_path = Path(root) / file
                yield full_path

    def count_files(self):
        """
        Quickly count files for progress bar initialization.
        """
        count = 0
        for _ in self.walk():
            count += 1
        return count
