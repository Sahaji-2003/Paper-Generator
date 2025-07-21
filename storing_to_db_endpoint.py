from KnowledgeBase.storingDataVectorDB import storing_in_vector_db
import os
from flask import Flask, request, jsonify
from threading import Thread


summary_results = {}

def store_summary_in_memory(knowledge_id, summary):
    """
    Store the summary in a global dictionary after it is computed.
    """
    summary_results[knowledge_id] = summary

def store_vector_db():
    files = request.files.getlist('files')
    knowledge_name = request.form.get('knowledge_name')
    agent_name = request.form.get('agent_name')

    if not files or not knowledge_name or not agent_name:
        return jsonify({"error": "files, knowledge_name, and agent_name are required."}), 400

    try:
        # Call the vector DB storing method with a callback to store the summary
        knowledge_id = storing_in_vector_db(files, knowledge_name, agent_name, summary_callback=lambda summary: store_summary_in_memory(knowledge_id, summary))

        # Return the knowledge ID immediately after documents are added
        return jsonify({"message": "Vector database created successfully", "knowledge_id": knowledge_id}), 200

    except Exception as e:
        print(f"Error storing vector DB: {e}")
        return jsonify({"error": str(e)}), 500
    
def get_summary(knowledge_id):
    """
    Endpoint to fetch the summary for the given knowledge ID if it is ready.
    """
    summary = summary_results.get(knowledge_id)
    if summary:
        return jsonify({"knowledge_id": knowledge_id, "summary": summary}), 200
    else:
        return jsonify({"message": "Summary is still being processed, please check back later."}), 202