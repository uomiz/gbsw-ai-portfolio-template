"""
실습 4: 유사도 검색 실험
"""

import os
import warnings
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma

warnings.filterwarnings("ignore", category=FutureWarning)

from langchain_google_genai import GoogleGenerativeAIEmbeddings


CHROMA_DIR = Path(__file__).resolve().parent / "chroma_db"


def search(question: str, k: int = 2):
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(".env 파일에 GEMINI_API_KEY를 설정하세요.")

    emb = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key,
    )
    db = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=emb,
    )
    hits = db.similarity_search(question, k=k)

    return hits


if __name__ == "__main__":
    question = "협업 경험이 드러나는 프로젝트는?"
    hits = search(question, k=2)

    print("질문:", question)
    for i, h in enumerate(hits, 1):
        print(f"\n[{i}위] {h.metadata.get('name', 'Unknown')}")
        print(h.page_content[:100], "...")
