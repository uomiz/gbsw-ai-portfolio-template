# Step 2: 포트폴리오 웹앱 제작

`data/projects.json`을 읽어 동적으로 렌더링하는 포트폴리오 사이트 만들기

---

## 🎯 학습 목표

- Single Source of Truth 개념 이해
- Fetch API로 JSON 데이터 로드
- JavaScript로 동적 HTML 렌더링
- CSS로 개성 있는 디자인 커스터마이징
- 반응형 레이아웃 구현

---

## 📂 파일 구조

```
web/
├── index.html      # HTML 구조
├── app.js          # projects.json 로드 및 렌더링
├── style.css       # 스타일링
└── widget.js       # 챗봇 위젯 (3단계에서 활성화)

data/
└── projects.json   # 데이터 소스
```

---

## 🚀 빠른 시작

### Step 1: 예시 코드 실행

먼저 제공된 예시를 실행해보세요:

#### 예시 1: 심플 버전 (web1)

```bash
# examples/web1 폴더로 이동
cd examples/web1

# 간단한 HTTP 서버 실행
python3 -m http.server 8000
```

브라우저에서 http://localhost:8000 접속

**특징:**
- 미니멀 디자인
- 기본 카드 레이아웃
- 심플한 색상

#### 예시 2: 풀 기능 버전 (web2)

```bash
cd examples/web2
python3 -m http.server 8001
```

브라우저에서 http://localhost:8001 접속

**특징:**
- 프로젝트 필터링
- 태그 검색
- 애니메이션 효과
- 다크 모드

### Step 2: 본인 웹사이트 실행

```bash
# 프로젝트 루트로 이동
cd ../../

# web 폴더 실행
python3 -m http.server 8080
```

브라우저에서 http://localhost:8080/web/ 접속

---

## 📖 동작 원리 이해하기

### 1. HTML 구조 ([index.html](../web/index.html))

```html
<!DOCTYPE html>
<html>
<head>
    <title>My AI Portfolio</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- 헤더 -->
    <header>
        <h1>내 이름</h1>
        <p>AI/ML 개발자</p>
    </header>

    <!-- 프로젝트 카드들이 렌더링될 공간 -->
    <main id="projects-container">
        <!-- JavaScript로 동적 생성됨 -->
    </main>

    <script src="app.js"></script>
</body>
</html>
```

### 2. JavaScript 로직 ([app.js](../web/app.js))

```javascript
// 1. projects.json 로드
fetch('../data/projects.json')
    .then(response => response.json())
    .then(projects => {
        // 2. 각 프로젝트를 카드로 렌더링
        projects.forEach(project => {
            const card = createProjectCard(project);
            container.appendChild(card);
        });
    });

// 3. 카드 HTML 생성
function createProjectCard(project) {
    const card = document.createElement('div');
    card.className = 'project-card';
    card.innerHTML = `
        <h3>${project.title}</h3>
        <p>${project.description}</p>
        <div class="tags">
            ${project.tags.map(tag => `<span>${tag}</span>`).join('')}
        </div>
    `;
    return card;
}
```

### 3. 스타일링 ([style.css](../web/style.css))

```css
/* 프로젝트 카드 스타일 */
.project-card {
    background: white;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.project-card h3 {
    color: #333;
    margin-bottom: 10px;
}

.tags span {
    background: #e3f2fd;
    padding: 5px 10px;
    border-radius: 5px;
    font-size: 0.9em;
}
```

---

## 🎨 커스터마이징 가이드

### 1. 개인 정보 수정

`web/index.html` 열기:

```html
<header>
    <h1>홍길동</h1>  <!-- 본인 이름으로 변경 -->
    <p>AI/ML Developer</p>  <!-- 본인 소개로 변경 -->
</header>
```

### 2. 색상 테마 변경

`web/style.css`에서:

```css
:root {
    --primary-color: #2196f3;    /* 메인 색상 */
    --secondary-color: #ff9800;  /* 강조 색상 */
    --background: #f5f5f5;       /* 배경색 */
    --text-color: #333;          /* 텍스트 색상 */
}
```

**색상 선택 도구:**
- [Coolors.co](https://coolors.co/) - 색상 팔레트 생성기
- [Adobe Color](https://color.adobe.com/) - 색상 조합

### 3. 레이아웃 변경

#### 그리드 레이아웃 (카드 나란히)

```css
#projects-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    padding: 20px;
}
```

#### 세로 레이아웃 (한 줄씩)

```css
#projects-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.project-card {
    margin-bottom: 30px;
}
```

### 4. 카드 스타일 커스터마이징

#### 예시 1: 미니멀 스타일

```css
.project-card {
    background: white;
    border-left: 4px solid var(--primary-color);
    padding: 20px;
    margin-bottom: 20px;
}
```

#### 예시 2: 카드 호버 효과

```css
.project-card {
    transition: transform 0.3s, box-shadow 0.3s;
}

.project-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}
```

#### 예시 3: 그라데이션 배경

```css
.project-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}
```

---

## 🎭 디자인 콘셉트 예시

### 콘셉트 1: 미니멀 모던

```css
body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    background: #fafafa;
    color: #333;
}

.project-card {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
}
```

### 콘셉트 2: 다크 테크

```css
body {
    font-family: 'Courier New', monospace;
    background: #1a1a1a;
    color: #00ff00;
}

.project-card {
    background: #2a2a2a;
    border: 1px solid #00ff00;
    box-shadow: 0 0 10px rgba(0,255,0,0.3);
}
```

### 콘셉트 3: 컬러풀 크리에이티브

```css
body {
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
    font-family: 'Poppins', sans-serif;
}

.project-card {
    background: rgba(255,255,255,0.9);
    backdrop-filter: blur(10px);
    border-radius: 20px;
}
```

---

## 📱 반응형 디자인

### 모바일 대응

```css
/* 데스크톱 */
#projects-container {
    grid-template-columns: repeat(3, 1fr);
}

/* 태블릿 */
@media (max-width: 1024px) {
    #projects-container {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* 모바일 */
@media (max-width: 768px) {
    #projects-container {
        grid-template-columns: 1fr;
    }

    .project-card {
        padding: 15px;
    }
}
```

---

## 🔧 고급 기능 추가 (선택)

### 1. 태그 필터링

```javascript
// app.js에 추가
function filterByTag(tag) {
    const cards = document.querySelectorAll('.project-card');
    cards.forEach(card => {
        const tags = card.dataset.tags.split(',');
        card.style.display = tags.includes(tag) ? 'block' : 'none';
    });
}
```

### 2. 검색 기능

```html
<!-- index.html에 추가 -->
<input type="text" id="search" placeholder="프로젝트 검색...">
```

```javascript
// app.js에 추가
document.getElementById('search').addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    const cards = document.querySelectorAll('.project-card');

    cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(query) ? 'block' : 'none';
    });
});
```

### 3. 프로젝트 상세 모달

```javascript
function showProjectDetail(project) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <h2>${project.title}</h2>
            <p>${project.description}</p>
            <a href="${project.link}" target="_blank">GitHub 보기</a>
            <button onclick="closeModal()">닫기</button>
        </div>
    `;
    document.body.appendChild(modal);
}
```

---

## ✅ 체크리스트

완성 후 확인:

- [ ] `data/projects.json`의 모든 프로젝트가 표시됨
- [ ] 카드 클릭/호버 시 반응이 있음
- [ ] 본인 이름과 소개가 표시됨
- [ ] 색상 테마가 적용됨
- [ ] 모바일에서도 잘 보임 (개발자 도구로 테스트)
- [ ] 브라우저 콘솔에 에러 없음 (F12)

---

## 🐛 문제 해결

### Q1. 프로젝트가 안 보여요!

**원인:** projects.json 경로 오류

**해결:**
```javascript
// app.js에서 경로 확인
fetch('../data/projects.json')  // 상대 경로 확인
```

브라우저 콘솔(F12)에서 네트워크 탭 확인

### Q2. 스타일이 안 먹혀요!

**원인:** CSS 파일 경로 오류 또는 선택자 오타

**해결:**
1. `<link href="style.css">`  경로 확인
2. 브라우저에서 F5로 강력 새로고침 (Ctrl+Shift+R)
3. 개발자 도구로 CSS 로드 확인

### Q3. localhost에서 CORS 에러가 나요!

**원인:** file:// 프로토콜로 열었을 때

**해결:**
```bash
# 반드시 HTTP 서버로 실행
python3 -m http.server 8080
```

---

## 💡 학습 팁

1. **예시부터 실행**: web1, web2를 먼저 실행하고 코드를 읽어보세요
2. **하나씩 수정**: 색상 하나 바꾸고 → 확인 → 다음 수정
3. **개발자 도구 활용**: F12로 실시간 CSS 수정 가능
4. **참고 사이트 분석**: [REFERENCES.md](REFERENCES.md)의 사이트들 참고

---

## 🎨 디자인 참고 자료

### 색상
- [Coolors](https://coolors.co/)
- [Color Hunt](https://colorhunt.co/)

### 폰트
- [Google Fonts](https://fonts.google.com/)
- 추천: Roboto, Open Sans, Poppins, Montserrat

### 아이콘
- [Font Awesome](https://fontawesome.com/)
- [Heroicons](https://heroicons.com/)

### 레이아웃 영감
- [Awwwards](https://www.awwwards.com/)
- [One Page Love](https://onepagelove.com/gallery/portfolio)

---

## 🎉 다음 단계

웹사이트 완성했나요?

✅ **완료했다면:**
👉 [03-RAG.md](03-RAG.md)로 이동하여 RAG 챗봇을 만들어보세요!

🎨 **더 꾸미고 싶다면:**
- `examples/web2/` 코드 참고
- 애니메이션 효과 추가
- 다크 모드 구현
