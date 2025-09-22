#!/usr/bin/env python3
"""
Translation utility for text translation using Google Cloud Translation API
"""

from google.cloud import translate_v2 as translate
from typing import List, Dict, Optional


class TextTranslator:
    """Handles text translation using Google Cloud Translation API."""

    def __init__(self, credentials_path: str = None):
        """
        Initialize the translator.

        Args:
            credentials_path: Path to Google Cloud credentials JSON file
        """
        if credentials_path:
            self.translate_client = translate.Client.from_service_account_json(credentials_path)
        else:
            self.translate_client = translate.Client()

    def detect_language(self, text: str) -> Dict[str, str]:
        """
        Detect the language of the given text.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with language code and confidence
        """
        result = self.translate_client.detect_language(text)
        return {
            'language': result['language'],
            'confidence': result['confidence']
        }

    def get_supported_languages(self) -> List[Dict[str, str]]:
        """
        Get list of supported languages.

        Returns:
            List of dictionaries with language codes and names
        """
        languages = self.translate_client.get_languages()
        return languages

    def translate_text(self, text: str, target_language: str, source_language: str = None) -> Dict[str, str]:
        """
        Translate text to target language.

        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'en', 'es', 'fr')
            source_language: Source language code (optional, auto-detect if None)

        Returns:
            Dictionary with translated text and metadata
        """
        if not text.strip():
            return {
                'translatedText': '',
                'detectedSourceLanguage': source_language or 'unknown',
                'originalText': text
            }

        # Perform translation
        result = self.translate_client.translate(
            text,
            target_language=target_language,
            source_language=source_language
        )

        return {
            'translatedText': result['translatedText'],
            'detectedSourceLanguage': result.get('detectedSourceLanguage', source_language),
            'originalText': text
        }

    def translate_page_texts(self, page_texts: List[str], target_language: str,
                           source_language: str = None) -> List[Dict[str, str]]:
        """
        Translate multiple page texts.

        Args:
            page_texts: List of text strings (one per page)
            target_language: Target language code
            source_language: Source language code (optional)

        Returns:
            List of translation results for each page
        """
        translated_pages = []

        for i, page_text in enumerate(page_texts):
            print(f"Translating page {i + 1}/{len(page_texts)}...")

            if not page_text.strip():
                translated_pages.append({
                    'translatedText': '',
                    'detectedSourceLanguage': source_language or 'unknown',
                    'originalText': page_text
                })
                continue

            try:
                result = self.translate_text(page_text, target_language, source_language)
                translated_pages.append(result)
            except Exception as e:
                print(f"Warning: Failed to translate page {i + 1}: {e}")
                # Keep original text if translation fails
                translated_pages.append({
                    'translatedText': page_text,  # Fallback to original
                    'detectedSourceLanguage': source_language or 'unknown',
                    'originalText': page_text,
                    'error': str(e)
                })

        return translated_pages

    @staticmethod
    def get_common_languages() -> Dict[str, str]:
        """
        Get commonly used language codes and names.

        Returns:
            Dictionary mapping language codes to names
        """
        return {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'zh': 'Chinese (Simplified)',
            'zh-TW': 'Chinese (Traditional)',
            'ja': 'Japanese',
            'ko': 'Korean',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'th': 'Thai',
            'vi': 'Vietnamese',
            'nl': 'Dutch',
            'sv': 'Swedish',
            'no': 'Norwegian',
            'da': 'Danish',
            'fi': 'Finnish',
            'pl': 'Polish',
            'tr': 'Turkish',
            'he': 'Hebrew'
        }