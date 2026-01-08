from embed_model import get_embedding_model
from qdb_store import get_vector_store
#import google.generativeai as genai

def inspect_vectors():
    vector_store = get_vector_store()
    client = vector_store.client

    collection_info = client.get_collection(vector_store.collection_name)

    print("Vector Count:", collection_info.points_count)

if __name__ == "__main__":
    inspect_vectors()
