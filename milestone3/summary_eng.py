from llama_index.core import VectorStoreIndex
from embed import get_embedding_model
from qdb import get_vector_store
from llm import get_llm

def generate_document_summary():
    embed_model = get_embedding_model()
    llm = get_llm()
    vector_store = get_vector_store()

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model
    )

    summary_engine = index.as_query_engine(
        llm=llm,
        response_mode="tree_summarize"
    )

    summary_prompt = (
        "Provide a concise, high-level summary of the uploaded documents. "
        "Focus on key concepts and important information."
    )

    response = summary_engine.query(summary_prompt)
    return response.response
