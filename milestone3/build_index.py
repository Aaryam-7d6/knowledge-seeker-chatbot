from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex
)
from embed import get_embedding_model
from qdb import get_vector_store
from rag_eng import load_index_from_storage, get_rag_engine
import config

DATA_DIR = "./data"
PERSIST_DIR = "./storage"

def main():
    print("📥 Loading documents...")
    documents = SimpleDirectoryReader(
        DATA_DIR,
        recursive=True
    ).load_data()

    if not documents:
        raise RuntimeError("No documents found in data directory")

    print(f"✅ Loaded {len(documents)} documents")

    vector_store = get_vector_store()

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    print("🧠 Building index...")
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=get_embedding_model()
    )

    print("💾 Persisting index...")
    index.storage_context.persist(persist_dir=PERSIST_DIR)

    print("🎉 Index build completed successfully")

if __name__ == "__main__":
    main()
