# file_text_extractor/file_extractor.py
from .extractors.gcs_extractor import extract_text_from_gcs
from .extractors.pdf_extractor import extract_text_from_pdf
from .extractors.docx_extractor import extract_text_from_docx
from .extractors.txt_extractor import extract_text_from_txt

def extract_text(file_path=None, gcs_uri=None):
    """Extracts text from a local file or a GCS URI."""
    if gcs_uri:
        return extract_text_from_gcs(gcs_uri)
    elif file_path:
        return _extract_from_local_file(file_path)
    else:
        raise ValueError("You must provide either a file_path or a gcs_uri")

def _extract_from_local_file(file_path):
    """Extracts text from a local file."""
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            return extract_text_from_pdf(f.read())
    elif file_path.endswith('.docx'):
        with open(file_path, 'rb') as f:
            return extract_text_from_docx(f.read())
    elif file_path.endswith('.txt'):
        with open(file_path, 'rb') as f:
            return extract_text_from_txt(f.read())
    else:
        raise ValueError("Unsupported file type.")