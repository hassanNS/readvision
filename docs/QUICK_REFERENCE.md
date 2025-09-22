# ReadVision OCR PDF Processor - Quick Reference

## 🚀 Installation & Setup

### Windows Setup

#### 1. Download Python
1. Download Python from [python.org](https://www.python.org/downloads/windows/)
2. Install Python (make sure to check "Add Python to PATH" during installation)

#### 2. Download This Project
```cmd
# Option 1: Clone with Git
git clone <repository-url>
cd readvision

# Option 2: Download ZIP
# Download ZIP file and extract to a folder like C:\readvision
```

#### 3. Install ReadVision
Open Command Prompt or PowerShell and navigate to the project folder:
```cmd
cd C:\readvision
pip install -e .
```

#### 4. Set Up Google Cloud Credentials
1. Get your Google Cloud Vision API credentials file (`gcp.json`)
2. Place it in the project folder: `C:\readvision\gcp.json`

### macOS/Linux Setup

#### 1. Download Python
```bash
# macOS with Homebrew
brew install python

# Or download from python.org
```

#### 2. Download This Project
```bash
# Clone with Git
git clone <repository-url>
cd readvision
```

#### 3. Install ReadVision
```bash
pip install -e .
```

#### 4. Set Up Google Cloud Credentials
1. Get your Google Cloud Vision API credentials file (`gcp.json`)
2. Place it in the project folder: `./gcp.json`

## 🎯 Usage

### Option 1: Web UI (Recommended for Beginners)
```bash
readvision-ui
```
This opens a user-friendly web interface in your browser where you can:
- Upload PDF files by drag & drop
- Configure all settings with dropdowns and checkboxes
- See real-time progress
- Download results directly

### Option 2: Command Line
```bash
readvision <pdf_file> <output_file> [options]
```

### Windows Examples

#### Web UI
```cmd
# Launch the web interface
readvision-ui
```

#### Command Line
```cmd
# Basic usage
readvision assets\document.pdf output.txt

# With full Windows paths
readvision "C:\Users\YourName\Documents\document.pdf" "C:\Users\YourName\Documents\output.txt"

# With custom credentials file
readvision assets\document.pdf output.txt --credentials "C:\path\to\your\gcp.json"

# For Arabic documents (default)
readvision assets\arabic_doc.pdf output.txt --text-direction rtl --language-hint ar

# For English documents
readvision assets\english_doc.pdf output.txt --text-direction ltr --language-hint en

# Debug mode
readvision assets\document.pdf output.txt --debug
```

### macOS/Linux Examples

#### Web UI
```bash
# Launch the web interface
readvision-ui
```

#### Command Line
```bash
# Basic usage
readvision assets/document.pdf output.txt

# With custom credentials file
readvision assets/document.pdf output.txt --credentials my_gcp.json

# Use custom GCS bucket for large files
readvision assets/document.pdf output.txt --bucket my-bucket

# Arabic document with RTL text direction (default)
readvision assets/arabic.pdf output.txt --text-direction rtl --encoding utf-8

# English document with LTR text direction
readvision assets/english.pdf output.txt --text-direction ltr --language-hint en

# Custom encoding (for special character sets)
readvision assets/document.pdf output.txt --encoding utf-16

# Debug page ordering issues
readvision assets/document.pdf output.txt --debug

# Show help
readvision --help
```

## 📱 Platform-Specific Notes

### Windows
- Use backslashes (`\`) or forward slashes (`/`) in file paths
- Enclose paths with spaces in quotes: `"C:\My Documents\file.pdf"`
- Both `.txt` and `.docx` files will be created automatically
- For large PDFs, ensure you have Google Cloud Storage bucket access

### macOS/Linux
- Use forward slashes (`/`) in file paths
- Enclose paths with spaces in quotes: `"/Users/name/My Documents/file.pdf"`
- Both `.txt` and `.docx` files will be created automatically

## 🛠️ Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--credentials` | `-c` | GCP credentials file | `gcp.json` |
| `--bucket` | `-b` | Custom GCS bucket name | Auto-generated |
| `--text-direction` | `-d` | Text direction (`ltr` or `rtl`) | `rtl` |
| `--encoding` | `-e` | File encoding | `utf-8` |
| `--language-hint` | | OCR language hint | `ar` |
| `--chars-per-page` | | Characters per page for text splitting | `3000` |
| `--debug` | | Enable debug output for page ordering | `False` |
| `--help` | `-h` | Show help message | |
| `--version` | | Show version | |

## ✨ Key Features

✅ **Page-by-Page Mapping**: Each PDF page maps to one Word document page
✅ **Arabic/RTL Support**: Full right-to-left text direction support
✅ **Cross-Platform**: Works on Windows, macOS, and Linux
✅ **Smart Processing**: Automatic handling of small vs. large PDFs
✅ **Multiple Output Formats**: Generate both text and Word documents
✅ **Batch Processing**: Efficient handling of large documents using Google Cloud Storage
✅ **Text Cleaning**: Advanced OCR text cleaning and formatting
✅ **Debug Mode**: Detailed debugging for page ordering issues

## 📄 Output Files

- `output.txt` - Text file with page separators (uses specified encoding)
- `output.docx` - Word document with 1:1 page mapping and proper text direction

## 🔧 Advanced Features

### Arabic/RTL Text Support
🔥 **Text Direction**: `--text-direction rtl` (default) or `ltr`
🔥 **Encoding Support**: `--encoding utf-8` (default) for Arabic characters
🔥 **Language Hints**: `--language-hint ar` (default) for better Arabic OCR
🔥 **RTL Word Documents**: Automatic right-to-left formatting in Word docs
🔥 **Arabic Fonts**: Uses "Arial Unicode MS" for better Arabic rendering

### File Size Handling
- **Small PDFs (≤5 pages)**: Fast synchronous processing
- **Large PDFs (>5 pages)**: Batch processing with Cloud Storage

## 📚 Python API Usage

You can also use ReadVision as a Python library:

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

## 🚨 Requirements

- Python 3.8+
- Google Cloud Vision API credentials (`gcp.json`)
- Google Cloud Storage (for large PDFs >5 pages)

## 🆘 Troubleshooting

### Common Issues

**Command not found: `readvision`**
```bash
# Make sure you installed the package
pip install -e .

# Check if it's in your PATH
which readvision  # macOS/Linux
where readvision  # Windows
```

**Credentials file not found**
```bash
# Make sure gcp.json exists in your project directory
ls gcp.json  # macOS/Linux
dir gcp.json  # Windows
```

**Permission errors on Windows**
- Run Command Prompt as Administrator
- Make sure Python is added to PATH

## 📈 Exit Codes

- `0` - Success
- `1` - Error (file not found, processing failed, etc.)

## 💡 Tips

- Use `--debug` flag to troubleshoot page ordering issues
- For large documents, consider using a custom GCS bucket with `--bucket`
- Arabic text works best with `--text-direction rtl --language-hint ar`
- English text works best with `--text-direction ltr --language-hint en`