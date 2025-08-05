#!/usr/bin/env python3
"""
PDF Data Extraction Tool

This script provides multiple methods to extract data from PDF files:
1. Text extraction using PyPDF2
2. Text extraction using pdfplumber (better for tables)
3. Table extraction using tabula-py
4. OCR-based extraction using pytesseract (for scanned PDFs)

Requirements:
- PyPDF2: pip install PyPDF2
- pdfplumber: pip install pdfplumber
- tabula-py: pip install tabula-py
- pytesseract: pip install pytesseract pillow
- pdf2image: pip install pdf2image

For OCR functionality, you also need to install Tesseract:
- Ubuntu/Debian: sudo apt-get install tesseract-ocr
- macOS: brew install tesseract
- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
"""

import os
import sys
from pathlib import Path
import argparse
from typing import List, Dict, Any, Optional

# PDF processing libraries
try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False
    print("Warning: PyPDF2 not installed. Install with: pip install PyPDF2")

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    print("Warning: pdfplumber not installed. Install with: pip install pdfplumber")

try:
    import tabula
    TABULA_AVAILABLE = True
except ImportError:
    TABULA_AVAILABLE = False
    print("Warning: tabula-py not installed. Install with: pip install tabula-py")

try:
    import pytesseract
    from pdf2image import convert_from_path
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("Warning: OCR libraries not installed. Install with: pip install pytesseract pillow pdf2image")


class PDFExtractor:
    """Main class for PDF data extraction with multiple methods."""
    
    def __init__(self, pdf_path: str):
        """Initialize with PDF file path."""
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
    def extract_text_pypdf2(self) -> str:
        """Extract text using PyPDF2 library."""
        if not PYPDF2_AVAILABLE:
            raise ImportError("PyPDF2 is not installed")
        
        text = ""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page.extract_text()
                    
        except Exception as e:
            print(f"Error extracting text with PyPDF2: {e}")
            
        return text
    
    def extract_text_pdfplumber(self) -> str:
        """Extract text using pdfplumber library (better for complex layouts)."""
        if not PDFPLUMBER_AVAILABLE:
            raise ImportError("pdfplumber is not installed")
        
        text = ""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    text += f"\n--- Page {page_num + 1} ---\n"
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
                        
        except Exception as e:
            print(f"Error extracting text with pdfplumber: {e}")
            
        return text
    
    def extract_tables_pdfplumber(self) -> List[List[List[str]]]:
        """Extract tables using pdfplumber."""
        if not PDFPLUMBER_AVAILABLE:
            raise ImportError("pdfplumber is not installed")
        
        all_tables = []
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    tables = page.extract_tables()
                    if tables:
                        print(f"Found {len(tables)} table(s) on page {page_num + 1}")
                        all_tables.extend(tables)
                        
        except Exception as e:
            print(f"Error extracting tables with pdfplumber: {e}")
            
        return all_tables
    
    def extract_tables_tabula(self, pages: str = "all") -> List[Any]:
        """Extract tables using tabula-py."""
        if not TABULA_AVAILABLE:
            raise ImportError("tabula-py is not installed")
        
        tables = []
        try:
            # Extract tables from PDF
            tables = tabula.read_pdf(
                str(self.pdf_path), 
                pages=pages, 
                multiple_tables=True,
                pandas_options={'header': 0}
            )
            print(f"Found {len(tables)} table(s) using tabula")
            
        except Exception as e:
            print(f"Error extracting tables with tabula: {e}")
            
        return tables
    
    def extract_text_ocr(self, dpi: int = 300) -> str:
        """Extract text using OCR for scanned PDFs."""
        if not OCR_AVAILABLE:
            raise ImportError("OCR libraries are not installed")
        
        text = ""
        try:
            # Convert PDF to images
            images = convert_from_path(str(self.pdf_path), dpi=dpi)
            
            for page_num, image in enumerate(images):
                text += f"\n--- Page {page_num + 1} (OCR) ---\n"
                # Extract text from image using OCR
                page_text = pytesseract.image_to_string(image)
                text += page_text
                
        except Exception as e:
            print(f"Error extracting text with OCR: {e}")
            
        return text
    
    def get_pdf_metadata(self) -> Dict[str, Any]:
        """Extract PDF metadata."""
        metadata = {}
        
        if PYPDF2_AVAILABLE:
            try:
                with open(self.pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    
                    metadata.update({
                        'num_pages': len(pdf_reader.pages),
                        'title': pdf_reader.metadata.get('/Title', 'N/A') if pdf_reader.metadata else 'N/A',
                        'author': pdf_reader.metadata.get('/Author', 'N/A') if pdf_reader.metadata else 'N/A',
                        'subject': pdf_reader.metadata.get('/Subject', 'N/A') if pdf_reader.metadata else 'N/A',
                        'creator': pdf_reader.metadata.get('/Creator', 'N/A') if pdf_reader.metadata else 'N/A',
                        'producer': pdf_reader.metadata.get('/Producer', 'N/A') if pdf_reader.metadata else 'N/A',
                        'creation_date': pdf_reader.metadata.get('/CreationDate', 'N/A') if pdf_reader.metadata else 'N/A',
                    })
                    
            except Exception as e:
                print(f"Error extracting metadata: {e}")
                
        return metadata
    
    def extract_all_data(self, use_ocr: bool = False, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """Extract all available data from PDF."""
        results = {
            'metadata': self.get_pdf_metadata(),
            'text_pypdf2': '',
            'text_pdfplumber': '',
            'text_ocr': '',
            'tables_pdfplumber': [],
            'tables_tabula': []
        }
        
        print(f"Processing PDF: {self.pdf_path}")
        print(f"Metadata: {results['metadata']}")
        
        # Extract text using different methods
        if PYPDF2_AVAILABLE:
            print("Extracting text with PyPDF2...")
            results['text_pypdf2'] = self.extract_text_pypdf2()
        
        if PDFPLUMBER_AVAILABLE:
            print("Extracting text with pdfplumber...")
            results['text_pdfplumber'] = self.extract_text_pdfplumber()
            
            print("Extracting tables with pdfplumber...")
            results['tables_pdfplumber'] = self.extract_tables_pdfplumber()
        
        if TABULA_AVAILABLE:
            print("Extracting tables with tabula...")
            results['tables_tabula'] = self.extract_tables_tabula()
        
        if use_ocr and OCR_AVAILABLE:
            print("Extracting text with OCR...")
            results['text_ocr'] = self.extract_text_ocr()
        
        # Save results if output directory is specified
        if output_dir:
            self.save_results(results, output_dir)
        
        return results
    
    def save_results(self, results: Dict[str, Any], output_dir: str):
        """Save extraction results to files."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        base_name = self.pdf_path.stem
        
        # Save text extractions
        for method in ['pypdf2', 'pdfplumber', 'ocr']:
            text_key = f'text_{method}'
            if results.get(text_key):
                with open(output_path / f"{base_name}_{method}_text.txt", 'w', encoding='utf-8') as f:
                    f.write(results[text_key])
        
        # Save tables
        if results['tables_pdfplumber']:
            with open(output_path / f"{base_name}_pdfplumber_tables.txt", 'w', encoding='utf-8') as f:
                for i, table in enumerate(results['tables_pdfplumber']):
                    f.write(f"\n=== Table {i+1} (pdfplumber) ===\n")
                    for row in table:
                        f.write('\t'.join(str(cell) if cell else '' for cell in row) + '\n')
        
        if results['tables_tabula']:
            for i, table in enumerate(results['tables_tabula']):
                table.to_csv(output_path / f"{base_name}_tabula_table_{i+1}.csv", index=False)
        
        # Save metadata
        with open(output_path / f"{base_name}_metadata.txt", 'w', encoding='utf-8') as f:
            for key, value in results['metadata'].items():
                f.write(f"{key}: {value}\n")
        
        print(f"Results saved to: {output_path}")


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(description='Extract data from PDF files')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('--output-dir', '-o', help='Output directory for extracted data')
    parser.add_argument('--use-ocr', action='store_true', help='Use OCR for scanned PDFs')
    parser.add_argument('--method', choices=['pypdf2', 'pdfplumber', 'tabula', 'ocr', 'all'], 
                       default='all', help='Extraction method to use')
    
    args = parser.parse_args()
    
    try:
        extractor = PDFExtractor(args.pdf_path)
        
        if args.method == 'all':
            results = extractor.extract_all_data(use_ocr=args.use_ocr, output_dir=args.output_dir)
            
            # Print summary
            print("\n=== EXTRACTION SUMMARY ===")
            print(f"Text length (PyPDF2): {len(results.get('text_pypdf2', ''))}")
            print(f"Text length (pdfplumber): {len(results.get('text_pdfplumber', ''))}")
            print(f"Tables found (pdfplumber): {len(results.get('tables_pdfplumber', []))}")
            print(f"Tables found (tabula): {len(results.get('tables_tabula', []))}")
            if args.use_ocr:
                print(f"Text length (OCR): {len(results.get('text_ocr', ''))}")
        
        elif args.method == 'pypdf2':
            text = extractor.extract_text_pypdf2()
            print(text)
        
        elif args.method == 'pdfplumber':
            text = extractor.extract_text_pdfplumber()
            print(text)
        
        elif args.method == 'tabula':
            tables = extractor.extract_tables_tabula()
            for i, table in enumerate(tables):
                print(f"\n=== Table {i+1} ===")
                print(table.to_string())
        
        elif args.method == 'ocr':
            text = extractor.extract_text_ocr()
            print(text)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()