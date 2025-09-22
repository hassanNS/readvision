"""Text cleaning utilities for OCR output."""

import re


class TextCleaner:
    """Utility class for cleaning OCR text output."""

    def clean_text(self, text):
        """
        Clean OCR text output

        Args:
            text: Raw OCR text

        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        # Fix common OCR errors
        text = text.replace('|', 'I')  # Common OCR mistake
        text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)  # Add space between camelCase

        # Remove non-printable characters
        text = ''.join(char for char in text if char.isprintable() or char in '\n\t')

        # Fix spacing around punctuation
        text = re.sub(r'\s+([.,;!?])', r'\1', text)
        text = re.sub(r'([.,;!?])(?=[A-Za-z])', r'\1 ', text)

        # Normalize line breaks
        text = re.sub(r'\n{3,}', '\n\n', text)

        return text.strip()