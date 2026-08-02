# Transcription with Whisper

ReadVision uses OpenAI Whisper for audio transcription, which runs entirely on your local machine.

## No Copyright Restrictions

Unlike cloud-based transcription services, Whisper:

✅ **Runs locally on your computer**
- No content uploaded to external services for transcription
- Complete privacy for audio processing

✅ **No content restrictions**
- Works with any publicly accessible YouTube video
- No copyright filters or safety blocks
- No API quotas or rate limits for transcription

✅ **Offline capable (after model download)**
- Models cached at `~/.cache/whisper/`
- Transcription works without internet connection
- Only translation/summarization requires internet (Gemini API)

## When Transcription May Fail

Whisper transcription only fails if:
- ❌ Audio file is corrupted or inaccessible
- ❌ Insufficient disk space for models (~40MB to 3GB)
- ❌ Insufficient RAM (especially for large models)
- ❌ Audio format issues (rare - yt-dlp handles conversion)

## Model Requirements

| Model | Disk Space | RAM | Best For |
|-------|-----------|-----|----------|
| tiny | 39MB | 1GB | Testing, simple audio |
| base | 140MB | 1GB | General use (default) |
| small | 466MB | 2GB | High quality |
| medium | 1.5GB | 5GB | Difficult audio |
| large | 2.9GB | 10GB | Professional quality |

## Related Documentation

- [YouTube Reference](YOUTUBE_REFERENCE.md) - CLI usage and options
- [Quick Start](../QUICK_START.md) - Getting started guide
