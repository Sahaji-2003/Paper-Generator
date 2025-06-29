# # KnowledgeBase/workflow.py

# from langgraph.checkpoint.memory import MemorySaver
# from langchain_core.messages import HumanMessage,AIMessage
# from langgraph.graph import END, StateGraph, MessagesState,START, END
# from KnowledgeBase.config import GROQ_API_KEY
# from KnowledgeBase.retrive import perform_context_search
# from typing import Annotated
# from typing_extensions import TypedDict
# import requests
# from langgraph.graph.message import add_messages
# from langgraph.prebuilt import ToolNode, tools_condition
# from langchain_groq import ChatGroq
# from pydantic.v1 import BaseModel, Field
# from langchain.tools import BaseTool, StructuredTool, tool

# llm = ChatGroq(temperature=0, api_key=GROQ_API_KEY, model="llama-3.1-70b-versatile")

# memory = MemorySaver()

# stored_context = {
#     "full_context": "",
#     "unique_index_name": "",
#     "session_id": "",
#     "user_histories": {}  
# }

# @tool
# def context_retriever_tool(user_query: str) -> str:
#     """
#     This tool retrieves the most relevant documents based on the user's query. 
#     It searches through a vector database to find related information and returns the contextual content from those documents.
    
#     **When to use this tool:**
#     - Use this tool for any general query or question that requires information retrieval from stored documents or knowledge bases.
#     - This tool helps find contextual information to support responses or provide details based on user requests.
#     - It is recommended to use this tool most frequently to provide relevant information.
#     """
#     unique_index_name = stored_context.get('unique_index_name', '')
#     retrieved_docs = perform_context_search(query_text=user_query, unique_index_name=unique_index_name)
#     try:
#         doc_texts = [doc['content'] for doc in retrieved_docs if 'content' in doc]
#         context_from_docs = "\n".join(doc_texts)
#         # print(context_from_docs+"\n\n")
#         # print("tool called")
#         return retrieved_docs
#     except Exception as e:
#         return f"Error while processing documents: {e}"



# class State(TypedDict):
#     messages: Annotated[list, add_messages]


# graph_builder = StateGraph(State)

# tools = [context_retriever_tool]
# llm_with_tools = llm.bind_tools(tools)



# def chatbot(state: State):

#     persona_prompt = "You are a Educational bot named PrashnAI your task is to hel educators with their task of finding the information about any subject for this you can use the too retrive to retrive the context and answer the teachers query in very proper format also tell the reference from where you have got this information."
#     system_prompt = "Use Tool to answer all the questions"
#     user_message = state["messages"][-1] if state["messages"] else ""
    
#     final_message = f"""  System : {system_prompt} \n\n
#                           Your Persona (Behave Like): {persona_prompt}\n\n
#                           User: {user_message}"""

#     state["messages"].append(final_message)
    
#     return {"messages": [llm_with_tools.invoke(state["messages"])]}


# graph_builder.add_node("chatbot",chatbot)
# tool_node = ToolNode(tools=tools)
# graph_builder.add_node("tools", tool_node)

# graph_builder.add_conditional_edges(
#     "chatbot",
#     tools_condition,
# )
# graph_builder.add_edge("tools", "chatbot")
# graph_builder.add_edge(START,"chatbot")

# graph = graph_builder.compile(checkpointer=memory)


# KnowledgeBase/workflow.py

from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import END, StateGraph, MessagesState, START
from KnowledgeBase.config import GEMINI_API_KEY,GROQ_API_KEY  # Update to use the correct API key variable
from KnowledgeBase.retrive import perform_context_search
from typing import Annotated
from typing_extensions import TypedDict
import requests
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_genai import ChatGoogleGenerativeAI  # Import the Gemini API class
from pydantic.v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool

# Initialize the Gemini model

llm = ChatGoogleGenerativeAI(temperature=0, api_key=GEMINI_API_KEY, model="gemini-2.0-flash")  # Use the appropriate Gemini model
# llm=ChatGroq(groq_api_key=GROQ_API_KEY,model_name="llama-3.1-70b-versatile")
memory = MemorySaver()

stored_context = {
    "full_context": "",
    "unique_index_name": "",
    "session_id": "",
    "knowledge_summary":"",
    "user_histories": {}  
}

@tool
def context_retriever_tool(context_keywords: str) -> str:
    """
    This tool retrieves the most relevant documents based on the search query. 
    It searches through a vector database to find related information and returns the contextual content from those documents.
    
    """
    unique_index_name = stored_context.get('unique_index_name', '')
    retrieved_docs = perform_context_search(query_text=context_keywords, unique_index_name=unique_index_name)
    try:
        doc_texts = [doc['content'] for doc in retrieved_docs if 'content' in doc]
        context_from_docs = "\n".join(doc_texts)
        return doc_texts # Return the concatenated document texts
    except Exception as e:
        return f"Error while processing documents: {e}"

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

tools = [context_retriever_tool]
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    persona_prompt = "You are an Educational bot named PrashnAI. Your task is to help educators with their task of finding information about any subject. For this, you can use the tool to retrieve context and answer the teachers' queries in a proper format, also telling the reference from where you have got this information."
    system_prompt = "Use Tool to answer all the questions. You are given the task to give the full context to generate the questions on that topic and give the context in proper formate with the reference of book <title> and page No. for every context give the reference. give full context so to create questions on that topic easily"
    user_message = state["messages"][-1] if state["messages"] else ""
    summary = stored_context["knowledge_summary"]
    final_message = f"""System: {system_prompt} \n\n
                        Your Persona (Behave Like): {persona_prompt}\n\n
                        Summary of Documents You Have: {summary}\n\n
                        User: {user_message}\n\n
                        Important: Don't Call the tool more than 2 times for a single user query\n\n
                        You need to just send the context so that next agent can generate questions based on it.
                        Also Give the reference and page no. properly
                        """

    state["messages"].append(final_message)
    
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile(checkpointer=memory)
