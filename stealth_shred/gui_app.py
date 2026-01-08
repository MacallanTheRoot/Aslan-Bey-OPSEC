import streamlit as st
import os
import shutil
import tempfile
import time
import pandas as pd
from datetime import datetime

# Import Core Logic
# We need to add the parent directory to sys.path to import stealth_shred if running from inside
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stealth_shred.core.detector import FileDetector
from stealth_shred.core.walker import DirectoryWalker
from stealth_shred.core.logger import AuditLogger
from stealth_shred.core.reporter import Reporter
from stealth_shred.handlers.utils.shredder import Shredder
from stealth_shred.handlers.image_handler import ImageHandler
from stealth_shred.handlers.pdf_handler import PdfHandler
from stealth_shred.handlers.office_handler import OfficeHandler
from stealth_shred.handlers.media_handler import MediaHandler

# --- CONFIGURATION & THEME ---
st.set_page_config(
    page_title="Aslan Bey Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Cybersecurity Dark Theme
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
        color: #00ff41;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00ff41 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #238636;
        color: white;
        border: 1px solid #2ea043;
        border-radius: 6px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2ea043;
        border-color: #3fb950;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00ff41;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-color: #00ff41;
    }

    /* Success/Error boxes */
    .stSuccess {
        background-color: rgba(35, 134, 54, 0.2);
        color: #3fb950;
    }
    .stError {
        background-color: rgba(218, 54, 51, 0.2);
        color: #f85149;
    }
</style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'cleaned_files' not in st.session_state:
    st.session_state.cleaned_files = [] 
if 'audit_logger' not in st.session_state:
    st.session_state.audit_logger = AuditLogger() # Persist logger

# --- UTILS ---
def get_handler_for_file(file_path, detector):
    is_supported, category = detector.is_supported(file_path)
    if not is_supported:
        return None, None
    
    logger = st.session_state.audit_logger
    
    if category == 'image': return ImageHandler(logger), category
    if category == 'pdf': return PdfHandler(logger), category
    if category == 'office': return OfficeHandler(logger), category
    if category == 'media': return MediaHandler(logger), category
    
    return None, None

def process_file_logic(input_path, output_path, force_mode):
    detector = FileDetector()
    handler, category = get_handler_for_file(input_path, detector)
    
    if not handler:
        return False, "Unsupported File Type", []
        
    try:
        # TEMP handling handled by caller usually, but logic here mirrors cli
        cleaned_fields = handler.process(input_path, output_path)
        
        if cleaned_fields is not None:
             if not cleaned_fields:
                 cleaned_fields.append("Verified Clean (No changes)")
             
             # Log it
             if os.path.exists(input_path) and os.path.exists(output_path):
                 orig_size = os.path.getsize(input_path)
                 new_size = os.path.getsize(output_path)
                 st.session_state.audit_logger.log_scrub(input_path, orig_size, new_size, cleaned_fields)
                 
             return True, "Success", cleaned_fields
        else:
             return False, "Processing Failed (Unknown Input Error)", []
             
    except Exception as e:
        return False, str(e), []

# --- APP LAYOUT ---

st.title("🛡️ ASLAN BEY v2.0")
st.markdown("### High-Stakes Metadata Reconstruction & OPSEC Intelligence")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    force_mode = st.toggle("Force Mode (Destructive)", value=False, help="Overwrites original files and securely shreds them.")
    recursion = st.toggle("Recursive Scan", value=True, help="Scan subdirectories in Directory Mode.")
    secure_shred_passes = st.slider("Shred Passes", 1, 7, 3, disabled=not force_mode)
    
    st.divider()
    st.info(f"Session ID: {id(st.session_state)}")
    if st.button("Clear Session History"):
        st.session_state.cleaned_files = []
        st.rerun()

# Tabs
tab_upload, tab_dir, tab_audit = st.tabs(["🚀 Single File Upload", "📂 Directory Mode", "📊 Audit Logs"])

# --- TAB 1: UPLOAD ---
with tab_upload:
    st.markdown("#### Secure File Upload Zone")
    uploaded_file = st.file_uploader("Drag & Drop File", type=None) # Accept all, verify via magic
    
    if uploaded_file:
        # Save temp
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as tmp_in:
            tmp_in.write(uploaded_file.getvalue())
            input_path = tmp_in.name
            
        # Detect
        detector = FileDetector()
        mime = detector.detect(input_path)
        is_supported, category = detector.is_supported(input_path)
        
        col1, col2 = st.columns(2)
        with col1:
             st.metric("Detected MIME", mime)
        with col2:
             if is_supported:
                 st.metric("Exposure Level", "HIGH", delta_color="inverse")
             else:
                 st.metric("Exposure Level", "Unknown", delta_color="off")
        
        if is_supported:
            if st.button("🚀 Shred Metadata", type="primary"):
                with st.spinner("Sanitizing..."):
                    # Output path
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_clean_{uploaded_file.name}") as tmp_out:
                        output_path = tmp_out.name
                    
                    success, msg, fields = process_file_logic(input_path, output_path, force=False) # Web mode always non-force on original upload buffer
                    
                    if success:
                        st.success("File Sanitized Successfully!")
                        st.write("Removed Fields:")
                        st.json(fields)
                        
                        # Download Button
                        with open(output_path, "rb") as f:
                            st.download_button(
                                label="⬇️ Download Cleaned File",
                                data=f,
                                file_name=f"clean_{uploaded_file.name}",
                                mime=mime
                            )
                    else:
                        st.error(f"Sanitization Failed: {msg}")
                        
                    # Cleanup Temp
                    # In a real app we might schedule cleanup, here we rely on OS temp cleaning or do it immediately if download read into memory
                    # Streamlit rerun might lose the file reference if we delete too early
        else:
            st.warning("File type not fully supported for deep scrubbing.")

# --- TAB 2: DIRECTORY ---
with tab_dir:
    st.markdown("#### Local Directory Scanner")
    target_dir = st.text_input("Target Directory Path (Local)")
    
    if target_dir and os.path.exists(target_dir):
        if st.button("Start Batch Job"):
            walker = DirectoryWalker(target_dir, ignore_hidden=True, follow_symlinks=False)
            files = list(walker.walk())
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            processed = 0
            
            for i, file_path in enumerate(files):
                status_text.text(f"Processing: {os.path.basename(file_path)}")
                
                # Logic similar to CLI
                # We need to construct output path
                # If force, use temp then overwrite
                # If not force, use _cleaned
                
                file_str = str(file_path)
                if force_mode:
                    out_path = file_str + ".tmp_shred"
                else:
                    base, ext = os.path.splitext(file_str)
                    out_path = f"{base}_cleaned{ext}"
                
                success, msg, fields = process_file_logic(file_str, out_path, force_mode)
                
                if success:
                    if force_mode:
                         Shredder.secure_delete(file_str, passes=secure_shred_passes)
                         os.rename(out_path, file_str)
                else:
                     # Cleanup temp if failed
                     if os.path.exists(out_path) and out_path != file_str:
                         try: os.remove(out_path)
                         except: pass

                processed += 1
                progress_bar.progress((i + 1) / len(files))
                
            status_text.text("Batch Job Complete!")
            st.success(f"Processed {processed} files.")
            st.balloons()
            
    elif target_dir:
        st.error("Directory not found.")

# --- TAB 3: LOGS ---
with tab_audit:
    st.markdown("#### 🕵️ Audit Logs")
    
    log_file = st.session_state.audit_logger.get_log_path()
    reporter = Reporter(log_file)
    summary = reporter.generate_summary()
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Processed", summary.get("total_processed", 0))
    c2.metric("Cleaned", summary.get("successfully_cleaned", 0))
    c3.metric("Errors", summary.get("errors", 0))
    c4.metric("Bytes Saved", f"{summary.get('total_bytes_saved', 0)/1024:.1f} KB")
    
    # Load Dataframe
    if os.path.exists(log_file):
        try:
             # Read jsonl
             df = pd.read_json(log_file, lines=True)
             if not df.empty:
                 st.dataframe(df, use_container_width=True)
                 
                 # Visualization
                 if 'cleaned_fields' in df.columns:
                      # Flatten fields
                      all_fields = []
                      for fp in df['cleaned_fields']:
                           if isinstance(fp, list):
                               all_fields.extend(fp)
                      
                      if all_fields:
                          field_counts = pd.Series(all_fields).value_counts()
                          st.bar_chart(field_counts)
        except Exception as e:
            st.error(f"Could not load logs: {e}")
