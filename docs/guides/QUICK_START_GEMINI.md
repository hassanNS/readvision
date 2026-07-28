# Quick Start: Using Gemini for Translation

Get started with Gemini-powered translation in ReadVision in 3 simple steps!

## Step 1: Get Your API Key

Visit [Google AI Studio](https://makersuite.google.com/app/apikey) and create a free API key.

## Step 2: Add API Key to Your Project

Create a `.env` file in the ReadVision directory:

```bash
GEMINI_API_KEY=your_api_key_here
```

**Where to put your API keys:**
- **Gemini API Key** → `.env` file (for translation)
- **Google Cloud credentials** → `gcp.json` file (for OCR - already configured)

## Step 3: Use Gemini Translation

### Command Line:
```bash
# Translate to English using Gemini
readvision document.pdf output.txt --translate-to en --use-gemini

# Translate to Spanish
readvision document.pdf output.txt --translate-to es --use-gemini
```

### Web Interface:
```bash
# Start the web UI
readvision-ui

# In the UI:
# 1. Enable Translation (checkbox)
# 2. Select "Gemini AI" as provider
# 3. Choose target language
# 4. Process your PDF
```

### Just Want to Translate Text Files?

If you already have a `.txt` file and don't need OCR:

```bash
# Translate text file directly
readvision-translate input.txt output.txt --to en --use-gemini

# With custom instructions
readvision-translate doc.txt translated.txt --to en --use-gemini \
  --instructions "Use formal tone"
```

See [TEXT_TRANSLATION_GUIDE.md](TEXT_TRANSLATION_GUIDE.md) for details!

## You Have Both API Keys? Perfect!

Since you have both Vertex AI and Google AI Studio keys, you can use either:

### Using Google AI Studio Key (Simpler):
```bash
# In .env file:
GEMINI_API_KEY=your_google_ai_studio_key

# Run:
readvision doc.pdf output.txt --translate-to en --use-gemini
```

### Using Vertex AI Key:
```bash
# Use your existing gcp.json
# Gemini will automatically use it through Google Cloud SDK
readvision doc.pdf output.txt --translate-to en --use-gemini
```

## That's It!

Your OCR workflow now includes AI-powered translation:
1. **OCR** → Google Cloud Vision (uses `gcp.json`)
2. **Translation** → Gemini AI (uses `.env` file)

## Example Output

When you process a PDF with translation:

```
✅ Processing complete!

Original files:
📄 output.txt
📝 output.docx

Translated files (Gemini):
🌐 output_translated_en.txt
🌐 output_translated_en.docx
```

Need more details? Check [GEMINI_SETUP.md](GEMINI_SETUP.md) for the complete guide!
