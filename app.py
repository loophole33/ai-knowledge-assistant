import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_deepseek import ChatDeepSeek
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

# 设置页面配置
st.set_page_config(page_title="我的知识库问答助手")
temperature = st.slider("回答温度", min_value=0.0, max_value=1.0, value=0.0, step=0.1, format="%.1f", help="回答温度，值越高，回答越随机")
chunk_size = st.slider("知识库片段大小", min_value=100, max_value=1000, value=200, step=50, format="%d", help="知识库片段大小，值越大，回答越准确，但耗时越长")
# 创建侧边栏
with st.sidebar:
    st.header("⚙️ 配置")  # 侧边栏标题
    # 创建API密钥输入框，密码类型隐藏输入
    deepseek_api_key = st.text_input("DeepSeek API Key", type="password",
                                     help="去 https://platform.deepseek.com/ 注册获取")
    file = st.file_uploader(
        "上传知识库文件", type=None, help="上传包含知识库的文本文件"
    )
    if st.button("🗑️ 清除知识库"):
        st.session_state["vectorstore"] = None
        st.rerun()
    st.markdown("---")  # 添加分隔线
    st.markdown("### 使用说明")  # 添加说明标题
    st.markdown("1. 可选提交文件，模型将基于所提交文件内容进行回答")  # 使用说明1
    st.markdown("2. 输入 DeepSeek API Key（可去官方网站免费获取）")  # 使用说明2
    st.markdown("3. 开始提问")  # 使用说明3

# 检查API密钥是否输入
if not deepseek_api_key:
    st.warning("⚠️ 请在左侧输入 DeepSeek API Key")  # 显示警告信息
    st.stop()
vectorstore = None
# 检查知识库文件是否存在
if file is not None:
    with st.spinner(f"📖 正在处理文件：{file.name}..."):
        # 读取原始字节并检测编码
        raw_content = file.getvalue()
        # 尝试用常见编码解码
        content = None
        for enc in ['utf-8', 'gbk', 'gb2312', 'gb18030']:
            try:
                content = raw_content.decode(enc)
                st.info(f"📝 检测到文件编码：{enc}")
                break
            except UnicodeDecodeError:
                continue
        if content is None:
            st.error("❌ 无法识别文件编码，请用记事本将文件另存为 UTF-8 格式")
            st.stop()
        documents = [Document(page_content=content, metadata={"source": "file"})]
        # 切分文档
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=50)  # 创建文本分割器
        texts = text_splitter.split_documents(documents)  # 分割文档

# 使用 HuggingFace 的 Embedding 模型（本地运行，免费）
# 这个模型会下载一次（约 80MB），之后离线可用
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",  # 指定模型名称
            model_kwargs={'device': 'cpu'},  # 设置设备为CPU
            encode_kwargs={'normalize_embeddings': True}  # 设置编码参数
        )

# 创建向量数据库
        vectorstore = Chroma.from_documents(texts, embeddings)  # 从文档创建向量存储
        st.session_state["vectorstore"] = vectorstore
        st.success("✅ 加载完成:"+file.name)  # 显示成功消息
elif "vectorstore" in st.session_state:
     vectorstore = st.session_state["vectorstore"]
     st.info(f"📁 当前使用已上传的知识库")

llm = ChatDeepSeek(
model="deepseek-chat",  # 指定模型名称
api_key=deepseek_api_key,  # 设置API密钥
temperature=temperature  # 设置温度参数为0，使输出更确定
)
if vectorstore is None:
    st.warning("⚠️ 未上传文档，模型将直接回答（不基于你的知识库）")
    # 直接问答，不检索
    prompt = PromptTemplate(
        input_variables=["question"],
        template="问题：{question}\n回答："
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    # 用 chain 替代 qa_chain
    def run_chain(q):
        return chain.run(question=q)
    qa_chain_run = run_chain
else:
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    qa_chain_run = qa_chain.run
st.header("💬 开始提问")
question = st.text_input("请输入你的问题：")
if question:
    with st.spinner("🤔 思考中..."):
        answer = qa_chain_run(question)
        st.write("### 回答：")
        st.write(answer)