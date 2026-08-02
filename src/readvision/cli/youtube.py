#!/usr/bin/env python3
"""Command line interface for YouTube video transcription and summarization."""

import sys
import argparse

from ..utils.youtube_processor import YouTubeProcessor


def main():
    """Main function for YouTube processing command"""

    parser = argparse.ArgumentParser(
        description='Transcribe and summarize YouTube videos or playlists using Whisper AI (transcription) and Gemini AI (translation/summarization).',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Single video - basic usage (auto-generates output filename)
  readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID"

  # Single video - specify output file
  readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID" --output summary.md

  # Playlist - process all videos
  readvision-youtube "https://www.youtube.com/playlist?list=PLAYLIST_ID" --playlist --output-dir ./playlist_output

  # Playlist - process videos 1-5
  readvision-youtube "https://www.youtube.com/playlist?list=PLAYLIST_ID" --playlist --output-dir ./output --start 1 --end 5

  # Playlist - process videos 10 onwards
  readvision-youtube "PLAYLIST_URL" --playlist --output-dir ./output --start 10

  # Keep the audio files
  readvision-youtube "VIDEO_URL" --output summary.md --keep-audio

  # Save audio to specific directory
  readvision-youtube "VIDEO_URL" --audio-dir ./audio --keep-audio

  # Use custom Gemini API key
  readvision-youtube "VIDEO_URL" --gemini-api-key YOUR_KEY

  # Use fast Whisper model (good for testing)
  readvision-youtube "VIDEO_URL" --whisper-model tiny

  # Use best quality Whisper model
  readvision-youtube "VIDEO_URL" --whisper-model large

Output:
  Single video (with translation, default):
    - [name]_summary.md: Detailed English summary with original quotes
    - [name]_transcript.txt: Full transcript in original language
    - [name]_transcript_en.txt: Full transcript translated to English

  Single video (--no-translate):
    - [name]_summary.md: Summary in original language
    - [name]_transcript.txt: Full transcript in original language

  Playlist (with translation):
    - output-dir/001_video_title_summary.md (English)
    - output-dir/001_video_title_transcript.txt (Original)
    - output-dir/001_video_title_transcript_en.txt (English)
    - ... (three files per video)

Note:
  Whisper is used for audio transcription (runs locally, no API key needed).
  Gemini is used for translation and summarization (requires GEMINI_API_KEY).
  Whisper models download automatically on first use (~40MB to 3GB depending on size).
  Get Gemini key from: https://makersuite.google.com/app/apikey
        '''
    )

    parser.add_argument('youtube_url',
                       help='YouTube video or playlist URL')
    parser.add_argument('--output', '-o',
                       help='Path for the output summary markdown file (single video only, auto-generated if not specified)')
    parser.add_argument('--playlist',
                       action='store_true',
                       help='Process as playlist (extracts and processes all videos in playlist)')
    parser.add_argument('--output-dir',
                       help='Directory for playlist output files (required for playlists)')
    parser.add_argument('--start',
                       type=int,
                       help='Starting video index for playlist (1-based, inclusive)')
    parser.add_argument('--end',
                       type=int,
                       help='Ending video index for playlist (1-based, inclusive)')
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
    parser.add_argument('--whisper-model',
                       default='base',
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper model size (default: base). tiny=fastest, large=best quality')
    parser.add_argument('--version',
                       action='version',
                       version='%(prog)s 1.1.0')

    args = parser.parse_args()

    # Validate arguments
    if args.playlist:
        # Playlist mode
        if not args.output_dir:
            print("Error: --output-dir is required for playlist processing")
            print("Example: readvision-youtube PLAYLIST_URL --playlist --output-dir ./output")
            sys.exit(1)

        if args.output:
            print("Warning: --output is ignored in playlist mode. Use --output-dir instead.")

        if args.start is not None and args.start < 1:
            print("Error: --start must be >= 1")
            sys.exit(1)

        if args.end is not None and args.end < 1:
            print("Error: --end must be >= 1")
            sys.exit(1)

        if args.start is not None and args.end is not None and args.start > args.end:
            print("Error: --start must be <= --end")
            sys.exit(1)

    else:
        # Single video mode
        if args.output_dir:
            print("Warning: --output-dir is only used in playlist mode. Use --output for single videos.")

        if args.start is not None or args.end is not None:
            print("Warning: --start and --end are only used in playlist mode.")

    # Validate YouTube URL
    youtube_url = args.youtube_url
    if not ('youtube.com' in youtube_url or 'youtu.be' in youtube_url):
        print(f"Error: Invalid YouTube URL: {youtube_url}")
        print("URL must contain 'youtube.com' or 'youtu.be'")
        sys.exit(1)

    # Configuration
    GEMINI_API_KEY = args.gemini_api_key
    TRANSLATE_TO_ENGLISH = not args.no_translate

    try:
        # Initialize processor
        processor = YouTubeProcessor(
            gemini_api_key=GEMINI_API_KEY,
            whisper_model=args.whisper_model
        )

        if args.playlist:
            # Playlist mode
            print(f"📋 YouTube Playlist Transcription & Summary")
            print(f"📺 Playlist URL: {youtube_url}")
            print(f"📁 Output directory: {args.output_dir}")
            if args.start or args.end:
                range_str = f"videos {args.start or 1} to {args.end or 'end'}"
                print(f"🎯 Range: {range_str}")
            else:
                print(f"🎯 Processing: All videos in playlist")
            if TRANSLATE_TO_ENGLISH:
                print(f"🌍 Translation: AI will translate non-English content to English")
            else:
                print(f"🌍 Translation: Keep original language")
            if args.keep_audio:
                audio_location = args.audio_dir if args.audio_dir else args.output_dir
                print(f"🔊 Audio files will be saved to: {audio_location}")
            print()

            # Process playlist
            results = processor.process_playlist(
                playlist_url=youtube_url,
                output_dir=args.output_dir,
                start_index=args.start,
                end_index=args.end,
                keep_audio=args.keep_audio,
                audio_dir=args.audio_dir,
                translate_to_english=TRANSLATE_TO_ENGLISH
            )

            # Print detailed results
            print()
            print("📋 Detailed Results:")
            print("-" * 80)
            for result in results:
                if result['status'] == 'success':
                    print(f"✅ Video {result['video_index']}: {result['video_title']}")
                    print(f"   📝 Summary: {result['summary_path']}")
                    print(f"   📄 Original: {result['transcript_path']}")
                    if result.get('transcript_en_path'):
                        print(f"   📄 English: {result['transcript_en_path']}")
                else:
                    print(f"❌ Video {result['video_index']}: {result['video_title']}")
                    print(f"   Error: {result['error']}")
                print()

        else:
            # Single video mode
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

            print(f"🎬 YouTube Video Transcription & Summary")
            print(f"📺 URL: {youtube_url}")
            print(f"📝 Summary will be saved to: {output_path}")
            print(f"📄 Original transcript will be saved to: {output_path.replace('.md', '_transcript.txt')}")
            if TRANSLATE_TO_ENGLISH:
                print(f"📄 English transcript will be saved to: {output_path.replace('.md', '_transcript_en.txt')}")
                print(f"🌍 Translation: AI will translate full transcript and summary to English")
            else:
                print(f"🌍 Translation: Keep original language only")
            if args.keep_audio:
                audio_location = args.audio_dir if args.audio_dir else "same directory as output"
                print(f"🔊 Audio will be saved to: {audio_location}")
            print()

            # Process video
            result = processor.process_youtube_video(
                youtube_url=youtube_url,
                output_path=output_path,
                keep_audio=args.keep_audio,
                audio_dir=args.audio_dir,
                translate_to_english=TRANSLATE_TO_ENGLISH
            )

            print()
            print("=" * 60)
            print("✅ Processing Complete!")
            print("=" * 60)
            print(f"📝 Summary: {result['summary_path']}")
            print(f"📄 Original Transcript: {result['transcript_path']}")
            if result.get('transcript_en_path'):
                print(f"📄 English Transcript: {result['transcript_en_path']}")
            if result.get('audio_path'):
                print(f"🔊 Audio: {result['audio_path']}")
            print()
            print(f"📊 Original transcript length: {result['transcript_length']:,} characters")
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
