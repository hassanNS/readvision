# ReadVision Documentation Index

Complete documentation for the ReadVision OCR and transcription toolkit.

## 📚 Quick Start Guides

### Getting Started
- **[Main README](../README.md)** - Project overview, installation, and basic usage
- **[Gemini Setup](guides/GEMINI_SETUP.md)** - Setting up Gemini API for AI-powered features
- **[Gemini Quick Start](guides/QUICK_START_GEMINI.md)** - Quick start with Gemini features

### Feature-Specific Guides
- **[YouTube Transcription Quick Start](guides/YOUTUBE_QUICK_START.md)** - Get started with YouTube video transcription
- **[Text Translation Guide](guides/TEXT_TRANSLATION_GUIDE.md)** - Standalone text translation
- **[Translation Instructions Guide](guides/TRANSLATION_INSTRUCTIONS_GUIDE.md)** - Custom translation instructions

## 📖 Reference Documentation

### Quick References
- **[Quick Reference](QUICK_REFERENCE.md)** - Common commands and options
- **[YouTube Reference](YOUTUBE_REFERENCE.md)** - YouTube feature reference card

### Technical Documentation
- **[CLAUDE.md](../CLAUDE.md)** - Architecture and implementation details for AI assistants
- **[YouTube Feature Summary](guides/YOUTUBE_FEATURE_SUMMARY.md)** - Technical implementation of YouTube feature
- **[Word Output](README_word_output.md)** - Word document generation details
- **[Page Ordering Fix](PAGE_ORDERING_FIX.md)** - Page ordering implementation details

## 🎯 Feature Documentation

### PDF OCR Processing
- Extract text from PDFs with Arabic/RTL support
- Automatic page-by-page mapping
- Word document generation
- See: [Main README](../README.md#usage)

### YouTube Transcription
- Download and transcribe YouTube videos
- AI-powered summarization with quotes
- Automatic translation to English
- See: [YouTube Quick Start](guides/YOUTUBE_QUICK_START.md)

### Text Translation
- Standalone text translation
- Google Translate or Gemini AI
- Custom translation instructions
- See: [Text Translation Guide](guides/TEXT_TRANSLATION_GUIDE.md)

## 🛠️ Development

### Setup
```bash
pip install -e ".[dev]"
pre-commit install
```

### Testing
```bash
pytest
pytest --cov=src/readvision
```

### Code Quality
```bash
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/
```

## 📂 Project Structure

```
readvision/
├── src/readvision/
│   ├── core/          # OCR processing
│   ├── utils/         # Translation, YouTube, document creation
│   ├── cli/           # Command-line interfaces
│   └── ui/            # Streamlit interface
├── docs/              # Documentation
│   └── guides/        # User guides
├── examples/          # Example outputs
│   └── outputs/       # Sample processed files
├── outputs/           # User-generated output directory
│   ├── youtube/       # YouTube transcriptions
│   ├── ocr/           # PDF OCR results
│   └── translations/  # Translation outputs
└── tests/             # Test suite
```

## 🔗 External Resources

- [Google AI Studio](https://makersuite.google.com/app/apikey) - Get Gemini API key
- [Google Cloud Console](https://console.cloud.google.com/) - GCP credentials for OCR
- [FFmpeg Download](https://ffmpeg.org/download.html) - Required for YouTube feature

## 💡 Common Tasks

### Process a PDF
```bash
readvision document.pdf outputs/ocr/result.txt
```

### Transcribe YouTube Video
```bash
readvision-youtube "URL" --output outputs/youtube/video_summary.md
```

### Translate Text
```bash
readvision-translate input.txt outputs/translations/output.txt --to en
```

## 🆘 Support

- 📧 Issues: [GitHub Issues](https://github.com/yourusername/readvision/issues)
- 📚 Examples: See [examples/](../examples/) directory
- 🔍 Search docs: Use your IDE's search across this directory

## 📝 License

MIT License - See [LICENSE](../LICENSE) file for details
