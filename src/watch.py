import time
import os
from pathlib import Path
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

DOWNLOADS_PATH = "/home/munzir/Downloads"


class DownloadDetector(FileSystemEventHandler):
    def __init__(self):
        self.open_files = {}

    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return

        if self._is_temp_file(event.src_path):
            return

        print(f"New file detected: {event.src_path}")
        self.open_files[event.src_path] = time.time()

    def on_closed(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return

        # Check if this was a file we were tracking
        if event.src_path in self.open_files:
            # File has been closed after writing - download completed
            del self.open_files[event.src_path]

            # Verify the file actually exists and has content
            if os.path.exists(event.src_path) and os.path.getsize(event.src_path) > 0:
                self._handle_completed_download(event.src_path)

    def _is_temp_file(self, filepath: str) -> bool:
        """Filter out temporary browser download files"""
        temp_extensions = {'.crdownload', '.part', '.tmp', '.download'}
        return any(filepath.endswith(ext) for ext in temp_extensions)

    def _handle_completed_download(self, filepath: str) -> None:
        """Called when a download is confirmed complete"""
        filename = os.path.basename(filepath)
        file_ext = Path(filepath).suffix.lower()
        file_size = os.path.getsize(filepath)

        print("\nDownload complete!")
        print(f"   File: {filename}")
        print(f"   Path: {filepath}")
        print(f"   Type: {file_ext}")
        print(f"   Size: {file_size:,} bytes")
        print("-" * 50)

    def cleanup_stale_tracking(self, timeout=300):
        """Remove files from tracking if they've been open too long (likely stalled)"""
        current_time = time.time()
        stale_files = [
            path for path, open_time in self.open_files.items()
            if current_time - open_time > timeout
        ]
        for path in stale_files:
            print(f"Removing stale tracking for: {path}")
            del self.open_files[path]


def main():
    event_handler = DownloadDetector()
    observer = Observer()
    observer.schedule(event_handler, DOWNLOADS_PATH, recursive=False)
    observer.start()

    print(f"Watching downloads folder: {DOWNLOADS_PATH}")

    try:
        while True:
            time.sleep(1)
            event_handler.cleanup_stale_tracking()
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()
