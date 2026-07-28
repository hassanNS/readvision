# Text Translation Guide

Translate `.txt` files directly with Gemini AI or Google Translate - **no PDF, no OCR needed!**

## Quick Start

```bash
# Translate a text file to English with Gemini
readvision-translate input.txt output.txt --to en --use-gemini

# That's it! ✅
```

## Why Use This?

### Use `readvision-translate` When:
- ✅ You already have extracted text in a `.txt` file
- ✅ You want to translate text without OCR processing
- ✅ You need fast translation of plain text documents
- ✅ Your PDF was already OCR'd and you just want translation

### Use `readvision` (PDF OCR + Translation) When:
- ✅ You have a scanned PDF that needs OCR first
- ✅ You want OCR and translation in one command
- ✅ You need page-by-page mapping to Word documents

## Command Reference

```bash
readvision-translate <input.txt> <output.txt> --to <language> [options]
```

### Required Parameters

- `input.txt` - Path to your input text file
- `output.txt` - Path for the translated output file
- `--to LANGUAGE` - Target language code (e.g., `en`, `es`, `fr`, `ar`)

### Optional Parameters

- `--from LANGUAGE` - Source language (auto-detect if not specified)
- `--use-gemini` - Use Gemini AI (default: Google Translate)
- `--gemini-api-key KEY` - Your Gemini API key (uses env var if not provided)
- `--instructions "..."` - Custom translation instructions for Gemini
- `--credentials PATH` - Google Cloud credentials file (for Google Translate)
- `--encoding TYPE` - Text file encoding (default: utf-8)

## Examples

### Basic Translation

```bash
# Translate to English with Gemini
readvision-translate arabic.txt english.txt --to en --use-gemini

# Translate to Spanish with Google Translate
readvision-translate document.txt spanish.txt --to es --credentials gcp.json

# Auto-detect source language
readvision-translate mystery.txt output.txt --to en --use-gemini
```

### With Source Language

```bash
# Arabic to English
readvision-translate arabic.txt english.txt --to en --from ar --use-gemini

# Spanish to French
readvision-translate spanish.txt french.txt --to fr --from es --use-gemini
```

### With Custom Instructions

```bash
# Formal tone
readvision-translate doc.txt formal.txt --to en --use-gemini \
  --instructions "Use formal, professional language"

# Preserve technical terms
readvision-translate manual.txt translated.txt --to es --use-gemini \
  --instructions "Keep all technical terminology in English"

# Legal document
readvision-translate contract.txt contract_en.txt --to en --use-gemini \
  --instructions "Legal contract: preserve all legal terms and maintain formal language"

# Marketing content
readvision-translate marketing.txt marketing_fr.txt --to fr --use-gemini \
  --instructions "Marketing content: use engaging, persuasive language for French audiences"
```

### With Custom API Key

```bash
# Pass API key directly
readvision-translate input.txt output.txt --to en --use-gemini \
  --gemini-api-key YOUR_API_KEY_HERE
```

### Different Encodings

```bash
# UTF-16 encoded file
readvision-translate utf16_file.txt output.txt --to en --use-gemini --encoding utf-16

# Latin-1 encoded file
readvision-translate latin1_file.txt output.txt --to en --use-gemini --encoding latin-1
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key (for Gemini)

Create a `.env` file:
```bash
GEMINI_API_KEY=your_api_key_here
```

Or export as environment variable:
```bash
export GEMINI_API_KEY="your_api_key_here"
```

Get your key from: https://makersuite.google.com/app/apikey

### 3. Set Up Google Cloud Credentials (for Google Translate)

If using Google Translate instead of Gemini:
```bash
# Download gcp.json from Google Cloud Console
# Place it in your project directory
```

## Common Use Cases

### Translating OCR Output

You already OCR'd a PDF and now want to translate:

```bash
# 1. Extract text from PDF (already done)
# You have: extracted_text.txt

# 2. Translate with Gemini
readvision-translate extracted_text.txt translated.txt --to en --use-gemini
```

### Batch Translation

Translate multiple files:

```bash
# Using a simple loop
for file in *.txt; do
  readvision-translate "$file" "translated_${file}" --to en --use-gemini
done
```

### Translation Pipeline

Chain with other tools:

```bash
# Extract text from PDF, then translate
pdftotext document.pdf extracted.txt
readvision-translate extracted.txt translated.txt --to en --use-gemini \
  --instructions "Use formal academic tone"
```

### Comparing Translations

Get both Google Translate and Gemini versions:

```bash
# Google Translate version
readvision-translate input.txt google_output.txt --to en --credentials gcp.json

# Gemini version
readvision-translate input.txt gemini_output.txt --to en --use-gemini

# Compare them
diff google_output.txt gemini_output.txt
```

## Output

The command will show:
- File being read
- Translation provider and language direction
- Custom instructions (if provided)
- File size in characters
- Translation progress
- Output file location
- Detected source language
- Sample of translated text

Example output:
```
📖 Reading: arabic.txt
🌐 Translating with Gemini AI: ar → en
📝 Custom instructions: Use formal tone
📄 File size: 5432 characters
⏳ Translating...
✅ Translation complete!
📝 Output saved to: english.txt
🔍 Detected source language: ar
📊 Translated text length: 5891 characters

Sample of translated text:
--------------------------------------------------
This is a formal document discussing the important
aspects of business communication...
--------------------------------------------------
```

## Tips

### ✅ DO:
- Use `--use-gemini` for more natural, context-aware translations
- Provide `--instructions` for domain-specific content (legal, medical, technical)
- Specify `--from` language for faster processing (skips detection)
- Check the sample output to verify translation quality

### ❌ DON'T:
- Translate extremely large files without checking memory (split them first)
- Use this for PDFs (use `readvision` command instead)
- Forget to set your API key (either in `.env` or via `--gemini-api-key`)

## Troubleshooting

### "Input file not found"
Check the file path is correct:
```bash
ls -la input.txt  # Verify file exists
```

### "Gemini API key not provided"
Set your API key:
```bash
echo "GEMINI_API_KEY=your_key" > .env
```

### "google-generativeai package not installed"
Install dependencies:
```bash
pip install google-generativeai python-dotenv
```

### Translation quality issues
Try adding custom instructions:
```bash
--instructions "Use formal tone and preserve technical terminology"
```

### Large files taking too long
Split the file first:
```bash
split -l 1000 large_file.txt chunk_
# Then translate each chunk
```

## Supported Languages

Use standard language codes:
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `ar` - Arabic
- `zh` - Chinese
- `ja` - Japanese
- `ko` - Korean
- `ru` - Russian
- `pt` - Portuguese
- `it` - Italian
- `nl` - Dutch
- `hi` - Hindi
- And many more!

See [GEMINI_SETUP.md](GEMINI_SETUP.md) for a complete list.

## Comparison: Gemini vs Google Translate

| Feature | Google Translate | Gemini AI |
|---------|-----------------|-----------|
| Speed | ⚡ Very Fast | 🐢 Moderate |
| Quality | ✅ Good | ✅ Excellent |
| Context | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Custom Instructions | ❌ No | ✅ Yes |
| Cost | 💰 Pay per char | 💰 Free tier available |
| Best For | Quick translations | Natural, contextual translations |

## Integration with ReadVision Workflow

### Full Workflow Example

```bash
# 1. OCR a PDF to text
readvision scanned_doc.pdf extracted.txt

# 2. Translate the extracted text
readvision-translate extracted.txt translated.txt --to en --use-gemini \
  --instructions "Technical document: preserve terminology"

# 3. Done! You have both original OCR and translation
```

### Or Do It All In One Command

```bash
# OCR + Translation in one step
readvision scanned_doc.pdf output.txt --translate-to en --use-gemini \
  --translation-instructions "Technical document: preserve terminology"
```

Both approaches work! Use `readvision-translate` when you already have text files.

## Need More Help?

- **Full Gemini Setup**: See [GEMINI_SETUP.md](GEMINI_SETUP.md)
- **Custom Instructions**: See [TRANSLATION_INSTRUCTIONS_GUIDE.md](TRANSLATION_INSTRUCTIONS_GUIDE.md)
- **ReadVision Main Docs**: See [README.md](README.md)
