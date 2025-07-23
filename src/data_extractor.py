from PyPDF2 import PdfReader
import os


def extract_data_from_file(file_path):
    """
    Extracts text from a single PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: A string containing the extracted text.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    if not file_path.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported.")

    reader = PdfReader(file_path)

    text = ""
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
        else:
            print(f"⚠️ No text found on page {i+1} of {file_path}")

    return text.strip()
