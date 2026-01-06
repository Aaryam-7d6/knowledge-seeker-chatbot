#COLLECTION_NAME = "knowledge_docs" # name 4 minilm-l6 mode
#COLLECTION_NAME = "knowledge_docs_4_search" # name 4 multi-qa-mpnet-base-dot-v1 model
COLLECTION_NAME = "knowledge_docs_bett_emb" # name 4 all-mpnet-base-v2 model
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
#EMBED_MODEL_NAME = "all-MiniLM-L6-v2" # good 4 fast and base line embaddings.
#EMBED_MODEL_NAME = "sentence-transformers/multi-qa-mpnet-base-dot-v1" # better for search use case.
EMBED_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2" # better embaddings but slower.