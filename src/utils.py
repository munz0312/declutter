import base64
import hashlib
from pathlib import Path
import fitz


def encode_image(image_path):
    """Read and encode image to base64"""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_mime_type(file_path):
    """Get MIME type based on file extension"""
    ext = Path(file_path).suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.pdf': 'application/pdf'
    }
    return mime_types.get(ext, 'application/octet-stream')


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyMuPDF"""
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    try:
        doc = fitz.open(pdf_path)
        text = ""

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()

        doc.close()
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def extract_metadata_from_pdf(pdf_path):
    """Extract metadata from PDF using PyMuPDF"""
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    try:
        doc = fitz.open(pdf_path)
        metadata = doc.metadata
        metadata['page_count'] = len(doc)
        doc.close()
        return metadata
    except Exception as e:
        raise Exception(f"Error extracting metadata from PDF: {str(e)}")


def is_pdf(file_path):
    """Check if file is a PDF"""
    return Path(file_path).suffix.lower() == '.pdf'


def is_image(file_path):
    """Check if file is an image"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    return Path(file_path).suffix.lower() in image_extensions


def get_file_hash(file_path):
    """Calculate MD5 hash of a file for content identification"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    hash_md5 = hashlib.md5()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        raise Exception(f"Error calculating file hash: {str(e)}")
