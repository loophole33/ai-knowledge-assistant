"""智能助手 - 主入口"""
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

from src.config import SYSTEM_PROMPT
from src.session_state import init_session_state
from src.persistence import save_messages_to_file, update_document
from src.knowledge_base import KnowledgeBase
from src.agent import build_agent
from src.ui import render_sidebar, render_chat_history

load_dotenv()
st.set_page_config(page_title="智能助手", page_icon="🤖", layout="wide")

# 初始化
init_session_state()

# 初始化知识库和 Agent
if st.session_state.kb is None:
    st.session_state.kb = KnowledgeBase()
if st.session_state.agent is None:
    st.session_state.agent = build_agent()

# UI 布局
st.title("🤖 智能助手")
st.markdown("支持数学计算、天气查询、知识库检索、文档写作与保存")

# 侧边栏（上传、文档预览、设置）
render_sidebar()

# 主区域：显示对话历史
render_chat_history()

# 处理用户输入
if prompt := st.chat_input("请输入你的问题..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_messages_to_file()

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                langchain_messages = [
                    HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"])
                    for m in st.session_state.messages
                ]
                result = st.session_state.agent.invoke({"messages": langchain_messages})
                final_answer = result["messages"][-1].content
                st.write(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
                save_messages_to_file()
            except Exception as e:
                st.error(f"出错: {e}")

    # 处理文档更新
    if st.session_state.pending_document:
        update_document(st.session_state.pending_document, "ai")
        st.session_state.pending_document = None
        st.rerun()
    if st.session_state.document_needs_rerun:
        st.session_state.document_needs_rerun = False
        st.rerun()