
#from llama_index import LlamaIndex
#from llama_index.embeddings.huggingface import HuggingFaceEmbedding
#from llama-index-embeddings-huggingface import HuggingFaceEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from config import EMBED_MODEL_NAME

def get_embedding_model():
    return HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)
