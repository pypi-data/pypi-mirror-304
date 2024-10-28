# file_text_extractor/extractors/docx_extractor.py
from docx import Document
from io import BytesIO

def extract_text_from_docx(file_content):
    """Extracts text from a DOCX file given its byte stream content."""
    try:
        file_stream = BytesIO(file_content) if isinstance(file_content, bytes) else file_content
        document = Document(file_stream)
        text = "\n".join([para.text for para in document.paragraphs])
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract text from DOCX: {str(e)}")