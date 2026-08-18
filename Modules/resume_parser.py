import pdfplumber
import pytesseract

from pdf2image import convert_from_path


# Tesseract path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# Poppler path
POPPLER_PATH = (
    r"C:\Users\Shivani Dhas\Downloads\Release-26.02.0-0"
    r"\poppler-26.02.0\Library\bin"
)


def extract_text_from_pdf(file_path):

    text = ""

    # Try normal PDF text extraction
    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    # If no text is found, use OCR
    if not text.strip():

        print("No text found. Using OCR...")

        images = convert_from_path(
            file_path,
            poppler_path=POPPLER_PATH
        )

        for image in images:

            ocr_text = pytesseract.image_to_string(image)

            if ocr_text:
                text += ocr_text + "\n"

    return text