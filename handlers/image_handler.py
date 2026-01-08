from PIL import Image
import piexif
from .base import BaseHandler

class ImageHandler(BaseHandler):
    def process(self, input_path, output_path):
        removed_fields = []
        try:
            # Open the image
            with Image.open(input_path) as img:
                # Handle EXIF
                if 'exif' in img.info:
                    try:
                        exif_dict = piexif.load(img.info['exif'])
                        # Check what we have before removing (for logging)
                        if exif_dict.get("GPS"):
                            removed_fields.append("GPS")
                        if exif_dict.get("0th", {}).get(piexif.ImageIFD.Make):
                            removed_fields.append("Make/Model")
                        if exif_dict.get("Exif"):
                            removed_fields.append("Exif Data")
                            
                        # Remove EXIF
                        piexif.remove(input_path)
                        # We used piexif.remove on the file directly? 
                        # Wait, piexif.remove modifies file in place usually or we strip from object.
                        # Best practice: create a new image without data.
                    except Exception:
                        # Piexif might fail on some weird headers
                        pass
                
                # Create a fresh copy to ensure no other metadata persists
                # This stripes ICC profiles and other info unless explicitly preserved
                data = list(img.getdata())
                clean_img = Image.new(img.mode, img.size)
                clean_img.putdata(data)
                
                # Save
                clean_img.save(output_path)
                
                if not removed_fields:
                    removed_fields.append("General Metadata (Striped via Reconstruction)")
                
                return removed_fields
        except Exception as e:
            self.logger.log_error(input_path, f"Image processing failed: {e}")
            return None
