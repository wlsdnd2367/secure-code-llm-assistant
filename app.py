import os

import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

from security_config import MissingGoogleAPIKeyError, get_google_api_key


load_dotenv()


def init_rag_pipeline():
    loader = TextLoader("secure_coding_guide.txt", encoding="utf-8")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    splits = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash"),
        google_api_key=get_google_api_key(),
        temperature=0,
    )

    prompt = PromptTemplate.from_template(
        """
당신은 웹 보안 엔지니어입니다.
반드시 아래 [시큐어 코딩 가이드]를 우선적으로 참고하여, [파이썬 코드]에
SQL Injection 또는 Command Injection 취약점이 있는지 분석하세요.

[시큐어 코딩 가이드]
{context}

[파이썬 코드]
{input}

답변 형식:
### 🚨 취약점 탐지 결과 (원인 상세 분석)
### 🛡️ 시큐어 코딩 패치 제안 (안전한 코드 작성)
"""
    )

    def format_documents(retrieved_documents):
        return "\n\n".join(
            document.page_content for document in retrieved_documents
        )

    return (
        {
            "context": retriever | format_documents,
            "input": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )


st.set_page_config(
    page_title="SecureCode LLM Assistant",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ SecureCode LLM Assistant")
st.markdown("**AI 기반 파이썬 취약점 탐지 및 시큐어 코딩 제안 도구**")
st.divider()

try:
    rag_engine = init_rag_pipeline()
except MissingGoogleAPIKeyError as error:
    st.error(str(error))
    st.stop()

input_column, output_column = st.columns(2)

with input_column:
    st.subheader("💻 소스 코드 입력")
    user_code = st.text_area(
        "분석할 파이썬 코드를 붙여넣으세요:",
        height=400,
    )
    analyze_button = st.button(
        "취약점 분석 및 패치 생성 🚀",
        use_container_width=True,
    )

with output_column:
    st.subheader("🔍 분석 결과 및 패치 코드")
    if analyze_button:
        if not user_code.strip():
            st.warning("⚠️ 분석할 코드를 먼저 입력해 주세요.")
        else:
            with st.spinner("가이드라인을 검색하고 코드를 분석하는 중입니다..."):
                response_text = rag_engine.invoke(user_code)
                st.success("분석을 완료했습니다.")
                st.markdown(response_text)
