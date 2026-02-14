---
name: pdf-reader
description: Extract text, search inside PDFs, and produce summaries.
homepage: "https://www.pymupdf.com"
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires": { "bins": ["python3"], "pip": ["PyMuPDF"] },
        "install":
          [
            {
              "id": "pymupdf",
              "kind": "pip",
              "package": "PyMuPDF",
              "label": "Install PyMuPDF",
            },
          ],
      },
  }
---

# PDF Reader Skill

The `pdf-reader` skill provides functionality to extract text, search inside PDFs, produce summaries, and retrieve metadata.

## Tool API

The skill provides four functions:

### extract_text
Extracts plain text from the specified PDF file.

- **Parameters:**
  - `file_path` (string): Path to the PDF file to extract text from.
  - `max_pages` (integer, optional): Maximum pages to extract.

```python
from pdfminer.high_level import extract_text

def extract_text_from_pdf(file_path: str, max_pages=None) -> str:
    """Extracts text from a PDF, up to max_pages."""
    return extract_text(file_path, maxpages=max_pages)
```

### search
Search for a specific term or phrase within the PDF.

- **Parameters:**
  - `file_path` (string): Path to the PDF file.
  - `query` (string): Term or phrase to search for in the document.

```python
from typing import List

def search_pdf(file_path: str, query: str) -> List[str]:
    """Searches for a term in the PDF and returns lines containing it."""
    pdf_text = extract_text_from_pdf(file_path)
    return [line.strip() for line in pdf_text.split("\n") if query.lower() in line.lower()]
```

### summarize
Generate a summary of the document by dividing it into digestible chunks.

- **Parameters:**
  - `file_path` (string): Path to the PDF file.

```python
from typing import List

def chunk_text(text: str, max_tokens=2000) -> List[str]:
    """Divides text into manageable chunks for processing."""
    words = text.split()
    max_word_count = max_tokens
    chunks = []
    current_chunk = []

    for word in words:
        if len(current_chunk) + len(word.split()) <= max_word_count:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def summarize_pdf(file_path: str) -> str:
    """Summarizes a PDF file by processing its text."""
    pdf_text = extract_text_from_pdf(file_path)
    chunks = chunk_text(pdf_text)
    summaries = [call_llm("Summarize this:", chunk) for chunk in chunks]
    return "\n".join(summaries)
```

### metadata
Retrieve metadata about the document.

- **Parameters:**
  - `file_path` (string): Path to the PDF file.

```python
from PyPDF2 import PdfReader

def get_pdf_metadata(file_path: str) -> dict:
    """Extracts metadata from a PDF file."""
    reader = PdfReader(file_path)
    metadata = reader.metadata
    return {
        "title": metadata.get("/Title", "Unknown"),
        "author": metadata.get("/Author", "Unknown"),
        "pages": len(reader.pages),
    }
```

## Testing
Use sample PDFs to ensure all functionalities work smoothly and output accurate results:

- Test text extraction with various layout formats.
- Verify summarization covers key points.
- Confirm search returns all relevant results.

Ensure summaries and searches are based on user-specific inputs and meet expectations.