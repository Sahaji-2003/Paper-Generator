from langchain_elasticsearch import ElasticsearchStore
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from KnowledgeBase.config import ES_URL, ES_API_KEY

def get_vector_store(unique_index_name, vector_store_type = "elastic", embeddings_type = "BGE"):
    # Initialize embeddings
    model_name = "BAAI/bge-small-en"
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": True}
    hf = HuggingFaceBgeEmbeddings(
        model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
    )
    
    # Initialize vector store
    vector_store = ElasticsearchStore(
        es_url=ES_URL,
        index_name=unique_index_name,
        embedding=hf,
        es_api_key=ES_API_KEY

    )
    
    return vector_store
