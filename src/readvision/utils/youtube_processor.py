#!/usr/bin/env python3
"""
YouTube video processor for audio extraction, transcription, and summarization.
"""

import os
import tempfile
from typing import Dict, Optional
import yt_dlp
from dotenv import load_dotenv

load_dotenv()


class YouTubeProcessor:
    """Handles YouTube video download, audio extraction, transcription, and summarization."""

    def __init__(self, gemini_api_key: Optional[str] = None):
        """
        Initialize the YouTube processor.

        Args:
            gemini_api_key: Gemini API key (optional, uses GEMINI_API_KEY env var if not provided)
        """
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
        # Use Gemini 2.0 Flash for fast and efficient audio transcription
        self.gemini_model = genai.GenerativeModel('gemini-3.1-flash-lite')
        self.genai = genai

    def download_audio(self, youtube_url: str, output_dir: Optional[str] = None) -> str:
        """
        Download audio from YouTube video.

        Args:
            youtube_url: URL of the YouTube video
            output_dir: Directory to save audio file (uses temp dir if not specified)

        Returns:
            Path to the downloaded audio file
        """
        if output_dir is None:
            output_dir = tempfile.mkdtemp()

        output_template = os.path.join(output_dir, '%(id)s.%(ext)s')

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
        }

        print(f"📥 Downloading audio from: {youtube_url}")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
                video_id = info['id']
                audio_file = os.path.join(output_dir, f"{video_id}.mp3")

                print(f"✅ Audio downloaded: {audio_file}")
                print(f"📊 Video title: {info.get('title', 'Unknown')}")
                print(f"📊 Duration: {info.get('duration', 0) // 60} minutes")

                return audio_file
        except Exception as e:
            raise Exception(f"Failed to download audio: {str(e)}")

    def transcribe_audio(self, audio_path: str) -> str:
        """
        Transcribe audio file using Gemini.

        Args:
            audio_path: Path to the audio file

        Returns:
            Transcribed text
        """
        print(f"🎙️  Transcribing audio with Gemini...")

        try:
            # Upload audio file to Gemini
            audio_file = self.genai.upload_file(path=audio_path)
            print(f"📤 Audio file uploaded to Gemini")

            # Create transcription prompt
            prompt = """Please transcribe this audio file verbatim.
Include all spoken words exactly as they appear, maintaining the natural flow of speech.
Do not add any commentary, summaries, or explanations - just the raw transcript."""

            # Generate transcription
            response = self.gemini_model.generate_content([prompt, audio_file])
            transcript = response.text.strip()

            print(f"✅ Transcription complete ({len(transcript)} characters)")

            # Clean up uploaded file
            audio_file.delete()

            return transcript

        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")

    def generate_summary(self, transcript: str, translate_to_english: bool = True) -> str:
        """
        Generate a detailed summary with original quotes from the transcript.

        Args:
            transcript: The transcribed text
            translate_to_english: Whether to translate non-English content to English

        Returns:
            Markdown-formatted summary
        """
        print(f"📝 Generating detailed summary with quotes...")

        if translate_to_english:
            translation_instruction = """
IMPORTANT: If the transcript is in a language other than English, you MUST:
1. Translate ALL content to English
2. Keep direct quotes in their original language and if arabic, keep full Tashkeel, but provide English translations in [brackets]
3. Write all analysis, descriptions, and section text in English
4. Give as detailed a summary as possible and also order the topics in a logical manner

Example format for non-English quotes:
> "Original quote in Arabic/other language"
[English translation]

Give this in .md formats.
"""
        else:
            translation_instruction = ""

        prompt = f"""Based on the following transcript, create a comprehensive, detailed summary in Markdown format.

{translation_instruction}

I want you to make a detailed summary and preserve any quotations from literature mentioned in the transcript or facts or figures
or similar things with their references.

Transcript:
{transcript}"""

        try:
            response = self.gemini_model.generate_content(
                prompt.format(transcript=transcript)
            )
            summary = response.text.strip()

            print(f"✅ Summary generated ({len(summary)} characters)")

            return summary

        except Exception as e:
            raise Exception(f"Summary generation failed: {str(e)}")

    def process_youtube_video(
        self,
        youtube_url: str,
        output_path: str,
        keep_audio: bool = False,
        audio_dir: Optional[str] = None,
        translate_to_english: bool = True
    ) -> Dict[str, str]:
        """
        Process a YouTube video: download audio, transcribe, and summarize.

        Args:
            youtube_url: URL of the YouTube video
            output_path: Path to save the summary markdown file
            keep_audio: Whether to keep the downloaded audio file
            audio_dir: Directory to save audio (temp dir if not specified)
            translate_to_english: Whether to translate non-English content to English (default: True)

        Returns:
            Dictionary with paths to generated files and metadata
        """
        temp_dir = None
        audio_path = None

        try:
            # Step 1: Download audio
            if audio_dir is None and not keep_audio:
                temp_dir = tempfile.mkdtemp()
                audio_dir = temp_dir

            audio_path = self.download_audio(youtube_url, audio_dir)

            # Step 2: Transcribe audio
            transcript = self.transcribe_audio(audio_path)

            # Save transcript
            transcript_path = output_path.replace('.md', '_transcript.txt')
            with open(transcript_path, 'w', encoding='utf-8') as f:
                f.write(transcript)
            print(f"💾 Transcript saved: {transcript_path}")

            # Step 3: Generate summary
            summary = self.generate_summary(transcript, translate_to_english=translate_to_english)

            # Save summary
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(summary)
            print(f"💾 Summary saved: {output_path}")

            result = {
                'summary_path': output_path,
                'transcript_path': transcript_path,
                'audio_path': audio_path if keep_audio else None,
                'transcript_length': len(transcript),
                'summary_length': len(summary),
            }

            # Cleanup
            if not keep_audio and audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
                print(f"🗑️  Temporary audio file removed")

            if temp_dir and os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)

            return result

        except Exception as e:
            # Cleanup on error
            if not keep_audio and audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
            if temp_dir and os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)
            raise e
