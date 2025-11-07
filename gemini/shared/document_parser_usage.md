# Document Parser - Usage Guide for Gemini

## What It Does

Universal document parser that handles:
- ✅ PDF (.pdf)
- ✅ Text (.txt, .md)
- ✅ JSON (.json, .jsonl)
- ✅ CSV (.csv)
- ✅ Word (.docx)
- ✅ HTML (.html, .htm)
- ✅ YouTube transcripts

## Quick Start

### Install Dependencies

```bash
# Core (required)
pip install PyPDF2 python-docx beautifulsoup4

# For YouTube transcripts
pip install youtube-transcript-api==0.6.1
```

### Basic Usage

```python
from document_parser import parse_document

# Parse any document
result = parse_document('document.pdf')

if result.success:
    print(result.content)  # Full text content
    print(f"Words: {result.word_count}")
    print(f"Format: {result.format}")
else:
    print(f"Error: {result.error}")
```

## Usage Examples

### 1. Parse PDF
```python
from document_parser import parse_document

result = parse_document('crypto_whitepaper.pdf')
if result.success:
    print(f"Pages: {result.metadata['page_count']}")
    print(f"Words: {result.word_count}")
    print(result.content)
```

### 2. Parse YouTube Transcript
```python
from document_parser import parse_youtube_transcript

# Just need video ID
result = parse_youtube_transcript('dQw4w9WgXcQ')
if result.success:
    print(f"Segments: {result.metadata['segment_count']}")
    print(result.content)
```

### 3. Parse YouTube with Timestamps
```python
from document_parser import YouTubeTranscriptParser

parser = YouTubeTranscriptParser()
result = parser.parse_transcript_with_timestamps('dQw4w9WgXcQ')

if result.success:
    print(result.content)
    # Output format:
    # [00:00] Never gonna give you up
    # [00:03] Never gonna let you down
    # [00:06] Never gonna run around
```

### 4. Parse Multiple Files
```python
from document_parser import BatchDocumentParser

batch = BatchDocumentParser()

# Parse all PDFs in directory
results = batch.parse_directory('documents/', '*.pdf')

# Get summary
summary = batch.get_summary(results)
print(f"Processed: {summary['successful']} files")
print(f"Total words: {summary['total_words']:,}")
```

### 5. Parse JSON/JSONL
```python
from document_parser import parse_document

# Parse JSON
result = parse_document('data.json')
if result.success:
    json_data = result.metadata['json_data']  # Parsed Python object
    print(f"Keys: {result.metadata['keys']}")

# Parse JSONL
result = parse_document('batch.jsonl')
if result.success:
    lines = result.metadata['jsonl_data']  # List of dicts
    print(f"Lines: {result.metadata['line_count']}")
```

### 6. Parse Markdown with Sections
```python
from document_parser import parse_document

result = parse_document('README.md')
if result.success:
    # Get sections
    for section in result.sections:
        print(f"{'#' * section['level']} {section['title']}")
        print(section['content'][:100])
```

### 7. Parse CSV
```python
from document_parser import parse_document

result = parse_document('data.csv')
if result.success:
    headers = result.metadata['headers']
    rows = result.metadata['csv_data']
    print(f"Columns: {headers}")
    print(f"Rows: {len(rows)}")
```

## Advanced Usage

### Custom Parser Instance

```python
from document_parser import DocumentParser

parser = DocumentParser()

# Parse multiple files
files = ['doc1.pdf', 'doc2.txt', 'doc3.md']
for file in files:
    result = parser.parse(file)
    if result.success:
        print(f"{file}: {result.word_count} words")
```

### YouTube Parser with Options

```python
from document_parser import YouTubeTranscriptParser

parser = YouTubeTranscriptParser(api_version="0.6.1")

# Try multiple languages
result = parser.parse_transcript(
    video_id='dQw4w9WgXcQ',
    languages=['en', 'es', 'fr']
)

if result.success:
    detected_lang = result.metadata['language_detected']
    print(f"Language: {detected_lang}")
    print(result.content)
```

### Batch Processing with Error Handling

```python
from document_parser import BatchDocumentParser

batch = BatchDocumentParser()

# Parse all files
results = batch.parse_directory('documents/')

# Separate successful and failed
successful = [r for r in results if r.success]
failed = [r for r in results if not r.success]

print(f"Success: {len(successful)}")
print(f"Failed: {len(failed)}")

# Show errors
for r in failed:
    print(f"  {r.file_path}: {r.error}")
```

## Integration with Your Workflow

### Example: Extract Q&A from YouTube Transcripts

```python
from document_parser import parse_youtube_transcript
import json

def process_youtube_video(video_id):
    """Extract transcript and prepare for Q&A generation"""

    # Get transcript
    result = parse_youtube_transcript(video_id)

    if not result.success:
        print(f"Error: {result.error}")
        return None

    # Prepare data for processing
    data = {
        'video_id': video_id,
        'transcript': result.content,
        'segments': result.metadata['segment_count'],
        'word_count': result.word_count,
        'raw_data': result.metadata['raw_transcript']
    }

    # Save for batch processing
    output_file = f'youtube_{video_id}_transcript.json'
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Saved: {output_file}")
    return data

# Use it
data = process_youtube_video('dQw4w9WgXcQ')
```

### Example: Process Multiple PDFs for Q&A

```python
from document_parser import BatchDocumentParser
import json

def process_pdf_directory(directory):
    """Process all PDFs in directory for Q&A generation"""

    batch = BatchDocumentParser()
    results = batch.parse_directory(directory, '*.pdf')

    qa_ready = []

    for result in results:
        if result.success:
            # Prepare for Q&A generation
            qa_ready.append({
                'source_file': result.metadata['filename'],
                'content': result.content,
                'word_count': result.word_count,
                'page_count': result.metadata.get('page_count', 0)
            })

    # Save batch
    with open('pdf_batch_ready.json', 'w') as f:
        json.dump(qa_ready, f, indent=2)

    print(f"Processed {len(qa_ready)} PDFs")
    return qa_ready

# Use it
data = process_pdf_directory('crypto_whitepapers/')
```

## Error Handling

The parser handles errors gracefully:

```python
from document_parser import parse_document

result = parse_document('document.pdf')

if result.success:
    # Success - use the data
    print(result.content)
else:
    # Failed - check error
    print(f"Failed to parse: {result.error}")

    # Common errors:
    if "not found" in result.error:
        print("File doesn't exist")
    elif "not installed" in result.error:
        print("Missing dependency")
    elif "Unsupported format" in result.error:
        print("Format not supported")
```

## ParsedDocument Object

Every parse returns a `ParsedDocument` with:

```python
result.file_path      # Original file path
result.format         # File extension (.pdf, .txt, etc)
result.content        # Full text content
result.success        # True/False
result.error          # Error message if failed
result.word_count     # Number of words
result.char_count     # Number of characters
result.metadata       # Dict with format-specific metadata
result.sections       # List of sections (for .md files)
```

## Metadata Examples

### PDF Metadata
```python
{
    'filename': 'document.pdf',
    'size_bytes': 12345,
    'page_count': 10,
    'pdf_metadata': {
        'title': 'Document Title',
        'author': 'Author Name'
    }
}
```

### YouTube Metadata
```python
{
    'video_id': 'dQw4w9WgXcQ',
    'segment_count': 100,
    'language_detected': 'en',
    'raw_transcript': [...]  # Full transcript data
}
```

### Markdown Metadata
```python
{
    'filename': 'README.md',
    'section_count': 5,
    'sections': [
        {'level': 1, 'title': 'Introduction', 'content': '...'},
        {'level': 2, 'title': 'Usage', 'content': '...'}
    ]
}
```

## Tips for Gemini

### 1. Always Check Success
```python
result = parse_document('file.pdf')
if not result.success:
    print(f"Error: {result.error}")
    return  # Don't try to use result.content
```

### 2. Use Batch for Multiple Files
```python
# DON'T do this:
for file in files:
    result = parse_document(file)

# DO this:
batch = BatchDocumentParser()
results = batch.parse_multiple_files(files)
summary = batch.get_summary(results)
```

### 3. Extract Metadata
```python
result = parse_document('file.pdf')
if result.success:
    # Don't just use content
    # Check metadata for extra info
    print(result.metadata)  # Lots of useful data!
```

### 4. Handle Large Files
```python
result = parse_document('huge_file.pdf')
if result.success:
    # Check size first
    if result.char_count > 1000000:  # 1M chars
        print("File too large, processing in chunks...")
        # Handle appropriately
```

## Integration with Gemini Batch Processing

```python
from document_parser import BatchDocumentParser
import json

# 1. Parse documents
batch = BatchDocumentParser()
results = batch.parse_directory('documents/', '*.pdf')

# 2. Convert to batch format
requests = []
for i, result in enumerate(results):
    if result.success:
        request = {
            "custom_id": f"doc_{i:03d}",
            "request": {
                "contents": [{
                    "parts": [{
                        "text": f"Generate Q&A pairs from this document:\n\n{result.content}"
                    }]
                }]
            }
        }
        requests.append(request)

# 3. Save for Gemini batch
with open('batch_requests.jsonl', 'w') as f:
    for req in requests:
        f.write(json.dumps(req) + '\n')

print(f"Created batch with {len(requests)} requests")
```

## Quick Reference

| Task | Command |
|------|---------|
| Parse any file | `parse_document('file.ext')` |
| Parse YouTube | `parse_youtube_transcript('video_id')` |
| Parse directory | `parse_directory('dir/', '*.pdf')` |
| Batch parse | `BatchDocumentParser().parse_directory(...)` |
| Get summary | `batch.get_summary(results)` |

## Troubleshooting

### Missing Dependencies
```bash
pip install PyPDF2 python-docx beautifulsoup4 youtube-transcript-api==0.6.1
```

### Import Error
```python
# Make sure document_parser.py is in same directory or:
import sys
sys.path.append('/path/to/document_parser')
from document_parser import parse_document
```

### Encoding Issues
```python
# Parser uses utf-8 by default
# If file has different encoding, convert it first
```

---

**Created for**: Gemini
**Date**: November 6, 2025
**Status**: PRODUCTION READY

**For the Greater Good of All**

*Parse anything. Extract everything. Mine perpetually.*
