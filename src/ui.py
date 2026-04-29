"""Streamlit UI 组件"""
import streamlit as st
import os
import tempfile
from src.persistence import update_document, save_document_to_file, delete_messages_file, delete_document_file
from src.knowledge_base import KnowledgeBase
from langchain_community.document_loaders import PyPDFLoader


def render_sidebar():
    """渲染侧边栏（配置、知识库管理、当前文档预览）"""
    with st.sidebar:
        st.header("⚙️ 配置")

        # API Key 输入
        api_key = st.text_input(
            "DeepSeek API Key",
            type="password",
            value=os.getenv("DEEPSEEK_API_KEY", "")
        )
        if api_key:
            os.environ["DEEPSEEK_API_KEY"] = api_key

        st.markdown("---")

        # 知识库管理
        st.header("📚 知识库管理")

        # 显示上传状态
        if st.session_state.get("upload_status"):
            st.success(st.session_state.upload_status)
            st.session_state.upload_status = None

        # 文件上传器
        uploaded_file = st.file_uploader(
            "上传文档 (PDF/TXT)",
            type=["pdf", "txt"],
            key=f"uploader_{st.session_state.get('file_uploader_key', 0)}"
        )

        if uploaded_file is not None:
            with st.spinner("正在处理..."):
                result, content = st.session_state.kb.add_document_from_bytes(
                    uploaded_file.getvalue(),
                    uploaded_file.name
                )
                if content is not None:
                    update_document(content, "upload")
                    st.session_state.file_uploader_key = st.session_state.get("file_uploader_key", 0) + 1
                    st.session_state.upload_status = result
                    st.rerun()
                else:
                    st.error(result)

        st.markdown("---")

        # 当前文档预览
        st.header("📄 当前文档")

        if st.session_state.document_content:
            doc_len = len(st.session_state.document_content)
            source = st.session_state.document_source or "未知"
            source_text = "上传" if source == "upload" else "AI生成" if source == "ai" else "未知"
            st.caption(f"共 {doc_len} 字符 | 来源: {source_text}")

            with st.expander("预览文档内容", expanded=True):
                st.text_area(
                    "文档内容",
                    st.session_state.document_content,
                    height=250,
                    key=f"doc_preview_{st.session_state.get('document_version', 0)}",
                    disabled=True,
                    label_visibility="collapsed"
                )

            if st.button("🗑️ 清空文档", use_container_width=True):
                update_document("", None)
                st.session_state.file_uploader_key = st.session_state.get("file_uploader_key", 0) + 1
                st.rerun()
        else:
            st.info("📭 暂无文档内容\n\n可通过：1.上传文件 2.让AI写文章")

        st.markdown("---")

        # 清除对话历史
        if st.button("🗑️ 清除对话历史", use_container_width=True):
            st.session_state.messages = []
            update_document("", None)
            st.session_state.file_uploader_key = st.session_state.get("file_uploader_key", 0) + 1
            delete_messages_file()
            delete_document_file()
            st.rerun()


def render_chat_history():
    """渲染对话历史"""
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.write(msg["content"])