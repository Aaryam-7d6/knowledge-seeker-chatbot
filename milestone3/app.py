import streamlit as st
from indexing import build_index
from rag_eng import get_rag_engine
from summary_eng import generate_document_summary
from utils.file-handl import save_uploaded_file

st.set_page_config(
    page_title="KnowledgeSeeker",
    layout="wide"
)

st.title(" KnowledgeSeeker ")
st.caption("A RAG-based conversational AI for knowledge seekers and autodidactic learners. NotebookLM-inspired Document Intelligence System")

# --- Sidebar ---
st.sidebar.header("Document Panel")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF, TXT, DOCX",
    type=["pdf", "txt", "docx"],
    accept_multiple_files=True
)

if st.sidebar.button("Index Documents"):
    if uploaded_files:
        for file in uploaded_files:
            save_uploaded_file(file)

        with st.spinner("Indexing documents..."):
            build_index(data_dir="data/uploads")

        st.sidebar.success("Documents indexed successfully!")

# --- Sidebar Summary ---
st.sidebar.markdown("---")
st.sidebar.subheader("Document Summary aka TL;DR")

if st.sidebar.button("Generate Summary"):
    with st.spinner("Summarizing documents..."):
        summary = generate_document_summary()
        st.sidebar.write(summary)

# --- Main Chat Area ---
st.subheader("?? Ask Questions ??")

query = st.text_input("Ask a question based on uploaded documents:")

if query:
    query_engine = get_rag_engine()

    with st.spinner("Thinking..."):
        response = query_engine.query(query)

    st.markdown("### Answer")
    st.write(response.response)

    st.markdown("### Sources")
    for node in response.source_nodes:
        st.markdown(
            f"- **{node.metadata.get('file_name', 'unknown')}** "
            f"(score: `{node.score:.3f}`)"
        )
