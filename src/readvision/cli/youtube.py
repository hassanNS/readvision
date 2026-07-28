#!/usr/bin/env python3
"""Command line interface for YouTube video transcription and summarization."""

import sys
import argparse

from ..utils.youtube_processor import YouTubeProcessor


def main():
    """Main function for YouTube processing command"""

    parser = argparse.ArgumentParser(
        description='Transcribe and summarize YouTube videos using Gemini AI. Creates detailed markdown summary with original quotes from the audio transcript.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Basic usage (auto-generates output filename)
  readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID"

  # Specify output file
  readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID" --output summary.md

  # Keep the audio file
  readvision-youtube "https://youtu.be/VIDEO_ID" --output summary.md --keep-audio

  # Save audio to specific directory
  readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID" --audio-dir ./audio --keep-audio

  # Use custom Gemini API key
  readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID" --gemini-api-key YOUR_KEY

Output:
  Creates two files:
  - [name]_summary.md: Detailed summary with quotes in Markdown format
  - [name]_transcript.txt: Full verbatim transcript

Note:
  Requires GEMINI_API_KEY environment variable or --gemini-api-key parameter.
  Get your free API key from: https://makersuite.google.com/app/apikey
        '''
    )

    parser.add_argument('youtube_url',
                       help='YouTube video URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)')
    parser.add_argument('--output', '-o',
                       help='Path for the output summary markdown file (auto-generated if not specified)')
    parser.add_argument('--keep-audio',
                       action='store_true',
                       help='Keep the downloaded audio file (deleted by default)')
    parser.add_argument('--audio-dir',
                       help='Directory to save audio file (uses temp directory if not specified)')
    parser.add_argument('--gemini-api-key',
                       help='Gemini API key (optional, uses GEMINI_API_KEY env var if not provided)')
    parser.add_argument('--no-translate',
                       action='store_true',
                       help='Keep summary in original language (default: translate to English)')
    parser.add_argument('--version',
                       action='version',
                       version='%(prog)s 1.0.0')

    args = parser.parse_args()

    # Validate YouTube URL
    youtube_url = args.youtube_url
    if not ('youtube.com' in youtube_url or 'youtu.be' in youtube_url):
        print(f"Error: Invalid YouTube URL: {youtube_url}")
        print("URL must contain 'youtube.com' or 'youtu.be'")
        sys.exit(1)

    # Generate output filename if not provided
    if args.output:
        output_path = args.output
    else:
        # Extract video ID and create filename
        try:
            import yt_dlp
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(youtube_url, download=False)
                video_title = info.get('title', 'youtube_video')
                # Clean filename
                import re
                clean_title = re.sub(r'[^\w\s-]', '', video_title)
                clean_title = re.sub(r'[-\s]+', '_', clean_title)
                output_path = f"{clean_title[:50]}_summary.md"
        except Exception as e:
            print(f"Warning: Could not extract video title: {e}")
            output_path = "youtube_summary.md"

    # Ensure output path ends with .md
    if not output_path.endswith('.md'):
        output_path += '.md'

    # Configuration
    YOUTUBE_URL = youtube_url
    OUTPUT_PATH = output_path
    KEEP_AUDIO = args.keep_audio
    AUDIO_DIR = args.audio_dir
    GEMINI_API_KEY = args.gemini_api_key
    TRANSLATE_TO_ENGLISH = not args.no_translate

    print(f"🎬 YouTube Video Transcription & Summary")
    print(f"📺 URL: {YOUTUBE_URL}")
    print(f"📝 Summary will be saved to: {OUTPUT_PATH}")
    print(f"📄 Transcript will be saved to: {OUTPUT_PATH.replace('.md', '_transcript.txt')}")
    if TRANSLATE_TO_ENGLISH:
        print(f"🌍 Translation: AI will translate non-English content to English")
    else:
        print(f"🌍 Translation: Keep original language")
    if KEEP_AUDIO:
        audio_location = AUDIO_DIR if AUDIO_DIR else "same directory as output"
        print(f"🔊 Audio will be saved to: {audio_location}")
    print()

    try:
        # Initialize processor
        processor = YouTubeProcessor(gemini_api_key=GEMINI_API_KEY)

        # Process video
        result = processor.process_youtube_video(
            youtube_url=YOUTUBE_URL,
            output_path=OUTPUT_PATH,
            keep_audio=KEEP_AUDIO,
            audio_dir=AUDIO_DIR,
            translate_to_english=TRANSLATE_TO_ENGLISH
        )

        print()
        print("=" * 60)
        print("✅ Processing Complete!")
        print("=" * 60)
        print(f"📝 Summary: {result['summary_path']}")
        print(f"📄 Transcript: {result['transcript_path']}")
        if result.get('audio_path'):
            print(f"🔊 Audio: {result['audio_path']}")
        print()
        print(f"📊 Transcript length: {result['transcript_length']:,} characters")
        print(f"📊 Summary length: {result['summary_length']:,} characters")
        print()

        # Show sample of summary
        with open(result['summary_path'], 'r', encoding='utf-8') as f:
            summary_preview = f.read(500)
            print("Preview of summary:")
            print("-" * 60)
            print(summary_preview)
            if result['summary_length'] > 500:
                print("\n[... content continues ...]")
            print("-" * 60)

    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
