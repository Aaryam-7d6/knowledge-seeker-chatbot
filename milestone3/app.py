import streamlit as st
from indexing import build_index
from rag_eng import get_rag_engine
from summary_eng import generate_document_summary
from search import get_query_engine
#from indexing import build_index
from utils.file_handl import save_uploaded_file
import config
import os
#from llama_index.core.memory import ChatMemoryBuffer


# for me information visit: #https://developers.llamaindex.ai/python/examples/agent/memory/chat_memory_buffer/

from llama_index.core.memory import ChatMemoryBuffer

memory = ChatMemoryBuffer.from_defaults(token_limit=1500)

if memory not in st.session_state:
    st.session_state.memory = ChatMemoryBuffer.from_defaults(token_limit = 1500)

st.set_page_config(page_title="KnowledgeSeeker",layout="wide")

st.title(" KnowledgeSeeker ")
st.caption("A RAG-based conversational AI for knowledge seekers and autodidactic learners.")
st.caption("NotebookLM-inspired Document Intelligence System.")


# --- Sidebar ---
st.sidebar.header("Document Panel")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF, TXT, DOCX, MD files",
    type=["pdf", "txt", "docx", "md"],
    accept_multiple_files=True
)

# os.makedirs(DATA_DIR, exist_ok=True)

# if uploaded_files is not None:
#     for uploaded_file in uploaded_files:
#         file_path = os.path.join(DATA_DIR, uploaded_file.name)
#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())

#         st.success(f"Uploaded {uploaded_files.name}")

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(config.DATA_DIR, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        #st.success(f"Uploaded {uploaded_file.name}")
        st.success(f"Uploaded {uploaded_file.name}")


# if st.sidebar.button("Index Documents"):
#     if uploaded_files:
#         for file in uploaded_files:
#             save_uploaded_file(file)

#         with st.spinner("Indexing documents..."):
#             #build_index(data_dir="data/uploads")
            
#             #build_index(data_dir="./storage")  # to index any previously stored docs
#             st.sidebar.success("Documents indexed successfully!")

if st.sidebar.button("Index Documents"):
    with st.spinner("Indexing documents..."):
        build_index(config.DATA_DIR)
    st.success("Indexing completed")

# --- Sidebar Summary ---
st.sidebar.markdown("---")
st.sidebar.subheader("Document Summary aka TL;DR")

if st.sidebar.button("Generate Summary"):
    with st.spinner("Summarizing documents..."):
        summary = generate_document_summary()
        st.sidebar.write(summary)

# --- Main Chat Area ---
st.subheader(f"Ask Questions because Questions are Welcomed here :)")
st.slider("Adjust Response Creativity aka the Temperature", 0.0,2.0, 0.5, key="creativity")
st.slider("Adjust the Top-K",5,10,6,key="top_k")

if creativity := st.session_state.get("creativity"):
    from config import TEMPERATURE
    TEMPERATURE = creativity
if top_k := st.session_state.get("top_k"):
    from config import TOP_K
    TOP_K = top_k
    
#search_mode = st.selectbox("Search Mode",["hybrid", "vector", "keyword"],index=0)
search_options = ["hybrid", "vector", "keyword"]
default_index = search_options.index(config.SEARCH_MODE) if config.SEARCH_MODE in search_options else 0

search_mode = st.selectbox(
    "Search Mode",
    search_options,
    index=default_index
)

if not os.path.exists(os.path.join(config.STORAGE_DIR, "docstore.json")):
    st.warning("Please upload and index documents first.")
    st.stop()


query = st.text_input("Ask a question based on uploaded documents:")

if query:
    with st.chat_message("user"):
        st.write(query)

    #response = query_engine.query(user_query)


# i use "Using Standalone" here, for me information visit: #https://developers.llamaindex.ai/python/examples/agent/memory/chat_memory_buffer/




#query_engine = get_query_engine(search_mode)


#if query:
    #query_engine = get_rag_engine()
    query_engine = get_query_engine(search_mode)
    

    with st.spinner("Thinking..."):
        #response = query_engine.query(query)
        #
        # response = query_engine.retrieve(query)
        #st.write(query_engine)
        #response = query_engine.retrieve(query)
        # response = query_engine.query(query)
        response = query_engine.chat(query)

        with st.chat_message("assistant"):
            #st.write(response.response)
            st.markdown("### Answer")
            st.write(response.response)
    #st.write(query_engine)

    st.markdown("### Sources")
    for node in response.source_nodes:
        st.markdown(
            f"- **{node.metadata.get('file_name', 'unknown')}** "
            f"(score: `{node.score:.3f}`)"
        )



# from llama_index.core.llms import ChatMessage

# chat_history = [
#     ChatMessage(role="user", content=query),
#     ChatMessage(role="assistant", content=response.response),
# ]

# # put a list of messages
# memory.put_messages(chat_history)

# # put one message at a time
# # memory.put_message(chat_history[0])

# # Get the last X messages that fit into a token limit
# history = memory.get()

# # Get all messages
# all_history = memory.get_all()

# ## clear the memory
# #memory.reset()

# st.markdown("---")
# st.markdown("### Chat History")
# # for msg in all_history:
# #     st.markdown(f"**{msg.role.capitalize()}**: {msg.content}")
# st.write(history)

# st.write("#### Full Chat History:")
# st.write(all_history)