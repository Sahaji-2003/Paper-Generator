# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from chat_service import set_user_data, chat, healthcheck
from storing_to_db_endpoint import store_vector_db,get_summary
from delete_index import delete_index

flask_app = Flask(__name__)
CORS(flask_app, resources={r"/*": {"origins": "*"}})

load_dotenv()
flask_app.route('/', methods=['GET'])(healthcheck)
flask_app.route('/set', methods=['POST'])(set_user_data)
flask_app.route('/chat', methods=['POST'])(chat)
flask_app.route('/store-vector-db', methods=['POST'])(store_vector_db)
flask_app.route('/get_summary/<knowledge_id>', methods=['GET'])(get_summary)
flask_app.route('/delete-index/<knowledge_id>', methods=['GET'])(delete_index)
if __name__ == "__main__":
    flask_app.run(port=5002)

# banna_bge_banna