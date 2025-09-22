# OCR to Word Document Feature

## Overview
The OCR processor creates Word documents (.docx) with 1:1 page mapping from PDF files, featuring **Arabic/RTL text support**. Each page in the original PDF corresponds to exactly one page in the Word document, with proper text direction formatting.

## Command Line Usage

### Basic Syntax
```bash
python translate.py <pdf_path> <output_path> [options]
```

### Required Arguments
- `pdf_path`: Path to the input PDF file
- `output_path`: Path for the output text file (Word doc created automatically)

### Arabic/RTL Options (🔥 NEW!)
- `--text-direction`, `-d`: Text direction (`rtl` or `ltr`, default: `rtl` for Arabic)
- `--encoding`, `-e`: File encoding (default: `utf-8` for Arabic support)
- `--language-hint`: OCR language hint (default: `ar` for Arabic)

### Other Optional Arguments
- `--credentials`, `-c`: Path to Google Cloud credentials JSON file (default: gcp.json)
- `--bucket`, `-b`: Google Cloud Storage bucket name for temporary storage
- `--chars-per-page`: Characters per page for legacy splitting (default: 3000)
- `--help`, `-h`: Show help message

### Examples

1. **Arabic document (default settings):**
```bash
python translate.py assets/arabic_book.pdf output.txt
# Uses RTL direction, UTF-8 encoding, Arabic language hint
```

2. **English document:**
```bash
python translate.py assets/english_doc.pdf output.txt --text-direction ltr --language-hint en
```

3. **Persian/Farsi document:**
```bash
python translate.py assets/persian.pdf output.txt --text-direction rtl --language-hint fa
```

4. **Custom encoding:**
```bash
python translate.py assets/document.pdf output.txt --encoding utf-16
```

5. **With custom credentials:**
```bash
python translate.py assets/document.pdf output.txt --credentials my_gcp.json
```

## Arabic/RTL Features 🔥

### Text Direction Support
- **RTL (Right-to-Left)**: Default for Arabic, Hebrew, Persian, Urdu
- **LTR (Left-to-Right)**: For English, French, Spanish, etc.
- **Word Document Formatting**: Automatic text alignment and direction

### Language Support
| Language | Code | Direction | Example |
|----------|------|-----------|---------|
| Arabic | `ar` | RTL | `--language-hint ar --text-direction rtl` |
| English | `en` | LTR | `--language-hint en --text-direction ltr` |
| Persian/Farsi | `fa` | RTL | `--language-hint fa --text-direction rtl` |
| Urdu | `ur` | RTL | `--language-hint ur --text-direction rtl` |
| Hebrew | `he` | RTL | `--language-hint he --text-direction rtl` |

### Encoding Options
- **UTF-8** (default): Best for Arabic and international text
- **UTF-16**: Alternative Unicode encoding
- **CP1256**: Windows Arabic encoding

### Word Document Features
- **Arabic Fonts**: Uses "Arial Unicode MS" for better Arabic rendering
- **RTL Formatting**: Proper right-to-left text alignment
- **Page Headers**: Positioned according to text direction
- **Paragraph Spacing**: Optimized for Arabic text readability

## Features

### Page-by-Page Mapping
- **1:1 correspondence**: Each PDF page = one Word document page
- **Maintains order**: Pages appear in the same sequence as the original PDF
- **Separate processing**: Each page's text is processed individually

### Output Files
For an input like `output.txt`, you'll get:
- `output.txt` - Plain text file with "--- PAGE BREAK ---" separators
- `output.docx` - Word document with actual page breaks

### Word Document Features
- **Title Page**: Shows source filename, total pages, and character count
- **Page Headers**: Each page has "Page X" in the top right
- **Paragraph Spacing**: Automatic spacing between paragraphs for readability
- **Progress Indicator**: Shows progress when processing large documents

## Processing Methods
- **Small PDFs (≤5 pages)**: Synchronous processing for faster results
- **Large PDFs (>5 pages)**: Asynchronous batch processing via Google Cloud Storage

## Requirements
- Python 3.7+
- python-docx library
- Google Cloud Vision API credentials
- Google Cloud Storage access (for large PDFs)

## Error Handling
The program validates:
- PDF file existence
- Credentials file existence
- Proper command line arguments

Exit codes:
- 0: Success
- 1: Error (file not found, processing error, etc.)

## Legacy Features
The `--chars-per-page` option is maintained for compatibility but not used in the new page-mapping approach.
