from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.response_synthesizers import get_response_synthesizer
from embed import get_embedding_model
from qdb import get_vector_store
from llm import get_llm
from config import TOP_K
#import google.generativeai as genai
#import llm_model as llmm

Settings.llm = get_llm()
Settings.embed_model = get_embedding_model()
Settings.node_parser = SentenceSplitter(chunk_size=512,chunk_overlap=51)


def get_rag_engine():
    #embed_model = get_embedding_model()
    #llm = get_llm()
    
    embed_model = Settings.embed_model
    llm = Settings.llm
    vector_store = get_vector_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store) #add it here

    index = VectorStoreIndex.from_vector_store(vector_store=vector_store,embed_model=embed_model,storage_context=storage_context) #add storage_context here

    retriever = VectorIndexRetriever(index=index,similarity_top_k=TOP_K)

    response_synthesizer = get_response_synthesizer(llm=llm,response_mode="compact")

    query_engine = RetrieverQueryEngine(retriever=retriever,response_synthesizer=response_synthesizer)

    return query_engine
