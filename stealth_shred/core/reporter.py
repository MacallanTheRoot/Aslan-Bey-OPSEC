import json
import os

class Reporter:
    """
    Generates post-process audit reports.
    """
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path

    def generate_summary(self):
        """
        Reads the audit log and returns a summary dict.
        """
        if not os.path.exists(self.log_file_path):
            return {"error": "Log file not found"}

        total_files = 0
        cleaned_files = 0
        errors = 0
        bytes_saved = 0
        
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        total_files += 1
                        if record['status'] == 'CLEANED':
                            cleaned_files += 1
                            orig = record.get('original_size', 0)
                            new = record.get('new_size', 0)
                            if orig and new:
                                bytes_saved += (orig - new)
                        elif record['status'] == 'ERROR':
                            errors += 1
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            return {"error": str(e)}

        return {
            "total_processed": total_files,
            "successfully_cleaned": cleaned_files,
            "errors": errors,
            "total_bytes_saved": bytes_saved,
            "log_location": self.log_file_path
        }

    def print_report(self):
        summary = self.generate_summary()
        print("\n" + "="*40)
        print(" STEALTH SHRED - AUDIT REPORT")
        print("="*40)
        if "error" in summary:
            print(f"Error reading logs: {summary['error']}")
        else:
            print(f" Total Processed:   {summary['total_processed']}")
            print(f" Cleaned:           {summary['successfully_cleaned']}")
            print(f" Errors:            {summary['errors']}")
            print(f" Storage Saved:     {summary['total_bytes_saved'] / 1024:.2f} KB")
            print(f" Detailed Log:      {summary['log_location']}")
        print("="*40 + "\n")
