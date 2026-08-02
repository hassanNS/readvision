# ReadVision - Quick Start Guide

## What It Does

ReadVision is a local desktop tool with three main capabilities:

1. **PDF OCR Processing** - Extract text from PDFs (especially Arabic/RTL languages)
2. **YouTube Transcription** - Download, transcribe, and summarize YouTube videos with AI
3. **Text Translation** - Translate text using Google Translate or Gemini AI

All processing happens locally on your machine using cloud APIs (Google Cloud Vision, Gemini).

## How It Works

### Architecture

```
ReadVision (Local Python Application)
├── CLI Commands (3 separate tools)
│   ├── readvision           → PDF OCR processing
│   ├── readvision-youtube   → YouTube transcription
│   └── readvision-translate → Text translation
├── Streamlit UI (optional web interface)
└── Cloud Services (API calls only)
    ├── Google Cloud Vision API (PDF OCR)
    ├── Gemini API (AI translation, YouTube summarization)
    └── Google Translate (basic translation)
```

### Dependencies

**Required:**
- Python 3.8+
- FFmpeg (for YouTube audio extraction)
- OpenAI Whisper (auto-installed, downloads models on first use)

**Optional:**
- Gemini API key (for translation and summarization, not required for transcription)
- Google Cloud Vision API credentials (`gcp.json`, for PDF OCR)
- Google Cloud Storage (for PDFs >5 pages)

## Installation

```bash
# Clone repository
git clone <repo-url>
cd readvision

# Install
pip install -e ".[dev]"

# Set up credentials
# 1. Place gcp.json in project root
# 2. Set GEMINI_API_KEY in .env file (optional)
```

## Basic Usage

### 1. PDF OCR Processing

```bash
# Extract text from PDF
readvision document.pdf outputs/ocr/result.txt

# With translation to English
readvision document.pdf outputs/ocr/result.txt --translate --to en
```

**Output:**
- `result.txt` - Extracted text with page breaks
- `result.docx` - Word document with 1:1 page mapping
- `result_translated_en.txt` and `result_translated_en.docx` (if translated)

### 2. YouTube Transcription

#### Single Video
```bash
# Transcribe and summarize YouTube video (auto-translates to English)
readvision-youtube "https://youtube.com/watch?v=VIDEO_ID" --output outputs/youtube/video

# Keep original language
readvision-youtube "URL" --output video --no-translate

# Keep audio file
readvision-youtube "URL" --output video --keep-audio
```

**Output (with translation, default):**
- `video_transcript.txt` - Full transcript in original language
- `video_transcript_en.txt` - Full transcript translated to English
- `video_summary.md` - English summary with original quotes
- `video_audio.mp3` - Downloaded audio (if `--keep-audio` used)

#### Playlist
```bash
# Process entire playlist
readvision-youtube "https://youtube.com/playlist?list=PLAYLIST_ID" --playlist --output-dir outputs/youtube/playlist

# Process videos 1-5 from playlist
readvision-youtube "PLAYLIST_URL" --playlist --output-dir outputs/youtube --start 1 --end 5

# Process from video 10 onwards
readvision-youtube "PLAYLIST_URL" --playlist --output-dir outputs/youtube --start 10
```

**Output (per video, with translation):**
- `001_video_title_transcript.txt` - Full transcript (original language)
- `001_video_title_transcript_en.txt` - Full transcript (English)
- `001_video_title_summary.md` - English summary with original quotes
- (Files numbered by playlist position)

### 3. Text Translation

```bash
# Translate with Google Translate
readvision-translate input.txt outputs/translations/output.txt --to en

# Translate with Gemini AI (more natural)
readvision-translate input.txt output.txt --to en --use-gemini

# With custom instructions
readvision-translate input.txt output.txt --to en --use-gemini \
  --instructions "Use formal academic tone"
```

### 4. Streamlit UI (Optional)

```bash
# Launch web interface
readvision-ui
```

Open browser to `http://localhost:8501`

## Project Structure

```
readvision/
├── src/readvision/
│   ├── core/
│   │   └── processor.py              # PDF OCR processing
│   ├── utils/
│   │   ├── translator.py             # Translation (Google + Gemini)
│   │   ├── youtube_processor.py      # YouTube download/transcription
│   │   ├── document_creator.py       # Word document generation
│   │   └── text_cleaner.py           # Text cleaning
│   ├── cli/
│   │   ├── main.py                   # readvision command
│   │   ├── youtube.py                # readvision-youtube command
│   │   └── translate.py              # readvision-translate command
│   └── ui/
│       └── streamlit_app.py          # Web UI
├── docs/                             # Documentation
│   ├── INDEX.md                      # Complete documentation index
│   └── guides/                       # Feature-specific guides
├── examples/                         # Example outputs
├── outputs/                          # Your output files (gitignored)
│   ├── youtube/
│   ├── ocr/
│   └── translations/
└── tests/                            # Test suite
```

## Key Features

### PDF OCR
- Supports Arabic and RTL languages
- Automatic page ordering
- Creates text files and Word documents
- Optional translation
- Handles small PDFs (<5 pages) and large PDFs (>5 pages) differently

### YouTube Processing
- Downloads audio from any YouTube video
- Transcribes using Gemini 2.0 Flash (fast, accurate)
- Generates detailed markdown summaries with:
  - Original quotes preserved
  - Automatic English translation
  - Organized topics and sections
  - Direct quotes in blockquotes

### Translation
- **Google Translate**: Fast, basic translation
- **Gemini AI**: Natural, context-aware translation
- Custom instructions support
- Preserves formatting

## Current State

**Status:** Fully functional local CLI/UI tool

**Next Steps:**
1. Refine existing code
2. Add more features
3. Package as desktop app (Electron + React)

## See Also

- **[Full Documentation Index](docs/INDEX.md)** - Complete guide to all features
- **[CLAUDE.md](CLAUDE.md)** - Developer/architecture documentation
- **[YouTube Quick Start](docs/guides/YOUTUBE_QUICK_START.md)** - YouTube feature details
- **[Translation Guide](docs/guides/TEXT_TRANSLATION_GUIDE.md)** - Translation usage
