from indexing import build_index
from logger import logger
from qdrant_client import QdrantClient
import config
import os

os.environ['HTT_TIMEOUT'] = '100'  # Increase timeout to 100 seconds

def pathc(path: str) -> bool:
    if os.path.exists(path):
        return True
    else:
        return False

def ip_path():
    #print("Please provide the path to the directory containing documents to be indexed. WITHOUT quotes.")
    logger.info("Please provide the path to the directory containing documents to be indexed. WITHOUT quotes.")
    path = input("Please enter a valid path to the directory containing documents: ")
    #n_path = path.split('"')[0]
    #x = path.strip()
    #y = x.strip('"')
    #path = y.strip()
    check = pathc(path)
    try: 
        if check:
            build_index(data_dir=path)
    
    except:
        #print("An error occurred while building the index. Please check the provided path and try again.")
        logger.info("An error occurred while building the index. Please check the provided path and try again.")
        ip_path()
    #return path

def main():
    logger.info("Starting document ingestion & indexing")
    #print(" Starting document ingestion & indexing... ")
    
    #index = build_index(data_dir="data")
    path = ip_path()
    #while not pathc(path):
        #print("The provided path does not exist. Please try again.")
        #path = ip_path()
    logger.info("Documents successfully indexed into Qdrant")
    #print(" Documents successfully indexed into Qdrant.")

if __name__ == "__main__":
    main()
    # checking scripts....
    client = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)
    print(client.get_collections()) #prints all collections
    print()
    print(client.get_collection(config.COLLECTION_NAME)) #prints specific collection details
    print()
