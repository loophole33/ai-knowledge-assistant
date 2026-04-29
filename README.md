# AI Knowledge Assistant

一个基于 Streamlit、LangChain、LangGraph、ChromaDB 和 DeepSeek API 构建的本地知识库智能助手。

项目支持对话问答、PDF/TXT 文档上传、知识库检索、AI 文档写作、当前文档预览、对话历史与文档内容持久化等能力。适合作为个人知识库、文档问答助手、学习资料助手或轻量级 RAG 应用原型。

## 功能特性

- 智能对话：通过 DeepSeek Chat API 完成自然语言问答。
- 知识库检索：上传 PDF 或 TXT 文件后，自动切分文本并写入 ChromaDB 向量库。
- 文档问答：可以围绕已上传文档提问，AI 会检索相关片段后回答。
- AI 写作：当用户要求生成文章、信件、总结、报告等内容时，AI 会将结果保存到“当前文档”。
- 当前文档预览：左侧栏实时显示 AI 生成或本地上传的最新文档内容。
- 上传覆盖：上传新的本地文档会直接覆盖当前文档预览，无需先手动清空。
- 多轮覆盖：连续让 AI 生成多篇内容时，左侧栏会显示最新一次生成的文档。
- 工具调用：内置数学计算、天气查询、时间查询、文档读取、文档保存等工具。
- 数据持久化：对话历史和当前文档会保存到本地 JSON 文件，刷新页面后仍可恢复。

## 技术栈

| 类型 | 技术 |
| --- | --- |
| Web 界面 | Streamlit |
| 大语言模型 | DeepSeek Chat API |
| Agent 编排 | LangGraph |
| LLM 工具封装 | LangChain |
| 向量数据库 | ChromaDB |
| Embedding 模型 | sentence-transformers/all-MiniLM-L6-v2 |
| 文档加载 | PyPDFLoader、TextLoader |
| 环境变量 | python-dotenv |
| 开发语言 | Python |

## 项目结构

```text
ai-knowledge-assistant/
├── app.py                     # Streamlit 主入口
├── requirements.txt           # Python 依赖
├── README.md                  # 项目说明文档
├── data/                      # 运行时数据目录，程序会自动生成
│   ├── chat_history.json      # 对话历史
│   ├── document_backup.json   # 当前文档备份
│   └── chroma_db/             # ChromaDB 向量库数据
└── src/
    ├── __init__.py
    ├── agent.py               # LangGraph Agent 构建
    ├── config.py              # 路径、模型、系统提示词配置
    ├── knowledge_base.py      # 文档加载、切分、向量库写入与检索
    ├── persistence.py         # 对话与文档持久化
    ├── session_state.py       # Streamlit session_state 初始化
    ├── tools.py               # AI 可调用工具
    └── ui.py                  # 侧边栏与聊天历史 UI
```

## 环境要求

- Python 3.9 或更高版本
- DeepSeek API Key
- Windows、macOS、Linux 均可运行

DeepSeek API Key 可在 [DeepSeek Platform](https://platform.deepseek.com/) 获取。

## 安装与运行

1. 克隆项目

```bash
git clone https://github.com/loophole33/ai-knowledge-assistant.git
cd ai-knowledge-assistant
```

如果你已经在本地拥有项目目录，可以直接进入项目根目录。

2. 创建虚拟环境

Windows PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows CMD：

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

macOS / Linux：

```bash
python -m venv .venv
source .venv/bin/activate
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 配置 API Key

方式一：创建 `.env` 文件。

```env
DEEPSEEK_API_KEY=你的 DeepSeek API Key
```

方式二：启动应用后，在左侧栏的 `DeepSeek API Key` 输入框中填写。

5. 启动应用

```bash
streamlit run app.py
```

启动后浏览器会自动打开页面；如果没有自动打开，可以访问终端中显示的本地地址，通常是：

```text
http://localhost:8501
```

## 使用说明

### 1. 普通对话

在页面底部输入问题，AI 会在主聊天区回答。

示例：

```text
请介绍一下 RAG 是什么
```

### 2. 上传本地文档

在左侧栏“知识库管理”区域上传 PDF 或 TXT 文件。上传成功后：

- 文档会被写入向量知识库。
- 文档全文会覆盖左侧栏“当前文档”的预览内容。
- 后续可以围绕该文档提问。

示例问题：

```text
这份文档主要讲了什么？
```

```text
请总结文档中的关键观点
```

```text
搜索文档里关于项目风险的内容
```

### 3. 让 AI 生成文章

当你要求 AI 写文章、信件、总结、报告等内容时，AI 会调用 `save_to_document` 工具，把生成内容保存到当前文档。

示例：

```text
帮我写一篇关于人工智能学习方法的文章
```

```text
写一封给客户的项目延期说明邮件
```

```text
生成一份个人知识库应用的产品介绍
```

生成完成后，左侧栏“当前文档”会显示最新内容。

### 4. 覆盖当前文档

当前文档有两种来源：

- AI 生成
- 本地上传

无论当前文档来自哪里，后续操作都会直接覆盖旧内容：

- 再次让 AI 写一篇新文章，会覆盖旧文章。
- 上传新的 PDF/TXT 文件，会覆盖旧的 AI 生成内容。
- 不需要先点击“清空文档”。

### 5. 读取当前文档

你可以直接问：

```text
当前文档写了什么？
```

```text
请读取当前文档并总结
```

AI 会调用 `read_document` 工具读取当前文档内容。

### 6. 保存当前文档到本地文件

示例：

```text
把当前文档保存为 result.txt
```

如果没有写 `.txt` 后缀，程序会自动补充。

保存路径默认为程序运行目录。

### 7. 其他内置工具

数学计算：

```text
计算 15% of 200
```

```text
sqrt(16) + 2**3
```

天气查询：

```text
查询北京天气
```

```text
London weather
```

时间查询：

```text
现在几点？
```

```text
纽约当前时间
```

## 数据文件说明

程序会在 `data/` 目录下保存运行数据：

| 文件或目录 | 说明 |
| --- | --- |
| `data/chat_history.json` | 保存聊天历史 |
| `data/document_backup.json` | 保存当前文档内容和来源 |
| `data/chroma_db/` | 保存 ChromaDB 向量库数据 |

如果想完全重置应用数据，可以在关闭应用后删除 `data/` 目录。

## 常见问题

### 1. 页面提示 DeepSeek API Key 错误

请检查：

- `.env` 文件中是否配置了 `DEEPSEEK_API_KEY`
- API Key 是否仍然有效
- 当前终端是否在项目根目录运行
- 是否在左侧栏输入框中填入了正确的 Key

### 2. 第一次运行下载模型较慢

Embedding 模型 `sentence-transformers/all-MiniLM-L6-v2` 首次使用时需要下载。下载完成后会走本地缓存，后续启动会更快。

### 3. 上传 PDF 后内容不完整

PDF 解析效果取决于原文件质量。如果 PDF 是扫描图片版，普通文本解析器可能无法提取文字，需要先进行 OCR。

### 4. 知识库检索结果不准确

可以尝试：

- 上传文本质量更高的文档
- 提问时使用更明确的关键词
- 调整 `src/knowledge_base.py` 中的 chunk 大小和 overlap 参数
- 更换更强的 Embedding 模型

### 5. 端口被占用

可以指定其他端口启动：

```bash
streamlit run app.py --server.port 8502
```

## 开发说明

主要模块职责：

- `app.py`：应用入口，负责初始化、页面主流程和用户输入处理。
- `src/ui.py`：负责侧边栏、上传、当前文档预览、清空按钮和聊天历史展示。
- `src/tools.py`：定义 AI 可以调用的工具函数。
- `src/knowledge_base.py`：负责文档读取、文本切分、向量化和相似度检索。
- `src/persistence.py`：负责聊天记录和当前文档的本地保存。
- `src/session_state.py`：集中初始化 Streamlit 状态。
- `src/agent.py`：构建 LangGraph Agent。
- `src/config.py`：集中管理模型名称、文件路径和系统提示词。

## 后续可优化方向

- 增加 OCR，支持扫描版 PDF。
- 增加 Word、Markdown、Excel 等更多文件格式。
- 增加知识库文件管理，可以删除指定文档。
- 增加多知识库切换。
- 增加聊天记录导出。
- 增加模型选择和温度参数配置。
- 增加 Docker 部署配置。

## License

本项目可作为学习、课程作业、个人工具或二次开发模板使用。正式发布前建议补充明确的开源许可证。
