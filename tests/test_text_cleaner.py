"""Tests for text cleaning utilities."""

import pytest
from readvision.utils.text_cleaner import TextCleaner


class TestTextCleaner:
    """Test cases for TextCleaner class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cleaner = TextCleaner()

    def test_clean_text_basic(self):
        """Test basic text cleaning functionality."""
        input_text = "Hello    world!   This is a test."
        expected = "Hello world! This is a test."
        result = self.cleaner.clean_text(input_text)
        assert result == expected

    def test_clean_text_ocr_errors(self):
        """Test OCR error correction."""
        input_text = "Hel|o wor|d"
        expected = "HelIo worId"
        result = self.cleaner.clean_text(input_text)
        assert result == expected

    def test_clean_text_camel_case(self):
        """Test camelCase word separation."""
        input_text = "HelloWorld"
        expected = "Hello World"
        result = self.cleaner.clean_text(input_text)
        assert result == expected

    def test_clean_text_punctuation_spacing(self):
        """Test punctuation spacing fixes."""
        input_text = "Hello , world !Test."
        expected = "Hello, world! Test."
        result = self.cleaner.clean_text(input_text)
        assert result == expected

    def test_clean_text_line_breaks(self):
        """Test line break normalization."""
        input_text = "Line 1\n\n\n\nLine 2"
        expected = "Line 1\n\nLine 2"
        result = self.cleaner.clean_text(input_text)
        assert result == expected

    def test_clean_text_empty_input(self):
        """Test cleaning empty text."""
        result = self.cleaner.clean_text("")
        assert result == ""

    def test_clean_text_whitespace_only(self):
        """Test cleaning whitespace-only text."""
        result = self.cleaner.clean_text("   \n\t   ")
        assert result == ""

    def test_clean_text_arabic(self):
        """Test cleaning Arabic text."""
        input_text = "مرحبا    بالعالم"
        expected = "مرحبا بالعالم"
        result = self.cleaner.clean_text(input_text)
        assert result == expected