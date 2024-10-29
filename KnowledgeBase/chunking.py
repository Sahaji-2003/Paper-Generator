from langchain_text_splitters import RecursiveCharacterTextSplitter


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=4000,  
    chunk_overlap=100,  
    length_function=len, 
    is_separator_regex=False  
)

def chunk_text(content_with_page_numbers):
    """Chunk the text content while retaining page number metadata."""

    documents = []

    for doc in content_with_page_numbers:
        text = doc.page_content
        metadata = doc.metadata  # Extract all metadata from the document

        # Create chunks of the text content
        chunks = text_splitter.create_documents([text])

        # Append the existing metadata to each chunk
        for chunk in chunks:
            chunk.metadata.update(metadata)  # Update chunk metadata with the original metadata
            documents.append(chunk)

    return documents
