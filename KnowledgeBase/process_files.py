import os
from tempfile import NamedTemporaryFile
from KnowledgeBase.text_extraction import extract_text_from_docx, extract_metadata, extract_text_from_pdf
from KnowledgeBase.chunking import chunk_text
from langchain_core.documents import Document
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import UnstructuredHTMLLoader, UnstructuredMarkdownLoader, PyPDFLoader
from langchain_community.document_loaders import JSONLoader

def process_file(file):
    """
    Processes a file, extracts text and metadata, and performs chunking.

    Arguments:
        file: A file-like object (e.g., Flask `request.files`).

    Returns:
        A list of documents with metadata and chunked content.
    """


    file_extension = file.filename.split('.')[-1].lower()
    
    with NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
        temp_file.write(file.read()) 
        temp_file_path = temp_file.name

    try:
        if file_extension == 'pdf':
            loader = PyPDFLoader(temp_file_path)
            pages = loader.load_and_split()
        
        elif file_extension == 'docx':
            pages = extract_text_from_docx(temp_file_path)

        elif file_extension == 'csv':
            loader = CSVLoader(temp_file_path)
            pages = loader.load()

        elif file_extension == 'html':
            loader = UnstructuredHTMLLoader(temp_file_path)
            pages = loader.load()

        elif file_extension == 'md':
            loader = UnstructuredMarkdownLoader(temp_file_path)
            pages = loader.load()

        else:
            raise ValueError("Unsupported file format. Please use PDF, DOCX, CSV, HTML, or MD files.")
        
     
        file_name, title = extract_metadata(file)  
        if file_name is None:
            file_name = "unknown_file_name"

        documents = chunk_text(pages)
        
        for doc in documents:
            doc_metadata = getattr(doc, 'metadata', None)
            if doc_metadata is not None:
                doc_metadata.update({
                    "file_name": file_name,
                    "file_path": temp_file_path,  
                })
            else:
                print(f"Metadata not found in document: {doc}")

        return documents
    
        

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
