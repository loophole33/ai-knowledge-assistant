"""session_state 初始化"""
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import EMBEDDING_MODEL
from src.persistence import load_messages_from_file, load_document_from_file

@st.cache_resource
def get_embeddings():
    """加载 Embedding 模型（缓存）"""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def init_session_state():
    """初始化所有 session_state 变量"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
        load_messages_from_file()
    if "kb" not in st.session_state:
        st.session_state.kb = None
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "document_content" not in st.session_state:
        st.session_state.document_content = ""
        load_document_from_file()
    if "document_source" not in st.session_state:
        st.session_state.document_source = ""
    if "pending_document" not in st.session_state:
        st.session_state.pending_document = None
    if "document_version" not in st.session_state:
        st.session_state.document_version = 0
    if "document_needs_rerun" not in st.session_state:
        st.session_state.document_needs_rerun = False
    if "file_uploader_key" not in st.session_state:
        st.session_state.file_uploader_key = 0
    if "upload_status" not in st.session_state:
        st.session_state.upload_status = None