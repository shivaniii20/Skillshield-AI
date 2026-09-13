import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import shutil


# ============================================================
# TESSERACT CONFIGURATION
# ============================================================

# Use Windows Tesseract if available.
# On Streamlit Cloud/Linux, Tesseract is already installed
# through packages.txt and can be found automatically.

if shutil.which("tesseract"):
    pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract")
else:
    windows_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    if shutil.which(windows_tesseract):
        pytesseract.pytesseract.tesseract_cmd = windows_tesseract


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(file_path):

    text = ""

    # --------------------------------------------------------
    # 1. Try normal PDF text extraction
    # --------------------------------------------------------

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"


    # --------------------------------------------------------
    # 2. If no text is found, use OCR
    # --------------------------------------------------------

    if not text.strip():

        print("No text found. Using OCR...")

        # IMPORTANT:
        # Do NOT specify poppler_path.
        # Streamlit Cloud already installs Poppler through
        # packages.txt and puts it in the system PATH.

        images = convert_from_path(
            file_path
        )

        for image in images:

            ocr_text = pytesseract.image_to_string(
                image
            )

            if ocr_text:

                text += ocr_text + "\n"


    return text