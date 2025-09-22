#!/usr/bin/env python3
"""
Migration script to help users transition from the old structure to the new package structure.
This script provides information about the changes and helps with installation.
"""

import os
import sys
import subprocess
from pathlib import Path


def print_banner():
    """Print migration banner."""
    print("=" * 60)
    print("ReadVision Package Structure Migration")
    print("=" * 60)
    print()


def check_old_structure():
    """Check if old structure files exist."""
    old_files = ["translate.py"]
    found_files = []

    for file in old_files:
        if os.path.exists(file):
            found_files.append(file)

    return found_files


def show_changes():
    """Show the structural changes."""
    print("📁 New Package Structure:")
    print("""
src/
├── readvision/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── processor.py       # Main OCR processor (was translate.py)
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main.py           # Command line interface
│   └── utils/
│       ├── __init__.py
│       ├── text_cleaner.py   # Text cleaning utilities
│       └── document_creator.py # Document creation utilities
tests/                        # Test suite
├── conftest.py
├── test_processor.py
├── test_cli.py
└── test_text_cleaner.py
docs/                        # Documentation
examples/                    # Example scripts
pyproject.toml              # Modern Python packaging
requirements.txt            # Dependencies
requirements-dev.txt        # Development dependencies
Makefile                    # Development commands
    """)


def show_usage_changes():
    """Show how usage has changed."""
    print("🔧 Usage Changes:")
    print()
    print("OLD way (translate.py):")
    print("  python translate.py document.pdf output.txt --credentials gcp.json")
    print()
    print("NEW way (after installation):")
    print("  readvision document.pdf output.txt --credentials gcp.json")
    print()
    print("Or using Python API:")
    print("  from readvision import PDFOCRProcessor")
    print("  processor = PDFOCRProcessor(credentials_path='gcp.json')")
    print("  processor.process_pdf('document.pdf', 'output.txt')")
    print()


def install_package():
    """Install the package in development mode."""
    print("🚀 Installing ReadVision package...")
    print()

    try:
        # Install in development mode
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-e", "."
        ], check=True, capture_output=True, text=True)

        print("✅ Package installed successfully!")
        print()
        print("You can now use:")
        print("  readvision --help")
        print()

    except subprocess.CalledProcessError as e:
        print("❌ Installation failed:")
        print(e.stderr)
        print()
        print("Please install manually:")
        print("  pip install -e .")
        print()


def main():
    """Main migration function."""
    print_banner()

    # Check for old structure
    old_files = check_old_structure()
    if old_files:
        print(f"📋 Found old structure files: {', '.join(old_files)}")
        print("These files are still available for reference.")
        print()

    show_changes()
    show_usage_changes()

    print("📦 Installation Options:")
    print("1. Development installation (recommended):")
    print("   pip install -e .")
    print()
    print("2. Production installation (when published):")
    print("   pip install readvision")
    print()

    # Ask if user wants to install
    try:
        response = input("Would you like to install the package now? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            install_package()
        else:
            print("Skipping installation. You can install later with: pip install -e .")
    except KeyboardInterrupt:
        print("\nSkipping installation.")

    print()
    print("🎉 Migration information complete!")
    print("The old files are preserved for compatibility.")
    print("Once you've tested the new structure, you can safely remove them.")


if __name__ == "__main__":
    main()