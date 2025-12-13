import utils
import time
import os
import sys
from pathlib import Path
from watchdog.events import FileSystemEvent, FileSystemEventHandler

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class FileDetector(FileSystemEventHandler):
    """Base class for detecting file system events"""

    def __init__(self):
        self.open_files = {}
        self.callbacks = []
        self.processed_hashes = set()  # Track hashes of processed files
        self.pending_moves = {}  # Track files that might be renamed

    def add_callback(self, callback):
        """Add a callback function to be called when a file is processed"""
        self.callbacks.append(callback)

    def on_created(self, event: FileSystemEvent) -> None:
        """Called when a file or directory is created"""
        if event.is_directory:
            return

        if self._is_temp_file(event.src_path):
            return

        print(f"New file detected: {event.src_path}")
        self.open_files[event.src_path] = time.time()

        # Check if this might be a renamed file by checking if we have a pending move
        # with similar size and recent timestamp
        self._check_for_potential_rename(event.src_path)

    def on_moved(self, event: FileSystemEvent) -> None:
        """Called when a file is moved or renamed"""
        if event.is_directory:
            return

        # Filter out temporary files
        if self._is_temp_file(event.dest_path):
            return
        print(f"File moved/renamed: {event.src_path} -> {event.dest_path}")

        # If the source file was being tracked, remove it from tracking
        if event.src_path in self.open_files:
            del self.open_files[event.src_path]

        # Check if this is a file we should process
        if os.path.exists(event.dest_path) and os.path.getsize(event.dest_path) > 0:
            # Check if we've already processed this content
            try:
                file_hash = utils.get_file_hash(event.dest_path)
                if file_hash in self.processed_hashes:
                    print(f"""Skipping already processed content: {
                          event.dest_path}""")
                    return

                # Add to pending moves for potential duplicate detection
                self.pending_moves[event.dest_path] = {
                    'hash': file_hash,
                    'timestamp': time.time()
                }

                # Process the renamed file
                self._handle_completed_download(event.dest_path)
            except Exception as e:
                print(f"Error handling moved file: {str(e)}")

    def on_closed(self, event: FileSystemEvent) -> None:
        """Called when a file is closed"""
        if event.is_directory:
            return

        # Check if this was a file we were tracking
        if event.src_path in self.open_files:
            # File has been closed after writing - download completed
            del self.open_files[event.src_path]

            # Verify the file actually exists and has content
            if os.path.exists(event.src_path) and os.path.getsize(event.src_path) > 0:
                # Check if we've already processed this content
                try:
                    file_hash = utils.get_file_hash(event.src_path)
                    if file_hash in self.processed_hashes:
                        print(f"""Skipping already processed content: {
                              event.src_path}""")
                        return

                    # Add to pending moves for potential duplicate detection
                    self.pending_moves[event.src_path] = {
                        'hash': file_hash,
                        'timestamp': time.time()
                    }

                    self._handle_completed_download(event.src_path)
                except Exception as e:
                    print(f"Error calculating file hash: {str(e)}")
                    # Still process the file even if hashing fails
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

        # Calculate and store file hash to prevent duplicate processing
        try:
            file_hash = utils.get_file_hash(filepath)
            self.processed_hashes.add(file_hash)
            print(f"   Hash: {file_hash}")
        except Exception as e:
            print(f"   Warning: Could not calculate file hash - {str(e)}")

        # Call all registered callbacks with the file info
        file_info = {
            'path': filepath,
            'name': filename,
            'extension': file_ext,
            'size': file_size
        }

        for callback in self.callbacks:
            try:
                callback(file_info)
            except Exception as e:
                print(f"   Error in callback: {str(e)}")

        print("-" * 50)

    def cleanup_stale_tracking(self, timeout=300):
        """Remove files from tracking if they've been open too long"""
        current_time = time.time()

        # Clean up stale open files
        stale_files = [
            path for path, open_time in self.open_files.items()
            if current_time - open_time > timeout
        ]
        for path in stale_files:
            print(f"Removing stale tracking for: {path}")
            del self.open_files[path]

        # Clean up old pending moves (older than 5 minutes)
        stale_moves = [
            path for path, move_info in self.pending_moves.items()
            if current_time - move_info['timestamp'] > 300
        ]
        for path in stale_moves:
            del self.pending_moves[path]

        # Clean up old processed hashes (keep only last 1000 to prevent memory issues)
        if len(self.processed_hashes) > 1000:
            # Convert to list and keep only the most recent 1000
            hash_list = list(self.processed_hashes)
            self.processed_hashes = set(hash_list[-1000:])

    def _check_for_potential_rename(self, filepath: str) -> None:
        """Check if a new file might be a renamed version of an existing file"""
        try:
            if not os.path.exists(filepath):
                return

            current_time = time.time()
            current_hash = utils.get_file_hash(filepath)

            # Check if this file matches any recently processed file
            for pending_path, pending_info in self.pending_moves.items():
                # Skip if it's the same file
                if pending_path == filepath:
                    continue

                # Check if the hash matches (same content)
                if pending_info['hash'] == current_hash:
                    # Check if the pending file was processed recently (within 30 seconds)
                    if current_time - pending_info['timestamp'] < 30:
                        print(f"""Detected potential rename: {
                              pending_path} -> {filepath}""")
                        # Mark this as already processed by adding its hash
                        self.processed_hashes.add(current_hash)
                        return
        except Exception as e:
            # Don't let errors in rename detection break normal processing
            pass
