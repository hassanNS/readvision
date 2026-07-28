#!/usr/bin/env python3
"""
Translation utility for text translation using Google Cloud Translation API and Gemini API
"""

import os
from google.cloud import translate_v2 as translate
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class TextTranslator:
    """Handles text translation using Google Cloud Translation API and Gemini API."""

    def __init__(self, credentials_path: str = None, use_gemini: bool = False, gemini_api_key: str = None,
                 translation_instructions: str = None):
        """
        Initialize the translator.

        Args:
            credentials_path: Path to Google Cloud credentials JSON file
            use_gemini: If True, use Gemini API for translation instead of Google Translate
            gemini_api_key: Gemini API key (optional, will use GEMINI_API_KEY env var if not provided)
            translation_instructions: Additional instructions for Gemini translation (optional)
        """
        self.use_gemini = use_gemini
        self.translation_instructions = translation_instructions

        if use_gemini:
            # Initialize Gemini
            try:
                import google.generativeai as genai
            except ImportError:
                raise ImportError(
                    "google-generativeai package not installed. "
                    "Install it with: pip install google-generativeai"
                )

            # Get API key from parameter or environment variable
            api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError(
                    "Gemini API key not provided. "
                    "Set GEMINI_API_KEY environment variable or pass gemini_api_key parameter. "
                    "Get your key from: https://makersuite.google.com/app/apikey"
                )

            genai.configure(api_key=api_key)
            # Use Gemini 3.1 Flash Lite Preview (optimized for speed and cost)
            self.gemini_model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')
            self.translate_client = None  # Not using Google Translate
        else:
            # Initialize Google Translate (existing behavior)
            if credentials_path:
                self.translate_client = translate.Client.from_service_account_json(credentials_path)
            else:
                self.translate_client = translate.Client()
            self.gemini_model = None

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

        if self.use_gemini:
            # Use Gemini API for translation
            return self._translate_with_gemini(text, target_language, source_language)
        else:
            # Use Google Translate API
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

    def _translate_with_gemini(self, text: str, target_language: str, source_language: str = None) -> Dict[str, str]:
        """
        Translate text using Gemini API.

        Args:
            text: Text to translate
            target_language: Target language code or name
            source_language: Source language code or name (optional)

        Returns:
            Dictionary with translated text and metadata
        """
        # Get language names for better prompting
        lang_names = self.get_common_languages()
        target_lang_name = lang_names.get(target_language, target_language)

        # Build prompt
        base_instruction = "Only provide the translation, without any additional explanation or commentary."

        # Add custom instructions if provided
        if self.translation_instructions:
            base_instruction += f"\n\nAdditional instructions: {self.translation_instructions}"

        if source_language:
            source_lang_name = lang_names.get(source_language, source_language)
            prompt = f"""Translate the following text from {source_lang_name} to {target_lang_name}.
{base_instruction}

Text to translate:
{text}"""
        else:
            prompt = f"""Translate the following text to {target_lang_name}.
{base_instruction}

Text to translate:
{text}"""

        try:
            response = self.gemini_model.generate_content(prompt)
            translated_text = response.text.strip()

            return {
                'translatedText': translated_text,
                'detectedSourceLanguage': source_language or 'auto-detected',
                'originalText': text,
                'provider': 'gemini'
            }
        except Exception as e:
            raise Exception(f"Gemini translation failed: {str(e)}")

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