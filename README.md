# 📚 AI 知识库问答助手

一个基于 RAG（检索增强生成）技术的智能问答系统。上传文档即可让 AI 基于文档内容回答问题，同时也支持无文档时直接对话。

## ✨ 功能特点

- 📄 **动态知识库**：支持上传 `.txt` 文件作为知识来源，可随时更换
- 🔍 **RAG 检索增强**：先检索相关内容再生成回答，有效避免 AI 胡编乱造
- 🆓 **免费 Embedding**：使用 HuggingFace 本地模型，无需额外付费，保护数据隐私
- 🎛️ **可调参数**：支持调节温度（回答随机性）和文本块大小
- 💬 **友好界面**：基于 Streamlit 构建，操作简单直观
- 🧹 **一键清除**：支持清空知识库，方便切换不同文档

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| 前端框架 | Streamlit |
| 大语言模型 | DeepSeek API |
| 向量数据库 | Chroma |
| Embedding 模型 | HuggingFace (all-MiniLM-L6-v2) |
| 开发语言 | Python 3.8+ |

## 📦 安装与运行

### 环境要求

- Python 3.8 或更高版本
- DeepSeek API Key（在 platform.deepseek.com 免费注册获取）

### 安装步骤

1. 克隆仓库

git clone https://github.com/suverice/ai-knowledge-assistant.git
cd ai-knowledge-assistant

2. 创建虚拟环境

python -m venv venv

3. 激活虚拟环境

Windows 系统：

venv\Scripts\activate

Mac 或 Linux 系统：

source venv/bin/activate

4. 安装依赖

pip install -r requirements.txt

5. 运行应用

streamlit run app.py

6. 打开浏览器访问

http://localhost:8501

## 使用说明

1. 在左侧边栏输入 DeepSeek API Key

2. 可选：上传 txt 格式的知识库文件

3. 在输入框中输入问题

4. 如果上传了文件，AI 会基于文件内容回答

5. 如果未上传文件，AI 会直接对话（不检索）

## 核心原理

本项目采用 RAG（检索增强生成）架构：

第一步：文档处理

上传的文档被切分成文本块，使用 HuggingFace Embedding 模型转换为向量

第二步：向量存储

向量数据存储在 Chroma 数据库中，便于快速检索

第三步：检索增强

用户提问时，先从向量库中检索最相关的文本块

第四步：生成回答

将检索到的内容和问题一起提交给 DeepSeek 模型生成答案

## 项目结构

ai-knowledge-assistant/
├── app.py              # 主程序
├── requirements.txt    # 依赖列表
└── README.md           # 项目说明

## 作者

suverice
GitHub主页链接：https://github.com/suverice

## 开源协议

MIT License
