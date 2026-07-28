# Custom Translation Instructions Guide

Get better translations from Gemini by providing custom instructions!

## What Are Translation Instructions?

Translation instructions are additional guidelines you give to Gemini to customize how it translates your documents. This feature is **only available when using Gemini** (not Google Translate).

## Quick Examples

```bash
# Keep it simple - formal tone
readvision doc.pdf output.txt --translate-to en --use-gemini \
  --translation-instructions "Use formal tone"

# Preserve technical terms
readvision manual.pdf output.txt --translate-to es --use-gemini \
  --translation-instructions "Keep technical terminology in English"

# Multiple instructions
readvision contract.pdf output.txt --translate-to fr --use-gemini \
  --translation-instructions "Use formal legal language. Preserve all legal terms. Maintain document structure."
```

## When to Use Custom Instructions

### ✅ Use Instructions When:
- You need a specific tone (formal, casual, academic)
- You want to preserve certain terms (technical, legal, brand names)
- The document has a specific purpose (legal, medical, marketing)
- You need cultural adaptation
- You want to maintain specific formatting

### ❌ Don't Need Instructions When:
- You just want a standard translation
- The document is straightforward
- Google Translate's default behavior is fine

## Instruction Templates

### By Document Type

**Legal Documents:**
```bash
--translation-instructions "Legal document: preserve all legal terminology, citations, and formal language structure"
```

**Medical Documents:**
```bash
--translation-instructions "Medical document: use proper medical terminology and maintain clinical precision"
```

**Technical Manuals:**
```bash
--translation-instructions "Technical manual: keep all technical terms, product names, and model numbers in English"
```

**Marketing Content:**
```bash
--translation-instructions "Marketing content: use engaging, persuasive language that resonates with the target audience"
```

**Academic Papers:**
```bash
--translation-instructions "Academic paper: use scholarly language and maintain citation formats"
```

**Business Correspondence:**
```bash
--translation-instructions "Business letter: use professional, courteous language appropriate for corporate communication"
```

### By Tone

**Formal:**
```bash
--translation-instructions "Use formal, professional language"
```

**Casual:**
```bash
--translation-instructions "Use conversational, friendly tone"
```

**Neutral:**
```bash
--translation-instructions "Use neutral, objective language"
```

### By Preservation Needs

**Preserve All Technical Terms:**
```bash
--translation-instructions "Keep all technical terminology in the original language"
```

**Preserve Brand Names:**
```bash
--translation-instructions "Do not translate brand names, product names, or company names"
```

**Preserve Numbers and Dates:**
```bash
--translation-instructions "Keep all numbers, dates, and measurements in their original format"
```

## Using in Web UI (Streamlit)

1. Launch the web UI: `readvision-ui`
2. In the sidebar:
   - Enable Translation ✓
   - Select "Gemini AI" as provider
   - You'll see a text area labeled **"Custom Instructions (Optional)"**
   - Enter your instructions (e.g., "Use formal tone")
3. Process your PDF

## Python API

```python
from readvision import PDFOCRProcessor

processor = PDFOCRProcessor(credentials_path="gcp.json")

processor.process_pdf(
    pdf_path="document.pdf",
    output_path="output.txt",
    translate_to="en",
    use_gemini=True,
    translation_instructions="Use formal tone and preserve technical terms"
)
```

## Tips for Writing Good Instructions

### ✅ DO:
- Be specific and clear
- Use simple language
- Combine multiple instructions with periods or commas
- Mention the document type if relevant
- Specify what to preserve

### ❌ DON'T:
- Use overly complex or contradictory instructions
- Write paragraphs (keep it concise - 1-3 sentences)
- Include irrelevant information
- Use vague terms like "translate well" (be specific!)

## Examples by Industry

### Healthcare
```bash
readvision patient_records.pdf output.txt --translate-to en --use-gemini \
  --translation-instructions "Medical record: use standard medical terminology, preserve all medication names and dosages"
```

### Legal
```bash
readvision agreement.pdf output.txt --translate-to es --use-gemini \
  --translation-instructions "Legal agreement: maintain formal legal language, preserve all legal terms and clause numbering"
```

### Technology
```bash
readvision api_docs.pdf output.txt --translate-to ja --use-gemini \
  --translation-instructions "Technical documentation: keep all code snippets, API names, and technical terms in English"
```

### Education
```bash
readvision textbook.pdf output.txt --translate-to fr --use-gemini \
  --translation-instructions "Educational textbook: use clear, instructional language appropriate for students"
```

### Real Estate
```bash
readvision property_listing.pdf output.txt --translate-to en --use-gemini \
  --translation-instructions "Real estate listing: use descriptive, appealing language while maintaining factual accuracy"
```

## Advanced Examples

### Combining Multiple Requirements
```bash
readvision report.pdf output.txt --translate-to de --use-gemini \
  --translation-instructions "Business report: use formal professional tone, preserve all company names and financial terms, maintain table formatting and section headers"
```

### Cultural Adaptation
```bash
readvision marketing.pdf output.txt --translate-to zh --use-gemini \
  --translation-instructions "Marketing material: adapt idioms and cultural references for Chinese-speaking audiences while maintaining the persuasive tone"
```

### Technical + Tone
```bash
readvision whitepaper.pdf output.txt --translate-to en --use-gemini \
  --translation-instructions "Technical whitepaper: use authoritative but accessible language, keep technical acronyms in English, explain complex concepts clearly"
```

## No Instructions Needed?

If you don't provide instructions, Gemini will use its default translation behavior, which is generally excellent for standard documents. Instructions are **optional** but powerful when you need specific results!

## Troubleshooting

**Q: My instructions aren't being followed**
- Make sure you're using `--use-gemini` flag
- Keep instructions clear and specific
- Try simplifying your instructions

**Q: Can I use instructions with Google Translate?**
- No, custom instructions only work with Gemini API

**Q: How long can my instructions be?**
- Keep it concise (1-3 sentences recommended)
- Too long might dilute the effectiveness

**Q: Can I save my instructions for reuse?**
- Create a shell script or bash alias with your common instructions
- In Python API, create preset configurations

## Need More Help?

Check out the full [GEMINI_SETUP.md](GEMINI_SETUP.md) guide for complete Gemini integration details!
