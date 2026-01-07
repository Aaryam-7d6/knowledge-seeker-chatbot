from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    Settings
)
from llama_index.core.node_parser import SentenceSplitter
from embed_model import get_embedding_model
from qdb_store import get_qdrant_vector_store
#import logger
from logger import logger
import os

# Chunking Configuration
Settings.node_parser = SentenceSplitter(chunk_size=512,chunk_overlap=51)


def build_index(data_dir: str):
    
    logger.info(f"Loading documents from {data_dir}")
    
    # load documents
    documents = SimpleDirectoryReader(data_dir).load_data()
    
    # add metadta
    for doc in documents:
        doc.metadata["source"] = os.path.basename(doc.metadata.get("file_path", "unknown"))
        doc.metadata["file_path"] = doc.metadata.get("file_path", "unknown")
    logger.info(f"Loaded {len(documents)} documents.")
    
    # embedding model
    embed_model = get_embedding_model()
    logger.info(f"Using embedding model: {embed_model}")    
    # Vector 
    vector_store = get_qdrant_vector_store()
    #logger.info(f"Using Qdrant vector store.")

    # Storage
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    #logger.info(f"Created storage context.")
    logger.info("Building vector index")
    # Building index
    index = VectorStoreIndex.from_documents(documents=documents,storage_context=storage_context,embed_model=embed_model)
    #logger.info(f"Index built with {len(documents)} documents.")
      
    return index