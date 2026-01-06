from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex
)
from embed_model import get_embedding_model
from qdb_store import get_qdrant_vector_store


def build_index(data_dir: str):
    # Load documents
    documents = SimpleDirectoryReader(data_dir).load_data()

    # Embedding model
    embed_model = get_embedding_model()

    # Vector store
    vector_store = get_qdrant_vector_store()

    # Storage context
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Build index
    index = VectorStoreIndex.from_documents(documents=documents,storage_context=storage_context,embed_model=embed_model)
    return index
