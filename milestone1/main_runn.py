from indexing import build_index

def main():
    print(" Starting document ingestion & indexing... ")

    index = build_index(data_dir="data")

    print(" Documents successfully indexed into Qdrant.")

if __name__ == "__main__":
    main()
