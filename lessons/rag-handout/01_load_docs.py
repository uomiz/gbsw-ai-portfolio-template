"""
실습 1: projects.json을 Document로 변환

목표:
- data/projects.json을 읽습니다.
- 각 프로젝트를 LangChain Document로 변환합니다.
- metadata에 출처로 사용할 프로젝트 이름을 넣습니다.
"""

import json
from pathlib import Path

from langchain_core.documents import Document


PROJECTS_JSON = Path(__file__).resolve().parent / "projects.sample.json"


def project_to_text(project: dict) -> str:
    """프로젝트 딕셔너리를 검색하기 좋은 텍스트로 바꿉니다."""
    # TODO: title, description, tags, link 필드를 포함한 문자열을 만드세요.
    return ""


def load_documents() -> list[Document]:
    # TODO 1: PROJECTS_JSON 파일을 utf-8로 읽어 projects 변수에 저장하세요.
    projects = []

    docs = []
    for project in projects:
        # TODO 2: project_to_text(project)를 page_content로 사용하는 Document를 만드세요.
        # TODO 3: metadata에는 {"name": 프로젝트 제목}을 넣으세요.
        pass

    return docs


if __name__ == "__main__":
    docs = load_documents()
    print(len(docs), "개의 Document 생성")
    if docs:
        print("--- 첫 번째 문서 ---")
        print(docs[0].page_content)
