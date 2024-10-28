# file_text_extractor/extractors/gcs_extractor.py
from google.cloud import storage
from io import BytesIO
from .pdf_extractor import extract_text_from_pdf
from .docx_extractor import extract_text_from_docx
from .txt_extractor import extract_text_from_txt

def extract_text_from_gcs(file_uri):
    """Streams a file from GCS and extracts its text."""
    try:
        # Validate GCS URI
        if not file_uri.startswith('gs://'):
            raise ValueError("Invalid GCS URI. Must start with 'gs://'")

        # Extract bucket and blob name from GCS URI
        uri_parts = file_uri[5:].split("/", 1)
        bucket_name, blob_name = uri_parts[0], uri_parts[1]

        # Initialize the storage client and download the file as a byte stream
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # Use a byte stream to avoid local file download
        file_stream = BytesIO(blob.download_as_bytes())

        # Extract text based on file type
        if blob_name.endswith('.pdf'):
            return extract_text_from_pdf(file_stream.getvalue())  # Pass bytes for PDF
        elif blob_name.endswith('.docx'):
            return extract_text_from_docx(file_stream.getvalue())  # Pass bytes for DOCX
        elif blob_name.endswith('.txt'):
            return extract_text_from_txt(file_stream.getvalue())  # Pass bytes for TXT
        else:
            raise ValueError("Unsupported file type.")
    
    except Exception as e:
        raise ValueError(f"Error processing file from GCS: {str(e)}")