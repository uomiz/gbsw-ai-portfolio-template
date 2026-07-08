# Step 5: 선택 심화 과제

00~07 실습으로 RAG의 기본 흐름을 이해한 뒤, `server/` 코드를 자신의 프로젝트에 맞게 수정합니다.

공통 과제:

- `lessons/rag-handout/00_hello_llm.py` ~ `07_eval/` 실습 완료
- `server/` 코드가 자신의 프로젝트 데이터 기반으로 답변하도록 수정
- 자신의 웹사이트 챗봇에서 RAG 답변이 정상 동작하는지 확인

이후 아래 선택 과제 중 **2개 이상**을 구현합니다.

선택 과제는 그대로 구현해도 되고, 자신의 포트폴리오 주제에 맞게 변형해도 됩니다. 단, 제출할 때는 **무엇을 목표로 했고, 어떤 파일을 수정했으며, 실행 결과가 어떻게 보이는지** 설명해야 합니다.

---

## 제출 기준

선택 과제 2개 이상에 대해 다음을 제출합니다.

```text
1. 선택한 과제명
2. 구현 목표
3. 수정한 파일 목록
4. 실행 방법
5. 동작 결과 스크린샷 또는 짧은 영상
6. 실패/어려웠던 점과 해결 방법
```

서버 기능을 추가한 경우에는 API 테스트 결과도 포함합니다.

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "프로젝트 중 FastAPI를 쓴 것은?"}'
```

---

## 선택 과제 1: 질문 라우팅 시스템

**난이도:** ⭐⭐⭐

### 목표

사용자 질문 유형에 따라 처리 방식을 다르게 나눕니다.

- 프로젝트 질문: RAG 검색 후 답변
- 일반 대화: 일반 LLM 답변
- 포트폴리오에 없는 민감/개인 정보 질문: 보류 응답

예시:

```text
질문: FastAPI를 쓴 프로젝트는?
처리: RAG

질문: 오늘 기분 좋게 코딩하려면?
처리: 일반 LLM

질문: 희망 연봉은 얼마야?
처리: 보류 응답
```

### 산출물

- 질문 라우팅 함수
- 라우팅 결과가 포함된 API 응답
- 웹 챗봇에서 라우팅 결과에 따른 답변 확인

예상 응답:

```json
{
  "answer": "FastAPI를 사용한 프로젝트는 급식 만족도 분석 서비스와 AI 자기소개서 피드백 도구입니다.",
  "route": "rag",
  "sources": ["급식 만족도 분석 서비스", "AI 자기소개서 피드백 도구"]
}
```

### 구현 예상 파일

- `server/api.py`
- `server/rag_core.py`
- `server/prompts.py`
- `web/widget.js`

### 구현 시나리오

1. `classify_question(question)` 함수를 만듭니다.
2. 질문에 `프로젝트`, `기술`, `포트폴리오`, `개발`, `성과` 등이 있으면 `rag`로 분류합니다.
3. `연봉`, `주소`, `전화번호`, `성적`처럼 데이터에 없는 개인 정보는 `abstain`으로 분류합니다.
4. 나머지는 `general`로 분류합니다.
5. `/chat` 응답에 `route` 값을 함께 반환합니다.

### 힌트

```python
def classify_question(question: str) -> str:
    q = question.lower()

    private_keywords = ["연봉", "주소", "전화번호", "성적", "주민등록"]
    project_keywords = ["프로젝트", "기술", "포트폴리오", "개발", "성과", "역할"]

    if any(keyword in q for keyword in private_keywords):
        return "abstain"
    if any(keyword in q for keyword in project_keywords):
        return "rag"
    return "general"
```

### 평가 기준

- 프로젝트 질문이 RAG로 처리된다.
- 일반 대화가 RAG 검색 없이 답변된다.
- 데이터에 없는 민감 정보는 추측하지 않는다.
- 응답에 현재 라우팅 결과가 표시된다.

---

## 선택 과제 2: 방명록 기록

**난이도:** ⭐⭐

### 목표

방문자가 포트폴리오 주인에게 짧은 메시지를 남길 수 있게 합니다.

예시:

```text
이름: 홍길동
메시지: 프로젝트 설명이 잘 정리되어 있어서 좋았습니다.
```

### 산출물

- 방명록 입력 UI
- 방명록 저장 API
- 방명록 목록 조회 API
- 서버 재시작 후에도 기록이 남아 있는 저장 파일

예상 API:

```text
POST /guestbook
GET /guestbook
```

예상 저장 파일:

```text
data/guestbook.json
```

### 구현 예상 파일

- `server/api.py`
- `web/index.html`
- `web/app.js`
- `web/style.css`
- `data/guestbook.json`

### 구현 시나리오

1. `data/guestbook.json` 파일을 만듭니다.
2. `POST /guestbook`에서 이름과 메시지를 받아 JSON 파일에 추가합니다.
3. `GET /guestbook`에서 저장된 메시지 목록을 반환합니다.
4. 웹에 입력 폼과 메시지 목록 영역을 만듭니다.
5. 메시지 등록 후 목록이 새로고침되게 만듭니다.

### 힌트

```python
from pydantic import BaseModel
from datetime import datetime

class GuestbookEntry(BaseModel):
    name: str
    message: str

@app.post("/guestbook")
async def add_guestbook(entry: GuestbookEntry):
    # 기존 JSON 읽기
    # created_at 추가
    # 다시 저장
    return {"ok": True}
```

프론트엔드에서는 `fetch()`를 사용합니다.

```javascript
await fetch(`${API_BASE_URL}/guestbook`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name, message })
});
```

### 평가 기준

- 새 메시지를 등록할 수 있다.
- 등록한 메시지가 화면에 표시된다.
- 서버를 재시작해도 메시지가 남아 있다.
- 빈 이름/빈 메시지는 저장되지 않는다.

---

## 선택 과제 3: 프로젝트 좋아요와 조회수

**난이도:** ⭐⭐

### 목표

각 프로젝트 카드에 조회수와 좋아요 수를 표시합니다.

예시:

```text
감정 분석 웹앱
조회수 12 · 좋아요 5
```

### 산출물

- 프로젝트별 조회수 증가 기능
- 프로젝트별 좋아요 증가 기능
- 웹 카드에 숫자 표시
- 서버에 숫자 저장

예상 API:

```text
GET /stats
POST /projects/{project_id}/view
POST /projects/{project_id}/like
```

예상 저장 파일:

```text
data/project_stats.json
```

### 구현 예상 파일

- `server/api.py`
- `web/app.js`
- `web/style.css`
- `data/project_stats.json`

### 구현 시나리오

1. 프로젝트 `id`별로 `views`, `likes`를 저장합니다.
2. 카드가 화면에 보이거나 클릭될 때 조회수를 증가시킵니다.
3. 좋아요 버튼을 누르면 좋아요 수를 증가시킵니다.
4. `GET /stats`로 모든 프로젝트의 통계를 가져와 카드에 표시합니다.

### 힌트

```json
{
  "sentiment-webapp": {
    "views": 12,
    "likes": 5
  }
}
```

```python
@app.post("/projects/{project_id}/like")
async def like_project(project_id: str):
    stats = load_stats()
    stats.setdefault(project_id, {"views": 0, "likes": 0})
    stats[project_id]["likes"] += 1
    save_stats(stats)
    return stats[project_id]
```

### 평가 기준

- 프로젝트별 숫자가 따로 저장된다.
- 좋아요 버튼 클릭 시 숫자가 증가한다.
- 조회수 증가 기준이 명확하다.
- 새로고침 후에도 숫자가 유지된다.

---

## 선택 과제 4: GitHub API 연동 + Tool Use

**난이도:** ⭐⭐⭐⭐

### 목표

GitHub API를 사용해 프로젝트 저장소의 최신 정보를 가져오고, 챗봇 답변에 활용합니다.

예시 질문:

```text
내 GitHub 저장소 중 스타가 가장 많은 프로젝트는?
최근 커밋이 있는 프로젝트는?
이 프로젝트의 GitHub 언어 비율은?
```

### 산출물

- GitHub 저장소 정보 조회 API
- GitHub 데이터를 사용하는 챗봇 응답
- 저장소 링크, 스타 수, 언어, 최근 업데이트 표시

예상 API:

```text
GET /github/repos
GET /github/repos/{owner}/{repo}
```

### 구현 예상 파일

- `server/api.py`
- `server/github_tool.py`
- `server/rag_core.py` 또는 `server/prompts.py`
- `web/app.js`

### 구현 시나리오

1. GitHub 사용자명을 `.env`에 저장합니다.
2. GitHub REST API로 저장소 목록을 가져옵니다.
3. 프로젝트 데이터의 `link`가 GitHub URL이면 저장소명을 추출합니다.
4. 질문에 `GitHub`, `스타`, `커밋`, `언어` 등이 있으면 GitHub API를 호출합니다.
5. API 결과를 LLM 프롬프트에 함께 넣어 답변합니다.

### 힌트

```python
import httpx

async def fetch_github_repos(username: str):
    url = f"https://api.github.com/users/{username}/repos"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
```

GitHub API 한도에 걸릴 수 있으므로 선택적으로 토큰을 사용할 수 있습니다.

```env
GITHUB_USERNAME=your_username
GITHUB_TOKEN=your_token_optional
```

### 평가 기준

- GitHub API에서 실제 데이터를 가져온다.
- 스타 수, 언어, 최근 업데이트 등 실시간 정보가 답변에 들어간다.
- GitHub 관련 질문과 일반 프로젝트 질문의 처리 방식이 구분된다.
- API 실패 시 사용자에게 적절한 오류 메시지를 보여준다.

---

## 선택 과제 5: 관리자 페이지

**난이도:** ⭐⭐⭐⭐

### 목표

포트폴리오 주인이 웹에서 프로젝트를 추가, 수정, 삭제할 수 있는 관리자 페이지를 만듭니다.

예시 기능:

```text
프로젝트 추가
프로젝트 설명 수정
프로젝트 삭제
projects.json 재생성
RAG 인덱스 재빌드
```

### 산출물

- 관리자 페이지 UI
- 프로젝트 CRUD API
- 수정된 프로젝트 데이터 저장
- 변경 후 RAG 재빌드 안내 또는 자동 재빌드

예상 API:

```text
GET /admin/projects
POST /admin/projects
PUT /admin/projects/{project_id}
DELETE /admin/projects/{project_id}
POST /admin/rebuild-index
```

### 구현 예상 파일

- `server/api.py`
- `server/admin.py`
- `data/projects.json`
- `web/admin.html`
- `web/admin.js`
- `web/style.css`

### 구현 시나리오

1. 관리자 페이지 `web/admin.html`을 만듭니다.
2. 프로젝트 목록을 불러와 표나 카드로 보여줍니다.
3. 추가/수정 폼을 만듭니다.
4. 서버에서 `projects.json`을 수정합니다.
5. 수정 후 RAG 인덱스를 다시 만들어야 한다는 안내를 표시합니다.

### 힌트

간단한 수업 버전에서는 로그인 대신 관리자 토큰을 사용할 수 있습니다.

```env
ADMIN_TOKEN=my-secret-token
```

```python
from fastapi import Header, HTTPException

def verify_admin(x_admin_token: str | None = Header(default=None)):
    if x_admin_token != os.getenv("ADMIN_TOKEN"):
        raise HTTPException(status_code=401, detail="관리자 권한이 없습니다.")
```

프론트엔드 요청:

```javascript
await fetch(`${API_BASE_URL}/admin/projects`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Admin-Token': adminToken
  },
  body: JSON.stringify(project)
});
```

### 평가 기준

- 관리자 페이지에서 프로젝트를 추가할 수 있다.
- 추가한 프로젝트가 웹 프로젝트 목록에 표시된다.
- 수정/삭제가 서버 파일에 반영된다.
- 관리자 토큰 없이 수정 API를 호출하면 거부된다.
- RAG 인덱스를 다시 만들어야 한다는 흐름을 설명할 수 있다.

---

## 선택 과제 난이도 요약

| 과제 | 난이도 | 중심 영역 | 추천 대상 |
|---|---:|---|---|
| 질문 라우팅 시스템 | ⭐⭐⭐ | RAG / LLM | 챗봇 동작을 똑똑하게 나누고 싶은 학생 |
| 방명록 기록 | ⭐⭐ | 백엔드 / 파일 저장 | 서버 API를 처음 확장해보고 싶은 학생 |
| 프로젝트 좋아요, 조회수 | ⭐⭐ | 풀스택 | 웹과 서버 연동을 연습하고 싶은 학생 |
| GitHub API 연동 + Tool Use | ⭐⭐⭐⭐ | 외부 API / LLM | 실시간 데이터를 답변에 넣고 싶은 학생 |
| 관리자 페이지 | ⭐⭐⭐⭐ | 풀스택 / CRUD | 포트폴리오를 직접 관리하는 도구를 만들고 싶은 학생 |

---

## 추천 조합

처음 도전하는 경우:

```text
방명록 기록 + 프로젝트 좋아요/조회수
```

챗봇을 더 똑똑하게 만들고 싶은 경우:

```text
질문 라우팅 시스템 + GitHub API 연동
```

서비스처럼 완성하고 싶은 경우:

```text
관리자 페이지 + 프로젝트 좋아요/조회수
```

---

## 추가 아이디어

아래 항목들은 위의 5개 선택 과제 외에 더 해보고 싶은 학생을 위한 아이디어입니다.

---

## 📂 분야별 추가 아이디어

### 🎨 프론트엔드 중심

관심사: UI/UX, 디자인, 사용자 경험

### 🤖 백엔드 / API 중심

관심사: 서버 로직, 데이터베이스, API 설계

### 🧠 RAG / LLM 중심

관심사: AI 모델, 프롬프트 엔지니어링, 검색 알고리즘

### 🔗 풀스택 통합

관심사: 프론트-백엔드 연동, 복합 기능

---

## 🎨 프론트엔드 심화 아이디어

### 1. 프로젝트 필터링 시스템

**난이도:** ⭐⭐

**목표:** 태그를 클릭하면 해당 프로젝트만 보이게

```javascript
// 힌트
function filterByTag(selectedTag) {
    const cards = document.querySelectorAll('.project-card');
    cards.forEach(card => {
        const tags = card.dataset.tags; // 데이터 속성 활용
        // 태그가 포함되어 있으면 보이기, 아니면 숨기기
    });
}
```

**확장 아이디어:**
- 여러 태그 동시 선택 (AND/OR 조건)
- 선택된 필터 표시 (현재 필터: NLP, Python)
- 필터 초기화 버튼

**참고:**
- JavaScript `classList.add()`, `classList.remove()`
- CSS `display: none` / `display: block`

---

### 2. 검색 기능

**난이도:** ⭐⭐

**목표:** 검색창에 키워드 입력 → 관련 프로젝트만 표시

```html
<input type="text" id="search" placeholder="프로젝트 검색...">
```

```javascript
// 힌트
searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    // 각 프로젝트 카드의 텍스트와 비교
});
```

**확장 아이디어:**
- 검색 결과 개수 표시 (3개 결과 발견)
- 검색어 하이라이트
- 자동완성 드롭다운

**참고:**
- `String.includes()`, `String.toLowerCase()`
- Debouncing (입력 지연 처리)

---

### 3. 다크 모드

**난이도:** ⭐⭐

**목표:** 라이트/다크 모드 토글 버튼

```css
/* 힌트 */
:root {
    --bg-color: #ffffff;
    --text-color: #333333;
}

[data-theme="dark"] {
    --bg-color: #1a1a1a;
    --text-color: #ffffff;
}

body {
    background: var(--bg-color);
    color: var(--text-color);
}
```

```javascript
// 힌트
toggleButton.addEventListener('click', () => {
    document.body.dataset.theme =
        document.body.dataset.theme === 'dark' ? 'light' : 'dark';
    // localStorage에 저장하여 다음 방문 시에도 유지
});
```

**확장 아이디어:**
- 시스템 다크 모드 자동 감지 (`prefers-color-scheme`)
- 부드러운 전환 애니메이션
- 테마별 아이콘 변경 (해/달)

**참고:**
- CSS Variables
- `localStorage.setItem()`, `localStorage.getItem()`

---

### 4. 프로젝트 상세 모달

**난이도:** ⭐⭐⭐

**목표:** 프로젝트 카드 클릭 → 팝업으로 상세 정보

```html
<div id="modal" class="modal">
    <div class="modal-content">
        <span class="close">&times;</span>
        <h2 id="modal-title"></h2>
        <p id="modal-description"></p>
    </div>
</div>
```

```javascript
// 힌트
function openModal(project) {
    modal.style.display = 'block';
    document.getElementById('modal-title').textContent = project.title;
    // 나머지 정보 채우기
}
```

**확장 아이디어:**
- 이미지 슬라이더 (프로젝트 스크린샷)
- YouTube 임베드 (데모 영상)
- GitHub 스타 개수 표시 (GitHub API)

**참고:**
- CSS `position: fixed`, `z-index`
- 배경 클릭 시 닫기
- ESC 키로 닫기

---

### 5. 애니메이션 효과

**난이도:** ⭐⭐

**목표:** 스크롤 시 카드가 하나씩 나타나는 효과

```javascript
// 힌트: Intersection Observer API
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
        }
    });
});

document.querySelectorAll('.project-card').forEach(card => {
    observer.observe(card);
});
```

```css
.project-card {
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.5s ease;
}

.project-card.fade-in {
    opacity: 1;
    transform: translateY(0);
}
```

**확장 아이디어:**
- 카드별 순차적 지연 (stagger animation)
- 다양한 등장 방향 (위, 아래, 왼쪽, 오른쪽)
- 페이지 로딩 애니메이션

**참고:**
- Intersection Observer API
- CSS `@keyframes`
- Animation libraries (AOS, Animate.css)

---

### 6. 배경 음악 (BGM)

**난이도:** ⭐

**목표:** 포트폴리오 사이트에 배경음악 추가

```html
<audio id="bgm" loop>
    <source src="assets/bgm.mp3" type="audio/mpeg">
</audio>
<button id="bgm-toggle">🔊</button>
```

```javascript
// 힌트
const bgm = document.getElementById('bgm');
const toggle = document.getElementById('bgm-toggle');

toggle.addEventListener('click', () => {
    if (bgm.paused) {
        bgm.play();
        toggle.textContent = '🔇';
    } else {
        bgm.pause();
        toggle.textContent = '🔊';
    }
});
```

**주의사항:**
- 자동 재생은 대부분 브라우저에서 차단됨
- 사용자가 먼저 클릭해야 재생 가능
- 볼륨은 낮게 (0.3 ~ 0.5 권장)

**확장 아이디어:**
- 볼륨 슬라이더
- 여러 BGM 선택 가능
- 시간대별 다른 음악 (아침/저녁)

**무료 음원:**
- YouTube Audio Library
- Incompetech (Kevin MacLeod)

---

### 7. 이력서 다운로드 기능

**난이도:** ⭐

**목표:** PDF 이력서 다운로드 버튼

```html
<a href="assets/resume.pdf" download="홍길동_이력서.pdf">
    📄 이력서 다운로드
</a>
```

**확장 아이디어:**
- JSON 데이터에서 자동으로 이력서 생성 (jsPDF 라이브러리)
- 한글/영문 이력서 선택
- Markdown → PDF 변환

---

### 8. 방문자 수 카운터

**난이도:** ⭐⭐

**목표:** 사이트 방문 횟수 표시

**옵션 1: 로컬 저장**
```javascript
let visits = parseInt(localStorage.getItem('visits')) || 0;
visits++;
localStorage.setItem('visits', visits);
console.log(`방문 횟수: ${visits}`);
```

**옵션 2: 외부 서비스**
- [Visitor Badge](https://visitor-badge.laobi.icu/)
- [Hits](https://hits.seeyoufarm.com/)

**확장 아이디어:**
- 일일 방문자 / 전체 방문자 구분
- 방문 시간 기록
- 방문자 통계 차트

---

## 🤖 백엔드 / API 심화 아이디어

### 1. 질문 라우팅 시스템

**난이도:** ⭐⭐⭐

**목표:** 질문 유형에 따라 다른 처리 (RAG vs 일반 LLM)

```python
# 힌트: server/api.py

class QuestionRouter:
    def classify(self, question: str) -> str:
        """
        질문을 분류
        - 'project': RAG 사용 (프로젝트 관련)
        - 'general': 일반 LLM (인사, 잡담)
        - 'unknown': 답변 불가
        """
        keywords = ['프로젝트', 'project', '경험', '기술']
        # 키워드 포함 여부로 1차 분류
        # 또는 LLM으로 분류
        pass

@app.post("/chat")
def chat(request: ChatRequest):
    router = QuestionRouter()
    question_type = router.classify(request.question)

    if question_type == 'project':
        # RAG 엔진 사용
        result = rag_engine.query(request.question)
    elif question_type == 'general':
        # 일반 LLM (RAG 없이)
        result = simple_llm_response(request.question)
    else:
        result = {"answer": "답변할 수 없는 질문입니다."}

    return result
```

**확장 아이디어:**
- LLM으로 자동 분류 (Few-shot classification)
- 사용자가 질문 유형 선택 (프론트에서 버튼)
- 통계: 어떤 유형 질문이 많은지 분석

**참고:**
- 키워드 기반 vs LLM 기반 분류
- FastAPI 라우팅
- Pydantic 모델

---

### 2. 방명록 기능

**난이도:** ⭐⭐⭐

**목표:** 방문자가 메시지를 남길 수 있는 방명록

```python
# 힌트: server/guestbook.py

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Guestbook(Base):
    __tablename__ = "guestbook"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    message = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

@app.post("/guestbook")
def create_guestbook(name: str, message: str):
    # 1. 입력 검증 (길이, 욕설 필터)
    # 2. DB에 저장
    # 3. 성공 응답
    pass

@app.get("/guestbook")
def get_guestbook(limit: int = 20):
    # 최신순으로 방명록 조회
    pass
```

**확장 아이디어:**
- 욕설 필터링 (나쁜 단어 리스트)
- 이모지 리액션 (좋아요, 하트)
- 방명록에 답글 기능
- 관리자 모드 (삭제 기능)

**참고:**
- SQLAlchemy (DB ORM)
- SQLite (개발) → PostgreSQL (배포)
- Render에서 PostgreSQL 무료 제공

---

### 3. 대화 히스토리 저장

**난이도:** ⭐⭐⭐

**목표:** 사용자와 챗봇의 대화 기록 저장 및 이어서 대화

```python
# 힌트
class ChatHistory:
    def __init__(self):
        self.sessions = {}  # session_id: [messages]

    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append({
            "role": role,  # "user" or "assistant"
            "content": content
        })

    def get_context(self, session_id: str, last_n: int = 5):
        # 최근 N개 메시지 반환
        return self.sessions.get(session_id, [])[-last_n:]

@app.post("/chat")
def chat(request: ChatRequest):
    # 이전 대화 컨텍스트 가져오기
    context = history.get_context(request.session_id)

    # 컨텍스트 포함하여 RAG 실행
    result = rag_engine.query_with_context(
        question=request.question,
        context=context
    )

    # 대화 저장
    history.add_message(request.session_id, "user", request.question)
    history.add_message(request.session_id, "assistant", result['answer'])

    return result
```

**확장 아이디어:**
- 대화 요약 (긴 히스토리는 요약하여 전달)
- 대화 내보내기 (TXT, JSON)
- 대화별 제목 자동 생성

**참고:**
- UUID로 세션 ID 생성
- Redis로 히스토리 저장 (선택)

---

### 4. 프로젝트 좋아요/조회수

**난이도:** ⭐⭐

**목표:** 프로젝트별 좋아요, 조회수 추적

```python
# 힌트
from collections import defaultdict

class ProjectStats:
    def __init__(self):
        self.views = defaultdict(int)
        self.likes = defaultdict(int)

    def increment_view(self, project_id: str):
        self.views[project_id] += 1

    def toggle_like(self, project_id: str, user_id: str):
        # 사용자별 좋아요 상태 저장
        pass

@app.post("/projects/{project_id}/view")
def view_project(project_id: str):
    stats.increment_view(project_id)
    return {"views": stats.views[project_id]}

@app.post("/projects/{project_id}/like")
def like_project(project_id: str, user_id: str):
    stats.toggle_like(project_id, user_id)
    return {"likes": stats.likes[project_id]}
```

**프론트 연동:**
```javascript
// 프로젝트 카드 클릭 시
fetch(`/projects/${projectId}/view`, {method: 'POST'});

// 좋아요 버튼 클릭 시
fetch(`/projects/${projectId}/like`, {
    method: 'POST',
    body: JSON.stringify({user_id: getUserId()})
});
```

**확장 아이디어:**
- 인기 프로젝트 순위
- 좋아요 중복 방지 (쿠키/localStorage)
- 실시간 업데이트 (WebSocket)

---

### 5. GitHub API 연동

**난이도:** ⭐⭐⭐

**목표:** 프로젝트의 GitHub 스타, 이슈 개수 자동 가져오기

```python
# 힌트
import requests

def get_github_stats(repo_url: str):
    # "https://github.com/user/repo" → API URL 변환
    api_url = repo_url.replace("github.com", "api.github.com/repos")

    response = requests.get(api_url)
    data = response.json()

    return {
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "issues": data.get("open_issues_count", 0),
        "language": data.get("language", "")
    }

@app.get("/github/stats")
def github_stats(repo_url: str):
    return get_github_stats(repo_url)
```

**프론트 표시:**
```javascript
fetch(`/github/stats?repo_url=${project.link}`)
    .then(res => res.json())
    .then(stats => {
        card.innerHTML += `
            <div class="github-stats">
                ⭐ ${stats.stars} | 🍴 ${stats.forks}
            </div>
        `;
    });
```

**주의:**
- GitHub API 제한: 시간당 60회 (인증 없이)
- 인증 시: 시간당 5000회

**확장 아이디어:**
- 최근 커밋 표시
- 기여자 목록
- 언어 비율 차트

---

### 6. 이메일 문의 기능

**난이도:** ⭐⭐⭐

**목표:** 포트폴리오에서 바로 이메일 보내기

```python
# 힌트: SMTP 또는 SendGrid API
import smtplib
from email.mime.text import MIMEText

@app.post("/contact")
def send_email(name: str, email: str, message: str):
    # 1. 입력 검증
    # 2. 스팸 방지 (reCAPTCHA)
    # 3. 이메일 전송

    msg = MIMEText(f"From: {name}\nEmail: {email}\n\n{message}")
    msg['Subject'] = f"[포트폴리오 문의] {name}"
    msg['From'] = 'noreply@myportfolio.com'
    msg['To'] = 'your-email@example.com'

    # SMTP 전송
    # ...

    return {"success": True}
```

**무료 서비스:**
- SendGrid (100통/일)
- Mailgun (5000통/월)
- FormSubmit (코드 없이 HTML만으로 가능)

**확장 아이디어:**
- 자동 응답 메일
- 문의 유형 선택 (채용, 협업, 기타)
- 문의 히스토리 관리자 페이지

---

## 🧠 RAG / LLM 심화 아이디어

### 1. 멀티모달 RAG

**난이도:** ⭐⭐⭐⭐

**목표:** 텍스트 + 이미지를 함께 검색

```python
# 힌트: CLIP 모델 사용
from sentence_transformers import SentenceTransformer, util
from PIL import Image

class MultimodalRAG:
    def __init__(self):
        self.text_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.clip_model = SentenceTransformer('clip-ViT-B-32')

    def embed_image(self, image_path: str):
        img = Image.open(image_path)
        return self.clip_model.encode(img)

    def search(self, query: str, include_images: bool = True):
        # 텍스트 검색
        text_results = self.text_search(query)

        if include_images:
            # 이미지 검색
            image_results = self.image_search(query)
            # 결합

        return combined_results
```

**사용 예:**
- "객체 인식 프로젝트" 검색 → 관련 프로젝트 + 스크린샷
- "웹 디자인" 검색 → 웹사이트 이미지 포함 결과

**참고:**
- CLIP 모델 (OpenAI)
- 이미지 임베딩

---

### 2. 하이브리드 검색

**난이도:** ⭐⭐⭐

**목표:** 벡터 검색 + 키워드 검색 결합으로 정확도 향상

```python
# 힌트
class HybridRetriever:
    def search(self, query: str, alpha: float = 0.5):
        # 벡터 검색 (의미 기반)
        vector_results = self.vector_search(query)

        # BM25 키워드 검색
        keyword_results = self.keyword_search(query)

        # 점수 결합 (alpha: 벡터 가중치)
        combined = self.rerank(vector_results, keyword_results, alpha)
        return combined

    def keyword_search(self, query: str):
        # BM25 알고리즘
        from rank_bm25 import BM25Okapi
        # 구현...
```

**효과:**
- 벡터 검색: 의미는 비슷하지만 단어가 다른 경우
- 키워드 검색: 정확한 기술명, 고유명사

**참고:**
- BM25 알고리즘
- Reciprocal Rank Fusion (RRF)

---

### 3. 스트리밍 응답

**난이도:** ⭐⭐⭐

**목표:** ChatGPT처럼 답변이 실시간으로 타이핑되는 효과

```python
# 힌트: FastAPI StreamingResponse
from fastapi.responses import StreamingResponse

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def generate():
        # RAG 검색
        docs = rag_engine.search(request.question)

        # LLM 스트리밍 호출
        for chunk in llm.stream(prompt):
            yield f"data: {chunk}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

```javascript
// 프론트 (Server-Sent Events)
const eventSource = new EventSource('/chat/stream');
eventSource.onmessage = (event) => {
    answerDiv.textContent += event.data;
};
```

**참고:**
- Server-Sent Events (SSE)
- FastAPI `StreamingResponse`
- Gemini API streaming mode

---

### 4. 출처 문서 뷰어

**난이도:** ⭐⭐⭐

**목표:** 답변의 출처를 클릭하면 원본 문서 내용을 보여주기

```python
# 백엔드: 출처에 문서 ID 포함
@app.post("/chat")
def chat(request: ChatRequest):
    result = rag_engine.query(request.question)

    # 출처에 문서 내용 포함
    sources_with_content = []
    for source in result['sources']:
        sources_with_content.append({
            "id": source['id'],
            "title": source['title'],
            "content": get_full_document(source['id']),  # 전체 내용
            "snippet": source['snippet']  # 미리보기
        })

    return {
        "answer": result['answer'],
        "sources": sources_with_content
    }
```

```javascript
// 프론트: 출처 클릭 시 모달
sources.forEach(source => {
    const link = document.createElement('a');
    link.textContent = source.title;
    link.onclick = () => openSourceModal(source);
});

function openSourceModal(source) {
    modal.innerHTML = `
        <h3>${source.title}</h3>
        <div class="source-content">${source.content}</div>
    `;
    modal.style.display = 'block';
}
```

**확장 아이디어:**
- 검색어 하이라이트
- 출처 신뢰도 점수 표시
- 출처 간 비교 뷰

---

### 5. 질문 추천 시스템

**난이도:** ⭐⭐⭐

**목표:** 사용자가 물어볼 만한 질문을 자동 추천

```python
# 방법 1: 미리 정의된 추천 질문
SUGGESTED_QUESTIONS = [
    "어떤 프로젝트를 했나요?",
    "가장 자신 있는 기술은?",
    "NLP 관련 경험은?",
    "팀 프로젝트 경험은?"
]

# 방법 2: 대화 기반 동적 생성
@app.post("/suggest")
def suggest_questions(chat_history: list):
    # 지금까지의 대화를 바탕으로 LLM이 다음 질문 생성
    prompt = f"""
    대화 히스토리:
    {chat_history}

    사용자가 다음에 물어볼 만한 질문 3개를 추천하세요.
    """
    suggestions = llm.generate(prompt)
    return {"suggestions": suggestions}
```

```javascript
// 프론트: 추천 질문 버튼
fetch('/suggest', {
    method: 'POST',
    body: JSON.stringify({chat_history: history})
})
.then(res => res.json())
.then(data => {
    data.suggestions.forEach(q => {
        const btn = document.createElement('button');
        btn.textContent = q;
        btn.onclick = () => sendQuestion(q);
        suggestionsDiv.appendChild(btn);
    });
});
```

**확장 아이디어:**
- 카테고리별 추천 (프로젝트, 기술, 경험)
- 사용자 맞춤 추천 (이전 질문 패턴 분석)

---

### 6. 답변 품질 피드백

**난이도:** ⭐⭐

**목표:** 사용자가 답변에 👍/👎 평가

```python
# 백엔드
class Feedback:
    def __init__(self):
        self.ratings = []

    def add_rating(self, question: str, answer: str, rating: bool):
        self.ratings.append({
            "question": question,
            "answer": answer,
            "rating": rating,  # True: 좋음, False: 나쁨
            "timestamp": datetime.now()
        })

@app.post("/feedback")
def submit_feedback(question: str, rating: bool):
    feedback.add_rating(question, rating)
    return {"success": True}
```

```javascript
// 프론트
answerDiv.innerHTML += `
    <div class="feedback">
        이 답변이 도움이 되었나요?
        <button onclick="sendFeedback(true)">👍</button>
        <button onclick="sendFeedback(false)">👎</button>
    </div>
`;
```

**활용:**
- 피드백 데이터로 프롬프트 개선
- 나쁜 평가가 많은 질문 분석
- 통계 대시보드

---

### 7. 평가 데이터셋 자동 생성

**난이도:** ⭐⭐⭐⭐

**목표:** 프로젝트 데이터에서 자동으로 평가 질문 생성

```python
# 힌트
def generate_eval_questions(projects_json: str):
    """
    projects.json을 읽고 LLM으로 평가 질문 자동 생성
    """
    with open(projects_json) as f:
        projects = json.load(f)

    questions = []
    for project in projects:
        prompt = f"""
        다음 프로젝트 정보를 보고, 이 프로젝트에 대한 질문 5개를 만드세요.
        - 기본 정보 질문 2개
        - 구체적 질문 2개
        - 문서에 없는 질문 1개 (모르는 질문 대응 테스트용)

        프로젝트: {project['title']}
        설명: {project['description']}
        """

        generated = llm.generate(prompt)
        questions.extend(generated)

    # CSV로 저장
    save_to_csv(questions, "eval_questions.csv")
```

**활용:**
- RAG 성능 자동 평가
- 회귀 테스트 (코드 변경 후 성능 확인)

---

## 🔗 풀스택 통합 아이디어

### 1. 실시간 채팅 (WebSocket)

**난이도:** ⭐⭐⭐⭐

**목표:** 여러 사용자가 동시에 챗봇과 대화

```python
# 힌트: FastAPI WebSocket
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        # 메시지 받기
        data = await websocket.receive_text()

        # RAG 처리
        result = rag_engine.query(data)

        # 응답 전송
        await websocket.send_json(result)
```

```javascript
// 프론트
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    displayAnswer(data.answer);
};

sendBtn.onclick = () => {
    ws.send(questionInput.value);
};
```

**확장 아이디어:**
- 여러 사용자 대화 표시 (채팅방)
- 온라인 사용자 수 표시
- 타이핑 중 표시

---

### 2. 관리자 대시보드

**난이도:** ⭐⭐⭐⭐

**목표:** 통계, 로그, 설정을 관리하는 관리자 페이지

**기능:**
- 질문 통계 (많이 물어본 질문 Top 10)
- 답변 품질 피드백 분석
- 프로젝트별 조회수 차트
- RAG 설정 변경 (top_k, 프롬프트)
- 방명록 관리 (삭제, 숨김)

```python
# 힌트
@app.get("/admin/stats")
def get_stats(api_key: str = Header(...)):
    # 인증 체크
    if api_key != ADMIN_API_KEY:
        raise HTTPException(401)

    return {
        "total_questions": len(question_log),
        "top_questions": get_top_questions(10),
        "avg_rating": calculate_avg_rating(),
        "project_views": project_stats.views
    }
```

**프론트:**
- Chart.js로 그래프
- 간단한 React/Vue 대시보드

---

### 3. 다국어 지원

**난이도:** ⭐⭐⭐

**목표:** 한국어/영어 전환

```javascript
// 프론트: i18n
const translations = {
    ko: {
        title: "AI 포트폴리오",
        search: "검색...",
        projects: "프로젝트"
    },
    en: {
        title: "AI Portfolio",
        search: "Search...",
        projects: "Projects"
    }
};

function setLanguage(lang) {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n;
        el.textContent = translations[lang][key];
    });
}
```

```python
# 백엔드: 언어별 프롬프트
PROMPTS = {
    "ko": "당신은 AI 포트폴리오 전문가입니다...",
    "en": "You are an AI portfolio expert..."
}

@app.post("/chat")
def chat(request: ChatRequest):
    prompt = PROMPTS[request.language]
    # ...
```

**확장 아이디어:**
- 자동 언어 감지
- projects.json도 다국어 지원

---

### 4. PWA (Progressive Web App)

**난이도:** ⭐⭐⭐

**목표:** 앱처럼 설치 가능한 웹사이트

```javascript
// manifest.json
{
    "name": "내 AI 포트폴리오",
    "short_name": "Portfolio",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#2196f3",
    "icons": [
        {
            "src": "icon-192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "icon-512.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
}
```

```javascript
// service-worker.js
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('v1').then((cache) => {
            return cache.addAll([
                '/',
                '/index.html',
                '/style.css',
                '/app.js'
            ]);
        })
    );
});
```

**효과:**
- 홈 화면에 추가 가능
- 오프라인에서도 기본 페이지 표시
- 네이티브 앱 같은 느낌

---

### 5. A/B 테스트 시스템

**난이도:** ⭐⭐⭐⭐

**목표:** 2가지 프롬프트/디자인을 비교하여 더 나은 것 선택

```python
# 힌트
import random

class ABTest:
    def __init__(self):
        self.variants = {
            "A": PROMPT_A,
            "B": PROMPT_B
        }
        self.results = {"A": [], "B": []}

    def get_variant(self, user_id: str):
        # 사용자를 A/B 그룹으로 분배
        return "A" if hash(user_id) % 2 == 0 else "B"

    def record_feedback(self, variant: str, rating: bool):
        self.results[variant].append(rating)

    def analyze(self):
        # A와 B의 평균 평점 비교
        avg_a = sum(self.results["A"]) / len(self.results["A"])
        avg_b = sum(self.results["B"]) / len(self.results["B"])

        return {
            "winner": "A" if avg_a > avg_b else "B",
            "confidence": calculate_confidence(self.results)
        }
```

**테스트 가능한 것:**
- 프롬프트 A vs B
- 카드 레이아웃 A vs B
- 색상 테마 A vs B
