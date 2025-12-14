from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import os
import shutil
from pathlib import Path
import utils


class FileOrganizerAgent:
    """Agent that analyzes file content and organizes files into appropriate directories"""

    def __init__(self, inference_host, organization_base_dir):
        self.client = ChatOllama(model="qwen3-vl:2b", base_url=inference_host)
        self.organization_base_dir = Path(organization_base_dir)
        self._ensure_base_directory_exists()
        self._setup_categories()

    def _ensure_base_directory_exists(self):
        """Ensure the base organization directory exists"""
        if not self.organization_base_dir.exists():
            self.organization_base_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created organization base directory: {
                  self.organization_base_dir}")

    def _setup_categories(self):
        """Define hard-coded categories and their keywords"""
        self.categories = {
            "documents": [
                "document",
                "text",
                "pdf",
                "report",
                "paper",
                "article",
                "manual",
                "guide",
                "ebook",
                "book",
            ],
            "images": [
                "photo",
                "picture",
                "image",
                "photograph",
                "screenshot",
                "graphic",
                "visual",
            ],
            "invoices": ["invoice", "bill", "receipt", "payment", "statement"],
            "presentations": ["presentation", "slide", "powerpoint", "ppt"],
            "spreadsheets": ["spreadsheet", "excel", "csv", "data", "table"],
            "misc": ["unknown", "other", "miscellaneous", "misc"],
        }

        # Create category directories if they don't exist
        for category in self.categories:
            category_dir = self.organization_base_dir / category
            if not category_dir.exists():
                category_dir.mkdir(exist_ok=True)
                print(f"Created category directory: {category_dir}")

    def determine_category(self, file_description):
        """Determine the appropriate category based on file description"""
        # Convert description to lowercase for case-insensitive matching
        description_lower = file_description.lower()

        # Check each category for matching keywords
        for category, keywords in self.categories.items():
            if category == "misc":
                continue  # Skip misc for now, use as fallback

            for keyword in keywords:
                if keyword in description_lower:
                    return category

        # If no match found, return misc
        return "misc"

    def organize_file(self, file_path, file_description):
        """Organize a file into the appropriate category directory"""
        try:
            # Determine the category
            category = self.determine_category(file_description)

            # Get the target directory
            target_dir = self.organization_base_dir / category

            # Get the filename
            filename = Path(file_path).name

            # Check if file already exists in target directory
            target_path = target_dir / filename
            if target_path.exists():
                # File exists, move to misc folder instead
                misc_dir = self.organization_base_dir / "misc"
                target_path = misc_dir / filename
                print(
                    f"File {filename} already exists in {
                        category} directory. Moving to misc folder."
                )

            # Move the file
            shutil.move(file_path, target_path)

            print(f"✅ Organized {filename} to {category} folder")
            return {
                "status": "success",
                "original_path": file_path,
                "new_path": str(target_path),
                "category": category,
                "message": f"File moved to {category} directory",
            }

        except Exception as e:
            error_msg = f"❌ Failed to organize {file_path}: {str(e)}"
            print(error_msg)
            return {"status": "error", "original_path": file_path, "message": error_msg}

    def get_category_description(self, category):
        """Get a description of what each category contains"""
        descriptions = {
            "documents": "Text documents, reports, articles, PDFs, books",
            "images": "Photos, pictures, screenshots, graphics",
            "invoices": "Invoices, bills, receipts, payment statements",
            "presentations": "Presentations, slides, PowerPoint files",
            "spreadsheets": "Spreadsheets, Excel files, CSV data, tables",
            "misc": "Files that don't fit other categories",
        }
        return descriptions.get(category, "Unknown category")
