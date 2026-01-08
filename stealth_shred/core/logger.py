import logging
import json
import os
from datetime import datetime

class AuditLogger:
    """
    Detailed logger for OPSEC auditing.
    Tracks exactly which metadata fields were removed.
    """
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(log_dir, f"stealth_shred_audit_{timestamp}.jsonl")
        
        # Setup Logger
        self.logger = logging.getLogger("AslanBeyAudit")
        self.logger.setLevel(logging.INFO)
        
        # File Handler (JSON Lines for easy parsing)
        fh = logging.FileHandler(self.log_file)
        fh.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(fh)

    def log_scrub(self, file_path, original_size, new_size, cleaned_fields, status="CLEANED"):
        """
        Log a single file scrub event.
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "file": file_path,
            "status": status,
            "original_size": original_size,
            "new_size": new_size,
            "cleaned_fields": cleaned_fields
        }
        self.logger.info(json.dumps(record))

    def log_error(self, file_path, error_msg):
        """
        Log an error during processing.
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "file": file_path,
            "status": "ERROR",
            "error": str(error_msg)
        }
        self.logger.error(json.dumps(record))

    def get_log_path(self):
        return self.log_file
