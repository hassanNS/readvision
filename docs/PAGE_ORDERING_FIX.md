# Page Number Ordering Fix - Documentation

## Problem Solved
Previously, the OCR processor relied on the order of responses from Google Cloud Vision API, which could sometimes result in pages being out of order in the final Word document.

## Solution Implemented
The program now uses the `pageNumber` field from the OCR response's `context` object to ensure correct page ordering.

## Key Changes

### 1. Page Number Extraction
```python
# OLD: Simple sequential processing
for page_response in response['responses']:
    if 'fullTextAnnotation' in page_response:
        page_texts.append(page_response['fullTextAnnotation']['text'])

# NEW: Extract page numbers and sort
for page_response in response['responses']:
    if 'fullTextAnnotation' in page_response and 'context' in page_response:
        page_number = page_response['context'].get('pageNumber', 0)
        page_text = page_response['fullTextAnnotation']['text']
        page_data.append((page_number, page_text))
```

### 2. Correct Sorting
```python
# Sort pages by actual page number from OCR
page_data.sort(key=lambda x: x[0])
page_texts = [text for page_num, text in page_data]
page_numbers = [page_num for page_num, text in page_data]
```

### 3. Debug Mode
Added `--debug` flag to help diagnose page ordering issues:

```bash
python translate.py document.pdf output.txt --debug
```

Debug output shows:
- Total pages found
- Page number range (min to max)
- Duplicate page numbers (if any)
- Missing page numbers (if any)
- Preview of first 3 pages

### 4. Accurate Page Headers
Word documents now show the actual page numbers from the PDF:
```
Page 1    <- From PDF page 1
Page 2    <- From PDF page 2
...
Page 100  <- From PDF page 100
```

## Usage Examples

### Basic usage (automatic page ordering):
```bash
python translate.py assets/document.pdf output.txt
```

### With debug information:
```bash
python translate.py assets/document.pdf output.txt --debug
```

### Example debug output:
```
🔍 Debug: Page Order Information
Total pages found: 50
Page numbers found: [1, 2, 3, 4, ..., 50]
Min page: 1, Max page: 50
First 3 pages preview:
  Page 1: This is the beginning of the document...
  Page 2: Chapter 1 starts here with important...
  Page 3: The methodology section describes...
```

## Benefits
1. **Correct Order**: Pages appear in the right sequence regardless of API response order
2. **Accurate Headers**: Page numbers in Word docs match original PDF pages
3. **Debugging**: Easy to identify and fix page ordering issues
4. **Reliability**: Handles edge cases like missing context or duplicate page numbers

## Technical Details
- Works for both small PDFs (≤5 pages) and large PDFs (>5 pages)
- Fallback to sequential numbering if page numbers unavailable
- Maintains backward compatibility with existing features
- Preserves all Arabic/RTL formatting and other enhancements
