import click
import os
import sys
from tqdm import tqdm
from colorama import init, Fore, Style

from .walker import DirectoryWalker
from .logger import AuditLogger
from .reporter import Reporter
from .detector import FileDetector
from ..handlers.utils.shredder import Shredder

# Import handlers (will implement these next)
# from ..handlers.image_handler import ImageHandler
# from ..handlers.pdf_handler import PdfHandler
# from ..handlers.office_handler import OfficeHandler
# from ..handlers.media_handler import MediaHandler

# Initialize Colorama
init(autoreset=True)

class Context:
    def __init__(self):
        self.detector = FileDetector()
        self.logger = AuditLogger()
        self.verbose = False
        self.force = False
        self.handlers = {}

    def register_handler(self, category, handler_class):
        self.handlers[category] = handler_class(self.logger)

    def get_handler(self, category):
        return self.handlers.get(category)

pass_context = click.make_pass_decorator(Context, ensure=True)

@click.group()
@click.option('--verbose', '-v', is_flag=True, help="Enable verbose output")
@click.option('--force', '-f', is_flag=True, help="Overwrite original files (Destructive)")
@pass_context
def cli(ctx, verbose, force):
    """
    Aslan Bey: High-Stakes Metadata Reconstruction & OPSEC Tool.
    """
    ctx.verbose = verbose
    ctx.force = force
    
    # We will register handlers here dynamically or explicitly when they are implemented
    # For now, we'll let the 'scan' or 'clean' command register them if available
    pass

@cli.command()
@click.argument('target_path', type=click.Path(exists=True))
@click.option('--recursive/--no-recursive', default=True, help="Recursively scan directories")
@pass_context
def clean(ctx, target_path, recursive):
    """
    Clean metadata from files in the target directory.
    """
    # Lazy import handlers to avoid errors before they exist
    try:
        from ..handlers.image_handler import ImageHandler
        ctx.register_handler('image', ImageHandler)
    except ImportError:
        pass
        
    try:
        from ..handlers.pdf_handler import PdfHandler
        ctx.register_handler('pdf', PdfHandler)
    except ImportError:
        pass

    try:
        from ..handlers.office_handler import OfficeHandler
        ctx.register_handler('office', OfficeHandler)
    except ImportError:
        pass
        
    try:
        from ..handlers.media_handler import MediaHandler
        ctx.register_handler('media', MediaHandler)
    except ImportError:
        pass

    walker = DirectoryWalker(target_path, follow_symlinks=False) # Symlinks False by default for safety
    
    if os.path.isfile(target_path):
        files = [target_path]
    else:
        print(f"{Fore.CYAN}Scanning directory...{Style.RESET_ALL}")
        files = list(walker.walk())
    
    print(f"{Fore.GREEN}Found {len(files)} potential files.{Style.RESET_ALL}")
    
    processed_count = 0
    
    with tqdm(total=len(files), unit="file") as pbar:
        for file_path in files:
            pbar.set_description(f"Processing {os.path.basename(file_path)}")
            
            # Detect
            is_supported, category = ctx.detector.is_supported(str(file_path))
            
            if not is_supported or not category:
                pbar.update(1)
                continue
                
            handler = ctx.get_handler(category)
            if not handler:
                ctx.logger.log_error(str(file_path), f"No handler for category {category}")
                pbar.update(1)
                continue
            
            # Determine Output Path
            if ctx.force:
                output_path = str(file_path) # Overwrite
                temp_output = str(file_path) + ".temp_shred"
            else:
                base, ext = os.path.splitext(str(file_path))
                output_path = f"{base}_cleaned{ext}"
                temp_output = output_path
            
            try:
                # We process to a temp/output path first
                cleaned_fields = handler.process(str(file_path), temp_output)
                
                if cleaned_fields is not None:
                    # Successful processing (even if empty list)
                    if not cleaned_fields:
                         cleaned_fields.append("Verified Clean (No changes)")
                    
                    orig_size = 0
                    if os.path.exists(str(file_path)):
                        orig_size = os.path.getsize(str(file_path))
                    
                    if os.path.exists(temp_output):
                        new_size = os.path.getsize(temp_output)
                        ctx.logger.log_scrub(str(file_path), orig_size, new_size, cleaned_fields)
                        processed_count += 1
                        
                        if ctx.force:
                            # If force, replace original
                            Shredder.secure_delete(str(file_path))
                            os.rename(temp_output, str(file_path))
                    else:
                        # Handler failed to produce output but returned list?
                         ctx.logger.log_error(str(file_path), "Handler returned success but no output file")
                
                else:
                    # Handler returned None (Error)
                    if os.path.exists(temp_output) and temp_output != str(file_path):
                        os.remove(temp_output) # Cleanup
                        
            except Exception as e:
                ctx.logger.log_error(str(file_path), str(e))
                if ctx.verbose:
                    print(f"\n{Fore.RED}Error processing {file_path}: {e}{Style.RESET_ALL}")
            
            pbar.update(1)

    # Generate Report
    reporter = Reporter(ctx.logger.get_log_path())
    reporter.print_report()

if __name__ == '__main__':
    cli()
