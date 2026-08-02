# YouTube Transcription - Quick Reference

## One-Line Usage

```bash
readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID"
```

## What You Get

**With Translation (default):**
- 📄 `[video_title]_transcript.txt` - Full transcript in original language
- 📄 `[video_title]_transcript_en.txt` - Full transcript translated to English
- 📝 `[video_title]_summary.md` - Detailed English summary with original quotes

**Without Translation (`--no-translate`):**
- 📄 `[video_title]_transcript.txt` - Full transcript in original language
- 📝 `[video_title]_summary.md` - Summary in original language

## Common Commands

### Single Video - Basic transcription
```bash
readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Single Video - Custom output name
```bash
readvision-youtube "https://youtu.be/VIDEO_ID" -o my_summary.md
```

### Single Video - Keep audio file
```bash
readvision-youtube "URL" --keep-audio --audio-dir ./audio
```

### Playlist - Process all videos
```bash
readvision-youtube "https://www.youtube.com/playlist?list=PLAYLIST_ID" --playlist --output-dir ./playlist_output
```

### Playlist - Process specific range (videos 1-5)
```bash
readvision-youtube "PLAYLIST_URL" --playlist --output-dir ./output --start 1 --end 5
```

### Playlist - Process from video 10 onwards
```bash
readvision-youtube "PLAYLIST_URL" --playlist --output-dir ./output --start 10
```

### Use custom API key
```bash
readvision-youtube "URL" --gemini-api-key YOUR_KEY
```

## Setup

### 1. Install FFmpeg
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### 2. Get Gemini API Key
- Visit: https://makersuite.google.com/app/apikey
- Create free API key
- Set environment variable:
  ```bash
  export GEMINI_API_KEY=your_api_key_here
  ```

### 3. Whisper Models (Automatic)

Whisper models download automatically on first use and are cached at `~/.cache/whisper/`:

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| tiny | 39MB | Fastest | Good | Quick tests, simple audio |
| base | 140MB | Fast | Better | **Default - balanced** |
| small | 466MB | Medium | Great | High-quality transcription |
| medium | 1.5GB | Slow | Excellent | Difficult audio, accents |
| large | 2.9GB | Slowest | Best | Professional quality |

**First-time setup:**
```bash
# First transcription downloads the model (one-time wait)
readvision-youtube "URL"  # Downloads base model (~140MB)

# Subsequent transcriptions use cached model (instant)
readvision-youtube "URL"  # Loads from cache
```

**Choose model size:**
```bash
# Fast mode (good for testing)
readvision-youtube "URL" --whisper-model tiny

# Balanced (default)
readvision-youtube "URL" --whisper-model base

# Best quality (for important content)
readvision-youtube "URL" --whisper-model large
```

### 4. Install ReadVision
```bash
pip install -e .
```

## Output Format

### Transcript (`.txt`)
```
[Verbatim transcription of all spoken words]
```

### Summary (`.md`)
```markdown
## Summary
[High-level overview]

## Main Topics

### Topic 1
[Description and context]

> "Direct quote from the video"

[Analysis and details]

### Topic 2
...

## Key Takeaways
- Point 1
- Point 2
```

## CLI Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `youtube_url` | - | YouTube video or playlist URL | Required |
| `--output` | `-o` | Output file path (single video only) | Auto-generated |
| `--playlist` | - | Process as playlist | False |
| `--output-dir` | - | Output directory (playlist mode) | Required for playlists |
| `--start` | - | Starting video index (1-based) | 1 |
| `--end` | - | Ending video index (1-based) | Last video |
| `--keep-audio` | - | Keep audio file(s) | Delete after processing |
| `--audio-dir` | - | Audio save location | Temp directory |
| `--no-translate` | - | Keep original language | Translate to English |
| `--whisper-model` | - | Whisper model size (tiny/base/small/medium/large) | base |
| `--gemini-api-key` | - | Custom Gemini API key | `GEMINI_API_KEY` env var |
| `--help` | `-h` | Show help | - |
| `--version` | - | Show version | - |

## Supported URL Formats

### Single Video
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID&t=123s`
- `https://m.youtube.com/watch?v=VIDEO_ID`

### Playlist
- `https://www.youtube.com/playlist?list=PLAYLIST_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID&list=PLAYLIST_ID`

## Tips

✅ **Best Practices**
- Works with videos of any length
- Better audio quality = better transcription
- Supports 99+ languages (powered by Whisper)
- Auto-cleans temp files (use `--keep-audio` to save)
- Use larger models for better accuracy on difficult audio
- First transcription downloads model (subsequent runs are instant)

⚠️ **Common Issues**
- Missing FFmpeg → Install FFmpeg first
- No API key → Set `GEMINI_API_KEY` (for translation/summary only)
- Download failed → Check internet connection and URL validity
- Private/restricted videos → Feature doesn't work with restricted content
- Slow transcription → Use smaller Whisper model (`--whisper-model tiny`)
- Out of memory → Use smaller model or close other applications

## Processing Time

Approximate times (varies by video length, hardware, and model):

**First Time (includes model download):**
- Model download: 30 seconds - 5 minutes (depending on model size and connection)
- Download audio: ~30 seconds per 10 min video
- Transcription (base model): ~2-5 minutes per 10 min video
- Translation: ~30-60 seconds
- Summary: ~30-60 seconds

**Subsequent Runs (model cached):**
- Download audio: ~30 seconds per 10 min video
- Transcription (base model): ~2-5 minutes per 10 min video
- Translation: ~30-60 seconds
- Summary: ~30-60 seconds

**Model Comparison (10-minute video):**
- tiny: ~1-2 minutes (good accuracy)
- base: ~2-5 minutes (better accuracy)
- small: ~5-8 minutes (great accuracy)
- medium: ~8-12 minutes (excellent accuracy)
- large: ~12-20 minutes (best accuracy)

*Times assume CPU-only. GPU acceleration can be 3-10x faster.*

## Example Workflow

```bash
# 1. Set API key (one time)
export GEMINI_API_KEY=your_key_here

# 2. Process video
readvision-youtube "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Output:
# 📥 Downloading audio...
# ✅ Audio downloaded
# 🎙️ Transcribing...
# ✅ Transcription complete
# 📝 Generating summary...
# ✅ Summary complete
# 💾 Files saved

# 3. Read your files
cat Rick_Astley_Never_Gonna_Give_You_Up_transcript.txt
open Rick_Astley_Never_Gonna_Give_You_Up_summary.md
```

## Python API

### Single Video Processing
```python
from readvision.utils.youtube_processor import YouTubeProcessor

# Initialize
processor = YouTubeProcessor(gemini_api_key="YOUR_KEY")

# Process video
result = processor.process_youtube_video(
    youtube_url="https://www.youtube.com/watch?v=VIDEO_ID",
    output_path="summary.md",
    keep_audio=False,
    translate_to_english=True
)

# Access results
print(result['summary_path'])         # Path to summary.md (English)
print(result['transcript_path'])      # Path to transcript.txt (original language)
print(result['transcript_en_path'])   # Path to transcript_en.txt (English, if translated)
print(result['transcript_length'])    # Character count
```

### Playlist Processing
```python
from readvision.utils.youtube_processor import YouTubeProcessor

# Initialize
processor = YouTubeProcessor(gemini_api_key="YOUR_KEY")

# Process entire playlist
results = processor.process_playlist(
    playlist_url="https://www.youtube.com/playlist?list=PLAYLIST_ID",
    output_dir="./output",
    keep_audio=False,
    translate_to_english=True
)

# Process with range
results = processor.process_playlist(
    playlist_url="PLAYLIST_URL",
    output_dir="./output",
    start_index=1,
    end_index=5,
    keep_audio=False
)

# Check results
for result in results:
    if result['status'] == 'success':
        print(f"✅ {result['video_title']}")
        print(f"   Summary: {result['summary_path']}")
    else:
        print(f"❌ {result['video_title']}: {result['error']}")
```

## Troubleshooting

### "Command not found: readvision-youtube"
```bash
# Reinstall package
pip install -e .
```

### "Gemini API key not provided"
```bash
# Set environment variable
export GEMINI_API_KEY=your_key
# Or use flag
readvision-youtube "URL" --gemini-api-key YOUR_KEY
```

### "FFmpeg not found"
```bash
# Install FFmpeg (see Setup section)
# Verify installation
ffmpeg -version
```

### "Failed to download audio"
- Check URL is correct
- Ensure video is public
- Check internet connection
- Try different URL format

## Advanced Usage

### Batch Processing with Playlists
```bash
# Process entire course/series playlist
readvision-youtube "PLAYLIST_URL" --playlist --output-dir ./course_transcripts

# Process only lectures 5-10 from a course
readvision-youtube "PLAYLIST_URL" --playlist --output-dir ./lectures --start 5 --end 10
```

### Manual Batch Processing
```bash
#!/bin/bash
# process_videos.sh - for individual videos
while IFS= read -r url; do
    readvision-youtube "$url"
done < video_urls.txt
```

### Custom Directory Structure
```bash
# Single video with organized output
mkdir -p transcripts summaries audio
readvision-youtube "URL" \
    --output summaries/video1_summary.md \
    --audio-dir audio \
    --keep-audio

# Playlist with organized output
readvision-youtube "PLAYLIST_URL" \
    --playlist \
    --output-dir ./course_materials \
    --audio-dir ./course_audio \
    --keep-audio
```

### Playlist Output Structure

**With Translation (default):**
```
output_dir/
├── 001_First_Video_Title_summary.md           # English summary
├── 001_First_Video_Title_transcript.txt       # Original language (full)
├── 001_First_Video_Title_transcript_en.txt    # English (full)
├── 002_Second_Video_Title_summary.md
├── 002_Second_Video_Title_transcript.txt
├── 002_Second_Video_Title_transcript_en.txt
├── 003_Third_Video_Title_summary.md
├── 003_Third_Video_Title_transcript.txt
└── 003_Third_Video_Title_transcript_en.txt
```

**Without Translation (`--no-translate`):**
```
output_dir/
├── 001_First_Video_Title_summary.md           # Original language summary
├── 001_First_Video_Title_transcript.txt       # Original language (full)
├── 002_Second_Video_Title_summary.md
├── 002_Second_Video_Title_transcript.txt
├── 003_Third_Video_Title_summary.md
└── 003_Third_Video_Title_transcript.txt
```

## Related Features

- **PDF OCR**: `readvision document.pdf output.txt`
- **Translation**: `readvision-translate input.txt output.txt --to en`
- **Streamlit UI**: `readvision-ui`

## Related Documentation

- 📚 [YouTube Quick Start](guides/YOUTUBE_QUICK_START.md) - Getting started guide
- 📋 [Playlist Feature](PLAYLIST_FEATURE.md) - Playlist processing details
- ⚖️ [Copyright Handling](COPYRIGHT_HANDLING.md) - Copyright detection and fallback
- 🐛 [GitHub Issues](https://github.com/yourusername/readvision/issues) - Bug reports
- 📖 [Main README](../README.md) - Project overview
