from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer
from embed import get_embedding_model
from qdb import get_vector_store
from llm import get_llm
from config import TOP_K, SEARCH_MODE
from llama_index.core import VectorStoreIndex


def get_query_engine(search_mode=SEARCH_MODE):
    embed_model = get_embedding_model()
    llm = get_llm()
    vector_store = get_vector_store()

    index = VectorStoreIndex.from_vector_store(vector_store=vector_store,embed_model=embed_model)

    # --- Vector (Semantic) Search ---
    vector_retriever = VectorIndexRetriever(index=index,similarity_top_k=TOP_K)

    # --- Keyword Search ---
    bm25_retriever = BM25Retriever.from_defaults(index=index,similarity_top_k=TOP_K)

    # --- Choose Mode ---
    if search_mode == "vector":
        retriever = vector_retriever

    elif search_mode == "keyword":
        retriever = bm25_retriever

    elif search_mode == "hybrid":
        retriever = [vector_retriever, bm25_retriever]

    else:
        raise ValueError("Invalid search mode")

    response_synthesizer = ResponseSynthesizer.from_args(llm=llm,response_mode="compact")

    return RetrieverQueryEngine(retriever=retriever,response_synthesizer=response_synthesizer)
