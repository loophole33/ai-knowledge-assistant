"""知识库管理类 - 向量数据库操作"""
import os
import tempfile
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from src.config import CHROMA_PERSIST_DIR, CHROMA_COLLECTION_NAME
from src.session_state import get_embeddings


class KnowledgeBase:
    """知识库管理类，支持向量存储和检索"""

    def __init__(self):
        self.persist_directory = CHROMA_PERSIST_DIR
        self.collection_name = CHROMA_COLLECTION_NAME
        self.vectorstore = None
        self.embeddings = get_embeddings()

        # 尝试加载已有知识库
        if os.path.exists(self.persist_directory) and os.listdir(self.persist_directory):
            try:
                self.vectorstore = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name
                )
            except Exception as e:
                st.error(f"加载知识库失败: {e}")

    def add_document_from_bytes(self, file_bytes, file_name: str):
        """
        从字节数据添加文档到知识库
        返回: (消息, 文档完整内容)
        """
        tmp_path = None
        full_content = ""
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_name)[1]) as tmp_file:
                tmp_file.write(file_bytes)
                tmp_path = tmp_file.name

            # 根据文件类型选择加载器
            if file_name.endswith('.pdf'):
                loader = PyPDFLoader(tmp_path)
            elif file_name.endswith('.txt'):
                loader = TextLoader(tmp_path, encoding='utf-8')
            else:
                return f"不支持的文件类型: {file_name}", None

            # 加载文档
            documents = loader.load()
            full_content = "\n\n".join([d.page_content for d in documents])

            # 切分文档
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(documents)

            # 添加到向量库
            if self.vectorstore is None:
                self.vectorstore = Chroma.from_documents(
                    documents=chunks,
                    embedding=self.embeddings,
                    persist_directory=self.persist_directory,
                    collection_name=self.collection_name
                )
            else:
                self.vectorstore.add_documents(chunks)

            # 持久化
            self.vectorstore.persist()
            return f"✅ 成功加载文档 {file_name}，共 {len(chunks)} 个文本块", full_content

        except Exception as e:
            return f"加载文档失败: {e}", None
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def search(self, query: str, k: int = 3) -> str:
        """在知识库中搜索相关内容"""
        if self.vectorstore is None:
            return "知识库为空，请先上传文档"

        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            if not docs:
                return "未找到相关信息"

            results = []
            for i, doc in enumerate(docs):
                source = doc.metadata.get('source', '未知来源')
                content = doc.page_content[:500]
                results.append(f"[{i + 1}] 来自 {source}:\n{content}\n")
            return "\n".join(results)
        except Exception as e:
            return f"搜索出错: {e}"