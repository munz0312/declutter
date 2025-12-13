# Declutter

A Python application that monitors your downloads folder and automatically processes images and PDFs using AI analysis.

## Features

- **File Monitoring**: Automatically detects new downloads in your specified folder
- **Smart Rename Detection**: Intelligently handles file renames during download (e.g., Canvas platform behavior)
- **Duplicate Prevention**: Uses file hashing to prevent processing the same content multiple times
- **Image Analysis**: Uses AI vision models to describe and analyze images
- **PDF Processing**: Extracts text and metadata from PDFs for AI analysis
- **AI Integration**: Leverages Ollama with the qwen3-vl:2b model for intelligent analysis
- **Modular Architecture**: Clean separation of concerns with reusable components

## Architecture

The application is organized into modular components:

- **[`src/utils.py`](src/utils.py)**: Core utilities for file processing, MIME type detection, and PDF operations
- **[`src/file_detector.py`](src/file_detector.py)**: File system monitoring and download detection
- **[`src/ai_processor.py`](src/ai_processor.py)**: AI processing for both images and PDFs
- **[`src/file_info.py`](src/file_info.py)**: File information display and formatting
- **[`src/main.py`](src/main.py)**: Manual file processing script
- **[`src/watch.py`](src/watch.py)**: File monitoring without AI processing
- **[`src/auto_processor.py`](src/auto_processor.py)**: Automated file monitoring with AI processing

## Installation

1. Clone this repository
2. Install dependencies using uv:
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

### Manual File Processing

Process a specific file manually:

```bash
# Pass the file path as an argument
uv run python src/main.py /path/to/your/file.pdf
```

### Watch Downloads Folder

Monitor your downloads folder and display file information:

```bash
# Basic file monitoring (no AI processing)
uv run python src/watch.py
```

### Auto-Process with AI

Monitor your downloads folder and automatically process new images and PDFs with AI:

```bash
# Full automated processing with AI analysis
uv run python src/auto_processor.py
```

## PDF Support

The application supports PDF processing with the following features:

- **Text Extraction**: Extracts text content from PDF files using PyMuPDF
- **Metadata Extraction**: Retrieves PDF metadata including title, author, and page count
- **AI Analysis**: Summarizes PDF content using the AI model
- **Large PDF Handling**: Truncates text content to prevent context window issues


### PDF Processing Details

- Text is extracted page by page and combined for analysis
- PDFs with no extractable text are detected and reported
- Large PDFs (>4000 characters) are truncated to maintain performance
- PDF metadata is displayed when files are downloaded

## Dependencies

- `dotenv`: Environment variable management
- `langchain-ollama`: LangChain integration for Ollama
- `ollama`: Ollama client library
- `pillow`: Image processing
- `watchdog`: File system monitoring
- `pymupdf`: PDF processing and text extraction

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

## Testing

Run the test suite to verify functionality:

```bash
uv run python test_pdf.py
```

## Troubleshooting

### Common Issues

1. **File not found errors**: Ensure the paths in your `.env` file are correct and accessible
2. **AI processing errors**: Make sure Ollama is running and the qwen3-vl:2b model is installed
3. **PDF processing errors**: Some PDFs may be protected or contain no extractable text
4. **Module import errors**: Use `uv run` to ensure proper dependency management

### Debug Mode

For debugging, you can modify the scripts to add more verbose logging or check specific file paths.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

