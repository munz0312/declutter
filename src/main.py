from file_detector import FileDetector
from file_organizer import FileOrganizerAgent
from ai_processor import AIProcessor
from file_info import display_pdf_info
import sys
import utils
import os
import time
from dotenv import load_dotenv
from watchdog.observers import Observer

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import modules


load_dotenv()
DOWNLOADS_PATH = os.getenv("DOWNLOADS_PATH")
INFERENCE_HOST = os.getenv("INFERENCE_HOST")
ORGANIZATION_BASE_DIR = os.getenv("ORGANIZATION_BASE_DIR")


def main():
    if not DOWNLOADS_PATH:
        print("Error: DOWNLOADS_PATH not set in environment variables")
        return

    if not INFERENCE_HOST:
        print("Error: INFERENCE_HOST not set in environment variables")
        return

    if not ORGANIZATION_BASE_DIR:
        print("Error: ORGANIZATION_BASE_DIR not set in environment variables")
        return

    # Initialize components
    file_detector = FileDetector()
    ai_processor = AIProcessor(INFERENCE_HOST)
    file_organizer = FileOrganizerAgent(INFERENCE_HOST, ORGANIZATION_BASE_DIR)

    # Set up callback for AI processing and organization
    def ai_and_organization_callback(file_info):
        file_path = file_info["path"]

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

                # Organize the file based on AI analysis
                print("\nOrganizing file based on AI analysis...")
                organization_result = file_organizer.organize_file(
                    file_path, result)
                if organization_result["status"] == "success":
                    print(
                        f"""✅ Successfully organized file to: {
                            organization_result['new_path']}"""
                    )
                else:
                    print(
                        f"""❌ Failed to organize file: {
                            organization_result['message']}"""
                    )

            except Exception as e:
                print(f"Error processing file with AI: {str(e)}")

    # Set up callback for AI processing
    file_detector.add_callback(ai_and_organization_callback)

    # Set up file system observer
    observer = Observer()
    observer.schedule(file_detector, DOWNLOADS_PATH, recursive=False)
    observer.start()

    print(f"Auto-processor watching downloads folder: {DOWNLOADS_PATH}")
    print(f"Using AI inference host: {INFERENCE_HOST}")
    print(f"Organizing files to: {ORGANIZATION_BASE_DIR}")
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
