from PyPDF2 import PdfReader
import os


# data extraction function
def extract_pdf_text(pdf_path: str):
    # load file
    rd = PdfReader(os.path.join("RAG", "Achievements Overview.pdf"))
    if not rd:
        raise FileNotFoundError("The PDF file could not be found or is empty.")

    # extract text
    text = ""
    for page in rd.pages:
        text += page.extract_text() if page.extract_text() else ""
    if not text:
        raise ValueError("No text could be extracted from the PDF file.")
    return text
