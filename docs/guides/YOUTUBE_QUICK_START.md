# YouTube Transcription Quick Start Guide

This guide will help you quickly get started with transcribing and summarizing YouTube videos using ReadVision.

## Prerequisites

1. **Gemini API Key** (Required)
   - Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Set it as an environment variable:
     ```bash
     export GEMINI_API_KEY=your_api_key_here
     ```
   - Or create a `.env` file in your project directory:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

2. **FFmpeg** (Required for audio extraction)
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt-get install ffmpeg`
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Installation

Install ReadVision with the YouTube feature:

```bash
pip install -e .
```

This will install all required dependencies including `yt-dlp`.

## Basic Usage

### Simple Transcription

Process a YouTube video with auto-generated output filename:

```bash
readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID"
```

This will create:
- `[Video_Title]_summary.md` - Detailed summary with quotes
- `[Video_Title]_transcript.txt` - Full verbatim transcript

### Custom Output File

Specify your own output filename:

```bash
readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID" --output my_summary.md
```

Creates:
- `my_summary.md` - Summary file
- `my_transcript.txt` - Transcript file

### Keep Audio File

If you want to keep the downloaded audio:

```bash
readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID" --keep-audio
```

### Save Audio to Specific Directory

```bash
readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID" --audio-dir ./audio --keep-audio
```

## What You Get

### Transcript File (`.txt`)

A verbatim transcription of the entire audio, exactly as spoken.

### Summary File (`.md`)

A comprehensive Markdown document with:
- **Overview**: High-level summary of the video
- **Organized Sections**: Content broken down by topic
- **Direct Quotes**: Extensive quotes from the transcript in blockquote format
- **Key Takeaways**: Important points highlighted
- **Proper Formatting**: Headers, lists, and emphasis

Example summary structure:
```markdown
## Summary
[Overview of the video content]

## Main Topics

### Topic 1: Introduction
[Context and description]

> "This is a direct quote from the video supporting the point"

[Additional analysis]

### Topic 2: Key Concepts
...

## Key Takeaways
- Important point 1
- Important point 2
```

## Advanced Usage

### Using Custom API Key

If you don't want to use environment variables:

```bash
readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID" --gemini-api-key YOUR_API_KEY
```

### Processing Multiple Videos

Create a simple bash script:

```bash
#!/bin/bash
urls=(
  "https://www.youtube.com/watch?v=VIDEO_ID_1"
  "https://www.youtube.com/watch?v=VIDEO_ID_2"
  "https://www.youtube.com/watch?v=VIDEO_ID_3"
)

for url in "${urls[@]}"; do
  readvision-youtube "$url"
done
```

## Tips

1. **Long Videos**: The transcription and summarization process may take a few minutes for longer videos
2. **Audio Quality**: Better audio quality results in better transcriptions
3. **Languages**: Works with any language supported by Gemini (English, Spanish, Arabic, etc.)
4. **Quotes**: The summary is designed to include extensive direct quotes to preserve the original content
5. **Cleanup**: Audio files are automatically deleted unless you use `--keep-audio`

## Troubleshooting

### "Gemini API key not provided"
- Make sure you've set the `GEMINI_API_KEY` environment variable
- Or use the `--gemini-api-key` flag

### "FFmpeg not found"
- Install FFmpeg using the instructions in Prerequisites

### "Failed to download audio"
- Check that the YouTube URL is valid
- Make sure you have internet connection
- Some videos may have download restrictions

### "Transcription failed"
- Large audio files may take longer - be patient
- Check your Gemini API quota
- Ensure the audio file was downloaded successfully

## Example Output

Here's what a typical workflow looks like:

```bash
$ readvision-youtube "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

🎬 YouTube Video Transcription & Summary
📺 URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
📝 Summary will be saved to: Never_Gonna_Give_You_Up_summary.md
📄 Transcript will be saved to: Never_Gonna_Give_You_Up_transcript.txt

📥 Downloading audio from: https://www.youtube.com/watch?v=dQw4w9WgXcQ
✅ Audio downloaded: /tmp/tmpxyz/dQw4w9WgXcQ.mp3
📊 Video title: Rick Astley - Never Gonna Give You Up (Official Video)
📊 Duration: 3 minutes
🎙️  Transcribing audio with Gemini...
📤 Audio file uploaded to Gemini
✅ Transcription complete (2,543 characters)
📝 Generating detailed summary with quotes...
✅ Summary generated (4,821 characters)
💾 Transcript saved: Never_Gonna_Give_You_Up_transcript.txt
💾 Summary saved: Never_Gonna_Give_You_Up_summary.md
🗑️  Temporary audio file removed

============================================================
✅ Processing Complete!
============================================================
📝 Summary: Never_Gonna_Give_You_Up_summary.md
📄 Transcript: Never_Gonna_Give_You_Up_transcript.txt

📊 Transcript length: 2,543 characters
📊 Summary length: 4,821 characters
```

## API Reference

For programmatic usage, see the Python API:

```python
from readvision.utils.youtube_processor import YouTubeProcessor

# Initialize processor
processor = YouTubeProcessor(gemini_api_key="YOUR_API_KEY")

# Process video
result = processor.process_youtube_video(
    youtube_url="https://www.youtube.com/watch?v=VIDEO_ID",
    output_path="summary.md",
    keep_audio=False,
    audio_dir=None
)

print(f"Summary: {result['summary_path']}")
print(f"Transcript: {result['transcript_path']}")
```

## Next Steps

- Check out the [README](README.md) for other ReadVision features
- Learn about PDF OCR processing
- Explore translation capabilities
- Try the Streamlit UI with `readvision-ui`
