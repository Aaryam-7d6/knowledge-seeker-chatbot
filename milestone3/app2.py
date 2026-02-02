import streamlit as st
from indexing import build_index
from rag_eng import get_rag_engine
from summary_eng import generate_document_summary
from search import get_query_engine
from utils.file_handl import save_uploaded_file
import config
import os
from llama_index.core.memory import ChatMemoryBuffer

# Page configuration
st.set_page_config(
    page_title="KnowledgeSeeker",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern, minimalistic design
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main container styling */
    .main {
        padding: 0rem 2rem;
    }
    
    /* Chat container */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem 0;
    }
    
    /* Header styling */
    .app-header {
        text-align: center;
        padding: 2rem 0 3rem 0;
        border-bottom: 1px solid rgba(128, 128, 128, 0.1);
        margin-bottom: 2rem;
    }
    
    .app-title {
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .app-subtitle {
        font-size: 0.95rem;
        color: #6b7280;
        font-weight: 400;
    }
    
    /* Settings panel */
    .settings-panel {
        background: rgba(128, 128, 128, 0.05);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    }
    
    /* Message bubbles */
    .stChatMessage {
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-radius: 12px;
    }
    
    /* Source cards */
    .source-card {
        background: rgba(128, 128, 128, 0.05);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #667eea;
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    /* File uploader */
    .stFileUploader {
        border-radius: 8px;
    }
    
    /* Input field */
    .stTextInput>div>div>input {
        border-radius: 8px;
        padding: 0.75rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        border-radius: 8px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'memory' not in st.session_state:
    st.session_state.memory = ChatMemoryBuffer.from_defaults(token_limit=15000)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'show_settings' not in st.session_state:
    st.session_state.show_settings = False

if 'show_summary' not in st.session_state:
    st.session_state.show_summary = False

# Header
st.markdown("""
<div class="app-header">
    <div class="app-title">KnowledgeSeeker</div>
    <div class="app-subtitle">A RAG-based conversational AI for knowledge seekers and autodidactic learners</div>
</div>
""", unsafe_allow_html=True)

# Top action bar
col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

# with col2:
#     if st.button("Settings", use_container_width=True):
#         st.session_state.show_settings = not st.session_state.show_settings

with col3:
    if st.button("Summary", use_container_width=True):
        st.session_state.show_summary = not st.session_state.show_summary

with col4:
    if st.button("Upload", use_container_width=True):
        st.session_state.show_upload = not st.session_state.get('show_upload', False)
        
with col2:
    if st.button("Settings", use_container_width=True):
        st.session_state.show_settings = not st.session_state.show_settings

# Settings Panel (collapsible)
if st.session_state.show_settings:
    with st.expander("Advanced Settings", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            creativity = st.slider(
                "Response Creativity (Temperature)",
                min_value=0.0,
                max_value=2.0,
                value=0.5,
                step=0.1,
                key="creativity",
                help="Higher values make responses more creative but less focused"
            )
            
        with col2:
            top_k = st.slider(
                "Top-K Results",
                min_value=5,
                max_value=10,
                value=6,
                key="top_k",
                help="Number of relevant chunks to retrieve"
            )
        
        search_options = ["hybrid", "vector", "keyword"]
        default_index = search_options.index(config.SEARCH_MODE) if config.SEARCH_MODE in search_options else 0
        
        search_mode = st.selectbox(
            "Search Mode",
            search_options,
            index=default_index,
            help="Hybrid combines vector and keyword search for best results"
        )

# Upload Panel (collapsible)
if st.session_state.get('show_upload', False):
    with st.expander("Document Management", expanded=True):
        uploaded_files = st.file_uploader(
            "Upload your documents (PDF, TXT, DOCX, MD)",
            type=["pdf", "txt", "docx", "md"],
            accept_multiple_files=True,
            help="Upload one or more documents to query"
        )
        
        if uploaded_files:
            st.markdown("**Uploaded files:**")
            for uploaded_file in uploaded_files:
                file_path = os.path.join(config.DATA_DIR, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"{uploaded_file.name}", icon="✅")
            
            if st.button("🔍 Index Documents", use_container_width=True):
                with st.spinner("Indexing documents..."):
                    build_index(config.DATA_DIR)
                st.success("Indexing completed successfully!", icon="✅")

# Summary Panel (collapsible)
if st.session_state.show_summary:
    with st.expander("Document Summary (TL;DR)", expanded=True):
        if st.button("Generate Summary", use_container_width=True):
            with st.spinner("Summarizing documents..."):
                summary = generate_document_summary()
                st.markdown(summary)

# Check if documents are indexed
if not os.path.exists(os.path.join(config.STORAGE_DIR, "docstore.json")):
    st.info("Welcome! Please upload and index documents to get started.", icon="ℹ️")
    st.stop()

# Chat history display
if st.session_state.chat_history:
    st.markdown("---")
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message and message["sources"]:
                with st.expander(" View Sources", expanded=False):
                    for source in message["sources"]:
                        st.markdown(
                            f'<div class="source-card">'
                            f'<strong>{source["file"]}</strong> '
                            f'<span style="color: #6b7280;">(relevance: {source["score"]:.1%})</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )

# Chat input
st.markdown("---")
query = st.chat_input("Ask a question about your documents...")

if query:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": query})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(query)
    
    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Get settings
            search_mode_val = search_mode if st.session_state.show_settings else config.SEARCH_MODE
            query_engine = get_query_engine(search_mode_val)
            
            # Update config if settings are shown
            if st.session_state.show_settings:
                config.TEMPERATURE = creativity
                config.TOP_K = top_k
            
            # Get response
            response = query_engine.chat(query)
            
            # Display response
            st.markdown(response.response)
            
            # Prepare sources
            sources = []
            if response.source_nodes:
                with st.expander("View Sources", expanded=False):
                    for node in response.source_nodes:
                        file_name = node.metadata.get('file_name', 'unknown')
                        score = node.score
                        sources.append({"file": file_name, "score": score})
                        st.markdown(
                            f'<div class="source-card">'
                            f'<strong>{file_name}</strong> '
                            f'<span style="color: #6b7280;">(relevance: {score:.1%})</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
            
            # Add assistant message to chat history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response.response,
                "sources": sources
            })

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #6b7280; font-size: 0.85rem; padding: 1rem 0;">'
    'Powered by Python, Streamlit, LlamaIndex & QdrantDB • Built for knowledge seekers and autodidactics • Inspired by NotebookLM • Document Intelligence System'
    '</div>',
    unsafe_allow_html=True
)