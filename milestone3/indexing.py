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

# Chunking Configuration
Settings.node_parser = SentenceSplitter(chunk_size=512,chunk_overlap=51)

def build_index(data_dir: str):
    logger.info(f"Loading documents from {data_dir}")
    
    documents = SimpleDirectoryReader(
        data_dir,
        recursive=True
    ).load_data()
    
     # add metadta
    for doc in documents:
        doc.metadata["source"] = os.path.basename(doc.metadata.get("file_path", "unknown"))
        doc.metadata["file_path"] = doc.metadata.get("file_path", "unknown")
    logger.info(f"Loaded {len(documents)} documents.")

    embed_model = get_embedding_model()
    logger.info(f"Using embedding model: {embed_model}")
    
    vector_store = get_vector_store()

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    logger.info("Building vector index")
    index = VectorStoreIndex.from_documents(documents=documents,storage_context=storage_context,embed_model=embed_model)
    logger.info(f"Index built with {len(documents)} documents.")

    return index
