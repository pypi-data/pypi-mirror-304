# file_text_extractor/extractors/txt_extractor.py
def extract_text_from_txt(file_content):
    """Extracts text from a plain text file."""
    try:
        text = file_content.decode('utf-8')
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract text from TXT file: {str(e)}")