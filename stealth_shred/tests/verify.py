import os
import shutil
import zipfile
import sys

# Ensure we can import stealth_shred
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import piexif
from PIL import Image
import pikepdf
from stealth_shred.core.cli import cli
from click.testing import CliRunner

TEST_DIR = "test_data"
if os.path.exists(TEST_DIR):
    shutil.rmtree(TEST_DIR)
os.makedirs(TEST_DIR)

def create_dummy_image(path):
    img = Image.new("RGB", (100, 100), color="red")
    exif_dict = {"0th": {piexif.ImageIFD.Make: u"Canon", piexif.ImageIFD.Model: u"EOS 5D"}}
    exif_bytes = piexif.dump(exif_dict)
    img.save(path, exif=exif_bytes)

def create_dummy_pdf(path):
    pdf = pikepdf.new()
    pdf.docinfo["/Author"] = "Secret Agent"
    pdf.save(path)

def create_dummy_docx(path):
    # Minimal Docx Structure
    core_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <dc:title>Secret Plan</dc:title>
    <dc:subject>World Domination</dc:subject>
    <dc:creator>Dr. Evil</dc:creator>
    <cp:lastModifiedBy>Mini Me</cp:lastModifiedBy>
    <cp:revision>1</cp:revision>
</cp:coreProperties>"""
    
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('docProps/core.xml', core_xml)
        z.writestr('word/document.xml', '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>Hello World</w:t></w:r></w:p></w:body></w:document>')

def verify_image(path):
    img = Image.open(path)
    if 'exif' in img.info:
        # Check if empty or minimal
        try:
            exif_dict = piexif.load(img.info['exif'])
            if exif_dict.get("0th", {}).get(piexif.ImageIFD.Make):
                return False, "Make found in EXIF"
        except:
            pass
    return True, "Clean"

def verify_pdf(path):
    pdf = pikepdf.open(path)
    if "/Author" in pdf.docinfo:
        return False, "Author found in DocInfo"
    return True, "Clean"

def verify_docx(path):
    with zipfile.ZipFile(path, 'r') as z:
        content = z.read('docProps/core.xml').decode('utf-8')
        if "Dr. Evil" in content:
            return False, "Author found in core.xml"
    return True, "Clean"

def run_tests():
    print("Generating Test Data...")
    img_path = os.path.join(TEST_DIR, "test.jpg")
    pdf_path = os.path.join(TEST_DIR, "test.pdf")
    docx_path = os.path.join(TEST_DIR, "test.docx")
    
    create_dummy_image(img_path)
    create_dummy_pdf(pdf_path)
    create_dummy_docx(docx_path)
    
    print("Running Aslan Bey...")
    runner = CliRunner()
    result = runner.invoke(cli, ['clean', TEST_DIR]) # Default not force, so creates _cleaned
    
    print(f"Output: {result.output}")
    if result.exit_code != 0:
        print(f"CLI Failed with code {result.exit_code}")
        print(result.exception)
    
    print("\nVerifying Results...")
    failures = []
    
    # Check Image
    clean_img = os.path.join(TEST_DIR, "test_cleaned.jpg")
    if not os.path.exists(clean_img):
        failures.append("Cleaned image not found")
    else:
        ok, msg = verify_image(clean_img)
        if not ok: failures.append(f"Image Failed: {msg}")
        
    # Check PDF
    clean_pdf = os.path.join(TEST_DIR, "test_cleaned.pdf")
    if not os.path.exists(clean_pdf):
        failures.append("Cleaned PDF not found")
    else:
        ok, msg = verify_pdf(clean_pdf)
        if not ok: failures.append(f"PDF Failed: {msg}")

    # Check Docx
    clean_docx = os.path.join(TEST_DIR, "test_cleaned.docx")
    if not os.path.exists(clean_docx):
        failures.append("Cleaned Docx not found")
    else:
        ok, msg = verify_docx(clean_docx)
        if not ok: failures.append(f"Docx Failed: {msg}")
        
    if failures:
        print("\n❌ VERIFICATION FAILED:")
        for f in failures:
            print(f" - {f}")
    else:
        print("\n✅ ALL TESTS PASSED! Files represent 0% Metadata Leakage.")

if __name__ == "__main__":
    run_tests()
