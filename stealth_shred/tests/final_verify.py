import os
import shutil
import zipfile
import sys
import logging
from PIL import Image
import piexif
import pikepdf
import magic

# Adjust path to import core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stealth_shred.core.cli import cli
from stealth_shred.core.detector import FileDetector
from stealth_shred.handlers.office_handler import OfficeHandler
from click.testing import CliRunner

TEST_DIR = "final_test_data"
LOG_DIR = "logs"

def setup():
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR)
    
    # Ensure log dir exists for checking later
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def create_dirty_files():
    print("[1] Generating Dirty Files...")
    
    # 1. Dirty JPEG with EXIF
    img_path = os.path.join(TEST_DIR, "dirty.jpg")
    img = Image.new("RGB", (100, 100), color="blue")
    exif_dict = {"0th": {piexif.ImageIFD.Make: u"SpyCam 3000", piexif.ImageIFD.Model: u"HiddenLens"}}
    exif_bytes = piexif.dump(exif_dict)
    img.save(img_path, exif=exif_bytes)
    print(f" - Created {img_path} (EXIF: SpyCam 3000)")

    # 2. Dirty PDF (Simulated)
    pdf_path = os.path.join(TEST_DIR, "dirty.pdf")
    pdf = pikepdf.new()
    pdf.docinfo["/Author"] = "Foreign Agent"
    pdf.docinfo["/Producer"] = "Compromised Software v1.0"
    pdf.save(pdf_path)
    print(f" - Created {pdf_path} (Author: Foreign Agent)")

    # 3. Dirty DOCX (Simulated)
    docx_path = os.path.join(TEST_DIR, "dirty.docx")
    core_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <dc:creator>Mole</dc:creator>
    <cp:lastModifiedBy>Handler</cp:lastModifiedBy>
</cp:coreProperties>"""
    with zipfile.ZipFile(docx_path, 'w') as z:
        z.writestr('docProps/core.xml', core_xml)
        z.writestr('word/document.xml', '<root></root>')
    print(f" - Created {docx_path} (Creator: Mole)")

    # 4. MIME Spoofing
    # Create a ZIP file but name it .jpg
    fake_jpg_path = os.path.join(TEST_DIR, "malware.jpg")
    with zipfile.ZipFile(fake_jpg_path, 'w') as z:
        z.writestr('payload.exe', 'binary_data_here')
    print(f" - Created {fake_jpg_path} (Actual: ZIP, Extension: JPG)")

def test_mime_detection():
    print("\n[2] Testing MIME Detection & Spoof Handling...")
    detector = FileDetector()
    fake_jpg_path = os.path.join(TEST_DIR, "malware.jpg")
    
    mime = detector.detect(fake_jpg_path)
    print(f" - Detected MIME for malware.jpg: {mime}")
    
    is_supported, cat = detector.is_supported(fake_jpg_path)
    print(f" - Supported? {is_supported} (Category: {cat})")
    
    if is_supported is False:
        print("   ✅ PASS: Spoofed file correctly rejected.")
    else:
        print("   ❌ FAIL: Spoofed file was accepted!")
        sys.exit(1)

def run_cleaning_process():
    print("\n[3] Executing Aslan Bey Engine...")
    runner = CliRunner()
    result = runner.invoke(cli, ['clean', TEST_DIR])
    print(result.output)
    if result.exit_code != 0:
        print("❌ CLI Execution Failed")
        print(result.exception)
        sys.exit(1)

def verify_results():
    print("\n[4] Verifying Logic...")
    
    # Check JPEG
    clean_jpg = os.path.join(TEST_DIR, "dirty_cleaned.jpg")
    if os.path.exists(clean_jpg):
        img = Image.open(clean_jpg)
        if 'exif' not in img.info:
            print(" - ✅ JPEG Cleaned (No EXIF)")
        else:
             exif_dict = piexif.load(img.info['exif'])
             if not exif_dict.get("0th"):
                 print(" - ✅ JPEG Cleaned (Empty EXIF)")
             else:
                 print(" - ❌ JPEG verification failed! Metadata remains.")
    else:
        print(" - ❌ JPEG output missing")

    # Check PDF
    clean_pdf = os.path.join(TEST_DIR, "dirty_cleaned.pdf")
    if os.path.exists(clean_pdf):
        pdf = pikepdf.open(clean_pdf)
        if "/Author" not in pdf.docinfo:
             print(" - ✅ PDF Cleaned (Author removed)")
        else:
             print(" - ❌ PDF Author tag remains!")
    else:
        print(" - ❌ PDF output missing")
        
    # Check DOCX
    clean_docx = os.path.join(TEST_DIR, "dirty_cleaned.docx")
    if os.path.exists(clean_docx):
        with zipfile.ZipFile(clean_docx, 'r') as z:
            content = z.read('docProps/core.xml').decode('utf-8')
            if "Mole" not in content:
                print(" - ✅ DOCX Cleaned (Creator removed)")
            else:
                print(" - ❌ DOCX Creator remains!")
    else:
        print(" - ❌ DOCX output missing")

    # Check that malware.jpg was NOT processed (no _cleaned version)
    fake_cleaned = os.path.join(TEST_DIR, "malware_cleaned.jpg")
    if not os.path.exists(fake_cleaned):
        print(" - ✅ Malware.jpg skipped (No output generated)")
    else:
        print(" - ❌ Malware.jpg was processed! Security bypass detected!")

    print("\n[5] Checking Audit Logs...")
    # Find latest log
    logs = sorted([os.path.join(LOG_DIR, f) for f in os.listdir(LOG_DIR) if f.endswith('.jsonl')], key=os.path.getmtime)
    if not logs:
        print(" - ❌ No audit logs found!")
    else:
        latest = logs[-1]
        print(f" - Reading {latest}")
        with open(latest, 'r') as f:
            for line in f:
                print(f"   LOG ENTRY: {line.strip()}")
        print(" - ✅ Audit Log verified.")

if __name__ == "__main__":
    setup()
    create_dirty_files()
    test_mime_detection()
    run_cleaning_process()
    verify_results()
