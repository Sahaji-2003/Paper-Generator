from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import load_summarize_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from KnowledgeBase.config import GEMINI_API_KEY, GROQ_API_KEY
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from PyPDF2 import PdfReader
from KnowledgeBase.config import GROQ_API_KEY

llm = ChatGoogleGenerativeAI(temperature=0, api_key=GEMINI_API_KEY, model="gemini-2.0-flash")

import random

def summary_extract(pages):
    # Randomly select up to 12 pages, or fewer if there are less than 12
    selected_pages = random.sample(pages, min(len(pages), 3))

    chunks_prompt = """
    Please summarize the below documents:
    Document: `{text}`
    Summary:
    """
    map_prompt_template = PromptTemplate(input_variables=['text'], template=chunks_prompt)

    final_combine_prompt = '''
    Provide a final summary of the entire documents with these important points.
    Add a Generic Title,
    Give the summary about what are the documents about
    the main context of the documents.
    Documents summary: `{text}`
    '''
    final_combine_prompt_template = PromptTemplate(input_variables=['text'], template=final_combine_prompt)

    # Load summarize chain using map-reduce strategy
    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type='map_reduce',
        map_prompt=map_prompt_template,
        combine_prompt=final_combine_prompt_template,
        verbose=False
    )

    # Invoke the chain with the selected pages
    output = summary_chain.invoke(selected_pages)

    return output['output_text']


# pdf_loader = PyPDFLoader(f"database\\budget_speech.pdf")  # Replace with your file path
# documents = pdf_loader.load()  
# def summary_extract(pages):

#     chunks_prompt="""
#     Please summarize the below documents:
#     Document:`{text}'
#     Summary:
#     """
#     map_prompt_template=PromptTemplate(input_variables=['text'], template=chunks_prompt)

#     final_combine_prompt='''
#     Provide a final summary of the entire documents with these important points.
#     Add a Generic Title,
#     Give the summary about what are the documents about 
#     the main context of the documents. 
#     Documents summary: `{text}`
#     '''
#     final_combine_prompt_template=PromptTemplate(input_variables=['text'],template=final_combine_prompt)

#     summary_chain = load_summarize_chain(
#         llm=llm,
#         chain_type='map_reduce',
#         map_prompt=map_prompt_template,
#         combine_prompt=final_combine_prompt_template,
#         verbose=False
#     )
#     output = summary_chain.invoke(pages)

#     return output['output_text']