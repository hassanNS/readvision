#!/usr/bin/env python3
"""
Google Cloud Vision API OCR Script for Large PDFs
Processes multi-page PDFs using batch operations for efficiency
"""

import os
import json
import time
import re
from pathlib import Path
from google.cloud import vision
from google.cloud import storage
from google.cloud import translate_v2 as translate
import PyPDF2

from ..utils.text_cleaner import TextCleaner
from ..utils.document_creator import DocumentCreator
from ..utils.translator import TextTranslator


class PDFOCRProcessor:
    """Main class for processing PDFs using Google Cloud Vision API."""

    def __init__(self, credentials_path=None, bucket_name=None):
        """
        Initialize the OCR processor

        Args:
            credentials_path: Path to Google Cloud credentials JSON file
            bucket_name: Google Cloud Storage bucket name for temporary storage
        """
        if credentials_path:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

        self.vision_client = vision.ImageAnnotatorClient()
        self.storage_client = storage.Client()
        self.translate_client = translate.Client.from_service_account_json(
            credentials_path or "gcp.json"
        )

        # Create or use existing bucket for batch operations
        if bucket_name:
            self.bucket_name = bucket_name
        else:
            self.bucket_name = f"ocr-temp-{int(time.time())}"
            self._create_bucket()

    def _create_bucket(self):
        """Create a temporary bucket for batch operations"""
        try:
            bucket = self.storage_client.create_bucket(self.bucket_name)
            print(f"Created bucket: {self.bucket_name}")
        except Exception as e:
            print(f"Bucket creation failed: {e}")
            # Use existing bucket or handle error

    def debug_page_order(self, page_data):
        """
        Debug function to show page ordering information

        Args:
            page_data: List of (page_number, text) tuples
        """
        print(f"\n🔍 Debug: Page Order Information")
        print(f"Total pages found: {len(page_data)}")

        if page_data:
            page_numbers = [page_num for page_num, text in page_data]
            print(f"Page numbers found: {sorted(set(page_numbers))}")
            print(f"Min page: {min(page_numbers)}, Max page: {max(page_numbers)}")

            # Check for duplicates
            duplicates = [num for num in set(page_numbers) if page_numbers.count(num) > 1]
            if duplicates:
                print(f"⚠️  Duplicate page numbers found: {duplicates}")

            # Check for missing pages
            expected_range = set(range(min(page_numbers), max(page_numbers) + 1))
            actual_pages = set(page_numbers)
            missing = expected_range - actual_pages
            if missing:
                print(f"⚠️  Missing page numbers: {sorted(missing)}")

            # Show first few pages for verification
            sorted_data = sorted(page_data, key=lambda x: x[0])
            print(f"\nFirst 3 pages preview:")
            for i, (page_num, text) in enumerate(sorted_data[:3]):
                preview = text.strip()[:100].replace('\n', ' ')
                print(f"  Page {page_num}: {preview}...")
        print("-" * 50)

    def process_small_pdf(self, pdf_path, output_path):
        """
        Process PDFs with fewer than 5 pages using synchronous requests

        Args:
            pdf_path: Path to input PDF
            output_path: Path to output text file
        """
        print(f"Processing small PDF: {pdf_path}")

        page_texts = []

        # Read PDF file
        with open(pdf_path, 'rb') as file:
            content = file.read()

        # Configure OCR parameters with language hint
        feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

        # Get language hint
        language_hint = getattr(self, 'language_hint', 'ar')

        # Create image context with language hints
        image_context = vision.ImageContext(language_hints=[language_hint])

        # Create request
        request = vision.AnnotateFileRequest(
            input_config=vision.InputConfig(
                content=content,
                mime_type='application/pdf'
            ),
            features=[feature],
            image_context=image_context
        )

        # Perform OCR
        response = self.vision_client.batch_annotate_files(requests=[request])

        # Extract text from all pages with page numbers for correct ordering
        page_data = []  # Store (page_number, text) tuples

        for page_response in response.responses[0].responses:
            if page_response.full_text_annotation:
                # Try to get page number from context
                page_number = 1  # default
                if hasattr(page_response, 'context') and page_response.context:
                    page_number = getattr(page_response.context, 'pageNumber', len(page_data) + 1)
                else:
                    page_number = len(page_data) + 1

                page_text = page_response.full_text_annotation.text
                page_data.append((page_number, page_text))

        # Sort pages by page number to ensure correct order
        page_data.sort(key=lambda x: x[0])

        # Debug page ordering if enabled
        if getattr(self, 'debug', False):
            self.debug_page_order(page_data)

        # Extract text and page numbers in correct order
        page_texts = [text for page_num, text in page_data]
        page_numbers = [page_num for page_num, text in page_data]

        print(f"Processed {len(page_texts)} pages in correct order")
        if page_numbers:
            print(f"Page number range: {min(page_numbers)} to {max(page_numbers)}")

        # Create Word document with page-by-page mapping
        word_output_path = output_path.replace('.txt', '.docx')
        document_creator = DocumentCreator(
            text_direction=getattr(self, 'text_direction', 'rtl'),
            encoding=getattr(self, 'encoding', 'utf-8')
        )
        document_creator.create_word_document_with_pages(page_texts, word_output_path, page_numbers)

        # Also save as combined text file if needed
        text_cleaner = TextCleaner()
        all_text = []
        for page_text in page_texts:
            all_text.append(text_cleaner.clean_text(page_text))

        combined_text = '\n\n--- PAGE BREAK ---\n\n'.join(all_text)

        # Use specified encoding
        encoding = getattr(self, 'encoding', 'utf-8')
        with open(output_path, 'w', encoding=encoding) as f:
            f.write(combined_text)

        # Handle translation if requested
        if getattr(self, 'translate_to', None):
            self._create_translated_files(page_texts, page_numbers, output_path)

        print(f"OCR completed. Output saved to: {word_output_path} and {output_path}")

    def process_large_pdf(self, pdf_path, output_path):
        """
        Process large PDFs using asynchronous batch operations

        Args:
            pdf_path: Path to input PDF
            output_path: Path to output text file
        """
        print(f"Processing large PDF: {pdf_path}")

        # Upload PDF to GCS
        blob_name = f"input/{Path(pdf_path).name}"
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(pdf_path)

        gcs_source_uri = f"gs://{self.bucket_name}/{blob_name}"
        gcs_destination_uri = f"gs://{self.bucket_name}/output/"

        # Configure batch request
        gcs_source = vision.GcsSource(uri=gcs_source_uri)
        input_config = vision.InputConfig(
            gcs_source=gcs_source,
            mime_type='application/pdf'
        )

        gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
        output_config = vision.OutputConfig(
            gcs_destination=gcs_destination,
            batch_size=100  # Max pages per output file
        )

        # Get language hint and create image context
        language_hint = getattr(self, 'language_hint', 'ar')
        image_context = vision.ImageContext(language_hints=[language_hint])

        async_request = vision.AsyncAnnotateFileRequest(
            features=[vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)],
            input_config=input_config,
            output_config=output_config,
            image_context=image_context
        )

        # Start async batch operation
        operation = self.vision_client.async_batch_annotate_files(
            requests=[async_request]
        )

        print("Waiting for operation to complete...")
        operation.result(timeout=600)  # 10 minute timeout

        # Download and process results
        page_data = []  # Store (page_number, text) tuples

        # List all output files and sort them to maintain order
        blobs = list(bucket.list_blobs(prefix='output/'))
        blobs.sort(key=lambda x: x.name)

        for blob in blobs:
            if blob.name.endswith('.json'):
                # Download JSON result
                json_content = blob.download_as_text()
                response = json.loads(json_content)

                # Extract text from each page with page number
                for page_response in response['responses']:
                    if 'fullTextAnnotation' in page_response and 'context' in page_response:
                        page_number = page_response['context'].get('pageNumber', 0)
                        page_text = page_response['fullTextAnnotation']['text']
                        page_data.append((page_number, page_text))
                    elif 'fullTextAnnotation' in page_response:
                        # Fallback if no context/pageNumber available
                        page_text = page_response['fullTextAnnotation']['text']
                        page_data.append((len(page_data) + 1, page_text))

        # Sort pages by page number to ensure correct order
        page_data.sort(key=lambda x: x[0])

        # Debug page ordering if enabled
        if getattr(self, 'debug', False):
            self.debug_page_order(page_data)

        # Extract text and page numbers in correct order
        page_texts = [text for page_num, text in page_data]
        page_numbers = [page_num for page_num, text in page_data]

        print(f"Processed {len(page_texts)} pages in correct order")
        if page_numbers:
            print(f"Page number range: {min(page_numbers)} to {max(page_numbers)}")

        # Create Word document with page-by-page mapping
        word_output_path = output_path.replace('.txt', '.docx')
        document_creator = DocumentCreator(
            text_direction=getattr(self, 'text_direction', 'rtl'),
            encoding=getattr(self, 'encoding', 'utf-8')
        )
        document_creator.create_word_document_with_pages(page_texts, word_output_path, page_numbers)

        # Also save as combined text file if needed
        text_cleaner = TextCleaner()
        all_text = []
        for page_text in page_texts:
            all_text.append(text_cleaner.clean_text(page_text))

        combined_text = '\n\n--- PAGE BREAK ---\n\n'.join(all_text)

        # Use specified encoding
        encoding = getattr(self, 'encoding', 'utf-8')
        with open(output_path, 'w', encoding=encoding) as f:
            f.write(combined_text)

        # Handle translation if requested
        if getattr(self, 'translate_to', None):
            self._create_translated_files(page_texts, page_numbers, output_path)

        # Cleanup GCS
        # self._cleanup_gcs()

        print(f"OCR completed. Output saved to: {word_output_path} and {output_path}")

    def _create_translated_files(self, page_texts, page_numbers, original_output_path):
        """
        Create translated versions of the text and Word files.

        Args:
            page_texts: List of original page texts
            page_numbers: List of page numbers
            original_output_path: Path to the original output file
        """
        print(f"🌐 Starting translation to '{self.translate_to}'...")

        # Initialize translator
        credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'gcp.json')
        translator = TextTranslator(credentials_path)

        # Translate all pages
        translated_results = translator.translate_page_texts(
            page_texts,
            target_language=self.translate_to,
            source_language=self.translate_from
        )

        # Extract translated texts
        translated_page_texts = [result['translatedText'] for result in translated_results]

        # Create translated file paths
        base_path = Path(original_output_path)
        translated_txt_path = str(base_path.with_name(f"{base_path.stem}_translated_{self.translate_to}.txt"))
        translated_docx_path = str(base_path.with_name(f"{base_path.stem}_translated_{self.translate_to}.docx"))

        # Create translated text file
        text_cleaner = TextCleaner()
        translated_all_text = []
        for page_text in translated_page_texts:
            translated_all_text.append(text_cleaner.clean_text(page_text))

        translated_combined_text = '\n\n--- PAGE BREAK ---\n\n'.join(translated_all_text)

        encoding = getattr(self, 'encoding', 'utf-8')
        with open(translated_txt_path, 'w', encoding=encoding) as f:
            f.write(translated_combined_text)

        # Create translated Word document
        document_creator = DocumentCreator(
            text_direction=getattr(self, 'text_direction', 'rtl'),
            encoding=getattr(self, 'encoding', 'utf-8')
        )
        document_creator.create_word_document_with_pages(
            translated_page_texts,
            translated_docx_path,
            page_numbers
        )

        print(f"✅ Translation completed. Files saved:")
        print(f"   📄 {translated_txt_path}")
        print(f"   📝 {translated_docx_path}")

        # Show translation summary
        detected_language = translated_results[0].get('detectedSourceLanguage', 'unknown') if translated_results else 'unknown'
        print(f"   🔍 Detected source language: {detected_language}")
        print(f"   🌐 Translated to: {self.translate_to}")

    def _cleanup_gcs(self):
        """Clean up temporary files from GCS bucket"""
        bucket = self.storage_client.bucket(self.bucket_name)
        blobs = bucket.list_blobs()
        for blob in blobs:
            blob.delete()

    def get_pdf_page_count(self, pdf_path):
        """Get number of pages in PDF"""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            return len(reader.pages)

    def process_pdf(self, pdf_path, output_path='output.txt', chars_per_page=3000,
                    text_direction='rtl', encoding='utf-8', language_hint='ar', debug=False,
                    translate_to=None, translate_from=None):
        """
        Main method to process a PDF file

        Args:
            pdf_path: Path to input PDF
            output_path: Path to output text file
            chars_per_page: Characters per page in Word document
            text_direction: Text direction ('ltr' or 'rtl')
            encoding: Text file encoding
            language_hint: Language hint for OCR processing
            debug: Enable debug output for page ordering
            translate_to: Target language code for translation (optional)
            translate_from: Source language code for translation (optional, auto-detect if None)
        """
        # Store parameters for later use
        self.chars_per_page = chars_per_page
        self.text_direction = text_direction
        self.encoding = encoding
        self.language_hint = language_hint
        self.debug = debug
        self.translate_to = translate_to
        self.translate_from = translate_from

        # Check if file exists
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Get page count
        page_count = self.get_pdf_page_count(pdf_path)
        print(f"PDF has {page_count} pages")

        # Choose processing method based on size
        if page_count <= 5:
            self.process_small_pdf(pdf_path, output_path)
        else:
            self.process_large_pdf(pdf_path, output_path)