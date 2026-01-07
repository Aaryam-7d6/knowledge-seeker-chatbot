from indexing import build_index
from logger import logger
from qdrant_client import QdrantClient
import config

def main():
    logger.info("Starting document ingestion & indexing")
    #print(" Starting document ingestion & indexing... ")

    index = build_index(data_dir="data")
    logger.info("Documents successfully indexed into Qdrant")
    #print(" Documents successfully indexed into Qdrant.")

if __name__ == "__main__":
    main()
    client = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)
    print(client.get_collections()) #prints all collections
    print()
    print(client.get_collection(config.COLLECTION_NAME)) #prints specific collection details
    print()
