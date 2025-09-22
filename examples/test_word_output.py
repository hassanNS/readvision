#!/usr/bin/env python3
"""
Test script to demonstrate Word document creation from OCR output
"""

from translate import PDFOCRProcessor
from pathlib import Path

def test_word_creation():
    """Test creating Word document from existing text file"""

    # Check if we have an existing output.txt file
    if Path("output.txt").exists():
        print("Found existing output.txt file")

        # Read the text
        with open("output.txt", 'r', encoding='utf-8') as f:
            text = f.read()

        print(f"Text length: {len(text):,} characters")

        # Create processor instance
        processor = PDFOCRProcessor(credentials_path="gcp.json")

        # Test with different page sizes
        test_configs = [
            (2000, "output_small_pages.docx"),
            (3000, "output_medium_pages.docx"),
            (5000, "output_large_pages.docx")
        ]

        for chars_per_page, filename in test_configs:
            print(f"\nCreating {filename} with ~{chars_per_page} chars per page...")
            processor.create_word_document(text, filename, chars_per_page)

            estimated_pages = (len(text) // chars_per_page) + 1
            print(f"Estimated pages: {estimated_pages}")

    else:
        print("No output.txt file found. Please run the main OCR process first.")
        print("You can run: python translate.py")

if __name__ == "__main__":
    test_word_creation()
