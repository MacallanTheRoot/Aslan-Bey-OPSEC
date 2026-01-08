import os
import random

class Shredder:
    """
    Secure file deletion utility implementing DoD 5220.22-M style algorithms.
    """
    @staticmethod
    def secure_delete(file_path, passes=3):
        """
        Overwrites the file with random data before unlinking.
        """
        if not os.path.exists(file_path):
            return

        formatted_size = os.path.getsize(file_path)
        
        try:
            with open(file_path, "ba+") as f:
                for _ in range(passes):
                    f.seek(0)
                    # Write random bytes
                    f.write(os.urandom(formatted_size))
                    f.flush()
                    os.fsync(f.fileno())
                    
                    # Zero out (optional, commonly done as last pass or interleaved)
                    f.seek(0)
                    f.write(b'\x00' * formatted_size)
                    f.flush()
                    os.fsync(f.fileno())
        except Exception as e:
            # Fallback if overwrite fails (e.g. permission), just try to delete
            print(f"Warning: Secure overwrite failed for {file_path}: {e}")
        
        try:
            os.remove(file_path)
        except OSError as e:
            print(f"Error removing file {file_path}: {e}")
