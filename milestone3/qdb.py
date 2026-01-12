from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from config import COLLECTION_NAME, QDRANT_HOST, QDRANT_PORT, TOP_K

def get_vector_store():
    client = QdrantClient(host=QDRANT_HOST,port=QDRANT_PORT)

    return QdrantVectorStore(client=client,collection_name=COLLECTION_NAME)
