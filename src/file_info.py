import utils


def display_file_info(file_info):
    """Display basic information about any file"""
    print(f"   File: {file_info['name']}")
    print(f"   Path: {file_info['path']}")
    print(f"   Type: {file_info['extension']}")
    print(f"   Size: {file_info['size']:,} bytes")


def display_pdf_info(file_path):
    """Display additional information for PDF files"""
    if not utils.is_pdf(file_path):
        return

    try:
        metadata = utils.extract_metadata_from_pdf(file_path)
        print(f"   Pages: {metadata.get('page_count', 'Unknown')}")
        if metadata.get('title'):
            print(f"   Title: {metadata['title']}")
        if metadata.get('author'):
            print(f"   Author: {metadata['author']}")
    except Exception as e:
        print(f"   Warning: Could not extract PDF metadata - {str(e)}")
