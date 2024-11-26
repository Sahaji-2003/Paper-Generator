import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
from flask import Flask, request, jsonify
load_dotenv()

ES_URL = os.getenv("ES_URL")
ES_API_KEY = os.getenv("ES_API_KEY")
INDEX_NAME = "old_dominion_bge"  # Replace with the name of the index you want to delete

# Initialize the Elasticsearch client
es = Elasticsearch(
    [ES_URL],
    api_key=ES_API_KEY,
)

# Function to delete an index
def delete_index(knowledge_id):
    index_name = knowledge_id
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        print(f"Index '{index_name}' deleted successfully.")
        response_message = f"index: {index_name} deleted successfully"
        return jsonify({'response': response_message})
    else:
        print(f"Index '{index_name}' does not exist.")
        response_message = f"index: {index_name}  does not exist."
        return jsonify({'response': response_message})

# Example usage
# if __name__ == "__main__":
#     delete_index(INDEX_NAME)