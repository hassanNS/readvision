"""Tests for the main PDF OCR processor."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from readvision.core.processor import PDFOCRProcessor


class TestPDFOCRProcessor:
    """Test cases for PDFOCRProcessor class."""

    @patch('readvision.core.processor.vision.ImageAnnotatorClient')
    @patch('readvision.core.processor.storage.Client')
    @patch('readvision.core.processor.translate.Client.from_service_account_json')
    def test_init_with_credentials(self, mock_translate, mock_storage, mock_vision, mock_credentials_path):
        """Test processor initialization with credentials."""
        processor = PDFOCRProcessor(credentials_path=mock_credentials_path)

        assert processor.vision_client is not None
        assert processor.storage_client is not None
        assert processor.translate_client is not None
        assert processor.bucket_name.startswith("ocr-temp-")

    @patch('readvision.core.processor.vision.ImageAnnotatorClient')
    @patch('readvision.core.processor.storage.Client')
    @patch('readvision.core.processor.translate.Client.from_service_account_json')
    def test_init_with_bucket_name(self, mock_translate, mock_storage, mock_vision, mock_credentials_path):
        """Test processor initialization with custom bucket name."""
        custom_bucket = "my-custom-bucket"
        processor = PDFOCRProcessor(
            credentials_path=mock_credentials_path,
            bucket_name=custom_bucket
        )

        assert processor.bucket_name == custom_bucket

    @patch('readvision.core.processor.PyPDF2.PdfReader')
    @patch('builtins.open', create=True)
    def test_get_pdf_page_count(self, mock_open, mock_pdf_reader, mock_credentials_path):
        """Test PDF page count calculation."""
        # Mock PDF reader
        mock_reader_instance = Mock()
        mock_reader_instance.pages = [Mock(), Mock(), Mock()]  # 3 pages
        mock_pdf_reader.return_value = mock_reader_instance

        with patch('readvision.core.processor.vision.ImageAnnotatorClient'), \
             patch('readvision.core.processor.storage.Client'), \
             patch('readvision.core.processor.translate.Client.from_service_account_json'):
            processor = PDFOCRProcessor(credentials_path=mock_credentials_path)
            result = processor.get_pdf_page_count("test.pdf")

        assert result == 3

    def test_debug_page_order_empty(self, mock_credentials_path, capsys):
        """Test debug page order with empty data."""
        with patch('readvision.core.processor.vision.ImageAnnotatorClient'), \
             patch('readvision.core.processor.storage.Client'), \
             patch('readvision.core.processor.translate.Client.from_service_account_json'):
            processor = PDFOCRProcessor(credentials_path=mock_credentials_path)
            processor.debug_page_order([])

        captured = capsys.readouterr()
        assert "Total pages found: 0" in captured.out

    def test_debug_page_order_with_pages(self, mock_credentials_path, capsys):
        """Test debug page order with page data."""
        page_data = [(1, "Page 1 text"), (2, "Page 2 text"), (3, "Page 3 text")]

        with patch('readvision.core.processor.vision.ImageAnnotatorClient'), \
             patch('readvision.core.processor.storage.Client'), \
             patch('readvision.core.processor.translate.Client.from_service_account_json'):
            processor = PDFOCRProcessor(credentials_path=mock_credentials_path)
            processor.debug_page_order(page_data)

        captured = capsys.readouterr()
        assert "Total pages found: 3" in captured.out
        assert "Page numbers found: [1, 2, 3]" in captured.out
        assert "Min page: 1, Max page: 3" in captured.out

    @patch('readvision.core.processor.os.path.exists')
    def test_process_pdf_file_not_found(self, mock_exists, mock_credentials_path):
        """Test process_pdf with non-existent file."""
        mock_exists.return_value = False

        with patch('readvision.core.processor.vision.ImageAnnotatorClient'), \
             patch('readvision.core.processor.storage.Client'), \
             patch('readvision.core.processor.translate.Client.from_service_account_json'):
            processor = PDFOCRProcessor(credentials_path=mock_credentials_path)

            with pytest.raises(FileNotFoundError, match="PDF file not found"):
                processor.process_pdf("nonexistent.pdf")

    @patch('readvision.core.processor.os.path.exists')
    def test_process_pdf_parameters_stored(self, mock_exists, mock_credentials_path):
        """Test that process_pdf stores parameters correctly."""
        mock_exists.return_value = True

        with patch('readvision.core.processor.vision.ImageAnnotatorClient'), \
             patch('readvision.core.processor.storage.Client'), \
             patch('readvision.core.processor.translate.Client.from_service_account_json'), \
             patch.object(PDFOCRProcessor, 'get_pdf_page_count', return_value=3), \
             patch.object(PDFOCRProcessor, 'process_small_pdf') as mock_process:

            processor = PDFOCRProcessor(credentials_path=mock_credentials_path)
            processor.process_pdf(
                "test.pdf",
                output_path="output.txt",
                text_direction="ltr",
                encoding="utf-16",
                language_hint="en",
                debug=True
            )

            assert processor.text_direction == "ltr"
            assert processor.encoding == "utf-16"
            assert processor.language_hint == "en"
            assert processor.debug == True
            mock_process.assert_called_once()