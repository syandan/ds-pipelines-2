#!/usr/bin/env python3
"""
Example usage of the PDF Extractor

This script demonstrates how to use the PDFExtractor class
to extract different types of data from PDF files.
"""

from pdf_extractor import PDFExtractor
import os

def example_basic_usage():
    """Basic example of extracting text from a PDF."""
    # Replace 'sample.pdf' with your actual PDF file path
    pdf_path = "sample.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Please place a PDF file named '{pdf_path}' in the current directory")
        return
    
    try:
        # Initialize the extractor
        extractor = PDFExtractor(pdf_path)
        
        # Get PDF metadata
        metadata = extractor.get_pdf_metadata()
        print("=== PDF METADATA ===")
        for key, value in metadata.items():
            print(f"{key}: {value}")
        
        # Extract text using PyPDF2
        print("\n=== TEXT EXTRACTION (PyPDF2) ===")
        text_pypdf2 = extractor.extract_text_pypdf2()
        print(f"Extracted {len(text_pypdf2)} characters")
        print("First 500 characters:")
        print(text_pypdf2[:500] + "..." if len(text_pypdf2) > 500 else text_pypdf2)
        
        # Extract text using pdfplumber (better for complex layouts)
        print("\n=== TEXT EXTRACTION (pdfplumber) ===")
        text_pdfplumber = extractor.extract_text_pdfplumber()
        print(f"Extracted {len(text_pdfplumber)} characters")
        
        # Extract tables using pdfplumber
        print("\n=== TABLE EXTRACTION (pdfplumber) ===")
        tables_pdfplumber = extractor.extract_tables_pdfplumber()
        print(f"Found {len(tables_pdfplumber)} tables")
        
        # Show first table if any
        if tables_pdfplumber:
            print("First table preview:")
            table = tables_pdfplumber[0]
            for i, row in enumerate(table[:5]):  # Show first 5 rows
                print(f"Row {i+1}: {row}")
        
        # Extract tables using tabula (if available)
        try:
            print("\n=== TABLE EXTRACTION (tabula) ===")
            tables_tabula = extractor.extract_tables_tabula()
            print(f"Found {len(tables_tabula)} tables")
            
            if tables_tabula:
                print("First table preview:")
                print(tables_tabula[0].head())
        except ImportError:
            print("tabula-py not available, skipping tabula extraction")
        
    except Exception as e:
        print(f"Error processing PDF: {e}")

def example_comprehensive_extraction():
    """Example of comprehensive data extraction with file output."""
    pdf_path = "sample.pdf"
    output_dir = "extracted_data"
    
    if not os.path.exists(pdf_path):
        print(f"Please place a PDF file named '{pdf_path}' in the current directory")
        return
    
    try:
        extractor = PDFExtractor(pdf_path)
        
        # Extract all data and save to files
        results = extractor.extract_all_data(
            use_ocr=False,  # Set to True if you have scanned PDFs
            output_dir=output_dir
        )
        
        print(f"\nExtraction complete! Check the '{output_dir}' directory for results.")
        
    except Exception as e:
        print(f"Error: {e}")

def example_ocr_extraction():
    """Example of OCR-based extraction for scanned PDFs."""
    pdf_path = "scanned_sample.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Please place a scanned PDF file named '{pdf_path}' in the current directory")
        return
    
    try:
        extractor = PDFExtractor(pdf_path)
        
        # Extract text using OCR
        print("=== OCR TEXT EXTRACTION ===")
        print("Note: OCR processing may take some time...")
        text_ocr = extractor.extract_text_ocr(dpi=300)
        
        print(f"Extracted {len(text_ocr)} characters using OCR")
        print("First 500 characters:")
        print(text_ocr[:500] + "..." if len(text_ocr) > 500 else text_ocr)
        
    except ImportError:
        print("OCR libraries not available. Install with:")
        print("pip install pytesseract pillow pdf2image")
        print("Also install Tesseract OCR engine on your system")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("PDF Data Extraction Examples")
    print("=" * 40)
    
    # Run basic example
    print("\n1. Basic Usage Example:")
    example_basic_usage()
    
    # Run comprehensive example
    print("\n2. Comprehensive Extraction Example:")
    example_comprehensive_extraction()
    
    # Uncomment to test OCR functionality
    # print("\n3. OCR Extraction Example:")
    # example_ocr_extraction()
    
    print("\nExamples completed!")
    print("\nTo use the command-line interface:")
    print("python pdf_extractor.py your_file.pdf --output-dir results")
    print("python pdf_extractor.py your_file.pdf --method pdfplumber")
    print("python pdf_extractor.py scanned_file.pdf --use-ocr --output-dir results")