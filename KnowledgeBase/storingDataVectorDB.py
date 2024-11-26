# import os
# from KnowledgeBase.process_files import process_file
# from KnowledgeBase.embeddings import get_vector_store
# from KnowledgeBase.summary import summary_extract
# from uuid import uuid4
# from concurrent.futures import ThreadPoolExecutor

# def set_unique_index(unique_index_name):
#     vector_store = get_vector_store(unique_index_name)
#     return vector_store 

# def storing_in_vector_db(files, knowledge_name, agent_name="default"):
#     """
#     Processes uploaded files and stores their contents in the vector database.
    
#     Args:
#         files (list): List of file objects (e.g., from Flask's `request.files.getlist('files')`).
#         knowledge_name (str): The name for the knowledge base.
#         agent_name (str): Optional agent name to include in the index name.
    
#     Returns:
#         str: Unique index name used to store the data in the vector store.
#     """
#     documents_to_insert = []  
#     uuids = []  
    
#     try:
#         # Process each file and extract documents
#         for file in files:
#             try:
#                 documents = process_file(file)
#                 for document in documents:
#                     documents_to_insert.append(document)
#                     uuids.append(str(uuid4()))  

#             except FileNotFoundError:
#                 print(f"Error: The file at {file.filename} was not found.")
#             except Exception as e:
#                 print(f"An error occurred while processing the file {file.filename}: {str(e)}")


#         if documents_to_insert:
#             unique_index_name = (agent_name + " bge " + knowledge_name).replace(" ", "_")
#             vector_store = set_unique_index(unique_index_name)

#             with ThreadPoolExecutor() as executor:

#                 summary_future = executor.submit(summary_extract, documents_to_insert)
#                 add_documents_future = executor.submit(vector_store.add_documents, documents=documents_to_insert, ids=uuids)

#                 summary = summary_future.result()
#                 add_documents_future.result()   

#         else:
#             print("No documents were found to insert into the vector store.")
#             return None
        
#         return unique_index_name, summary
    
#     except Exception as e:
#         print(f"An error occurred while storing in the vector database: {str(e)}")
#         return None


import os
import re
from KnowledgeBase.process_files import process_file
from KnowledgeBase.embeddings import get_vector_store
from KnowledgeBase.summary import summary_extract
from uuid import uuid4
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

def set_unique_index(unique_index_name):
    vector_store = get_vector_store(unique_index_name)
    return vector_store

def background_summary_extraction(documents, callback=None):
    """
    Runs the summary extraction in the background and invokes the callback when done.
    """
    try:
        summary = summary_extract(documents)
        if callback:
            callback(summary)
    except Exception as e:
        print(f"An error occurred while extracting the summary: {str(e)}")

def storing_in_vector_db(files, knowledge_name, agent_name="default", summary_callback=None):
    """
    Processes uploaded files and stores their contents in the vector database.

    Args:
        files (list): List of file objects (e.g., from Flask's `request.files.getlist('files')`).
        knowledge_name (str): The name for the knowledge base.
        agent_name (str): Optional agent name to include in the index name.
        summary_callback (callable): Optional callback function to be called when the summary is ready.

    Returns:
        str: Unique index name used to store the data in the vector store.
    """
    documents_to_insert = []
    uuids = []

    try:
        # Process each file and extract documents
        for file in files:
            try:
                documents = process_file(file)
                for document in documents:
                    documents_to_insert.append(document)
                    uuids.append(str(uuid4()))

            except FileNotFoundError:
                print(f"Error: The file at {file.filename} was not found.")
            except Exception as e:
                print(f"An error occurred while processing the file {file.filename}: {str(e)}")

        if documents_to_insert:
            unique_index_name = re.sub(r'\W+', '', (agent_name + " bge " + knowledge_name).replace(" ", "_").lower())

  
            vector_store = set_unique_index(unique_index_name)


            vector_store.add_documents(documents=documents_to_insert, ids=uuids)


            summary_thread = threading.Thread(target=background_summary_extraction, args=(documents_to_insert, summary_callback))
            summary_thread.start()

            return unique_index_name

        else:
            print("No documents were found to insert into the vector store.")
            return None

    except Exception as e:
        print(f"An error occurred while storing in the vector database: {str(e)}")
        return None
