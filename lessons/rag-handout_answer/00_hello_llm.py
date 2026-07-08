"""
실습 0: 환경 설정과 첫 LLM 호출
"""

import os
import warnings

from dotenv import load_dotenv

warnings.filterwarnings("ignore", category=FutureWarning)

from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError(".env 파일에 GEMINI_API_KEY를 설정하세요.")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
)
answer = llm.invoke("안녕! 한 줄로 인사해줘.")

print(answer.content)
