# ReadVision

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced OCR PDF processor using Google Cloud Vision API with comprehensive Arabic/RTL text support.

## Features

✅ **Page-by-Page Mapping**: Each PDF page maps to one Word document page
✅ **Arabic/RTL Support**: Full right-to-left text direction support
✅ **Multiple Output Formats**: Generate both text and Word documents
✅ **Smart Processing**: Automatic handling of small vs. large PDFs
✅ **AI-Powered Translation**: Translate documents using Google Translate or Gemini AI
✅ **Standalone Text Translation**: Translate `.txt` files directly without OCR
✅ **YouTube Transcription**: Transcribe and summarize YouTube videos with detailed quotes
✅ **Command Line Interface**: Easy-to-use CLI with comprehensive options
✅ **Batch Processing**: Efficient handling of large documents using Google Cloud Storage
✅ **Text Cleaning**: Advanced OCR text cleaning and formatting
✅ **Debug Mode**: Detailed debugging for page ordering issues

## Installation

### From PyPI (when published)
```bash
pip install readvision
```

### From Source
```bash
git clone https://github.com/yourusername/readvision.git
cd readvision
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/yourusername/readvision.git
cd readvision
pip install -e ".[dev]"
pre-commit install
```

## Project Structure

```
readvision/
├── src/readvision/       # Source code
│   ├── core/            # PDF OCR processing
│   ├── utils/           # Translation, YouTube, document creation
│   ├── cli/             # Command-line interfaces
│   └── ui/              # Streamlit interface
├── docs/                # Documentation
│   ├── guides/          # User guides and tutorials
│   └── INDEX.md         # Documentation index
├── examples/            # Example outputs and use cases
│   └── outputs/         # Sample processed files
├── outputs/             # Default output directory (gitignored)
│   ├── youtube/         # YouTube transcriptions
│   ├── ocr/             # PDF OCR results
│   └── translations/    # Translation outputs
└── tests/               # Test suite
```

📚 **Full Documentation**: See [docs/INDEX.md](docs/INDEX.md) for complete documentation index.

## Quick Start

1. **Set up Google Cloud credentials:**
   ```bash
   # Download your service account key from Google Cloud Console
   # Save it as gcp.json in your project directory
   ```

2. **Set up Gemini API (Optional - for AI-powered translation):**
   ```bash
   # Create a .env file in your project directory
   echo "GEMINI_API_KEY=your_api_key_here" > .env

   # Get your API key from:
   # - Google AI Studio: https://makersuite.google.com/app/apikey (Free tier available)
   # - OR use Vertex AI with your Google Cloud project
   ```

3. **Basic usage:**
   ```bash
   readvision document.pdf output.txt
   ```

4. **With custom settings:**
   ```bash
   readvision arabic_doc.pdf output.txt --text-direction rtl --language-hint ar
   ```

## Usage

### Command Line Interface

```bash
readvision <pdf_file> <output_file> [options]
```

### Options

- `--credentials, -c`: Path to Google Cloud credentials JSON file (default: gcp.json)
- `--bucket, -b`: Google Cloud Storage bucket name for large files
- `--text-direction, -d`: Text direction (`ltr` or `rtl`, default: `rtl`)
- `--encoding, -e`: Text file encoding (default: `utf-8`)
- `--language-hint`: OCR language hint (default: `ar` for Arabic)
- `--chars-per-page`: Characters per page for text splitting (default: 3000)
- `--translate-to`: Target language code for translation (e.g., `en`, `es`, `fr`)
- `--translate-from`: Source language code for translation (optional, auto-detect if not specified)
- `--use-gemini`: Use Gemini API for translation instead of Google Translate
- `--gemini-api-key`: Gemini API key (optional, uses `GEMINI_API_KEY` env var if not provided)
- `--translation-instructions`: Additional instructions for Gemini translation (e.g., "Use formal tone", "Keep technical terms in original language")
- `--debug`: Enable debug output for page ordering
- `--help`: Show help message

### Examples

```bash
# Arabic document (default settings)
readvision assets/arabic.pdf output.txt

# English document
readvision assets/english.pdf output.txt --text-direction ltr --language-hint en

# With custom credentials and bucket
readvision document.pdf output.txt --credentials my_gcp.json --bucket my-bucket

# Translate Arabic to English using Google Translate
readvision assets/arabic.pdf output.txt --translate-to en --translate-from ar

# Translate using Gemini AI (more natural translation)
readvision assets/arabic.pdf output.txt --translate-to en --use-gemini

# Translate with custom Gemini API key
readvision assets/arabic.pdf output.txt --translate-to en --use-gemini --gemini-api-key YOUR_API_KEY

# Translate with custom instructions (formal tone)
readvision assets/arabic.pdf output.txt --translate-to en --use-gemini --translation-instructions "Use formal tone and preserve technical terminology"

# Translate keeping proper nouns in original language
readvision document.pdf output.txt --translate-to en --use-gemini --translation-instructions "Keep all proper nouns and place names in their original language"

# Debug mode for troubleshooting
readvision document.pdf output.txt --debug
```

### Standalone Text Translation

Translate `.txt` files directly without OCR:

```bash
# Basic translation with Gemini
readvision-translate input.txt output.txt --to en --use-gemini

# Translate with custom instructions
readvision-translate arabic.txt english.txt --to en --from ar --use-gemini --instructions "Use formal tone"

# Using Google Translate
readvision-translate input.txt output.txt --to es --credentials gcp.json

# Multiple instructions
readvision-translate legal.txt translated.txt --to en --use-gemini --instructions "Legal document: preserve terminology and formal language"
```

**Output Files:**
- `output.txt` - Translated text with page break markers
- `output.docx` - Word document with page-by-page mapping

**Command:** `readvision-translate`

**Options:**
- `--to`: Target language code (required)
- `--from`: Source language code (optional, auto-detect)
- `--use-gemini`: Use Gemini AI instead of Google Translate
- `--gemini-api-key`: Gemini API key
- `--instructions`: Translation instructions for Gemini
- `--credentials, -c`: Google Cloud credentials for Google Translate
- `--encoding, -e`: Text file encoding (default: utf-8)

**Note:** If your input file contains page markers (`--- PAGE BREAK ---` or form feed `\f`), each page will be translated separately and mapped to individual pages in the Word document.

### YouTube Video Transcription

Transcribe and summarize YouTube videos with detailed markdown output including original quotes:

```bash
# Basic usage (auto-generates output filename)
readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID"

# Specify output file
readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID" --output summary.md

# Keep the audio file
readvision-youtube "https://youtu.be/VIDEO_ID" --output summary.md --keep-audio

# Save audio to specific directory
readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID" --audio-dir ./audio --keep-audio

# Use custom Gemini API key
readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID" --gemini-api-key YOUR_KEY
```

**Output Files:**
- `[name]_summary.md` - Detailed summary with extensive quotes in Markdown format
- `[name]_transcript.txt` - Full verbatim audio transcript

**Command:** `readvision-youtube`

**Options:**
- `youtube_url`: YouTube video URL (required)
- `--output, -o`: Output summary file path (auto-generated if not specified)
- `--keep-audio`: Keep downloaded audio file (deleted by default)
- `--audio-dir`: Directory to save audio (temp directory if not specified)
- `--gemini-api-key`: Gemini API key (uses `GEMINI_API_KEY` env var if not provided)

**Features:**
- Automatic audio extraction from YouTube videos
- High-quality transcription using Gemini 1.5 Pro
- Detailed summaries with extensive direct quotes
- Organized markdown output with sections and headers
- Original speaker language and terminology preserved

## Python API

```python
from readvision import PDFOCRProcessor

# Initialize processor
processor = PDFOCRProcessor(credentials_path="gcp.json")

# Process PDF
processor.process_pdf(
    pdf_path="document.pdf",
    output_path="output.txt",
    text_direction="rtl",
    language_hint="ar"
)
```

## Requirements

- Python 3.8+
- Google Cloud Vision API credentials (required for OCR)
- Google Cloud Storage (for large PDFs >5 pages)
- Gemini API key (optional, for AI-powered translation and YouTube transcription)
  - Get free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
  - OR use Vertex AI with your Google Cloud project
- FFmpeg (required for YouTube audio extraction)
  - macOS: `brew install ffmpeg`
  - Ubuntu/Debian: `sudo apt-get install ffmpeg`
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## File Size Handling

- **Small PDFs (≤5 pages)**: Fast synchronous processing
- **Large PDFs (>5 pages)**: Batch processing with Cloud Storage

## Output Files

The tool generates two output files:
- `output.txt`: Text file with page separators
- `output.docx`: Word document with 1:1 page mapping and proper formatting

## Development

### Setup Development Environment

```bash
git clone https://github.com/yourusername/readvision.git
cd readvision
pip install -e ".[dev]"
pre-commit install
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint
flake8 src/ tests/
mypy src/

# Run all checks
pre-commit run --all-files
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📚 [Documentation](docs/)
- 🐛 [Report Issues](https://github.com/yourusername/readvision/issues)
- 💬 [Discussions](https://github.com/yourusername/readvision/discussions)