import fitz  # PyMuPDF for PDFs
import re
import docx  # for DOCX files
import os

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file and includes page numbers."""
    with fitz.open(pdf_path) as pdf:
        content_with_page_numbers = []
        for page_num, page in enumerate(pdf, start=1):
            text = page.get_text("text")  # Extract text only
            clean_text = re.sub(r'[^A-Za-z0-9\s\n]+', '', text)  # Clean non-alphanumeric characters
            content_with_page_numbers.append((clean_text, page_num))
    return content_with_page_numbers

def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file (DOCX files have no concept of page numbers)."""
    doc = docx.Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    clean_text = re.sub(r'[^A-Za-z0-9\s\n]+', '', text)  
    return [(clean_text, 1)] 

def extract_metadata(file):
    """Extracts the file name and title from the document."""
    file_name = file.filename 
    title = os.path.splitext(file_name)[0]  
    return file_name, title
