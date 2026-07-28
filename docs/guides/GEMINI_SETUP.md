# Gemini API Integration Setup Guide

This guide explains how to set up and use Gemini API for translation in ReadVision.

## What is Gemini Translation?

ReadVision now supports **two translation providers**:

1. **Google Translate API** (Default)
   - Fast and reliable
   - Requires Google Cloud credentials
   - Uses the same `gcp.json` file as OCR

2. **Gemini AI** (New!)
   - More natural, context-aware translations
   - Better handling of idioms and cultural nuances
   - Supports both Google AI Studio API key and Vertex AI

## Getting Your Gemini API Key

### Option 1: Google AI Studio (Recommended - Free Tier Available)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### Option 2: Vertex AI (Google Cloud)

If you're already using Google Cloud for OCR, you can use the same credentials:

1. Enable Vertex AI API in your Google Cloud project
2. Use your existing `gcp.json` service account file
3. No additional API key needed

## Setup Instructions

### Method 1: Using Environment Variable (Recommended)

1. Create a `.env` file in your project directory:
   ```bash
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

2. Run ReadVision with Gemini translation:
   ```bash
   readvision document.pdf output.txt --translate-to en --use-gemini
   ```

### Method 2: Pass API Key Directly

```bash
readvision document.pdf output.txt --translate-to en --use-gemini --gemini-api-key YOUR_API_KEY
```

### Method 3: Use in Web UI (Streamlit)

1. Run the Streamlit app:
   ```bash
   readvision-ui
   ```

2. In the sidebar:
   - Check "Enable Translation"
   - Select "Gemini AI" as the translation provider
   - Enter your API key (or leave blank if using `.env`)
   - Choose your target language
   - (Optional) Add custom instructions in the text area
   - Upload and process your PDF

## Usage Examples

### CLI Examples

```bash
# Translate Arabic to English using Gemini
readvision arabic_doc.pdf output.txt --translate-to en --use-gemini

# Translate with auto-detect source language
readvision document.pdf output.txt --translate-to es --use-gemini

# Translate with specified source language
readvision arabic_doc.pdf output.txt --translate-to en --translate-from ar --use-gemini

# Using custom API key
readvision document.pdf output.txt --translate-to en --use-gemini --gemini-api-key sk-...

# With custom translation instructions (formal tone)
readvision document.pdf output.txt --translate-to en --use-gemini --translation-instructions "Use formal, professional tone"

# Keep technical terms in original language
readvision technical_doc.pdf output.txt --translate-to en --use-gemini --translation-instructions "Preserve all technical terminology in the source language"

# Multiple instructions
readvision legal_doc.pdf output.txt --translate-to en --use-gemini --translation-instructions "Use formal legal language. Keep all legal terms and citations in original language. Maintain document structure."
```

### Python API Examples

```python
from readvision import PDFOCRProcessor

# Initialize processor
processor = PDFOCRProcessor(credentials_path="gcp.json")

# Process with Gemini translation
processor.process_pdf(
    pdf_path="document.pdf",
    output_path="output.txt",
    translate_to="en",
    translate_from="ar",
    use_gemini=True  # Use Gemini instead of Google Translate
)
)

# With custom instructions
processor.process_pdf(
    pdf_path="document.pdf",
    output_path="output.txt",
    translate_to="en",
    use_gemini=True,
    translation_instructions="Use formal tone and keep technical terms in English"
)
```

## Custom Translation Instructions

The `--translation-instructions` parameter allows you to guide Gemini's translation behavior. This is particularly useful for:

### Common Use Cases

**1. Tone Control**
```bash
--translation-instructions "Use formal, professional language"
--translation-instructions "Use casual, conversational tone"
--translation-instructions "Use academic writing style"
```

**2. Preserving Terminology**
```bash
--translation-instructions "Keep all technical terms in the original language"
--translation-instructions "Preserve brand names and product names"
--translation-instructions "Do not translate legal terminology"
```

**3. Domain-Specific Translation**
```bash
--translation-instructions "This is a medical document. Use proper medical terminology."
--translation-instructions "This is a legal contract. Maintain formal legal language."
--translation-instructions "This is marketing content. Use persuasive, engaging language."
```

**4. Formatting Preservation**
```bash
--translation-instructions "Maintain all formatting, including bullet points and numbering"
--translation-instructions "Preserve the document structure and headings"
```

**5. Cultural Adaptation**
```bash
--translation-instructions "Adapt idioms and cultural references for the target audience"
--translation-instructions "Keep cultural references in the original language with brief explanations"
```

### Examples with Instructions

```bash
# Legal document - preserve legal terms
readvision contract.pdf output.txt \
  --translate-to en \
  --use-gemini \
  --translation-instructions "Legal document: preserve all legal terminology, case citations, and formal language structure"

# Technical manual - keep technical terms
readvision manual.pdf output.txt \
  --translate-to es \
  --use-gemini \
  --translation-instructions "Technical manual: keep all technical terms and product names in English, use clear instructional language"

# Marketing content - engaging tone
readvision brochure.pdf output.txt \
  --translate-to fr \
  --use-gemini \
  --translation-instructions "Marketing brochure: use engaging, persuasive language that appeals to French-speaking audiences"
```

## Where Does the API Key Go?

Your API key is stored in one of these locations (in priority order):

1. **Command-line argument**: `--gemini-api-key YOUR_KEY`
2. **Environment variable**: `.env` file with `GEMINI_API_KEY=...`
3. **System environment**: Export `GEMINI_API_KEY` in your shell

The `.env` file is automatically loaded by ReadVision and is ignored by git (already in `.gitignore`).

## Security Best Practices

1. **Never commit your API key to version control**
   - The `.env` file is already in `.gitignore`
   - Never hardcode API keys in scripts

2. **Use environment variables in production**
   ```bash
   export GEMINI_API_KEY="your-key-here"
   ```

3. **Rotate your keys regularly**
   - Regenerate API keys periodically
   - Delete unused keys in Google AI Studio

## Troubleshooting

### "Gemini API key not provided" Error

**Solution**: Set your API key using one of these methods:
```bash
# Method 1: Create .env file
echo "GEMINI_API_KEY=your_key" > .env

# Method 2: Export environment variable
export GEMINI_API_KEY="your_key"

# Method 3: Pass as argument
readvision doc.pdf out.txt --translate-to en --use-gemini --gemini-api-key your_key
```

### "google-generativeai package not installed" Error

**Solution**: Install the Gemini SDK:
```bash
pip install google-generativeai python-dotenv
```

Or reinstall ReadVision with updated dependencies:
```bash
pip install -r requirements.txt
```

### Translation Quality Issues

- **For formal documents**: Use Google Translate (`--translate-to en` without `--use-gemini`)
- **For conversational text**: Use Gemini (`--translate-to en --use-gemini`)
- Gemini provides more natural translations but may take slightly longer

## Comparison: Google Translate vs Gemini

| Feature | Google Translate | Gemini AI |
|---------|-----------------|-----------|
| Speed | ⚡ Very Fast | 🐢 Moderate |
| Accuracy | ✅ High | ✅ Very High |
| Context Awareness | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Cost | 💰 Pay per character | 💰 Pay per token (Free tier available) |
| Setup | Uses `gcp.json` | Requires API key |
| Best For | Technical docs, formal text | Natural language, conversational text |

## Output Files

When translation is enabled, you'll get these files:

1. `output.txt` - Original extracted text
2. `output.docx` - Original text in Word format
3. `output_translated_en.txt` - Translated text file
4. `output_translated_en.docx` - Translated Word document

## Need Help?

- 📚 [ReadVision Documentation](docs/)
- 🐛 [Report Issues](https://github.com/yourusername/readvision/issues)
- 🔑 [Google AI Studio](https://makersuite.google.com/app/apikey)
- 📖 [Gemini API Documentation](https://ai.google.dev/docs)
