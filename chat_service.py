
from flask import request, jsonify
from workflow import  stored_context, graph


store = {}

def set_user_data():
    data = request.get_json()
    unique_index_name = data.get('unique_index_name', '')
    knowledge_summary = data.get('knowledge_summary','')

    
    if not unique_index_name:
        return jsonify({'error': 'Missing unique_index_name'}), 400
    
    stored_context['unique_index_name'] = unique_index_name
    stored_context['knowledge_summary'] = knowledge_summary
    return jsonify({'message': 'Context, knowledge_summary and unique_index_name set successfully.'}), 200


def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    session_id = data.get('session_id', '')  
    user_id = data.get('user_id','')
    
    stored_context['session_id'] = session_id
    
    config = {"configurable": {"thread_id": session_id}}

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:

        # final_state = graph.invoke(
        #     {"messages": [("user", user_message)]}, config)
    
        events = graph.stream(
        {"messages": [("user", user_message)]}, config, stream_mode="values")

        for event in events:
            event["messages"][-1].pretty_print()

        response_message = event["messages"][-1].content

        return jsonify({'response': response_message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# {
#  "full_context":"you are a very emotional bot you first ask the user name and then response with starting with user name ",
#  "unique_index_name":"cloudbot_bge_cloudbot"
# }

def healthcheck():
    return jsonify({"status": "API is running good"}), 200
