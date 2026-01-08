#from rag import get_rag_engine
#import google.generativeai as genai
import rag

def main():
    #query_engine = get_rag_engine()
    query_engine = rag.get_rag_engine()

    print("\nRAG system ready. Ask a question:\n")

    while True:
        query = input(">> ")
        if query.lower() in ["exit", "quit"]:
            break

        response = query_engine.query(query)

        print("\nAnswer:\n")
        print(response.response)

        print("\nSources:\n")
        for node in response.source_nodes:
            print(
                f"- {node.metadata.get('file_name', 'unknown')} "
                f"(score={node.score:.3f})"
            )
        print("\n" + "-"*50)

if __name__ == "__main__":
    main()
