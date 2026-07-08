"""
실습 7: RAG 평가 파이프라인 정답
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
ABSTAIN_PHRASES = ["포트폴리오에 없는 정보", "제공된", "찾을 수 없습니다", "알 수 없습니다"]
SECTION_LINE = "=" * 80
SUB_LINE = "-" * 80


def load_dataset(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def preprocess_query(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def build_queries(item: dict) -> list[str]:
    raw_queries = [item["question"], *item.get("query_variants", [])]
    queries = []
    seen = set()
    for query in raw_queries:
        cleaned = preprocess_query(query)
        key = cleaned.casefold()
        if cleaned and key not in seen:
            queries.append(cleaned)
            seen.add(key)
    return queries


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
    docs_by_source = {}
    for query in queries:
        for doc in db.similarity_search(query, k=k):
            source = doc.metadata.get("name", "Unknown")
            docs_by_source.setdefault(source, doc)
    return list(docs_by_source.values())


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


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
    message = prompt.format_messages(context=format_docs(docs), question=question)
    response = llm.invoke(message)
    return response.content


def evaluate_sources(found_sources: list[str], expected_sources: list[str]) -> dict:
    missing = [source for source in expected_sources if source not in found_sources]
    return {
        "source_pass": len(missing) == 0,
        "missing_sources": missing,
        "source_coverage": 1.0 if not expected_sources else (len(expected_sources) - len(missing)) / len(expected_sources),
    }


def evaluate_answer(answer: str, expected_keywords: list[str], should_abstain: bool) -> dict:
    missing_keywords = [keyword for keyword in expected_keywords if keyword not in answer]
    abstained = any(phrase in answer for phrase in ABSTAIN_PHRASES)

    if should_abstain:
        answer_pass = abstained and len(missing_keywords) == 0
    else:
        answer_pass = len(missing_keywords) == 0 and not abstained

    return {
        "answer_pass": answer_pass,
        "missing_keywords": missing_keywords,
        "abstained": abstained,
    }


def ask_human_judgement(item: dict, answer: str) -> bool:
    print("\n" + SUB_LINE)
    print("[사람 평가 입력]")
    print("아래 기준과 모델 응답을 비교해서, 이 문항의 의도한 행동을 했으면 y를 입력합니다.")
    print("\n[질문]")
    print(item["question"])
    print("\n[정답/의도 기준]")
    print("- 난이도:", item.get("difficulty", "unknown"))
    print("- 의도:", item["intended_behavior"])
    print("- 기대 출처:", format_list(item["expected_sources"]))
    print("- 기대 키워드:", format_list(item["expected_keywords"]))
    print("- 보류 응답 필요:", "예" if item["should_abstain"] else "아니오")
    print("\n[모델 응답]")
    print(answer)

    while True:
        value = input("의도한 행동을 했나요? (y/n): ").strip().lower()
        if value in ("y", "yes"):
            return True
        if value in ("n", "no"):
            return False
        print("y 또는 n으로 입력하세요.")


def save_result(result: dict):
    with open(RESULTS_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")


def format_list(values: list[str]) -> str:
    return ", ".join(values) if values else "(없음)"


def pass_label(value: bool) -> str:
    return "PASS" if value else "FAIL"


def print_case_result(result: dict):
    print("\n" + SECTION_LINE)
    print(f"[문항] {result['id']}")
    print("\n[질문]")
    print(result["question"])

    print("\n[정답/의도 기준]")
    print("- 난이도:", result.get("difficulty", "unknown"))
    print("- 의도:", result["intended_behavior"])
    print("- 기대 출처:", format_list(result["expected_sources"]))
    print("- 기대 키워드:", format_list(result["expected_keywords"]))
    print("- 보류 응답 필요:", "예" if result["should_abstain"] else "아니오")

    print("\n[검색 결과]")
    print("- 멀티 쿼리:", format_list(result["queries"]))
    print("- 검색된 출처:", format_list(result["found_sources"]))

    print("\n[모델 응답]")
    print(result["answer"])

    print("\n[평가 결과]")
    print("- 출처 평가:", pass_label(result["source_pass"]), f"(coverage={result['source_coverage']:.2f})")
    print("- 답변 평가:", pass_label(result["answer_pass"]))
    print("- 보류 응답 감지:", "예" if result["abstained"] else "아니오")
    print("- 자동 평가:", pass_label(result["auto_pass"]))
    print("- 사람 평가:", pass_label(result["human_pass"]) if result["human_evaluated"] else "SKIP")

    if result["missing_sources"] or result["missing_keywords"]:
        print("\n[누락 항목]")
        if result["missing_sources"]:
            print("- 누락 출처:", format_list(result["missing_sources"]))
        if result["missing_keywords"]:
            print("- 누락 키워드:", format_list(result["missing_keywords"]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--no-human", action="store_true")
    args = parser.parse_args()

    dataset = load_dataset(DATASET_PATH)
    llm, db = create_llm_and_db()

    if RESULTS_PATH.exists():
        RESULTS_PATH.unlink()

    results = []
    for item in dataset:
        queries = build_queries(item)
        docs = retrieve_multi_query(db, queries, k=args.k)
        found_sources = [doc.metadata.get("name", "Unknown") for doc in docs]
        answer = generate_answer(llm, item["question"], docs)

        source_eval = evaluate_sources(found_sources, item["expected_sources"])
        answer_eval = evaluate_answer(answer, item["expected_keywords"], item["should_abstain"])
        auto_pass = source_eval["source_pass"] and answer_eval["answer_pass"]

        human_evaluated = not args.no_human
        human_pass = True
        if not args.no_human:
            human_pass = ask_human_judgement(item, answer)

        result = {
            "id": item["id"],
            "question": item["question"],
            "difficulty": item.get("difficulty", "unknown"),
            "queries": queries,
            "found_sources": found_sources,
            "expected_sources": item["expected_sources"],
            "expected_keywords": item["expected_keywords"],
            "should_abstain": item["should_abstain"],
            "intended_behavior": item["intended_behavior"],
            "answer": answer,
            "auto_pass": auto_pass,
            "human_evaluated": human_evaluated,
            "human_pass": human_pass,
            **source_eval,
            **answer_eval,
        }
        results.append(result)
        save_result(result)
        print_case_result(result)

    auto_pass_count = sum(1 for result in results if result["auto_pass"])
    human_pass_count = sum(1 for result in results if result["human_pass"])
    complete_count = sum(1 for result in results if result["auto_pass"] and result["human_pass"])

    print("\n" + "=" * 80)
    print("평가 요약")
    print(f"자동 평가 PASS: {auto_pass_count}/{len(results)}")
    print(f"사람 평가 PASS: {human_pass_count}/{len(results)}")
    print(f"완료 기준 PASS: {complete_count}/{len(results)}")
    print("결과 파일:", RESULTS_PATH)

    if complete_count == len(results):
        print("실습 7 완료: 모든 문항이 기준을 만족했습니다.")
    else:
        print("튜닝 필요: FAIL 문항의 검색 출처, 키워드, 보류 응답을 확인하세요.")


if __name__ == "__main__":
    main()
