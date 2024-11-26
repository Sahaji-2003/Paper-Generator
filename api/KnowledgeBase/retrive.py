import os
from langchain_elasticsearch import ElasticsearchStore
from langchain_community.embeddings import JinaEmbeddings
from KnowledgeBase.embeddings import get_vector_store

def perform_context_search(query_text,unique_index_name,k=3):
    """
    Perform similarity search with the provided query and return matching documents.

    Parameters:
    query_text (str): The query text for the search.
    k (int): Number of top documents to retrieve.

    Returns:
    list: A list of documents that match the query.
    """
    if not query_text.strip():
        return []
    # Initialize the Elasticsearch vector store
    vector_store = get_vector_store(unique_index_name)

    # Perform similarity search with the query text and retrieve top k matching documents
    results = vector_store.similarity_search(query_text, k=k)

    # Process and store the results
    documents = []
    for result in results:
        doc_info = {
            "file_path": result.metadata.get('file_path'),
            "file_name": result.metadata.get('file_name'),
            "page_number": result.metadata.get('page_number'),
            "title": result.metadata.get('title'),
            "content": result.page_content
        }
        documents.append(doc_info)

    return documents

# # Example usage
# query = "author of budget"
# documents = perform_context_search(query, k=2)

# # Display the results
# for doc in documents:
#     print(f"Document Source: {doc['file_path']}")
#     print(f"File Name: {doc['file_name']}")
#     print(f"Page Number: {doc['page_number']}")
#     print(f"Title: {doc['title']}")
#     print("\n")

# # Print the total number of documents retrieved
# print(f"Total documents retrieved: {len(documents)}")
