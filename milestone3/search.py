from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core import StorageContext, load_index_from_storage,Settings
from llama_index.core.node_parser import SentenceSplitter
from embed import get_embedding_model
from qdb import get_vector_store
from llm import get_llm
from config import TOP_K, SEARCH_MODE, STORAGE_DIR, DATA_DIR, COLLECTION_NAME
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import QueryFusionRetriever
#from llama_index.core.response_synthesizers import ResponseSynthesizer
from rag_eng import load_index_from_storage, get_rag_engine,load_index
import config
import os
from llama_index.core.retrievers import QueryFusionRetriever


Settings.llm = get_llm()
Settings.embed_model = get_embedding_model()
Settings.node_parser = SentenceSplitter(chunk_size=512,chunk_overlap=51)

# def load_index():
#     storage_context = StorageContext.from_defaults(persist_dir="./storage")
#     return load_index_from_storage(storage_context)

# def get_query_engine(search_mode=SEARCH_MODE):
#     #embed_model = get_embedding_model()
#     #llm = get_llm()
#     #vector_store = get_vector_store()
#     #best for semintic search.
#     #index = VectorStoreIndex.from_vector_store(vector_store=vector_store,embed_model=embed_model)
#     #index = load_index()
#     embed_model = Settings.embed_model
#     llm = Settings.llm
#     vector_store = get_vector_store()
#     storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
#     index = load_index()
    
#     if index.docstore is None or len(index.docstore.docs) == 0:
#         raise RuntimeError("No documents available for keyword or hybrid search.")


#     # --- Vector (Semantic) Search ---
#     vector_retriever = VectorIndexRetriever(index=index,similarity_top_k=TOP_K)

#     # --- Keyword Search ---
#     bm25_retriever = BM25Retriever.from_defaults(index=index,similarity_top_k=TOP_K)

#     # --- Choose Mode ---
#     if search_mode == "vector":
#         retriever = vector_retriever

#     elif search_mode == "keyword":
#         retriever = bm25_retriever

#     elif search_mode == "hybrid":
#         retriever = [vector_retriever, bm25_retriever]

#     else:
#         raise ValueError("Invalid search mode")

#     response_synthesizer = ResponseSynthesizer.from_args(llm=llm,response_mode="compact")

#     query_engine = RetrieverQueryEngine(retriever=retriever,response_synthesizer=response_synthesizer)

#     #return RetrieverQueryEngine(retriever=retriever,response_synthesizer=response_synthesizer)
#     return query_engine
# def load_index():
#     qdrant_store = get_vector_store()

#     storage_context = StorageContext.from_defaults(
#         persist_dir="./storage",
#         vector_stores={
#             "default": qdrant_store
#         }
#     )

#     index = load_index_from_storage(storage_context)
#     return index

#-- form documentation --
from llama_index.core import SimpleDirectoryReader

docs = SimpleDirectoryReader(DATA_DIR).load_data()

from llama_index.core.storage.docstore import SimpleDocumentStore

docstore = SimpleDocumentStore()
docstore.add_documents(docs)
#-- --


def get_query_engine(search_mode=SEARCH_MODE):
    
    index = load_index()
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    # index = load_index_from_storage(storage_context)
    
    # if index.docstore is None or len(index.docstore.docs) == 0:
    #     raise RuntimeError("No documents available. Please index first.")
    
    if not os.path.exists(os.path.join(STORAGE_DIR, "docstore.json")):
        raise RuntimeError("No index found. Please click 'Index Documents' first.")


    vector_retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=TOP_K
    )

    bm25_retriever = BM25Retriever.from_defaults(
        #index=index,
        #index = docs,
        docstore= docstore,
        similarity_top_k=TOP_K
    )

    if search_mode == "vector":
        retriever = vector_retriever

    elif search_mode == "keyword":
        retriever = bm25_retriever

    elif search_mode == "hybrid":
        # retriever = QueryFusionRetriever(
        #     retrievers=[vector_retriever, bm25_retriever],
        #     #retrievers= vector_retriever & bm25_retriever,
        #     similarity_top_k=TOP_K,
        #     num_queries=1
        # )
        
        fusion = QueryFusionRetriever(
            retrievers=[vector_retriever, bm25_retriever],
            similarity_top_k=TOP_K,
        )

        return RetrieverQueryEngine.from_args(fusion)

    else:
        raise ValueError("Invalid search mode")

    response_synthesizer = get_response_synthesizer(
        llm=Settings.llm,
        response_mode="compact"
    ) #, num_queries=1 -- u can add this param if needed

    return RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer
    )
