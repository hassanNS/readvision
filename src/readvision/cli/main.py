#!/usr/bin/env python3
"""Command line interface for ReadVision OCR PDF processor."""

import os
import sys
import argparse
from pathlib import Path

from ..core.processor import PDFOCRProcessor


def main():
    """Main function with command line argument support"""

    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description='OCR PDF processor that creates Word documents with page-by-page mapping',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  readvision assets/document.pdf output.txt
  readvision assets/document.pdf output.txt --credentials gcp.json
  readvision assets/document.pdf output.txt --bucket my-bucket
  readvision assets/arabic.pdf output.txt --text-direction rtl --encoding utf-8
  readvision assets/english.pdf output.txt --text-direction ltr --language-hint en
        '''
    )

    parser.add_argument('pdf_path',
                       help='Path to the input PDF file')
    parser.add_argument('output_path',
                       help='Path for the output text file (Word doc will be created automatically)')
    parser.add_argument('--credentials', '-c',
                       default='gcp.json',
                       help='Path to Google Cloud credentials JSON file (default: gcp.json)')
    parser.add_argument('--bucket', '-b',
                       help='Google Cloud Storage bucket name for temporary storage (optional)')
    parser.add_argument('--chars-per-page',
                       type=int,
                       default=3000,
                       help='Characters per page for legacy text-based splitting (default: 3000)')
    parser.add_argument('--text-direction', '-d',
                       choices=['ltr', 'rtl'],
                       default='rtl',
                       help='Text direction: ltr (left-to-right) or rtl (right-to-left) (default: rtl for Arabic)')
    parser.add_argument('--encoding', '-e',
                       default='utf-8',
                       help='Text file encoding (default: utf-8 for Arabic support)')
    parser.add_argument('--language-hint',
                       default='ar',
                       help='Language hint for OCR processing (default: ar for Arabic)')
    parser.add_argument('--debug',
                       action='store_true',
                       help='Enable debug output for page ordering')
    parser.add_argument('--version',
                       action='version',
                       version='%(prog)s 1.0.0')

    args = parser.parse_args()

    # Validate input file exists
    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file not found: {args.pdf_path}")
        sys.exit(1)

    # Validate credentials file exists
    if not os.path.exists(args.credentials):
        print(f"Error: Credentials file not found: {args.credentials}")
        sys.exit(1)

    # Configuration from command line arguments
    CREDENTIALS_PATH = args.credentials
    BUCKET_NAME = args.bucket
    PDF_PATH = args.pdf_path
    OUTPUT_PATH = args.output_path
    CHARS_PER_PAGE = args.chars_per_page
    TEXT_DIRECTION = args.text_direction
    ENCODING = args.encoding
    LANGUAGE_HINT = args.language_hint
    DEBUG = args.debug

    print(f"Processing PDF: {PDF_PATH}")
    print(f"Output will be saved to: {OUTPUT_PATH}")
    print(f"Word document will be saved to: {OUTPUT_PATH.replace('.txt', '.docx')}")
    print(f"Text direction: {TEXT_DIRECTION.upper()}")
    print(f"Encoding: {ENCODING}")
    print(f"Language hint: {LANGUAGE_HINT}")
    if DEBUG:
        print(f"🔍 Debug mode: ENABLED")

    # Initialize processor
    processor = PDFOCRProcessor(
        credentials_path=CREDENTIALS_PATH,
        bucket_name=BUCKET_NAME
    )

    try:
        # Process PDF
        processor.process_pdf(
            PDF_PATH,
            OUTPUT_PATH,
            chars_per_page=CHARS_PER_PAGE,
            text_direction=TEXT_DIRECTION,
            encoding=ENCODING,
            language_hint=LANGUAGE_HINT,
            debug=DEBUG
        )

        # Read and display sample of output
        with open(OUTPUT_PATH, 'r', encoding=ENCODING) as f:
            sample = f.read(500)
            print("\nSample of extracted text:")
            print("-" * 50)
            print(sample)
            print("-" * 50)

        # Inform about Word document
        word_path = OUTPUT_PATH.replace('.txt', '.docx')
        print(f"\nWord document created: {word_path}")
        print("Each page of the PDF maps to a page in the Word document.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()