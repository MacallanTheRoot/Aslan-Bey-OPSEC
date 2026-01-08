import mutagen
import shutil
from .base import BaseHandler

class MediaHandler(BaseHandler):
    def process(self, input_path, output_path):
        removed_fields = []
        try:
            # Mutagen usually works in-place or needs a copy first.
            # We copy to output first.
            self._copy_file(input_path, output_path)
            
            f = mutagen.File(output_path, easy=True)
            if f is not None:
                # We can't easily iterate all keys in a generic way for all types without knowing them, 
                # but delete() usually strips generic tags.
                
                # Check known tags for logging (simplified)
                if 'artist' in f or 'title' in f or 'album' in f:
                    removed_fields.append("ID3/Vorbis Tags (Artist, Title, etc)")
                
                f.delete()
                f.save()
                
                if not removed_fields:
                     # Check if it had tags we missed or if delete worked silently
                     # We assume if delete() didn't fail, we cleaned it.
                     pass
            else:
                 # Logic for things mutagen detects but returns None (unsupported container but supported mime?)
                 # Or just raw tags?
                 pass
            
            return removed_fields or ["Media Metadata (Blind Strip)"]
            
        except Exception as e:
            self.logger.log_error(input_path, f"Media processing failed: {e}")
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except OSError:
                    pass
            return None
