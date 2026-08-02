#!/usr/bin/env python3
"""
YouTube video processor for audio extraction, transcription, and summarization.
"""

import os
import tempfile
from typing import Dict, List, Optional, Tuple
import yt_dlp
from dotenv import load_dotenv

load_dotenv()


class YouTubeProcessor:
    """Handles YouTube video download, audio extraction, transcription, and summarization."""

    def __init__(
        self,
        gemini_api_key: Optional[str] = None,
        whisper_model: str = "base",
        whisper_model_dir: Optional[str] = None
    ):
        """
        Initialize the YouTube processor.

        Args:
            gemini_api_key: Gemini API key (for translation and summarization)
            whisper_model: Whisper model size ("tiny", "base", "small", "medium", "large")
            whisper_model_dir: Custom directory for Whisper models (for desktop app bundling)
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
        # Use Gemini Flash for translation and summarization
        self.gemini_model = genai.GenerativeModel('gemini-3.1-flash-lite')
        self.genai = genai

        # Whisper configuration
        self.whisper_model = whisper_model
        self.whisper_model_dir = whisper_model_dir

    def download_audio(self, youtube_url: str, output_dir: Optional[str] = None) -> str:
        """
        Download audio from YouTube video with multiple fallback strategies.

        Args:
            youtube_url: URL of the YouTube video
            output_dir: Directory to save audio file (uses temp dir if not specified)

        Returns:
            Path to the downloaded audio file
        """
        if output_dir is None:
            output_dir = tempfile.mkdtemp()

        output_template = os.path.join(output_dir, '%(id)s.%(ext)s')

        # Strategy 1: Chrome cookies + alternative clients + flexible format
        ydl_opts_strategies = [
            {
                'name': 'Chrome cookies with alternative clients',
                'opts': {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': output_template,
                    'quiet': True,
                    'no_warnings': True,
                    'cookiesfrombrowser': ('chrome',),
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['android', 'web_embedded', 'ios'],
                        }
                    },
                }
            },
            {
                'name': 'Alternative clients only',
                'opts': {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': output_template,
                    'quiet': True,
                    'no_warnings': True,
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['android', 'web_embedded', 'ios'],
                        }
                    },
                }
            },
            {
                'name': 'Basic download (no special options)',
                'opts': {
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
            },
        ]

        print(f"📥 Downloading audio from: {youtube_url}")

        last_error = None
        for strategy in ydl_opts_strategies:
            try:
                print(f"🔄 Trying: {strategy['name']}...")
                with yt_dlp.YoutubeDL(strategy['opts']) as ydl:
                    info = ydl.extract_info(youtube_url, download=True)
                    video_id = info['id']
                    audio_file = os.path.join(output_dir, f"{video_id}.mp3")

                    print(f"✅ Audio downloaded: {audio_file}")
                    print(f"📊 Video title: {info.get('title', 'Unknown')}")
                    print(f"📊 Duration: {info.get('duration', 0) // 60} minutes")

                    return audio_file
            except Exception as e:
                last_error = e
                error_msg = str(e).lower()
                print(f"⚠️  Strategy failed: {str(e)[:100]}")

                # Don't try more strategies for certain errors
                if 'private' in error_msg or 'unavailable' in error_msg or 'removed' in error_msg:
                    raise Exception(f"Video is not accessible: {str(e)}")

                continue

        # All strategies failed
        raise Exception(f"Failed to download audio after trying all strategies. Last error: {str(last_error)}")

    def transcribe_audio(self, audio_path: str, use_fallback: bool = False) -> str:
        """
        Transcribe audio file using Gemini.

        Args:
            audio_path: Path to the audio file
            use_fallback: If True, uses paraphrasing mode to avoid copyright issues

        Returns:
            Transcribed text
        """
        print(f"🎙️  Transcribing audio with Gemini...")

        audio_file = None
        try:
            # Upload audio file to Gemini
            audio_file = self.genai.upload_file(path=audio_path)
            print(f"📤 Audio file uploaded to Gemini")

            # Create transcription prompt
            if use_fallback:
                print(f"⚠️  Using fallback mode (paraphrasing instead of verbatim)")
                prompt = """Please provide a detailed description of what is being discussed in this audio file.
Include all main topics, key points, concepts, and important information mentioned.
Paraphrase the content to capture the meaning while avoiding direct verbatim quotes.
Be as comprehensive and detailed as possible."""
            else:
                prompt = """Please transcribe this audio file verbatim.
Include all spoken words exactly as they appear, maintaining the natural flow of speech.
Do not add any commentary, summaries, or explanations - just the raw transcript."""

            # Generate transcription
            response = self.gemini_model.generate_content([prompt, audio_file])

            # Check if response was blocked
            if not response.parts:
                # Check finish_reason
                finish_reason = response.candidates[0].finish_reason if response.candidates else None

                if finish_reason == 4:  # RECITATION (copyrighted content)
                    if not use_fallback:
                        # Try fallback approach
                        print(f"⚠️  Copyright detected, retrying with paraphrasing mode...")
                        if audio_file:
                            try:
                                audio_file.delete()
                            except:
                                pass
                        return self.transcribe_audio(audio_path, use_fallback=True)
                    else:
                        raise Exception(
                            "Content blocked: Video contains copyrighted material. "
                            "Even paraphrasing mode was blocked. This video cannot be processed."
                        )
                elif finish_reason == 3:  # SAFETY (harmful content)
                    raise Exception(
                        "Content blocked: Video was flagged for safety reasons."
                    )
                else:
                    raise Exception(
                        f"Content blocked: Gemini blocked this content (finish_reason: {finish_reason}). "
                        "The video may contain restricted material."
                    )

            transcript = response.text.strip()

            if use_fallback:
                print(f"✅ Paraphrased content generated ({len(transcript)} characters)")
            else:
                print(f"✅ Transcription complete ({len(transcript)} characters)")

            return transcript

        except Exception as e:
            error_msg = str(e)

            # Provide helpful error messages
            if "finish_reason" in error_msg.lower() or "recitation" in error_msg.lower():
                if not use_fallback:
                    # Try fallback approach
                    print(f"⚠️  Copyright detected, retrying with paraphrasing mode...")
                    if audio_file:
                        try:
                            audio_file.delete()
                        except:
                            pass
                    return self.transcribe_audio(audio_path, use_fallback=True)
                else:
                    raise Exception(
                        f"Transcription blocked: Video contains copyrighted material. "
                        f"Gemini's safety filters prevent processing this content even in paraphrasing mode. "
                        f"Original error: {error_msg}"
                    )
            else:
                raise Exception(f"Transcription failed: {error_msg}")

        finally:
            # Clean up uploaded file
            if audio_file:
                try:
                    audio_file.delete()
                except:
                    pass  # Ignore cleanup errors

    def transcribe_with_whisper(self, audio_path: str, model_size: str = "base", download_root: Optional[str] = None) -> str:
        """
        Transcribe audio file using OpenAI Whisper (local).

        Args:
            audio_path: Path to the audio file
            model_size: Whisper model size ("tiny", "base", "small", "medium", "large")
            download_root: Custom directory for models (for desktop app bundling)

        Returns:
            Transcribed text with detected language info
        """
        print(f"🎙️  Transcribing audio with Whisper (local)...")

        try:
            import whisper
        except ImportError:
            raise ImportError(
                "openai-whisper package not installed. "
                "Install it with: pip install openai-whisper"
            )

        try:
            # Load Whisper model
            if download_root and os.path.exists(download_root):
                # Use bundled models (for desktop app)
                print(f"📥 Loading bundled Whisper '{model_size}' model...")
                model = whisper.load_model(model_size, download_root=download_root)
            else:
                # Download to cache (for CLI usage)
                print(f"📥 Loading Whisper '{model_size}' model (downloads on first use)...")
                model = whisper.load_model(model_size)

            print(f"🔄 Transcribing with Whisper...")
            result = model.transcribe(audio_path)

            transcript = result["text"].strip()
            detected_language = result.get("language", "unknown")

            print(f"✅ Whisper transcription complete ({len(transcript)} characters)")
            print(f"🌍 Detected language: {detected_language}")

            return transcript

        except Exception as e:
            raise Exception(f"Whisper transcription failed: {str(e)}")

    def translate_transcript(self, transcript: str) -> str:
        """
        Translate full transcript to English without summarizing.

        Args:
            transcript: The original transcript text

        Returns:
            Full English translation of the transcript
        """
        print(f"🌐 Translating full transcript to English...")

        prompt = """Translate this entire transcript to English.

IMPORTANT:
- Translate ALL content verbatim - do not summarize, shorten, or skip any parts
- Preserve the natural flow and structure of the speech
- Maintain all details, examples, and explanations from the original
- Keep technical terms accurate
- This should be a complete, word-for-word translation, not a summary

Transcript to translate:
{transcript}"""

        try:
            response = self.gemini_model.generate_content(
                prompt.format(transcript=transcript)
            )
            translated_transcript = response.text.strip()

            print(f"✅ Translation complete ({len(translated_transcript)} characters)")

            return translated_transcript

        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")

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

            # Step 2: Transcribe audio using Whisper
            transcript = self.transcribe_with_whisper(
                audio_path,
                model_size=self.whisper_model,
                download_root=self.whisper_model_dir
            )

            # Save original transcript
            transcript_path = output_path.replace('.md', '_transcript.txt')
            with open(transcript_path, 'w', encoding='utf-8') as f:
                f.write(transcript)
            print(f"💾 Transcript saved: {transcript_path}")

            # Step 3: Translate transcript to English (if requested)
            translated_transcript_path = None
            if translate_to_english:
                translated_transcript = self.translate_transcript(transcript)
                translated_transcript_path = output_path.replace('.md', '_transcript_en.txt')
                with open(translated_transcript_path, 'w', encoding='utf-8') as f:
                    f.write(translated_transcript)
                print(f"💾 English transcript saved: {translated_transcript_path}")

            # Step 4: Generate summary
            summary = self.generate_summary(transcript, translate_to_english=translate_to_english)

            # Save summary
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(summary)
            print(f"💾 Summary saved: {output_path}")

            result = {
                'summary_path': output_path,
                'transcript_path': transcript_path,
                'transcript_en_path': translated_transcript_path,
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

    def get_playlist_videos(self, playlist_url: str) -> List[Dict[str, str]]:
        """
        Extract video information from a YouTube playlist.

        Args:
            playlist_url: URL of the YouTube playlist

        Returns:
            List of dictionaries containing video information (id, title, url)
        """
        print(f"📋 Extracting playlist information...")

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,  # Don't download, just get metadata
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                playlist_info = ydl.extract_info(playlist_url, download=False)

                if 'entries' not in playlist_info:
                    raise ValueError("URL does not appear to be a valid playlist")

                videos = []
                for idx, entry in enumerate(playlist_info['entries'], 1):
                    if entry:  # Some entries might be None
                        videos.append({
                            'index': idx,
                            'id': entry.get('id', ''),
                            'title': entry.get('title', f'Video {idx}'),
                            'url': entry.get('url', f"https://www.youtube.com/watch?v={entry.get('id')}"),
                            'duration': entry.get('duration', 0),
                        })

                print(f"✅ Found {len(videos)} videos in playlist")
                print(f"📊 Playlist title: {playlist_info.get('title', 'Unknown')}")

                return videos

        except Exception as e:
            raise Exception(f"Failed to extract playlist: {str(e)}")

    def process_playlist(
        self,
        playlist_url: str,
        output_dir: str,
        start_index: Optional[int] = None,
        end_index: Optional[int] = None,
        keep_audio: bool = False,
        audio_dir: Optional[str] = None,
        translate_to_english: bool = True
    ) -> List[Dict[str, str]]:
        """
        Process multiple videos from a YouTube playlist.

        Args:
            playlist_url: URL of the YouTube playlist
            output_dir: Directory to save all output files
            start_index: Starting video index (1-based, inclusive)
            end_index: Ending video index (1-based, inclusive)
            keep_audio: Whether to keep downloaded audio files
            audio_dir: Directory to save audio files
            translate_to_english: Whether to translate non-English content to English

        Returns:
            List of dictionaries with processing results for each video
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Get playlist videos
        videos = self.get_playlist_videos(playlist_url)

        # Apply range filtering
        if start_index is not None or end_index is not None:
            start = (start_index or 1) - 1  # Convert to 0-based index
            end = end_index if end_index is not None else len(videos)

            if start < 0 or start >= len(videos):
                raise ValueError(f"Start index {start_index} is out of range (1-{len(videos)})")
            if end < start or end > len(videos):
                raise ValueError(f"End index {end_index} is out of range ({start_index}-{len(videos)})")

            videos = videos[start:end]
            print(f"🎯 Processing videos {start + 1} to {end} (total: {len(videos)} videos)")
        else:
            print(f"🎯 Processing all {len(videos)} videos from playlist")

        results = []
        successful = 0
        failed = 0

        for video in videos:
            print()
            print("=" * 80)
            print(f"📹 Processing video {video['index']}/{len(videos) + (start_index or 1) - 1}: {video['title']}")
            print("=" * 80)

            try:
                # Generate output filename from video title
                import re
                clean_title = re.sub(r'[^\w\s-]', '', video['title'])
                clean_title = re.sub(r'[-\s]+', '_', clean_title)
                output_filename = f"{video['index']:03d}_{clean_title[:50]}_summary.md"
                output_path = os.path.join(output_dir, output_filename)

                # Process video
                result = self.process_youtube_video(
                    youtube_url=video['url'],
                    output_path=output_path,
                    keep_audio=keep_audio,
                    audio_dir=audio_dir,
                    translate_to_english=translate_to_english
                )

                result['video_index'] = video['index']
                result['video_title'] = video['title']
                result['video_id'] = video['id']
                result['status'] = 'success'

                results.append(result)
                successful += 1

                print(f"✅ Successfully processed video {video['index']}")

            except Exception as e:
                print(f"❌ Failed to process video {video['index']}: {str(e)}")
                results.append({
                    'video_index': video['index'],
                    'video_title': video['title'],
                    'video_id': video['id'],
                    'status': 'failed',
                    'error': str(e)
                })
                failed += 1

        # Print summary
        print()
        print("=" * 80)
        print("📊 PLAYLIST PROCESSING SUMMARY")
        print("=" * 80)
        print(f"✅ Successful: {successful}/{len(videos)}")
        print(f"❌ Failed: {failed}/{len(videos)}")
        print(f"📁 Output directory: {output_dir}")
        print("=" * 80)

        return results
