import base64
from pathlib import Path


def encode_image(image_path):
    """Read and encode image to base64"""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_mime_type(image_path):
    """Get MIME type based on file extension"""
    ext = Path(image_path).suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    return mime_types.get(ext, 'image/jpeg')
