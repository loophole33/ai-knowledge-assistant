"""LangChain 工具函数"""
import math
import requests
import streamlit as st
from datetime import datetime
import pytz
from langchain_core.tools import tool
from src.persistence import update_document


@tool
def calculate(expression: str) -> str:
    """计算数学表达式的值。支持 + - * / ** sqrt sin cos log 等。"""
    try:
        allowed_funcs = {
            'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'log': math.log, 'log10': math.log10, 'exp': math.exp, 'pow': math.pow,
            'pi': math.pi, 'e': math.e, 'abs': abs, 'round': round
        }
        if '% of' in expression:
            parts = expression.split('% of')
            percent = float(parts[0].strip())
            number = float(parts[1].strip())
            result = (percent / 100) * number
            return f"计算结果: {expression} = {result}"
        safe_dict = {'__builtins__': {}, **allowed_funcs}
        result = eval(expression, safe_dict, {})
        return f"计算结果: {expression} = {result}"
    except Exception as e:
        return f"计算表达式出错: {e}"


@tool
def get_weather(city: str) -> str:
    """查询指定城市的当前天气。"""
    try:
        response = requests.get(f"https://wttr.in/{city}?format=%C+%t&lang=zh", timeout=10)
        if response.status_code == 200:
            return f"{city}的天气: {response.text.strip()}"
        return f"无法获取{city}的天气信息"
    except Exception as e:
        return f"查询天气出错: {e}"


@tool
def get_current_time(timezone: str = "Asia/Shanghai") -> str:
    """获取指定时区的当前时间。"""
    try:
        city_to_timezone = {
            '北京': 'Asia/Shanghai', '上海': 'Asia/Shanghai', '香港': 'Asia/Hong_Kong',
            '东京': 'Asia/Tokyo', '纽约': 'America/New_York', '伦敦': 'Europe/London'
        }
        if timezone in city_to_timezone:
            timezone = city_to_timezone[timezone]
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return f"{timezone} 当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    except Exception as e:
        return f"获取时间失败: {e}"


@tool
def save_to_document(content: str) -> str:
    """将生成的文档内容保存到当前文档中。"""
    update_document(content, "ai")
    st.session_state.document_needs_rerun = True
    preview = content[:200] + "..." if len(content) > 200 else content
    return f"✅ 内容已保存到当前文档！\n\n📝 预览：\n{preview}\n\n📊 共 {len(content)} 字符。"


@tool
def read_document() -> str:
    """读取当前文档的内容。"""
    if st.session_state.document_content:
        content = st.session_state.document_content
        preview = content[:500] + "..." if len(content) > 500 else content
        return f"当前文档内容：\n{preview}\n\n共 {len(content)} 字符"
    return "当前没有文档内容。"


@tool
def save_to_file(filename: str) -> str:
    """将当前文档保存到本地文件。"""
    if not st.session_state.document_content:
        return "没有可保存的内容"
    if not filename.endswith('.txt'):
        filename = filename + '.txt'
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(st.session_state.document_content)
        return f"✅ 文档已保存为: {filename}"
    except Exception as e:
        return f"保存失败: {e}"


@tool
def search_knowledge(query: str) -> str:
    """在知识库中搜索相关信息。"""
    if st.session_state.kb is None:
        return "知识库未初始化"
    return st.session_state.kb.search(query)

tools = [calculate, get_weather, get_current_time, save_to_document, read_document, save_to_file, search_knowledge]