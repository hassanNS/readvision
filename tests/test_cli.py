"""Tests for the CLI module."""

import pytest
import sys
from unittest.mock import patch, Mock
from readvision.cli.main import main


class TestCLI:
    """Test cases for CLI functionality."""

    def test_main_help(self, capsys):
        """Test CLI help output."""
        with patch.object(sys, 'argv', ['readvision', '--help']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert "OCR PDF processor" in captured.out
        assert "--text-direction" in captured.out

    def test_main_version(self, capsys):
        """Test CLI version output."""
        with patch.object(sys, 'argv', ['readvision', '--version']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert "1.0.0" in captured.out

    @patch('readvision.cli.main.os.path.exists')
    def test_main_file_not_found(self, mock_exists, capsys):
        """Test CLI with non-existent PDF file."""
        mock_exists.return_value = False

        with patch.object(sys, 'argv', ['readvision', 'nonexistent.pdf', 'output.txt']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "PDF file not found" in captured.out

    @patch('readvision.cli.main.os.path.exists')
    def test_main_credentials_not_found(self, mock_exists, capsys):
        """Test CLI with non-existent credentials file."""
        def exists_side_effect(path):
            if path.endswith('.pdf'):
                return True
            if path.endswith('.json'):
                return False
            return True

        mock_exists.side_effect = exists_side_effect

        with patch.object(sys, 'argv', ['readvision', 'test.pdf', 'output.txt']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Credentials file not found" in captured.out

    @patch('readvision.cli.main.PDFOCRProcessor')
    @patch('readvision.cli.main.os.path.exists')
    @patch('builtins.open', create=True)
    def test_main_successful_processing(self, mock_open, mock_exists, mock_processor_class, capsys):
        """Test successful CLI processing."""
        mock_exists.return_value = True
        mock_processor = Mock()
        mock_processor_class.return_value = mock_processor

        # Mock file reading
        mock_file = Mock()
        mock_file.read.return_value = "Sample extracted text"
        mock_open.return_value.__enter__.return_value = mock_file

        with patch.object(sys, 'argv', [
            'readvision', 'test.pdf', 'output.txt',
            '--text-direction', 'ltr',
            '--language-hint', 'en',
            '--debug'
        ]):
            main()

        # Verify processor was called with correct arguments
        mock_processor.process_pdf.assert_called_once_with(
            'test.pdf',
            'output.txt',
            chars_per_page=3000,
            text_direction='ltr',
            encoding='utf-8',
            language_hint='en',
            debug=True
        )

        captured = capsys.readouterr()
        assert "Processing PDF: test.pdf" in captured.out
        assert "Text direction: LTR" in captured.out
        assert "Language hint: en" in captured.out
        assert "🔍 Debug mode: ENABLED" in captured.out

    @patch('readvision.cli.main.PDFOCRProcessor')
    @patch('readvision.cli.main.os.path.exists')
    def test_main_processing_error(self, mock_exists, mock_processor_class, capsys):
        """Test CLI handling of processing errors."""
        mock_exists.return_value = True
        mock_processor = Mock()
        mock_processor.process_pdf.side_effect = Exception("Processing failed")
        mock_processor_class.return_value = mock_processor

        with patch.object(sys, 'argv', ['readvision', 'test.pdf', 'output.txt']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Error: Processing failed" in captured.out