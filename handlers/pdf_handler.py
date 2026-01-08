import pikepdf
from .base import BaseHandler

class PdfHandler(BaseHandler):
    def process(self, input_path, output_path):
        removed_fields = []
        try:
            # Open PDF
            pdf = pikepdf.open(input_path)
            
            # Remove Document Info (Author, Title, etc.)
            if pdf.docinfo:
                removed_fields.append("Document Info (Author, Title, etc.)")
                del pdf.docinfo
            
            # Remove XMP
            if 'metadata' in pdf.Root:
                removed_fields.append("XMP Metadata")
                del pdf.Root.metadata
                
            # Remove PieceInfo (App specific data)
            if 'PieceInfo' in pdf.Root:
                removed_fields.append("PieceInfo")
                del pdf.Root.PieceInfo
                
            # Save cleaned PDF
            # linearize=False is default
            # force_version=None
            # preserve_pdfa=False (we want to strip everything)
            pdf.save(output_path)
            
            # To ensure incremental updates are gone, pikepdf.save does a full rewrite by default
            # unless incremental=True is passed. We use default (False).
            removed_fields.append("Incremental Updates (History)")
            
            return removed_fields
            
        except Exception as e:
            self.logger.log_error(input_path, f"PDF processing failed: {e}")
            return None
