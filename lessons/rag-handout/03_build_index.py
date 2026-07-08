"""
실습 3: 벡터 인덱스 구축

목표:
- chunk를 Gemini 임베딩으로 변환합니다.
- ChromaDB에 저장합니다.
"""

from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# TODO: 실습 2의 split_documents를 import하세요.


CHROMA_DIR = Path(__file__).resolve().parent / "chroma_db"


def build_index():
    load_dotenv()

    # TODO 1: split_documents()로 chunks를 가져오세요.
    chunks = []

    # TODO 2: GoogleGenerativeAIEmbeddings를 만드세요.
    # 힌트: model="models/gemini-embedding-001"
    emb = None

    # TODO 3: Chroma.from_documents(...)로 DB를 만들고 CHROMA_DIR에 저장하세요.
    db = None

    return db


if __name__ == "__main__":
    db = build_index()
    print("저장된 조각:", "TODO")

