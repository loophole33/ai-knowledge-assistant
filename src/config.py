"""配置文件和常量定义"""
import os

# ========== 文件路径 ==========
CHAT_HISTORY_FILE = "data/chat_history.json"
DOCUMENT_BACKUP_FILE = "data/document_backup.json"
CHROMA_PERSIST_DIR = "data/chroma_db"
CHROMA_COLLECTION_NAME = "knowledge_base"

# ========== 模型配置 ==========
DEEPSEEK_MODEL = "deepseek-chat"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ========== 系统提示 ==========
SYSTEM_PROMPT = """你是智能助手，可以调用以下工具：

1. calculate(expression): 数学计算
2. get_weather(city): 天气查询  
3. get_current_time(timezone): 时间查询
4. search_knowledge(query): 知识库搜索
5. save_to_document(content): 保存文章/信件到文档
6. read_document(): 读取当前文档
7. save_to_file(filename): 保存文档到文件

【重要规则】
- 用户要求"写"内容时，生成后必须调用 save_to_document()
- 回答问题简洁准确"""

# ========== 目录初始化 ==========
os.makedirs("data", exist_ok=True)