/* ════════════════════════════════════════════════════════════
   widget.js — 포트폴리오 챗봇 위젯.
   지금은 projects.json을 로컬 검색해 답하는 "데모 모드"로 동작.
   실제 RAG 백엔드가 준비되면 CONFIG.useRAG = true 로 바꾸고
   callRAG() 안의 fetch 를 활성화하면 됨.
   app.js가 노출한 window.PortfolioApp.search 를 재사용.
   ════════════════════════════════════════════════════════════ */

(function () {
  "use strict";

  const CONFIG = {
    useRAG: false,               // TODO: 백엔드 준비되면 true
    endpoint: "/api/chat",       // TODO: 실제 RAG 엔드포인트
    title: "포트폴리오 도우미",
    status: "온라인 · 데모 모드",
    greeting:
      "안녕하세요! 이 포트폴리오에 대해 무엇이든 물어보세요. 기술 스택, 프로젝트, 역할 등을 찾아드릴게요.",
    suggestions: ["RAG 프로젝트 보여줘", "백엔드 경험", "어떤 기술을 쓰나요?"],
  };

  const root = document.getElementById("chat-widget-root");
  if (!root) return;

  let open = false;
  let ready = false;
  let bodyEl, inputEl, fabEl, panelEl;

  mount();

  // 데이터 준비되면 활성화
  if (window.PortfolioApp) ready = true;
  document.addEventListener("portfolio:ready", () => (ready = true));

  // 카드 클릭 → 해당 프로젝트를 챗봇에게 질문
  document.addEventListener("portfolio:ask", (e) => {
    openPanel(true);
    handleUser(`"${e.detail.title}" 프로젝트 알려줘`);
  });

  // ── 마운트 ──────────────────────────────
  function mount() {
    fabEl = document.createElement("button");
    fabEl.className = "chat-fab";
    fabEl.type = "button";
    fabEl.setAttribute("aria-label", "챗봇 열기");
    fabEl.textContent = "✦";
    fabEl.addEventListener("click", () => openPanel(!open));

    panelEl = document.createElement("div");
    panelEl.className = "chat-panel";
    panelEl.hidden = true;
    panelEl.innerHTML = `
      <div class="chat-panel-head">
        <div class="chat-avatar">✦</div>
        <div class="chat-head-txt">
          <b>${CONFIG.title}</b>
          <small>${CONFIG.status}</small>
        </div>
      </div>
      <div class="chat-panel-body" id="chat-body"></div>
      <div class="chat-panel-foot">
        <input id="chat-input" type="text" placeholder="메시지를 입력하세요…" autocomplete="off" />
        <button class="chat-send" id="chat-send" aria-label="전송">↑</button>
      </div>`;

    root.appendChild(fabEl);
    root.appendChild(panelEl);
    bodyEl = panelEl.querySelector("#chat-body");
    inputEl = panelEl.querySelector("#chat-input");

    // 첫 인사 + 추천 질문
    botSay(CONFIG.greeting);
    renderSuggestions(CONFIG.suggestions);

    inputEl.addEventListener("keydown", (e) => {
      if (e.key === "Enter") submit();
    });
    panelEl.querySelector("#chat-send").addEventListener("click", submit);
  }

  // ── 패널 토글 ───────────────────────────
  function openPanel(v) {
    open = v;
    panelEl.hidden = !open;
    fabEl.classList.toggle("open", open);
    fabEl.textContent = open ? "×" : "✦";
    if (open) setTimeout(() => inputEl.focus(), 60);
  }

  function submit() {
    const text = inputEl.value.trim();
    if (!text) return;
    inputEl.value = "";
    handleUser(text);
  }

  // ── 사용자 메시지 처리 ──────────────────
  async function handleUser(text) {
    userSay(text);
    clearSuggestions();
    const typing = showTyping();

    let reply;
    if (CONFIG.useRAG) {
      reply = await callRAG(text);
    } else {
      await wait(420 + Math.random() * 320); // 사람처럼 잠깐 대기
      reply = answerLocally(text);
    }

    typing.remove();
    botSay(reply.text, reply.cards);
    if (reply.followups) renderSuggestions(reply.followups);
  }

  // ── 로컬 검색 응답 (데모) ───────────────
  function answerLocally(query) {
    const app = window.PortfolioApp;
    if (!app || !ready) {
      return { text: "데이터를 아직 불러오는 중이에요. 잠시 후 다시 시도해 주세요." };
    }

    // "기술 스택" 류 질문 → 태그 요약
    if (/기술|스택|스킬|tech|stack|무엇|뭐/i.test(query) && !hasProjectHint(query)) {
      const tags = [...new Set(app.projects.flatMap((p) => p.tags || []))];
      return {
        text: `주로 다루는 기술은 다음과 같아요: ${tags.join(", ")}. 특정 기술이 들어간 프로젝트가 궁금하면 이름을 말씀해 주세요.`,
        followups: tags.slice(0, 3).map((t) => `${t} 쓴 프로젝트`),
      };
    }

    // 프로젝트 검색
    const hits = app.search(query, app.projects).slice(0, 3);
    if (!hits.length) {
      return {
        text: "관련된 프로젝트를 찾지 못했어요. '백엔드', 'RAG', '추천' 같은 키워드로 다시 물어봐 주세요.",
        followups: CONFIG.suggestions,
      };
    }

    const lead =
      hits.length === 1
        ? `"${hits[0].title}" 프로젝트를 찾았어요.`
        : `관련 프로젝트 ${hits.length}건을 찾았어요.`;
    return {
      text: `${lead} ${hits[0].summary}`,
      cards: hits.map((p) => ({
        title: p.title,
        meta: `${p.period || ""} · ${(p.tags || []).join(", ")}`,
        href: (p.links && (p.links.demo || p.links.repo)) || "#",
      })),
    };
  }

  function hasProjectHint(q) {
    const app = window.PortfolioApp;
    if (!app) return false;
    return app.projects.some((p) =>
      q.includes((p.title || "").slice(0, 3))
    );
  }

  // ── 실제 RAG 호출 (준비되면 사용) ───────
  async function callRAG(question) {
    try {
      // TODO(2일차): 아래 fetch 를 실제 백엔드에 맞게 구현.
      const res = await fetch(CONFIG.endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question,
          context: window.PortfolioApp && window.PortfolioApp.projects,
        }),
      });
      const data = await res.json();
      return { text: data.reply, cards: data.sources };
    } catch (err) {
      console.error("[widget] RAG 호출 실패:", err);
      return { text: "응답을 가져오지 못했어요. 잠시 후 다시 시도해 주세요." };
    }
  }

  // ── 메시지 출력 ─────────────────────────
  function botSay(text, cards) {
    const msg = div("msg bot");
    msg.textContent = text;
    if (cards && cards.length) {
      const wrap = div("msg-cards");
      cards.forEach((c) => {
        const a = document.createElement("a");
        a.className = "msg-card";
        a.href = c.href || "#";
        a.target = "_blank";
        a.rel = "noopener";
        a.innerHTML = `<b></b><span></span>`;
        a.querySelector("b").textContent = c.title;
        a.querySelector("span").textContent = c.meta || "";
        wrap.appendChild(a);
      });
      msg.appendChild(wrap);
    }
    bodyEl.appendChild(msg);
    scrollDown();
  }

  function userSay(text) {
    const msg = div("msg user");
    msg.textContent = text;
    bodyEl.appendChild(msg);
    scrollDown();
  }

  function showTyping() {
    const msg = div("msg bot");
    msg.innerHTML = `<span class="typing"><i></i><i></i><i></i></span>`;
    bodyEl.appendChild(msg);
    scrollDown();
    return msg;
  }

  // ── 추천 질문 칩 ────────────────────────
  function renderSuggestions(items) {
    clearSuggestions();
    const wrap = div("chat-suggest");
    wrap.id = "chat-suggest";
    items.forEach((q) => {
      const b = document.createElement("button");
      b.type = "button";
      b.textContent = q;
      b.addEventListener("click", () => handleUser(q));
      wrap.appendChild(b);
    });
    bodyEl.appendChild(wrap);
    scrollDown();
  }
  function clearSuggestions() {
    const old = document.getElementById("chat-suggest");
    if (old) old.remove();
  }

  // ── 유틸 ────────────────────────────────
  function div(cls) {
    const n = document.createElement("div");
    n.className = cls;
    return n;
  }
  function scrollDown() {
    bodyEl.scrollTop = bodyEl.scrollHeight;
  }
  function wait(ms) {
    return new Promise((r) => setTimeout(r, ms));
  }
})();
