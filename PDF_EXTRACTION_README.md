# PDF Data Extraction Tool

A comprehensive Python tool for extracting data from PDF files using multiple libraries and approaches.

## Features

- **Multiple extraction methods**: PyPDF2, pdfplumber, tabula-py, and OCR
- **Text extraction**: Extract plain text from regular PDFs
- **Table extraction**: Extract structured tables from PDFs
- **OCR support**: Extract text from scanned/image-based PDFs
- **Metadata extraction**: Get PDF document information
- **Command-line interface**: Easy-to-use CLI
- **Batch processing**: Process multiple files
- **Multiple output formats**: Save results as text files, CSV, etc.

## Installation

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Install system dependencies (for OCR functionality)

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install poppler-utils  # for pdf2image
```

**macOS:**
```bash
brew install tesseract
brew install poppler  # for pdf2image
```

**Windows:**
- Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
- Install poppler: Download from https://blog.alivate.com.au/poppler-windows/

### 3. Java (for tabula-py)

Tabula-py requires Java to be installed:
- **Ubuntu/Debian**: `sudo apt-get install default-jdk`
- **macOS**: `brew install openjdk`
- **Windows**: Download from https://www.oracle.com/java/technologies/downloads/

## Usage

### Command Line Interface

#### Basic usage:
```bash
# Extract all data using all available methods
python pdf_extractor.py document.pdf

# Save results to a directory
python pdf_extractor.py document.pdf --output-dir results

# Use specific extraction method
python pdf_extractor.py document.pdf --method pdfplumber

# Extract from scanned PDFs using OCR
python pdf_extractor.py scanned_document.pdf --use-ocr --output-dir results
```

#### Available methods:
- `pypdf2`: Basic text extraction
- `pdfplumber`: Better for complex layouts and tables
- `tabula`: Specialized for table extraction
- `ocr`: For scanned/image-based PDFs
- `all`: Use all available methods (default)

### Python API

#### Basic text extraction:
```python
from pdf_extractor import PDFExtractor

# Initialize extractor
extractor = PDFExtractor("document.pdf")

# Extract text using different methods
text_pypdf2 = extractor.extract_text_pypdf2()
text_pdfplumber = extractor.extract_text_pdfplumber()

# Get metadata
metadata = extractor.get_pdf_metadata()
print(f"Document has {metadata['num_pages']} pages")
```

#### Table extraction:
```python
# Extract tables using pdfplumber
tables_pdfplumber = extractor.extract_tables_pdfplumber()

# Extract tables using tabula (returns pandas DataFrames)
tables_tabula = extractor.extract_tables_tabula()

# Save first table to CSV
if tables_tabula:
    tables_tabula[0].to_csv("table1.csv", index=False)
```

#### OCR extraction:
```python
# Extract text from scanned PDFs
text_ocr = extractor.extract_text_ocr(dpi=300)
```

#### Comprehensive extraction:
```python
# Extract all available data
results = extractor.extract_all_data(
    use_ocr=True,
    output_dir="extraction_results"
)

# Access results
print(f"Text length: {len(results['text_pdfplumber'])}")
print(f"Tables found: {len(results['tables_tabula'])}")
```

## Library Comparison

| Library | Best For | Pros | Cons |
|---------|----------|------|------|
| **PyPDF2** | Simple text extraction | Fast, lightweight | Poor formatting, no tables |
| **pdfplumber** | Complex layouts, tables | Good formatting, table detection | Slower than PyPDF2 |
| **tabula-py** | Table extraction | Excellent table parsing | Requires Java, tables only |
| **OCR (pytesseract)** | Scanned PDFs | Works with images | Slow, requires preprocessing |

## Examples

### Example 1: Extract text from a research paper
```python
extractor = PDFExtractor("research_paper.pdf")
text = extractor.extract_text_pdfplumber()
print(f"Extracted {len(text)} characters")
```

### Example 2: Extract financial tables
```python
extractor = PDFExtractor("financial_report.pdf")
tables = extractor.extract_tables_tabula()
for i, table in enumerate(tables):
    table.to_csv(f"financial_table_{i+1}.csv")
```

### Example 3: Process scanned documents
```python
extractor = PDFExtractor("scanned_contract.pdf")
text = extractor.extract_text_ocr(dpi=300)
with open("contract_text.txt", "w") as f:
    f.write(text)
```

## Output Files

When using `--output-dir`, the tool creates:

- `{filename}_pypdf2_text.txt`: Text extracted with PyPDF2
- `{filename}_pdfplumber_text.txt`: Text extracted with pdfplumber
- `{filename}_ocr_text.txt`: Text extracted with OCR (if enabled)
- `{filename}_pdfplumber_tables.txt`: Tables from pdfplumber
- `{filename}_tabula_table_{n}.csv`: Tables from tabula (CSV format)
- `{filename}_metadata.txt`: PDF metadata

## Troubleshooting

### Common Issues:

1. **"Java not found" error**:
   - Install Java JDK/JRE
   - Ensure `java` is in your PATH

2. **OCR not working**:
   - Install Tesseract OCR engine
   - Install poppler-utils for PDF to image conversion

3. **Empty text extraction**:
   - Try different methods (pdfplumber vs PyPDF2)
   - For scanned PDFs, use OCR with `--use-ocr`

4. **Table extraction issues**:
   - Try both pdfplumber and tabula methods
   - Some PDFs may need manual parameter tuning

### Performance Tips:

- Use PyPDF2 for simple text extraction (fastest)
- Use pdfplumber for complex layouts
- Use tabula for table-heavy documents
- OCR is slowest - only use for scanned PDFs
- Process large files in smaller batches

## License

This tool is provided as-is for educational and research purposes.

## Contributing

Feel free to submit issues and enhancement requests!