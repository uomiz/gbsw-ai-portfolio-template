"""
실습 5: QnA 체인 완성
"""

import os
import warnings
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

warnings.filterwarnings("ignore", category=FutureWarning)

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


CHROMA_DIR = Path(__file__).resolve().parent / "chroma_db"


def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)


def create_chain():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(".env 파일에 GEMINI_API_KEY를 설정하세요.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
    )
    emb = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key,
    )
    db = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=emb,
    )
    retriever = db.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_template(
        """
너는 지원자의 포트폴리오를 소개하는 어시스턴트야.
아래 문서 내용만 근거로 답변해.
문서에 없는 내용은 "포트폴리오에 없는 정보입니다"라고 답해.

[문서]
{context}

[질문]
{question}
"""
    )

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


chain = create_chain()


if __name__ == "__main__":
    print(chain.invoke("학교 생활의 문제를 해결하려고 만든 서비스는?"))
