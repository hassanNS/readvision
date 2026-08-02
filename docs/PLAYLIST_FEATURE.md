# YouTube Playlist Feature

## Overview

Version 1.1.0 adds comprehensive YouTube playlist support to ReadVision, allowing you to batch process entire playlists or specific ranges of videos with a single command.

## Quick Start

### Process Entire Playlist
```bash
readvision-youtube "https://www.youtube.com/playlist?list=PLAYLIST_ID" \
    --playlist \
    --output-dir ./playlist_output
```

### Process Specific Range
```bash
# Videos 1-5
readvision-youtube "PLAYLIST_URL" --playlist --output-dir ./output --start 1 --end 5

# From video 10 onwards
readvision-youtube "PLAYLIST_URL" --playlist --output-dir ./output --start 10
```

## Features

### Playlist Extraction
- Automatically extracts all video metadata from playlist
- Shows playlist title and video count
- No downloads until processing begins

### Range Selection
- `--start N`: Start from video N (1-based index)
- `--end N`: Stop at video N (1-based index, inclusive)
- Both parameters are optional
- If omitted, processes all videos

### Batch Processing
- Processes videos sequentially
- Continues even if individual videos fail
- Shows progress for each video
- Provides detailed summary at completion

### Output Organization
- Files numbered by playlist position: `001_`, `002_`, `003_`, etc.
- Each video gets two files:
  - `NNN_video_title_summary.md` - AI summary
  - `NNN_video_title_transcript.txt` - Full transcript
- All files saved to specified output directory

### Error Handling
- Robust error handling per video
- Failed videos don't stop processing
- Detailed error messages for failures
- Success/failure summary at end

## Command Line Options

### Required for Playlists
- `youtube_url`: Playlist URL
- `--playlist`: Flag to enable playlist mode
- `--output-dir DIR`: Output directory for all files

### Optional
- `--start N`: Starting video index (default: 1)
- `--end N`: Ending video index (default: last video)
- `--keep-audio`: Save audio files (default: delete after processing)
- `--audio-dir DIR`: Directory for audio files
- `--no-translate`: Keep original language (default: translate to English)
- `--gemini-api-key KEY`: Override API key

## Examples

### Educational Course Playlist
```bash
# Process entire course
readvision-youtube "https://www.youtube.com/playlist?list=PLxxx" \
    --playlist \
    --output-dir ./course_transcripts

# Output:
# course_transcripts/
# ├── 001_Lecture_1_Introduction_summary.md
# ├── 001_Lecture_1_Introduction_transcript.txt
# ├── 002_Lecture_2_Fundamentals_summary.md
# ├── 002_Lecture_2_Fundamentals_transcript.txt
# └── ...
```

### Conference Talks (Select Range)
```bash
# Process only talks 5-10
readvision-youtube "PLAYLIST_URL" \
    --playlist \
    --output-dir ./conference_talks \
    --start 5 \
    --end 10
```

### Podcast Series (With Audio)
```bash
# Keep audio files for podcast playlist
readvision-youtube "PLAYLIST_URL" \
    --playlist \
    --output-dir ./podcast_transcripts \
    --audio-dir ./podcast_audio \
    --keep-audio
```

### Multilingual Content (No Translation)
```bash
# Process in original language
readvision-youtube "PLAYLIST_URL" \
    --playlist \
    --output-dir ./original_language \
    --no-translate
```

## Output Example

### Console Output
```
📋 YouTube Playlist Transcription & Summary
📺 Playlist URL: https://www.youtube.com/playlist?list=PLxxx
📁 Output directory: ./output
🎯 Processing: All videos in playlist
🌍 Translation: AI will translate non-English content to English

📋 Extracting playlist information...
✅ Found 15 videos in playlist
📊 Playlist title: Python Programming Course
🎯 Processing all 15 videos from playlist

================================================================================
📹 Processing video 1/15: Introduction to Python
================================================================================
📥 Downloading audio from: https://www.youtube.com/watch?v=xxx
✅ Audio downloaded
🎙️  Transcribing audio with Gemini...
✅ Transcription complete (12,450 characters)
📝 Generating detailed summary with quotes...
✅ Summary generated (3,210 characters)
💾 Transcript saved: output/001_Introduction_to_Python_transcript.txt
💾 Summary saved: output/001_Introduction_to_Python_summary.md
✅ Successfully processed video 1

[... continues for each video ...]

================================================================================
📊 PLAYLIST PROCESSING SUMMARY
================================================================================
✅ Successful: 14/15
❌ Failed: 1/15
📁 Output directory: ./output
================================================================================

📋 Detailed Results:
--------------------------------------------------------------------------------
✅ Video 1: Introduction to Python
   📝 output/001_Introduction_to_Python_summary.md
   📄 output/001_Introduction_to_Python_transcript.txt

✅ Video 2: Variables and Data Types
   📝 output/002_Variables_and_Data_Types_summary.md
   📄 output/002_Variables_and_Data_Types_transcript.txt

❌ Video 3: Control Flow
   Error: Private video - download failed

[... etc ...]
```

## Python API

### Process Entire Playlist
```python
from readvision.utils.youtube_processor import YouTubeProcessor

processor = YouTubeProcessor(gemini_api_key="YOUR_KEY")

results = processor.process_playlist(
    playlist_url="https://www.youtube.com/playlist?list=PLAYLIST_ID",
    output_dir="./playlist_output"
)

# Check results
for result in results:
    if result['status'] == 'success':
        print(f"✅ {result['video_title']}")
        print(f"   Transcript: {result['transcript_path']}")
        print(f"   Summary: {result['summary_path']}")
    else:
        print(f"❌ {result['video_title']}: {result['error']}")
```

### Process With Range
```python
results = processor.process_playlist(
    playlist_url="PLAYLIST_URL",
    output_dir="./output",
    start_index=1,
    end_index=5,
    keep_audio=False,
    translate_to_english=True
)
```

### Extract Playlist Info Only
```python
videos = processor.get_playlist_videos("PLAYLIST_URL")

for video in videos:
    print(f"{video['index']}: {video['title']}")
    print(f"   Duration: {video['duration']}s")
    print(f"   URL: {video['url']}")
```

## Implementation Details

### Methods Added

**`get_playlist_videos(playlist_url)`**
- Extracts video metadata without downloading
- Returns list of dictionaries with video info
- Uses yt-dlp's `extract_flat` mode for efficiency

**`process_playlist(playlist_url, output_dir, start_index, end_index, ...)`**
- Batch processes multiple videos
- Handles range filtering
- Error handling per video
- Returns comprehensive results list

### File Naming Convention
- Format: `{index:03d}_{sanitized_title}_{type}.{ext}`
- Index: 3-digit zero-padded (001, 002, 003, ...)
- Title: Sanitized (special chars removed, spaces to underscores)
- Type: `summary` or `transcript`
- Extension: `.md` for summaries, `.txt` for transcripts

### Error Recovery
- Each video processed independently
- Errors logged but don't halt processing
- Failed videos recorded in results
- Summary shows success/failure counts

## Performance Considerations

### Processing Time
- Per video: ~3-4 minutes for 10-minute video
- Depends on: video length, audio quality, network speed
- Sequential processing (one at a time)

### API Costs
- Gemini API calls: 2 per video (transcription + summarization)
- yt-dlp: Free, no API key needed
- Consider Gemini API quotas for large playlists

### Disk Space
- Audio files: ~1MB per minute (if kept)
- Transcripts: ~100KB per 10-minute video
- Summaries: ~50KB per 10-minute video

## Troubleshooting

### "URL does not appear to be a valid playlist"
- Ensure URL contains `list=PLAYLIST_ID`
- Check playlist is public
- Try different URL format

### "Start index out of range"
- Check playlist actually has that many videos
- Remember: 1-based indexing (first video is 1, not 0)

### Some Videos Fail
- Private/restricted videos will fail
- Age-restricted content may fail
- Check individual error messages in summary

### Slow Processing
- Normal for large playlists
- Consider using `--start` and `--end` to process in batches
- Processing is sequential (one video at a time)

## Best Practices

1. **Test with small range first**
   ```bash
   readvision-youtube "PLAYLIST_URL" --playlist --output-dir ./test --start 1 --end 3
   ```

2. **Organize output by topic**
   ```bash
   mkdir -p course/transcripts course/summaries
   readvision-youtube "PLAYLIST_URL" --playlist --output-dir course/transcripts
   ```

3. **Process in batches for large playlists**
   ```bash
   # Videos 1-10
   readvision-youtube "URL" --playlist --output-dir ./batch1 --start 1 --end 10
   # Videos 11-20
   readvision-youtube "URL" --playlist --output-dir ./batch2 --start 11 --end 20
   ```

4. **Check API quotas before large jobs**
   - Gemini has daily quotas
   - Large playlists (>50 videos) may hit limits
   - Consider spreading over multiple days

## Related Documentation

- [YouTube Reference](YOUTUBE_REFERENCE.md) - Complete CLI reference
- [YouTube Quick Start](guides/YOUTUBE_QUICK_START.md) - Getting started guide
- [Main README](../README.md) - Project overview

## Version History

- **v1.1.0** (2025-07-27): Playlist support added
  - `get_playlist_videos()` method
  - `process_playlist()` method
  - CLI flags: `--playlist`, `--output-dir`, `--start`, `--end`
  - Comprehensive documentation

- **v1.0.0**: Initial single video support
