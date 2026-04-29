"""LangGraph Agent 构建"""
import streamlit as st
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Sequence, Annotated
from langchain_core.messages import BaseMessage
from src.config import DEEPSEEK_MODEL, SYSTEM_PROMPT
from src.tools import tools


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def agent_node(state: AgentState):
    """LLM 节点"""
    messages = state["messages"]
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)
    response = st.session_state.llm_with_tools.invoke(messages)
    return {"messages": [response]}


def should_continue(state: AgentState) -> str:
    """判断是否调用工具"""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"


@st.cache_resource
def build_agent():
    """构建并编译 Agent 图"""
    llm = ChatDeepSeek(model=DEEPSEEK_MODEL, temperature=0)
    st.session_state.llm_with_tools = llm.bind_tools(tools)

    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(tools))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
    graph.add_edge("tools", "agent")
    return graph.compile()