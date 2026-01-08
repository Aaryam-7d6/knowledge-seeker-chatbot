from llama_index.core import VectorStoreIndex
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.response_synthesizers import get_response_synthesizer
from embed_model import get_embedding_model
from qdb_store import get_vector_store
from llm_model import get_llm
from config import TOP_K
#import google.generativeai as genai

def get_rag_engine():
    embed_model = get_embedding_model()
    llm = get_llm()
    vector_store = get_vector_store()

    index = VectorStoreIndex.from_vector_store(vector_store=vector_store,embed_model=embed_model)

    retriever = VectorIndexRetriever(index=index,similarity_top_k=TOP_K)

    response_synthesizer = get_response_synthesizer(llm=llm,response_mode="compact")

    query_engine = RetrieverQueryEngine(retriever=retriever,response_synthesizer=response_synthesizer)

    return query_engine
