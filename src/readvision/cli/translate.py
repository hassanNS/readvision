#!/usr/bin/env python3
"""Command line interface for standalone text translation using Gemini or Google Translate."""

import os
import sys
import argparse

from ..utils.translator import TextTranslator
from ..utils.document_creator import DocumentCreator


def main():
    """Main function for text translation command"""

    parser = argparse.ArgumentParser(
        description='Translate text files using Gemini AI or Google Translate. Creates both .txt and .docx outputs with page-by-page mapping.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  readvision-translate input.txt output.txt --to en
  readvision-translate arabic.txt english.txt --to en --from ar --use-gemini
  readvision-translate doc.txt translated.txt --to es --use-gemini --instructions "Use formal tone"
  readvision-translate file.txt out.txt --to fr --use-gemini --gemini-api-key YOUR_KEY

Output:
  Creates two files:
  - output.txt: Translated text with page break markers
  - output.docx: Word document with 1:1 page mapping
        '''
    )

    parser.add_argument('input_file',
                       help='Path to the input text file')
    parser.add_argument('output_file',
                       help='Path for the output translated text file (Word doc will be created automatically)')
    parser.add_argument('--to', '--translate-to',
                       required=True,
                       dest='translate_to',
                       help='Target language code (required, e.g., en, es, fr, de)')
    parser.add_argument('--from', '--translate-from',
                       dest='translate_from',
                       help='Source language code (optional, auto-detect if not specified)')
    parser.add_argument('--use-gemini',
                       action='store_true',
                       help='Use Gemini API instead of Google Translate')
    parser.add_argument('--gemini-api-key',
                       help='Gemini API key (optional, uses GEMINI_API_KEY env var if not provided)')
    parser.add_argument('--instructions', '--translation-instructions',
                       dest='translation_instructions',
                       help='Additional instructions for Gemini translation (e.g., "Use formal tone")')
    parser.add_argument('--credentials', '-c',
                       default='gcp.json',
                       help='Path to Google Cloud credentials JSON file for Google Translate (default: gcp.json)')
    parser.add_argument('--encoding', '-e',
                       default='utf-8',
                       help='Text file encoding (default: utf-8)')
    parser.add_argument('--version',
                       action='version',
                       version='%(prog)s 1.0.0')

    args = parser.parse_args()

    # Validate input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file not found: {args.input_file}")
        sys.exit(1)

    # Validate input is a text file
    if not args.input_file.endswith('.txt'):
        print(f"Warning: Input file '{args.input_file}' is not a .txt file")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)

    # Validate credentials for Google Translate
    if not args.use_gemini and not os.path.exists(args.credentials):
        print(f"Error: Google Cloud credentials file not found: {args.credentials}")
        print("Either provide credentials file or use --use-gemini flag")
        sys.exit(1)

    # Configuration
    INPUT_FILE = args.input_file
    OUTPUT_FILE = args.output_file
    TRANSLATE_TO = args.translate_to
    TRANSLATE_FROM = args.translate_from
    USE_GEMINI = args.use_gemini
    GEMINI_API_KEY = args.gemini_api_key
    TRANSLATION_INSTRUCTIONS = args.translation_instructions
    CREDENTIALS_PATH = args.credentials
    ENCODING = args.encoding

    provider = "Gemini AI" if USE_GEMINI else "Google Translate"
    print(f"📖 Reading: {INPUT_FILE}")
    print(f"🌐 Translating with {provider}: {TRANSLATE_FROM or 'auto-detect'} → {TRANSLATE_TO}")
    if TRANSLATION_INSTRUCTIONS and USE_GEMINI:
        print(f"📝 Custom instructions: {TRANSLATION_INSTRUCTIONS}")

    try:
        # Read input file
        with open(INPUT_FILE, 'r', encoding=ENCODING) as f:
            input_text = f.read()

        if not input_text.strip():
            print("Error: Input file is empty")
            sys.exit(1)

        print(f"📄 File size: {len(input_text)} characters")

        # Split text by page breaks (if they exist)
        # Look for common page break markers
        page_texts = []
        if '--- PAGE BREAK ---' in input_text:
            page_texts = [page.strip() for page in input_text.split('--- PAGE BREAK ---') if page.strip()]
            print(f"📑 Detected {len(page_texts)} pages (using page break markers)")
        elif '\f' in input_text:  # Form feed character
            page_texts = [page.strip() for page in input_text.split('\f') if page.strip()]
            print(f"📑 Detected {len(page_texts)} pages (using form feed)")
        else:
            # Single page or no page markers
            page_texts = [input_text]
            print(f"📑 Processing as single page (no page markers found)")

        # Initialize translator
        translator = TextTranslator(
            credentials_path=CREDENTIALS_PATH if not USE_GEMINI else None,
            use_gemini=USE_GEMINI,
            gemini_api_key=GEMINI_API_KEY,
            translation_instructions=TRANSLATION_INSTRUCTIONS
        )

        # Translate page by page
        print(f"⏳ Translating {len(page_texts)} page(s)...")
        translated_results = translator.translate_page_texts(
            page_texts=page_texts,
            target_language=TRANSLATE_TO,
            source_language=TRANSLATE_FROM
        )

        # Extract translated texts
        translated_page_texts = [result['translatedText'] for result in translated_results]

        # Write text output file with page breaks
        combined_text = '\n\n--- PAGE BREAK ---\n\n'.join(translated_page_texts)
        with open(OUTPUT_FILE, 'w', encoding=ENCODING) as f:
            f.write(combined_text)

        # Create Word document with page-by-page mapping
        word_output_path = OUTPUT_FILE.replace('.txt', '.docx')
        document_creator = DocumentCreator(
            text_direction='ltr',  # Default to left-to-right for translations
            encoding=ENCODING
        )
        page_numbers = list(range(1, len(translated_page_texts) + 1))
        document_creator.create_word_document_with_pages(
            translated_page_texts,
            word_output_path,
            page_numbers
        )

        print(f"✅ Translation complete!")
        print(f"📝 Text file saved to: {OUTPUT_FILE}")
        print(f"📄 Word document saved to: {word_output_path}")
        print(f"🔍 Detected source language: {translated_results[0].get('detectedSourceLanguage', 'unknown') if translated_results else 'unknown'}")
        print(f"📊 Translated {len(translated_page_texts)} page(s)")
        print(f"📊 Total translated text length: {sum(len(text) for text in translated_page_texts)} characters")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
