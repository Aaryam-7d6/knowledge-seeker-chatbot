from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from config import COLLECTION_NAME, QDRANT_HOST, QDRANT_PORT

def get_qdrant_vector_store():
    client = QdrantClient(host=QDRANT_HOST,port=QDRANT_PORT)
    vector_store = QdrantVectorStore(client=client,collection_name=COLLECTION_NAME)
    return vector_store
