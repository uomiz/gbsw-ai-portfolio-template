"""
실습 7: RAG 평가 파이프라인

학생용 TODO 버전입니다.

완료 목표:
- eval_dataset.json을 읽습니다.
- 원 질문과 query_variants를 함께 검색합니다.
- 기대한 근거 프로젝트를 찾았는지 자동 평가합니다.
- 답변에 핵심 키워드가 있는지 자동 평가합니다.
- 정보가 없는 질문은 보류 응답했는지 확인합니다.
- 문항마다 사람이 "의도한 행동을 했는지" 평가합니다.
"""

import argparse
import json
import os
import re
import warnings
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

warnings.filterwarnings("ignore", category=FutureWarning)

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


EVAL_DIR = Path(__file__).resolve().parent
LESSON_DIR = EVAL_DIR.parent
DATASET_PATH = EVAL_DIR / "eval_dataset.json"
RESULTS_PATH = EVAL_DIR / "eval_results.jsonl"
CHROMA_DIR = LESSON_DIR / "chroma_db"


def load_dataset(path: Path) -> list[dict]:
    # TODO: JSON 평가셋을 읽어서 list[dict]로 반환하세요.
    raise NotImplementedError


def preprocess_query(text: str) -> str:
    # TODO: 검색 전에 공백 정리, 앞뒤 공백 제거 등 간단한 전처리를 하세요.
    raise NotImplementedError


def build_queries(item: dict) -> list[str]:
    # TODO: item["question"]과 item["query_variants"]를 합치고 중복을 제거하세요.
    raise NotImplementedError


def create_llm_and_db():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(".env 파일에 GEMINI_API_KEY를 설정하세요.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.2,
    )
    emb = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key,
    )
    db = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=emb,
    )
    return llm, db


def retrieve_multi_query(db, queries: list[str], k: int) -> list:
    # TODO: 여러 query로 similarity_search를 실행하고, 프로젝트명 기준으로 중복 제거하세요.
    raise NotImplementedError


def format_docs(docs) -> str:
    # TODO: 검색된 Document 리스트를 LLM에 넣을 context 문자열로 합치세요.
    raise NotImplementedError


def generate_answer(llm, question: str, docs) -> str:
    prompt = ChatPromptTemplate.from_template(
        """
너는 지원자의 포트폴리오를 소개하는 어시스턴트야.
아래 문서 내용만 근거로 답변해.
문서에 없는 내용은 "포트폴리오에 없는 정보입니다"라고 답해.
가능하면 답변에 근거가 된 프로젝트명을 포함해.

[문서]
{context}

[질문]
{question}
"""
    )

    # TODO: prompt와 llm을 사용해 답변 문자열을 생성하세요.
    raise NotImplementedError


def evaluate_sources(found_sources: list[str], expected_sources: list[str]) -> dict:
    # TODO: 기대한 source가 검색 결과에 모두 포함됐는지 평가하세요.
    raise NotImplementedError


def evaluate_answer(answer: str, expected_keywords: list[str], should_abstain: bool) -> dict:
    # TODO: 키워드 포함 여부와 보류 응답 여부를 평가하세요.
    # 힌트:
    # - should_abstain=False: 핵심 키워드가 모두 있고, 보류 응답은 없어야 합니다.
    # - should_abstain=True + expected_keywords 없음: 보류 응답만 있으면 됩니다.
    # - should_abstain=True + expected_keywords 있음: 일부 정보는 답하고, 없는 정보는 보류해야 하는 복합 문항입니다.
    raise NotImplementedError


def ask_human_judgement(item: dict, answer: str) -> bool:
    print("\n" + "-" * 80)
    print("[사람 평가 입력]")
    print("아래 기준과 모델 응답을 비교해서, 이 문항의 의도한 행동을 했으면 y를 입력합니다.")
    print("\n[질문]")
    print(item["question"])
    print("\n[정답/의도 기준]")
    print("- 난이도:", item.get("difficulty", "unknown"))
    print("- 의도:", item["intended_behavior"])
    print("- 기대 출처:", ", ".join(item["expected_sources"]) if item["expected_sources"] else "(없음)")
    print("- 기대 키워드:", ", ".join(item["expected_keywords"]) if item["expected_keywords"] else "(없음)")
    print("- 보류 응답 필요:", "예" if item["should_abstain"] else "아니오")
    print("\n[모델 응답]")
    print(answer)

    # TODO: y/n 입력을 받아 True/False를 반환하세요.
    raise NotImplementedError


def save_result(result: dict):
    with open(RESULTS_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--no-human", action="store_true")
    args = parser.parse_args()

    # TODO: 전체 평가 루프를 완성하세요.
    raise NotImplementedError


if __name__ == "__main__":
    main()
