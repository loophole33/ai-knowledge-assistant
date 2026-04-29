"""数据持久化函数"""
import os
import json
import streamlit as st
from datetime import datetime
from src.config import CHAT_HISTORY_FILE, DOCUMENT_BACKUP_FILE


def save_messages_to_file():
    try:
        with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.messages, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存对话历史失败: {e}")


def load_messages_from_file():
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
                messages = json.load(f)
                if isinstance(messages, list):
                    st.session_state.messages = messages
        except Exception as e:
            print(f"加载对话历史失败: {e}")
            st.session_state.messages = []
    else:
        st.session_state.messages = []


def delete_messages_file():
    try:
        if os.path.exists(CHAT_HISTORY_FILE):
            os.remove(CHAT_HISTORY_FILE)
    except Exception as e:
        print(f"删除文件失败: {e}")


def save_document_to_file():
    try:
        data = {
            "content": st.session_state.document_content,
            "source": st.session_state.document_source,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(DOCUMENT_BACKUP_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存文档失败: {e}")


def load_document_from_file():
    if os.path.exists(DOCUMENT_BACKUP_FILE):
        try:
            with open(DOCUMENT_BACKUP_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                st.session_state.document_content = data.get("content", "")
                st.session_state.document_source = data.get("source", None)
        except Exception as e:
            print(f"加载文档失败: {e}")
            st.session_state.document_content = ""
            st.session_state.document_source = None
    else:
        st.session_state.document_content = ""
        st.session_state.document_source = None


def delete_document_file():
    try:
        if os.path.exists(DOCUMENT_BACKUP_FILE):
            os.remove(DOCUMENT_BACKUP_FILE)
    except Exception as e:
        print(f"删除文件失败: {e}")


def update_document(content: str, source: str):
    """统一更新文档内容"""
    st.session_state.document_content = content or ""
    st.session_state.document_source = source
    st.session_state.document_version = st.session_state.get("document_version", 0) + 1
    save_document_to_file()