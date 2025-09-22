#!/usr/bin/env python3
"""
Example usage script for the OCR processor with command line arguments
"""

import subprocess
import sys
from pathlib import Path

def run_ocr_example():
    """Run OCR with different command line options"""

    print("OCR PDF Processor - Command Line Examples")
    print("=" * 50)

    # Check if assets directory exists
    assets_dir = Path("assets")
    if not assets_dir.exists():
        print("Error: assets directory not found")
        return

    # List available PDF files
    pdf_files = list(assets_dir.glob("*.pdf"))
    if not pdf_files:
        print("Error: No PDF files found in assets directory")
        return

    print(f"Found {len(pdf_files)} PDF files:")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"  {i}. {pdf_file.name}")

    print("\nExample commands you can run:")
    print("-" * 30)

    # Example 1: Basic usage
    example_pdf = pdf_files[0].name
    print(f"1. Basic usage:")
    print(f"   python translate.py assets/{example_pdf} output.txt")

    # Example 2: With custom credentials
    print(f"\n2. With custom credentials file:")
    print(f"   python translate.py assets/{example_pdf} output.txt --credentials my_gcp.json")

    # Example 3: With custom bucket
    print(f"\n3. With custom GCS bucket:")
    print(f"   python translate.py assets/{example_pdf} output.txt --bucket my-ocr-bucket")

    # Example 4: Help
    print(f"\n4. Show help:")
    print(f"   python translate.py --help")

    print(f"\n5. Run a quick test (if you want to try now):")
    print(f"   python translate.py assets/{example_pdf} test_output.txt")

    print("\nNote: Make sure you have:")
    print("- Google Cloud credentials file (gcp.json)")
    print("- Google Cloud Vision API enabled")
    print("- Proper permissions for Cloud Storage")

if __name__ == "__main__":
    run_ocr_example()
