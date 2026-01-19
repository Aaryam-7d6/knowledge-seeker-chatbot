from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    Settings
)
from embed import get_embedding_model
from llama_index.core.node_parser import SentenceSplitter
from qdb import get_vector_store
from logger import logger
import os
from rag_eng import load_index_from_storage, get_rag_engine
import config

# Chunking Configuration
Settings.node_parser = SentenceSplitter(chunk_size=512,chunk_overlap=51)

# def build_index(data_dir: str):
#     logger.info(f"Loading documents from {data_dir}")
    
#     documents = SimpleDirectoryReader(data_dir,recursive=True).load_data()
    
#      # add metadta
#     for doc in documents:
#         doc.metadata["source"] = os.path.basename(doc.metadata.get("file_path", "unknown"))
#         doc.metadata["file_path"] = doc.metadata.get("file_path", "unknown")
#     logger.info(f"Loaded {len(documents)} documents.")
    
#     vector_store = get_vector_store()


#     #embed_model = get_embedding_model() #-- useful for only similarity and simentic search.
#     #logger.info(f"Using embedding model: {embed_model}")
    
#     #vector_store = get_vector_store()

#     storage_context = StorageContext.from_defaults(vector_store=vector_store)

#     logger.info("Building vector index")
#     index = VectorStoreIndex.from_documents(documents=documents,storage_context=storage_context,embed_model=get_embedding_model())
#     #logger.info(f"--- Index built with {len(documents)} documents. && {vector_store.num_entities} vectors. && {vector_store.num_collections} collections. && embedding model: {get_embedding_model()}. ---")
#     logger.info(f"Index built successfully with {len(documents)} documents "f"using embedding model: {config.EMBED_MODEL_NAME}")

#     # Persist docstore + index
#     index.storage_context.persist(persist_dir="./storage")

#     return index

# indexing.py
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from config import DATA_DIR, STORAGE_DIR, COLLECTION_NAME
import os

def build_index(data_dir):
    documents = SimpleDirectoryReader(data_dir).load_data()

    if not documents:
        raise RuntimeError("No documents found to index.")

    #client = QdrantClient(path=STORAGE_DIR)
    #client = QdrantClient(host=QDRANT_HOST,port=QDRANT_PORT)

    #vector_store = QdrantVectorStore(client=client,collection_name=COLLECTION_NAME)
    vector_store = get_vector_store()

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
    )

    index.storage_context.persist(persist_dir=STORAGE_DIR)
    #return index

