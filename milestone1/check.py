from qdrant_client import QdrantClient
'''
client = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)
print(client.get_collections())
print(client.get_collection(config.COLLECTION_NAME))
-------

#need OpenAI API key here to run this code :
query_engine = index.as_query_engine()
response = query_engine.query("test query")
print(response)
'''
'''
from llama_index.core import VectorStoreIndex
from qdb_store import get_qdrant_vector_store
from embed_model import get_embedding_model

def verify():
    vector_store = get_qdrant_vector_store()
    embed_model = get_embedding_model()

    index = VectorStoreIndex.from_vector_store(vector_store=vector_store,embed_model=embed_model)

    query_engine = index.as_query_engine()
    response = query_engine.query("test query")

    print("Verification response:")
    print(response)

if __name__ == "__main__":
    verify()
--------
'''
import config
#2nd way to verify

client = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)
print(client.get_collections()) #prints all collections
print(client.get_collection(config.COLLECTION_NAME)) #prints specific collection details