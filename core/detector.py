import magic
import mimetypes
import os

class FileDetector:
    """
    Expert Mode: Uses magic numbers (binary signatures) to detect file types,
    preventing extension spoofing attacks.
    """
    def __init__(self):
        # Initialize magic detector
        # mime=True returns 'application/pdf' instead of 'PDF document...'
        try:
            self.mime_detector = magic.Magic(mime=True)
        except Exception as e:
            # Fallback or error handling if magic libs missing (though requirements enforce it)
            print(f"Warning: python-magic initialization failed: {e}")
            self.mime_detector = None

    def detect(self, file_path):
        """
        Returns the MIME type of the file based on content analysis.
        """
        if not os.path.exists(file_path):
            return None
        
        if self.mime_detector:
            try:
                return self.mime_detector.from_file(file_path)
            except Exception:
                # Fallback to mimetypes if magic fails (e.g. empty file)
                pass
        
        # Fallback
        mime, _ = mimetypes.guess_type(file_path)
        return mime

    def is_supported(self, file_path):
        """
        Checks if file is a supported type for scrubbing.
        Returns: (bool, category_string)
        """
        mime = self.detect(file_path)
        if not mime:
            return False, None
            
        if mime.startswith('image/'):
            return True, 'image'
        elif mime == 'application/pdf':
            return True, 'pdf'
        elif mime in [
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'application/msword', 
            'application/vnd.ms-excel',
            'application/vnd.ms-powerpoint'
        ]:
            return True, 'office'
        elif mime.startswith('audio/') or mime.startswith('video/'):
            return True, 'media'
            
        return False, None
