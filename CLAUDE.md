# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ReadVision is an OCR PDF processor using Google Cloud Vision API with comprehensive Arabic/RTL text support, optional translation capabilities, and YouTube video transcription. The tool processes PDFs, extracts text, creates both text files and Word documents with 1:1 page mapping, and can transcribe and summarize YouTube videos with detailed quotes.

## Core Architecture

### Processing Pipeline

The application has two main processing paths:

1. **Small PDFs (≤5 pages)**: Synchronous processing via `process_small_pdf()` in [processor.py](src/readvision/core/processor.py)
2. **Large PDFs (>5 pages)**: Asynchronous batch processing via `process_large_pdf()` using Google Cloud Storage

### Key Components

- **PDFOCRProcessor** ([src/readvision/core/processor.py](src/readvision/core/processor.py)): Main orchestrator that handles OCR, page ordering, and translation coordination
- **TextTranslator** ([src/readvision/utils/translator.py](src/readvision/utils/translator.py)): Supports both Google Translate and Gemini AI translation with custom instructions
- **YouTubeProcessor** ([src/readvision/utils/youtube_processor.py](src/readvision/utils/youtube_processor.py)): Handles YouTube video download, audio extraction, transcription, and summarization
- **DocumentCreator** ([src/readvision/utils/document_creator.py](src/readvision/utils/document_creator.py)): Generates Word documents with proper RTL/LTR formatting
- **TextCleaner** ([src/readvision/utils/text_cleaner.py](src/readvision/utils/text_cleaner.py)): OCR text cleaning and formatting

### CLI Entry Points

The project provides four CLI commands defined in [pyproject.toml](pyproject.toml):

- `readvision`: Main OCR processing ([src/readvision/cli/main.py](src/readvision/cli/main.py))
- `readvision-translate`: Standalone text translation ([src/readvision/cli/translate.py](src/readvision/cli/translate.py))
- `readvision-youtube`: YouTube video transcription and summarization ([src/readvision/cli/youtube.py](src/readvision/cli/youtube.py))
- `readvision-ui`: Streamlit UI ([src/readvision/ui/streamlit_app.py](src/readvision/ui/streamlit_app.py))

## Development Commands

### Environment Setup

```bash
# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Testing

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src/readvision

# Run specific test file
pytest tests/test_processor.py

# Run specific test
pytest tests/test_processor.py::test_function_name
```

### Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
flake8 src/ tests/
mypy src/

# Run all pre-commit checks
pre-commit run --all-files
```

## Important Implementation Details

### Page Ordering System

The processor maintains page order through `(page_number, text)` tuples. Pages are sorted by page number before creating output files. Debug mode (`--debug` flag) provides diagnostic information about page ordering, duplicates, and missing pages via the `debug_page_order()` method.

### Translation Architecture

Translation is handled in two ways:
1. **Google Translate**: Traditional translation service via Google Cloud Translation API
2. **Gemini AI**: Uses `gemini-3.1-flash-lite-preview` model with custom instruction support for more natural translations

The `_translate_with_gemini()` method constructs prompts that include custom instructions (e.g., "Use formal tone", "Keep technical terms in original language").

### Output Format

All processing generates two files:
- `.txt`: Text file with `--- PAGE BREAK ---` separators
- `.docx`: Word document with 1:1 page mapping, proper RTL/LTR support, and page headers

When translation is enabled, additional files are created with `_translated_{lang_code}` suffix.

### RTL Text Support

For Arabic and other RTL languages:
- Uses `Arial Unicode MS` font
- Applies bidirectional (bidi) XML properties to paragraphs
- Right-aligns text and headers
- Default language hint is `ar` (Arabic)

### YouTube Transcription Architecture

The YouTube feature uses a multi-stage pipeline:
1. **Audio Extraction**: Uses `yt-dlp` to download audio in MP3 format (best quality available)
2. **Transcription**: Uploads audio to Gemini 2.0 Flash for verbatim transcription
3. **Summarization**: Generates detailed markdown summary with extensive direct quotes from transcript

Key implementation details:
- Uses Gemini 2.0 Flash for fast and efficient audio transcription
- Automatically cleans up temporary audio files unless `--keep-audio` is specified
- Summary format includes sections, headers, blockquotes for direct quotes, and organized topics
- Both transcript (`.txt`) and summary (`.md`) are saved

## Configuration

### Required Credentials

- **Google Cloud Vision API**: `gcp.json` credentials file (required for OCR)
- **Google Cloud Storage**: Bucket for large PDFs >5 pages
- **Gemini API** (optional): Set `GEMINI_API_KEY` environment variable or use `.env` file

### Project Structure

```
src/readvision/
├── core/
│   └── processor.py          # Main OCR processing logic
├── utils/
│   ├── translator.py         # Translation utilities
│   ├── youtube_processor.py  # YouTube video processing
│   ├── document_creator.py   # Word document generation
│   └── text_cleaner.py       # Text cleaning utilities
├── cli/
│   ├── main.py              # Main CLI entry point
│   ├── translate.py         # Translation CLI
│   └── youtube.py           # YouTube transcription CLI
└── ui/
    ├── app.py               # UI launcher
    └── streamlit_app.py     # Streamlit interface
```

## Testing Strategy

Tests are located in `tests/` and use pytest. Key test files:
- `test_processor.py`: OCR processor functionality
- `test_text_cleaner.py`: Text cleaning utilities
- `test_cli.py`: CLI argument parsing and execution

## Python Version Support

Supports Python 3.8+ (excluding 3.9.7 due to compatibility issues). Type checking configured with mypy for strict type safety.
