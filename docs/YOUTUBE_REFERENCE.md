# YouTube Transcription - Quick Reference

## One-Line Usage

```bash
readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID"
```

## What You Get

- 📄 `[video_title]_transcript.txt` - Full verbatim transcript
- 📝 `[video_title]_summary.md` - Detailed markdown summary with quotes

## Common Commands

### Basic transcription
```bash
readvision-youtube "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Custom output name
```bash
readvision-youtube "https://youtu.be/VIDEO_ID" -o my_summary.md
```

### Keep audio file
```bash
readvision-youtube "URL" --keep-audio --audio-dir ./audio
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

### 3. Install ReadVision
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
| `youtube_url` | - | YouTube video URL | Required |
| `--output` | `-o` | Output file path | Auto-generated |
| `--keep-audio` | - | Keep audio file | Delete after processing |
| `--audio-dir` | - | Audio save location | Temp directory |
| `--gemini-api-key` | - | Custom API key | `GEMINI_API_KEY` env var |
| `--help` | `-h` | Show help | - |
| `--version` | - | Show version | - |

## Supported URL Formats

All standard YouTube URL formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID&t=123s`
- `https://m.youtube.com/watch?v=VIDEO_ID`

## Tips

✅ **Best Practices**
- Works with videos of any length
- Better audio quality = better transcription
- Supports all languages (powered by Gemini 2.0 Flash)
- Auto-cleans temp files (use `--keep-audio` to save)

⚠️ **Common Issues**
- Missing FFmpeg → Install FFmpeg first
- No API key → Set `GEMINI_API_KEY` environment variable
- Download failed → Check internet connection and URL validity
- Private/restricted videos → Feature doesn't work with restricted content

## Processing Time

Approximate times (varies by video length and internet speed):
- Download: ~30 seconds per 10 min video
- Transcription: ~1-2 minutes per 10 min video
- Summary: ~30-60 seconds

Total: ~3-4 minutes for a 10-minute video

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

```python
from readvision.utils.youtube_processor import YouTubeProcessor

# Initialize
processor = YouTubeProcessor(gemini_api_key="YOUR_KEY")

# Process video
result = processor.process_youtube_video(
    youtube_url="https://www.youtube.com/watch?v=VIDEO_ID",
    output_path="summary.md",
    keep_audio=False
)

# Access results
print(result['summary_path'])      # Path to summary.md
print(result['transcript_path'])   # Path to transcript.txt
print(result['transcript_length']) # Character count
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

### Batch Processing
```bash
#!/bin/bash
# process_videos.sh
while IFS= read -r url; do
    readvision-youtube "$url"
done < video_urls.txt
```

### Custom Directory Structure
```bash
# Create organized output
mkdir -p transcripts summaries audio
readvision-youtube "URL" \
    --output summaries/video1_summary.md \
    --audio-dir audio \
    --keep-audio
```

## Related Features

- **PDF OCR**: `readvision document.pdf output.txt`
- **Translation**: `readvision-translate input.txt output.txt --to en`
- **Streamlit UI**: `readvision-ui`

## Support

- 📚 Full guide: [YOUTUBE_QUICK_START.md](../YOUTUBE_QUICK_START.md)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/readvision/issues)
- 📖 Main docs: [README.md](../README.md)
