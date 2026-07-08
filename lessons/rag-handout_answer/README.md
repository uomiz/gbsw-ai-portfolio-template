# RAG 실습 핸드아웃 - 정답

이 폴더는 학생용 실습의 정답 코드입니다.

## 실행 순서

프로젝트 루트에서 실행합니다.

```bash
source .venv/bin/activate
python lessons/rag-handout_answer/00_hello_llm.py
python lessons/rag-handout_answer/01_load_docs.py
python lessons/rag-handout_answer/02_split_docs.py
python lessons/rag-handout_answer/03_build_index.py
python lessons/rag-handout_answer/04_search_test.py
python lessons/rag-handout_answer/05_qna_chain.py
python lessons/rag-handout_answer/06_chat.py
python lessons/rag-handout_answer/07_eval/evaluate.py
```

Windows PowerShell에서는 가상환경 활성화 명령만 바꿉니다.

```powershell
.venv\Scripts\Activate.ps1
```

API 키는 프로젝트 루트의 `.env` 파일에 넣습니다.

```env
GEMINI_API_KEY=your_key_here
```

프로젝트 예시 데이터는 이 폴더의 `projects.sample.json`을 사용합니다.

예시 질문은 `QUESTIONS.md`에 있습니다.

튜닝 결과 평가는 `07_eval/` 폴더에서 진행합니다. 평가셋과 평가 기준은 `07_eval/eval_dataset.json`, `07_eval/EVALUATION_GUIDE.md`를 확인하세요.

사람 평가를 건너뛰고 자동 평가만 확인하려면 다음처럼 실행합니다.

```bash
python lessons/rag-handout_answer/07_eval/evaluate.py --no-human
```

인덱스를 새로 만들고 싶으면 다음 폴더를 삭제한 뒤 `03_build_index.py`를 다시 실행합니다.

```bash
rm -rf lessons/rag-handout_answer/chroma_db
```

