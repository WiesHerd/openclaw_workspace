# PDF Making Skill

## Overview
This skill enables PDF creation from various source formats and data using command-line tools and Python libraries.

## Prerequisites
- System with Python 3.8+ (ideally Python 3.10+)
- Required libraries installed:
  - `reportlab` (for PDF creation from scratch)
  - `fpdf2` (for FPDF-based PDF creation)
  - `pypandoc` + `pandoc` (for Markdown to PDF)
  - `wkhtmltopdf` (for HTML to PDF conversion)
- Optional: `ghostscript` for advanced PDF manipulation

## Skills Provided
### 1. Convert Markdown to PDF
   - Input: `.md` file or markdown string
   - Output: `.pdf` file
   - Method: `pandoc` or `wkhtmltopdf`

### 2. Convert Text/HTML to PDF
   - Input: Text content or HTML
   - Output: `.pdf` file
   - Method: `reportlab` or `fpdf2`

### 3. Create PDF from Scratch
   - Define pages, tables, images, text
   - Full control over layout and styling

### 4. Merge PDFs
   - Combine multiple `.pdf` files into one

### 5. Extract Pages/Content
   - Split PDFs into separate files
   - Extract text from existing PDFs

## Usage Example
```python
from pdf_skills import MarkdownToPdf, TextToPdf, CreatePdf

# Convert Markdown to PDF
md_to_pdf(MarkdownToPdf)
result = convert("report.md", output="report.pdf")

# Create simple PDF
text_content = "Hello World!\nThis is a PDF."
result = create_text_pdf(text_content, filename="simple.pdf")
```

## Integration
- Can be called from OpenClaw sessions
- Integrates with `skill-creator` for custom workflows
- Supports batch processing

## Limitations
- Requires pre-installed libraries
- Some tools may require elevated privileges on certain systems
- Image handling requires `RLE` encoding for clarity

## Troubleshooting
- **Missing library:** `pip install reportlab fpdf2 pypandoc wkhtmltopdf`
- **Permission denied:** Check file paths and directory permissions
- **Unicode errors:** Ensure UTF-8 encoding for input strings

## Developer Notes
- This skill relies on external command-line tools
- Fallback to `pandoc` if `wkhtmltopdf` unavailable
- All transformations are logged for audit trails