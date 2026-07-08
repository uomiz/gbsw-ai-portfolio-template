"""
실습 5: QnA 체인 완성

목표:
- retriever, prompt, llm을 LCEL 파이프(|)로 연결합니다.
- 검색된 문서만 근거로 답변하게 만듭니다.
"""

from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


CHROMA_DIR = Path(__file__).resolve().parent / "chroma_db"


def format_docs(docs):
    # TODO: Document 리스트를 하나의 문자열로 합치세요.
    return ""


def create_chain():
    load_dotenv()

    # TODO 1: llm, emb, db, retriever를 준비하세요.
    llm = None
    emb = None
    db = None
    retriever = None

    # TODO 2: ChatPromptTemplate.from_template(...)로 프롬프트를 만드세요.
    prompt = None

    # TODO 3: LCEL 체인을 조립하세요.
    chain = None

    return chain


chain = create_chain()


if __name__ == "__main__":
    print(chain.invoke("가장 도전적이었던 프로젝트는?"))

