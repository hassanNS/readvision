#!/usr/bin/env python3
"""
Arabic OCR Examples - Demonstrating the new text direction and encoding features
"""

from pathlib import Path

def show_arabic_examples():
    """Show examples of using the OCR processor with Arabic-specific options"""

    print("🔥 OCR PDF Processor - Arabic & RTL Support Examples")
    print("=" * 60)

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

    example_pdf = pdf_files[0].name

    print(f"\n🌟 New Arabic/RTL Features:")
    print("-" * 40)

    # Arabic examples
    print("1. 📖 Arabic document (default settings):")
    print(f"   python translate.py assets/{example_pdf} arabic_output.txt")
    print("   → Uses RTL text direction, UTF-8 encoding, Arabic language hint")

    print(f"\n2. 📖 Arabic document (explicit settings):")
    print(f"   python translate.py assets/{example_pdf} arabic_output.txt \\")
    print("     --text-direction rtl --encoding utf-8 --language-hint ar")

    print(f"\n3. 📄 English document:")
    print(f"   python translate.py assets/{example_pdf} english_output.txt \\")
    print("     --text-direction ltr --language-hint en")

    print(f"\n4. 🔤 Alternative encoding:")
    print(f"   python translate.py assets/{example_pdf} output.txt \\")
    print("     --encoding utf-16")

    print(f"\n5. 📊 Urdu document:")
    print(f"   python translate.py assets/{example_pdf} urdu_output.txt \\")
    print("     --text-direction rtl --language-hint ur")

    print(f"\n6. 📚 Persian/Farsi document:")
    print(f"   python translate.py assets/{example_pdf} persian_output.txt \\")
    print("     --text-direction rtl --language-hint fa")

    print(f"\n🎯 Key Features:")
    print("-" * 20)
    print("✅ RTL text direction (default for Arabic)")
    print("✅ UTF-8 encoding (default for Arabic characters)")
    print("✅ Arabic language hints for better OCR accuracy")
    print("✅ Word documents with proper RTL formatting")
    print("✅ Arabic Unicode fonts (Arial Unicode MS)")
    print("✅ Right-aligned text in Word documents")

    print(f"\n📋 Text Direction Options:")
    print("• --text-direction rtl → Right-to-left (Arabic, Hebrew, Persian)")
    print("• --text-direction ltr → Left-to-right (English, French, etc.)")

    print(f"\n🔤 Encoding Options:")
    print("• --encoding utf-8 → Default, supports Arabic")
    print("• --encoding utf-16 → Alternative Unicode encoding")
    print("• --encoding cp1256 → Windows Arabic encoding")

    print(f"\n🌍 Language Hints:")
    print("• --language-hint ar → Arabic")
    print("• --language-hint en → English")
    print("• --language-hint ur → Urdu")
    print("• --language-hint fa → Persian/Farsi")
    print("• --language-hint he → Hebrew")

    print(f"\n💡 Output:")
    print("• .txt file → Plain text with specified encoding and page breaks")
    print("• .docx file → Word document with proper RTL/LTR formatting")

    print(f"\n🚀 Quick Test (Arabic defaults):")
    print(f"   python translate.py assets/{example_pdf} test_arabic.txt")

if __name__ == "__main__":
    show_arabic_examples()
