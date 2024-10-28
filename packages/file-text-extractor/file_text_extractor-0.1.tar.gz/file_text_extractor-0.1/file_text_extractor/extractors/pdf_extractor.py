# file_text_extractor/extractors/pdf_extractor.py
import fitz  # PyMuPDF

def extract_text_from_pdf(file_content):
    """Extracts text from a PDF file given its byte content."""
    try:
        pdf_document = fitz.open(stream=file_content, filetype="pdf")
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text("text")
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")