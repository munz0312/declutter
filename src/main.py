import utils
from file_info import display_pdf_info
from ai_processor import AIProcessor
from file_detector import FileDetector
import time
import os
import sys
from dotenv import load_dotenv
from watchdog.observers import Observer

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()
DOWNLOADS_PATH = os.getenv("DOWNLOADS_PATH")
INFERENCE_HOST = os.getenv("INFERENCE_HOST")


def create_ai_callback(ai_processor):
    """Create a callback function that processes files with AI"""
    def callback(file_info):
        file_path = file_info['path']

        # Display additional info for PDFs
        if utils.is_pdf(file_path):
            display_pdf_info(file_path)

        # Process with AI if it's an image or PDF
        if utils.is_image(file_path) or utils.is_pdf(file_path):
            print(f"\nProcessing {file_info['extension']} file with AI...")
            try:
                result = ai_processor.process_file(file_path)
                print("\nAI Analysis Result:")
                print(result)
                print("=" * 50)
            except Exception as e:
                print(f"Error processing file with AI: {str(e)}")

    return callback


def main():
    if not DOWNLOADS_PATH:
        print("Error: DOWNLOADS_PATH not set in environment variables")
        return

    if not INFERENCE_HOST:
        print("Error: INFERENCE_HOST not set in environment variables")
        return

    # Initialize components
    file_detector = FileDetector()
    ai_processor = AIProcessor(INFERENCE_HOST)

    # Set up callback for AI processing
    ai_callback = create_ai_callback(ai_processor)
    file_detector.add_callback(ai_callback)

    # Set up file system observer
    observer = Observer()
    observer.schedule(file_detector, DOWNLOADS_PATH, recursive=False)
    observer.start()

    print(f"Auto-processor watching downloads folder: {DOWNLOADS_PATH}")
    print(f"Using AI inference host: {INFERENCE_HOST}")
    print("Press Ctrl+C to stop...")

    try:
        while True:
            time.sleep(1)
            file_detector.cleanup_stale_tracking()
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()
