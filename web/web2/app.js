/* ════════════════════════════════════════════════════════════
   app.js — projects.json fetch → 프로필/카드 렌더 + 검색·태그
   필터·리빌 애니메이션·테마 토글.
   window.PortfolioApp 로 데이터/검색 유틸을 노출 → widget.js 재사용.
   ════════════════════════════════════════════════════════════ */

(function () {
  "use strict";

  const grid = document.getElementById("project-grid");
  const countEl = document.getElementById("project-count");
  const emptyState = document.getElementById("empty-state");
  const tagFilters = document.getElementById("tag-filters");
  const searchInput = document.getElementById("search-input");
  const searchClear = document.getElementById("search-clear");

  const state = {
    all: [],        // 원본 프로젝트
    query: "",      // 검색어
    activeTags: new Set(), // 선택된 태그
  };

  init();
  initTheme();

  // ── 진입점 ──────────────────────────────
  async function init() {
    try {
      const data = await loadData();
      renderProfile(data.profile, data.projects);
      state.all = Array.isArray(data.projects) ? data.projects : [];
      buildTagFilters(state.all);
      apply();
      bindControls();

      // 위젯이 사용할 API 노출
      window.PortfolioApp = {
        profile: data.profile,
        projects: state.all,
        search: searchProjects,
      };
      document.dispatchEvent(new CustomEvent("portfolio:ready"));
    } catch (err) {
      console.error("[app] 데이터 로드 실패:", err);
      grid.innerHTML =
        '<p class="loading">데이터를 불러오지 못했습니다. (projects.json 확인)</p>';
    }
  }

  async function loadData() {
    const res = await fetch("projects.json", { cache: "no-store" });
    if (!res.ok) throw new Error("HTTP " + res.status);
    return res.json();
  }

  // ── 프로필 + 헤더 통계 ──────────────────
  function renderProfile(profile, projects) {
    if (!profile) return;
    setText("profile-name", profile.name);
    setText("profile-role", profile.role);
    setText("profile-summary", profile.summary);

    const avatar = document.getElementById("profile-avatar");
    if (avatar && profile.name) avatar.textContent = profile.name.slice(0, 2);

    // 헤더 통계: 프로젝트 수 / 고유 기술 수 / 최근 연도
    const list = projects || [];
    const techCount = new Set(list.flatMap((p) => p.tags || [])).size;
    const years = list
      .map((p) => (p.period || "").match(/\d{4}/g))
      .flat()
      .filter(Boolean);
    const latest = years.length ? Math.max(...years.map(Number)) : "—";
    renderStats([
      [list.length, "Projects"],
      [techCount, "Tech used"],
      [latest, "Latest"],
    ]);
  }

  function renderStats(pairs) {
    const box = document.getElementById("header-stats");
    if (!box) return;
    box.innerHTML = "";
    pairs.forEach(([val, label]) => {
      const s = el("div", "stat");
      s.appendChild(el("b", "", String(val)));
      s.appendChild(el("span", "", label));
      box.appendChild(s);
    });
  }

  // ── 태그 필터 칩 생성 ───────────────────
  function buildTagFilters(projects) {
    const tags = [...new Set(projects.flatMap((p) => p.tags || []))];
    tagFilters.innerHTML = "";
    tags.forEach((tag) => {
      const chip = el("button", "chip", tag);
      chip.type = "button";
      chip.setAttribute("aria-pressed", "false");
      chip.addEventListener("click", () => toggleTag(tag, chip));
      tagFilters.appendChild(chip);
    });
  }

  function toggleTag(tag, chip) {
    if (state.activeTags.has(tag)) {
      state.activeTags.delete(tag);
      chip.setAttribute("aria-pressed", "false");
    } else {
      state.activeTags.add(tag);
      chip.setAttribute("aria-pressed", "true");
    }
    apply();
  }

  // ── 검색 + 필터 적용 ────────────────────
  function apply() {
    let list = state.all;

    if (state.activeTags.size) {
      list = list.filter((p) =>
        (p.tags || []).some((t) => state.activeTags.has(t))
      );
    }
    if (state.query) {
      list = searchProjects(state.query, list);
    }

    renderProjects(list);
  }

  // ── 검색 유틸 (위젯도 재사용) ───────────
  function searchProjects(query, source) {
    const q = query.trim().toLowerCase();
    if (!q) return source || state.all;
    const words = q.split(/\s+/);
    return (source || state.all)
      .map((p) => ({ p, score: scoreProject(p, words) }))
      .filter((x) => x.score > 0)
      .sort((a, b) => b.score - a.score)
      .map((x) => x.p);
  }

  function scoreProject(p, words) {
    const hay = [
      p.title, p.summary, p.role, p.period, (p.tags || []).join(" "),
    ].join(" ").toLowerCase();
    let score = 0;
    words.forEach((w) => {
      if (!w) return;
      if ((p.title || "").toLowerCase().includes(w)) score += 5;
      if ((p.tags || []).some((t) => t.toLowerCase().includes(w))) score += 4;
      if (hay.includes(w)) score += 1;
    });
    return score;
  }

  // ── 카드 렌더 ───────────────────────────
  function renderProjects(list) {
    countEl.textContent = `${list.length} / ${state.all.length}`;

    if (!list.length) {
      grid.innerHTML = "";
      emptyState.hidden = false;
      return;
    }
    emptyState.hidden = true;
    grid.innerHTML = "";

    const frag = document.createDocumentFragment();
    list.forEach((p, i) => frag.appendChild(buildCard(p, i)));
    grid.appendChild(frag);

    revealCards();
  }

  // ── 카드 1개 ────────────────────────────
  function buildCard(p, i) {
    const card = el("article", "card");
    card.tabIndex = 0;

    card.appendChild(el("span", "card-index", `0${i + 1}`.slice(-2)));
    card.appendChild(el("h3", "card-title", p.title || "제목 없음"));

    const meta = el("div", "card-meta");
    if (p.period) meta.appendChild(el("span", "", p.period));
    if (p.period && p.role) meta.appendChild(el("span", "dot", "·"));
    if (p.role) meta.appendChild(el("span", "", p.role));
    card.appendChild(meta);

    if (p.summary) card.appendChild(el("p", "card-summary", p.summary));

    if (Array.isArray(p.tags) && p.tags.length) {
      const tags = el("div", "card-tags");
      p.tags.forEach((t) => {
        const tag = el("span", "tag", t);
        if (state.activeTags.has(t) || matchesQuery(t)) tag.classList.add("hot");
        tags.appendChild(tag);
      });
      card.appendChild(tags);
    }

    const links = buildLinks(p.links);
    if (links) card.appendChild(links);

    // 카드 클릭 → 챗봇에게 이 프로젝트 질문 (위젯 연동)
    card.addEventListener("click", (e) => {
      if (e.target.closest("a")) return; // 링크 클릭은 통과
      document.dispatchEvent(
        new CustomEvent("portfolio:ask", { detail: { title: p.title } })
      );
    });

    return card;
  }

  function matchesQuery(t) {
    return state.query && t.toLowerCase().includes(state.query.toLowerCase());
  }

  function buildLinks(links) {
    if (!links) return null;
    const wrap = el("div", "card-links");
    let has = false;
    if (links.demo) { wrap.appendChild(anchor(links.demo, "↗ 데모")); has = true; }
    if (links.repo) { wrap.appendChild(anchor(links.repo, "↗ 코드")); has = true; }
    return has ? wrap : null;
  }

  // ── 스크롤 리빌 애니메이션 ──────────────
  function revealCards() {
    const cards = grid.querySelectorAll(".card");
    if (!("IntersectionObserver" in window)) {
      cards.forEach((c) => c.classList.add("in"));
      return;
    }
    const io = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const idx = [...cards].indexOf(entry.target);
            entry.target.style.transitionDelay = `${Math.min(idx, 6) * 55}ms`;
            entry.target.classList.add("in");
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08 }
    );
    cards.forEach((c) => io.observe(c));
  }

  // ── 컨트롤 바인딩 ───────────────────────
  function bindControls() {
    searchInput.addEventListener("input", () => {
      state.query = searchInput.value;
      searchClear.hidden = !state.query;
      apply();
    });
    searchClear.addEventListener("click", () => {
      searchInput.value = "";
      state.query = "";
      searchClear.hidden = true;
      apply();
      searchInput.focus();
    });
    document.getElementById("reset-filters").addEventListener("click", resetAll);

    // 챗봇/키보드에서 검색어 주입 지원
    document.addEventListener("portfolio:set-query", (e) => {
      searchInput.value = e.detail.query;
      state.query = e.detail.query;
      searchClear.hidden = !state.query;
      apply();
      searchInput.scrollIntoView({ block: "center" });
    });
  }

  function resetAll() {
    state.query = "";
    state.activeTags.clear();
    searchInput.value = "";
    searchClear.hidden = true;
    tagFilters.querySelectorAll(".chip").forEach((c) =>
      c.setAttribute("aria-pressed", "false")
    );
    apply();
  }

  // ── 테마 토글 (localStorage 유지) ───────
  function initTheme() {
    const KEY = "portfolio-theme";
    const saved = localStorage.getItem(KEY);
    const prefersDark =
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches;
    const theme = saved || (prefersDark ? "dark" : "light");
    document.documentElement.setAttribute("data-theme", theme);

    const btn = document.getElementById("theme-toggle");
    if (btn) {
      btn.addEventListener("click", () => {
        const cur = document.documentElement.getAttribute("data-theme");
        const next = cur === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", next);
        localStorage.setItem(KEY, next);
      });
    }
  }

  // ── DOM 헬퍼 ────────────────────────────
  function el(tag, cls, text) {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function anchor(href, text) {
    const a = document.createElement("a");
    a.href = href || "#";
    a.textContent = text;
    a.target = "_blank";
    a.rel = "noopener";
    return a;
  }
  function setText(id, text) {
    const n = document.getElementById(id);
    if (n) n.textContent = text || "";
  }
})();
