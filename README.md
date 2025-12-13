# Declutter

A Python application that monitors your downloads folder and automatically processes images and PDFs using AI analysis.

## Features

- **File Monitoring**: Automatically detects new downloads in your specified folder
- **Image Analysis**: Uses AI vision models to describe and analyze images
- **PDF Processing**: Extracts text and metadata from PDFs for AI analysis
- **AI Integration**: Leverages Ollama with the qwen3-vl:2b model for intelligent analysis

## Architecture

The application is organized into modular components:

- **[`src/utils.py`](src/utils.py)**: Core utilities for file processing
- **[`src/file_detector.py`](src/file_detector.py)**: File system monitoring and download detection
- **[`src/ai_processor.py`](src/ai_processor.py)**: AI processing for both images and PDFs
- **[`src/file_info.py`](src/file_info.py)**: File information display and formatting
- **[`src/main.py`](src/main.py)**: Automated file monitoring with AI processing

## Installation

1. Clone this repository
2. Install dependencies using [uv](https://docs.astral.sh/uv/getting-started/installation/):
   ```bash
   uv sync
   ```
3. Copy the example environment file and configure it:
   ```bash
   cp .env_example .env
   ```

## Configuration

Edit the `.env` file with your settings:

```env
# Path to your downloads folder (use absolute path)
DOWNLOADS_PATH=/home/username/Downloads

# Ollama inference host URL
INFERENCE_HOST=http://localhost:11434
```

## Usage

### Auto-Process with AI

Monitor your downloads folder and automatically process new images and PDFs with AI:

```bash
# Full automated processing with AI analysis
uv run python src/main.py
```

## PDF Support

The application supports PDF processing with the following features:

- **Text Extraction**: Extracts text content from PDF files using PyMuPDF
- **Metadata Extraction**: Retrieves PDF metadata including title, author, and page count
- **AI Analysis**: Summarizes PDF content using the AI model

## AI Model

This application uses the `qwen3-vl:2b` model from Ollama, which supports both:
- Vision capabilities for image analysis
- Text processing for PDF content analysis

Make sure you have this model installed in your Ollama instance:

```bash
ollama pull qwen3-vl:2b
```

## File Type Support

### Images
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)

### Documents
- PDF (.pdf)
