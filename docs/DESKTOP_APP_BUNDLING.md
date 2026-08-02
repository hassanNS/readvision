# Desktop App Model Bundling Guide

This guide explains how to bundle Whisper models with an Electron desktop app.

## Overview

For desktop app distribution, you can pre-bundle Whisper models to avoid download on first run.

## Bundling Strategy

### 1. Download Models During Build

Create build script `scripts/download_whisper_models.py`:

```python
#!/usr/bin/env python3
"""Download Whisper models for bundling with desktop app."""

import whisper
import os
import shutil

# Model to bundle (base = good balance of size vs quality)
MODEL_SIZE = "base"
OUTPUT_DIR = "./app-resources/whisper-models"

print(f"Downloading Whisper '{MODEL_SIZE}' model...")

# Download model to cache
model = whisper.load_model(MODEL_SIZE)

# Copy from cache to bundle directory
cache_dir = os.path.expanduser("~/.cache/whisper")
model_file = f"{MODEL_SIZE}.pt"
source = os.path.join(cache_dir, model_file)
destination = os.path.join(OUTPUT_DIR, model_file)

os.makedirs(OUTPUT_DIR, exist_ok=True)
shutil.copy2(source, destination)

print(f"✅ Model bundled at: {destination}")
print(f"📊 Size: {os.path.getsize(destination) / (1024*1024):.1f} MB")
```

### 2. Electron Package Configuration

In `package.json` for Electron Builder:

```json
{
  "build": {
    "extraResources": [
      {
        "from": "app-resources/whisper-models",
        "to": "whisper-models",
        "filter": ["*.pt"]
      }
    ]
  }
}
```

### 3. Python Code for Bundled Models

In your Electron app's Python backend:

```python
import sys
import os

def get_whisper_model_dir():
    """Get path to bundled Whisper models."""
    if getattr(sys, 'frozen', False):
        # Running in bundled app
        base_path = sys._MEIPASS
        return os.path.join(base_path, "whisper-models")
    else:
        # Running in development
        return None  # Use default cache

# Initialize processor with bundled models
processor = YouTubeProcessor(
    gemini_api_key=GEMINI_API_KEY,
    whisper_model="base",
    whisper_model_dir=get_whisper_model_dir()
)
```

### 4. App Size Impact

| Model Bundled | App Size Increase |
|---------------|-------------------|
| None (download on demand) | +0 MB |
| tiny | +39 MB |
| base | +140 MB |
| small | +466 MB |

**Recommendation:** Bundle `base` model (140MB) for best balance.

## User Experience

**With bundled model:**
- ✅ Works offline immediately
- ✅ No first-run download wait
- ✅ Predictable performance
- ❌ Larger app download

**Without bundled model:**
- ✅ Smaller app download
- ❌ Requires internet on first run
- ❌ 2-5 minute wait on first transcription
- ✅ Users can choose model size

## Advanced: Offering Multiple Models

Allow users to choose quality in app settings:

```python
class WhisperConfig:
    MODELS = {
        "fast": "tiny",      # Bundled
        "balanced": "base",  # Bundled
        "quality": "small",  # Download on demand
        "best": "large"      # Download on demand
    }

    def get_model(self, quality_setting):
        return self.MODELS.get(quality_setting, "base")
```

Bundle tiny + base (~180MB total), allow downloading larger models via settings.

## Build Process Integration

### package.json Scripts

```json
{
  "scripts": {
    "prebuild": "python scripts/download_whisper_models.py",
    "build": "electron-builder",
    "build:mac": "electron-builder --mac",
    "build:win": "electron-builder --win",
    "build:linux": "electron-builder --linux"
  }
}
```

### CI/CD Integration

For GitHub Actions:

```yaml
- name: Download Whisper Models
  run: python scripts/download_whisper_models.py

- name: Build Electron App
  run: npm run build
```

## Model Verification

After bundling, verify the model is accessible:

```python
import os

def verify_bundled_model():
    model_dir = get_whisper_model_dir()
    if model_dir:
        model_path = os.path.join(model_dir, "base.pt")
        if os.path.exists(model_path):
            print(f"✅ Bundled model found: {model_path}")
            print(f"📊 Size: {os.path.getsize(model_path) / (1024*1024):.1f} MB")
            return True
    print("❌ Bundled model not found, will download on first use")
    return False
```

## Troubleshooting

### Model Not Found in Bundled App

**Issue**: App tries to download model even though it's bundled

**Solution**:
- Check `whisper_model_dir` path is correct
- Verify model file exists in bundle
- Ensure Electron Builder includes the `extraResources`

### App Size Too Large

**Issue**: App download is too large with bundled model

**Options**:
1. Bundle smaller model (tiny = 39MB)
2. Don't bundle, allow download on first run
3. Offer "lite" version without bundled models

### Permission Issues

**Issue**: Can't read bundled model file

**Solution**:
- Check file permissions in bundle
- Verify path resolution in packaged app
- Test with actual built app, not dev mode

## Related Documentation

- [YouTube Reference](YOUTUBE_REFERENCE.md) - CLI usage
- [Copyright Handling](COPYRIGHT_HANDLING.md) - Whisper benefits
- [Quick Start](../QUICK_START.md) - Installation guide
