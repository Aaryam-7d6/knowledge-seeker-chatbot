#COLLECTION_NAME = "knowledge_docs" # name 4 minilm-l6 mode
#COLLECTION_NAME = "knowledge_docs_4_search" # name 4 multi-qa-mpnet-base-dot-v1 model
#COLLECTION_NAME = "knowledge_docs_bett_emb" # name 4 all-mpnet-base-v2 model
#COLLECTION_NAME = "knowledge_docs_test_with_metadata_andlogs" # name 4 all-mpnet-base-v2 model with metadata and logs
#COLLECTION_NAME = "knowledge_docs_test_with_ip_path0" # name 4 all-mpnet-base-v2 model with metadata and logs + user ip path #------ -ve failed to do that-----
COLLECTION_NAME = "knowledge_docs_test_with_chat" # name 4 all-mpnet-base-v2 model with metadata and logs + user ip path

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

#EMBED_MODEL_NAME = "all-MiniLM-L6-v2" # good 4 fast and base line embaddings.
#EMBED_MODEL_NAME = "sentence-transformers/multi-qa-mpnet-base-dot-v1" # better for search use case.
EMBED_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2" # better embaddings but slower.

# Retrieval config
TOP_K = 6

# Gemini
GEMINI_MODEL = "models/gemini-1.5-flash"
