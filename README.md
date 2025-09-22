# ReadVision

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced OCR PDF processor using Google Cloud Vision API with comprehensive Arabic/RTL text support.

## Features

✅ **Page-by-Page Mapping**: Each PDF page maps to one Word document page
✅ **Arabic/RTL Support**: Full right-to-left text direction support
✅ **Multiple Output Formats**: Generate both text and Word documents
✅ **Smart Processing**: Automatic handling of small vs. large PDFs
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
```

## Quick Start

1. **Set up Google Cloud credentials:**
   ```bash
   # Download your service account key from Google Cloud Console
   # Save it as gcp.json in your project directory
   ```

2. **Basic usage:**
   ```bash
   readvision document.pdf output.txt
   ```

3. **With custom settings:**
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

# Debug mode for troubleshooting
readvision document.pdf output.txt --debug
```

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
- Google Cloud Vision API credentials
- Google Cloud Storage (for large PDFs >5 pages)

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