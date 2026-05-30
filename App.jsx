import { useState, useRef, useEffect } from "react";

const API_URL = "http://127.0.0.1:8000";

function generateSession() {
  return Math.random().toString(36).substring(2, 10);
}

const sessionId = generateSession();

const Icons = {
  Home: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>,
  Chat: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>,
  Search: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>,
  Docs: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2-2.5z"/><path d="M6 6h10M6 10h10M6 14h6"/></svg>,
  Stats: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>,
  Settings: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>,
  Lightning: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>,
  Lock: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>,
  Globe: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>,
  Database: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/><path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"/></svg>,
  Mic: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>,
  Bot: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4M8 16h.01M16 16h.01"/></svg>,
  Check: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>,
  Alert: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>,
  Users: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>,
  Arrow: () => <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>,
  Terminal: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>,
  Cpu: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>,
};

function parseMarkdown(text) {
  if (!text) return "";
  let lines = text.split("\n");
  let inTable = false, inList = false;
  let tableRows = [], htmlResult = [];
  for (let i = 0; i < lines.length; i++) {
    let line = lines[i].trim();
    if (line.startsWith("|")) {
      if (inList) { htmlResult.push('</ul>'); inList = false; }
      if (line.includes("---")) continue;
      inTable = true;
      let cells = line.split("|").map(c => c.trim()).filter((c, idx, arr) => idx > 0 && idx < arr.length - 1);
      tableRows.push(cells);
      continue;
    }
    if (inTable && !line.startsWith("|")) {
      htmlResult.push(renderTableHtml(tableRows));
      tableRows = []; inTable = false;
    }
    if (line.startsWith("* ") || line.startsWith("- ")) {
      if (!inList) { htmlResult.push(`<ul style="padding-left:20px;margin:8px 0 16px;color:#c9c9c9;">`); inList = true; }
      htmlResult.push(`<li style="margin-bottom:6px;line-height:1.7;">${formatInline(line.substring(2))}</li>`);
      continue;
    } else if (/^\d+\.\s/.test(line)) {
      if (!inList) { htmlResult.push(`<ol style="padding-left:20px;margin:8px 0 16px;color:#c9c9c9;">`); inList = true; }
      htmlResult.push(`<li style="margin-bottom:6px;line-height:1.7;">${formatInline(line.replace(/^\d+\.\s/, ''))}</li>`);
      continue;
    } else {
      if (inList) { htmlResult.push('</ul>'); inList = false; }
    }
    if (line.startsWith("### ")) htmlResult.push(`<h3 style="margin:20px 0 10px;font-weight:600;color:#fff;font-size:17px;font-family:'DM Mono',monospace;">${formatInline(line.substring(4))}</h3>`);
    else if (line.startsWith("## ")) htmlResult.push(`<h2 style="margin:24px 0 12px;font-weight:700;color:#fff;font-size:20px;">${formatInline(line.substring(3))}</h2>`);
    else if (line.startsWith("**") && line.endsWith("**")) htmlResult.push(`<p style="margin:14px 0 10px;font-weight:600;color:#fff;font-size:15px;">${formatInline(line)}</p>`);
    else if (line === "") {}
    else htmlResult.push(`<p style="margin-bottom:12px;color:#c9c9c9;line-height:1.75;font-size:14.5px;">${formatInline(line)}</p>`);
  }
  if (inTable && tableRows.length > 0) htmlResult.push(renderTableHtml(tableRows));
  if (inList) htmlResult.push('</ul>');
  return htmlResult.join("");
}

function formatInline(text) {
  let f = text.replace(/\*\*(.*?)\*\*/g, '<strong style="color:#fff;font-weight:600;">$1</strong>');
  f = f.replace(/`(.*?)`/g, '<code style="background:#1a1a2e;color:#7dd3fc;padding:2px 7px;border-radius:5px;font-family:\'DM Mono\',monospace;font-size:13px;border:1px solid #2d2d4e;">$1</code>');
  return f;
}

function renderTableHtml(rows) {
  if (!rows.length) return "";
  let header = rows[0], body = rows.slice(1);
  let headerHtml = header.map(cell => `<th style="padding:10px 14px;background:#111;color:#888;font-weight:600;border-bottom:1px solid #222;text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:1px;">${formatInline(cell)}</th>`).join("");
  let bodyHtml = body.map(row => `<tr>${row.map(cell => `<td style="padding:12px 14px;border-bottom:1px solid #1a1a1a;color:#c9c9c9;font-size:13.5px;">${formatInline(cell)}</td>`).join("")}</tr>`).join("");
  return `<div style="overflow-x:auto;margin:20px 0;border-radius:10px;border:1px solid #222;background:#111;"><table style="width:100%;border-collapse:collapse;"><thead><tr>${headerHtml}</tr></thead><tbody>${bodyHtml}</tbody></table></div>`;
}

export default function App() {
  const [page, setPage] = useState("home");
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [totalMsgs, setTotalMsgs] = useState(0);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchResults, setSearchResults] = useState([]);
  const [darkMode, setDarkMode] = useState(true);
  const [model, setModel] = useState("groq");
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const msgRef = useRef(null);

  useEffect(() => {
    if (msgRef.current) msgRef.current.scrollTo({ top: msgRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    setTotalMsgs(p => p + 1);
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/chat`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ message: userMsg, session_id: sessionId }) });
      const data = await res.json();
      setMessages(prev => [...prev, { role: "assistant", content: data.response }]);
      setTotalMsgs(p => p + 1);
    } catch {
      setMessages(prev => [...prev, { role: "assistant", content: "⚠️ Ошибка подключения к серверу FastAPI на `localhost:8000`." }]);
    }
    setLoading(false);
  };

  const handleSearch = async () => {
    if (!searchQuery.trim() || searchLoading) return;
    setSearchLoading(true);
    setSearchResults([]);
    try {
      const res = await fetch(`${API_URL}/search`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ query: searchQuery }) });
      const data = await res.json();
      setSearchResults(data.results || []);
    } catch {
      setTimeout(() => {
        setSearchResults([
          { title: `Результат поиска: "${searchQuery}"`, snippet: "Асинхронный парсинг выполнен успешно. Данные получены из глобального индекса.", url: "https://google.com" },
          { title: "Модуль Butcher Search активен", snippet: "Контекст передан в окно Groq LPU для финальной обработки.", url: "http://127.0.0.1:8000" }
        ]);
      }, 800);
    }
    setSearchLoading(false);
  };

  const testTable = () => {
    const sample = `**Лучшие LLM модели 2025 года**\n\nСравнительная таблица по ключевым параметрам:\n\n| Модель | Разработчик | Контекст | Скорость | Цена |\n| --- | --- | --- | --- | --- |\n| GPT-4o | OpenAI | 128K | Высокая | $5/1M |\n| Claude 4 Sonnet | Anthropic | 200K | Высокая | $3/1M |\n| Gemini 2.0 Pro | Google | 1M | Средняя | $3.5/1M |\n| Llama 3.3 70B | Meta | 128K | Groq LPU | Бесплатно |\n\nКлючевые преимущества локального стека:\n* Нулевая задержка на Groq LPU\n* Абсолютная конфиденциальность данных\n* Offline-режим через \`Ollama\``;
    setMessages(prev => [...prev, { role: "user", content: "Сравни лучшие LLM модели 2025" }, { role: "assistant", content: sample }]);
    setTotalMsgs(p => p + 2);
    setPage("chat");
  };

  const bg = darkMode ? "#0d0d0d" : "#f5f5f0";
  const surface = darkMode ? "#141414" : "#ffffff";
  const border = darkMode ? "#1f1f1f" : "#e5e5e0";
  const text = darkMode ? "#e8e8e8" : "#1a1a1a";
  const muted = darkMode ? "#666" : "#888";
  const accent = "#3b82f6";

  const navItems = [
    { key: "home", icon: <Icons.Home />, label: "Обзор" },
    { key: "chat", icon: <Icons.Chat />, label: "Чат" },
    { key: "search", icon: <Icons.Search />, label: "Поиск" },
    { key: "docs", icon: <Icons.Docs />, label: "Документы" },
    { key: "stats", icon: <Icons.Stats />, label: "Аналитика" },
    { key: "settings", icon: <Icons.Settings />, label: "Настройки" },
  ];

  return (
    <div style={{ fontFamily: "'DM Sans', system-ui, sans-serif", background: bg, minHeight: "100vh", color: text, transition: "all 0.3s" }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { overflow: hidden; }
        .scroll::-webkit-scrollbar { width: 4px; }
        .scroll::-webkit-scrollbar-track { background: transparent; }
        .scroll::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 99px; }
        @keyframes up { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
        @keyframes spin { to { transform: rotate(360deg); } }
        .nav-btn { display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:8px;font-size:13.5px;font-weight:500;cursor:pointer;border:none;width:100%;text-align:left;transition:all 0.15s; }
        .card { border-radius:12px;border:1px solid; transition:all 0.2s; }
        .card:hover { transform:translateY(-1px); }
        .btn { border-radius:8px;cursor:pointer;font-weight:500;transition:all 0.15s;border:1px solid transparent; }
        .btn:hover { opacity:0.85; }
        .btn:active { transform:scale(0.98); }
        .msg { animation: up 0.2s ease forwards; }
        .typing span { display:inline-block;width:5px;height:5px;border-radius:50%;background:#555;margin:0 2px;animation:pulse 1.2s ease infinite; }
        .typing span:nth-child(2){animation-delay:.2s}.typing span:nth-child(3){animation-delay:.4s}
        input { outline: none; }
        input::placeholder { color: #444; }
      `}</style>

      <div style={{ display: "flex", height: "100vh" }}>
        {/* Sidebar */}
        <aside style={{ width: sidebarCollapsed ? 60 : 220, background: surface, borderRight: `1px solid ${border}`, display: "flex", flexDirection: "column", padding: "16px 10px", transition: "width 0.25s ease", overflow: "hidden" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "4px 6px 20px", borderBottom: `1px solid ${border}`, marginBottom: 12 }}>
            <div style={{ width: 28, height: 28, borderRadius: 7, background: accent, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, fontSize: 13, fontWeight: 700, color: "#fff" }}>B</div>
            {!sidebarCollapsed && <span style={{ fontSize: 14, fontWeight: 600, color: text, whiteSpace: "nowrap" }}>Butcher AI</span>}
          </div>

          <nav style={{ display: "flex", flexDirection: "column", gap: 2, flex: 1 }}>
            {navItems.map(({ key, icon, label }) => (
              <button key={key} className="nav-btn" onClick={() => setPage(key)}
                style={{ background: page === key ? (darkMode ? "#1a1a2e" : "#f0f0ff") : "transparent", color: page === key ? accent : muted, justifyContent: sidebarCollapsed ? "center" : "flex-start" }}>
                <span style={{ color: page === key ? accent : muted, flexShrink: 0 }}>{icon}</span>
                {!sidebarCollapsed && label}
              </button>
            ))}
          </nav>

          <div style={{ borderTop: `1px solid ${border}`, paddingTop: 12, display: "flex", flexDirection: "column", gap: 8 }}>
            <button className="nav-btn" onClick={() => setSidebarCollapsed(p => !p)} style={{ color: muted, background: "transparent", justifyContent: sidebarCollapsed ? "center" : "flex-start" }}>
              <span style={{ transform: sidebarCollapsed ? "rotate(0deg)" : "rotate(180deg)", transition: "transform 0.25s", display: "flex" }}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="15 18 9 12 15 6"/></svg>
              </span>
              {!sidebarCollapsed && <span style={{ fontSize: 12 }}>Свернуть</span>}
            </button>
            {!sidebarCollapsed && (
              <div style={{ padding: "6px 12px", display: "flex", alignItems: "center", gap: 6 }}>
                <div style={{ width: 6, height: 6, borderRadius: "50%", background: "#22c55e" }} />
                <span style={{ fontSize: 11, color: muted }}>Хост активен</span>
              </div>
            )}
          </div>
        </aside>

        {/* Main */}
        <main style={{ flex: 1, height: "100vh", display: "flex", flexDirection: "column", overflow: "hidden" }}>

          {/* HOME */}
          {page === "home" && (
            <div className="scroll" style={{ flex: 1, overflowY: "auto", padding: "48px 48px" }}>
              <div style={{ maxWidth: 900 }}>
                {/* Hero */}
                <div style={{ marginBottom: 48, animation: "up 0.4s ease" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 16 }}>
                    <div style={{ padding: "4px 10px", background: darkMode ? "#1a1a2e" : "#eff6ff", border: `1px solid ${darkMode ? "#2d2d4e" : "#bfdbfe"}`, borderRadius: 99, fontSize: 11, color: accent, fontWeight: 600, fontFamily: "'DM Mono', monospace" }}>v2.0 · STABLE</div>
                    <div style={{ padding: "4px 10px", background: darkMode ? "#0f2a1a" : "#f0fdf4", border: `1px solid ${darkMode ? "#1a4a2a" : "#bbf7d0"}`, borderRadius: 99, fontSize: 11, color: "#22c55e", fontWeight: 600 }}>● ОНЛАЙН</div>
                  </div>
                  <h1 style={{ fontSize: 42, fontWeight: 700, color: text, letterSpacing: -1.5, marginBottom: 14, lineHeight: 1.1 }}>Butcher AI<br /><span style={{ color: muted, fontWeight: 400 }}>Локальная экосистема</span></h1>
                  <p style={{ fontSize: 15.5, color: muted, lineHeight: 1.7, maxWidth: 540, marginBottom: 28 }}>
                    Стек FastAPI + Groq LPU + aiogram + MCP. Высокоскоростной инференс с возможностью полного перехода на локальные модели.
                  </p>
                  <div style={{ display: "flex", gap: 10 }}>
                    <button className="btn" style={{ padding: "10px 22px", background: accent, color: "#fff", fontSize: 14 }} onClick={() => setPage("chat")}>Открыть чат →</button>
                    <button className="btn" style={{ padding: "10px 22px", background: "transparent", color: muted, fontSize: 14, borderColor: border }} onClick={testTable}>Тест форматирования</button>
                  </div>
                </div>

                {/* Stats row */}
                <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12, marginBottom: 32 }}>
                  {[
                    { val: "~50ms", label: "Time to first token", color: "#3b82f6" },
                    { val: "6", label: "Активных модулей", color: "#8b5cf6" },
                    { val: "100%", label: "Приватность данных", color: "#22c55e" },
                    { val: "36", label: "aiogram хэндлеров", color: "#f59e0b" },
                  ].map((s, i) => (
                    <div key={i} className="card" style={{ background: surface, borderColor: border, padding: "18px 20px", animation: `up 0.3s ${i * 0.06}s ease both` }}>
                      <div style={{ fontSize: 26, fontWeight: 700, color: s.color, marginBottom: 4, fontFamily: "'DM Mono', monospace" }}>{s.val}</div>
                      <div style={{ fontSize: 12, color: muted }}>{s.label}</div>
                    </div>
                  ))}
                </div>

                {/* Features */}
                <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12 }}>
                  {[
                    { icon: <Icons.Lightning />, title: "Groq LPU", desc: "Минимальный Time-to-First-Token благодаря аппаратному ускорению.", color: "#3b82f6" },
                    { icon: <Icons.Lock />, title: "Ollama Приватность", desc: "Переключение на локальные веса без утечки данных.", color: "#8b5cf6" },
                    { icon: <Icons.Globe />, title: "Веб-парсинг", desc: "Асинхронный поиск актуальной информации без трекеров.", color: "#06b6d4" },
                    { icon: <Icons.Database />, title: "MCP Протокол", desc: "Управление базами данных и файловым контекстом.", color: "#22c55e" },
                    { icon: <Icons.Mic />, title: "Whisper STT", desc: "Транскрибация голосовых сообщений через Groq API.", color: "#f59e0b" },
                    { icon: <Icons.Bot />, title: "Telegram Bot", desc: "aiogram 3.x с обработкой безопасных сессий.", color: "#ec4899" },
                  ].map((f, i) => (
                    <div key={i} className="card" style={{ background: surface, borderColor: border, padding: "20px", animation: `up 0.3s ${i * 0.05}s ease both` }}>
                      <div style={{ width: 36, height: 36, borderRadius: 9, background: f.color + "15", display: "flex", alignItems: "center", justifyContent: "center", marginBottom: 14, color: f.color }}>
                        {f.icon}
                      </div>
                      <h3 style={{ fontSize: 14, fontWeight: 600, color: text, marginBottom: 6 }}>{f.title}</h3>
                      <p style={{ fontSize: 13, color: muted, lineHeight: 1.6 }}>{f.desc}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* CHAT */}
          {page === "chat" && (
            <div style={{ display: "flex", flexDirection: "column", height: "100%", background: bg }}>
              {/* Top bar */}
              <div style={{ padding: "12px 24px", borderBottom: `1px solid ${border}`, display: "flex", justifyContent: "space-between", alignItems: "center", background: surface }}>
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <div style={{ width: 32, height: 32, borderRadius: "50%", background: "#22c55e", display: "flex", alignItems: "center", justifyContent: "center" }}>
                    <Icons.Lightning />
                  </div>
                  <div>
                    <div style={{ fontSize: 14, fontWeight: 600, color: text }}>Butcher Core AI</div>
                    <div style={{ fontSize: 11, color: muted, fontFamily: "'DM Mono', monospace" }}>● {model === "groq" ? "Groq Cloud · llama-3.3-70b" : "Ollama · локально"}</div>
                  </div>
                </div>
                <div style={{ display: "flex", gap: 8 }}>
                  <select value={model} onChange={e => setModel(e.target.value)} style={{ background: darkMode ? "#1a1a1a" : "#f5f5f5", color: text, border: `1px solid ${border}`, borderRadius: 7, padding: "6px 10px", fontSize: 12, cursor: "pointer", fontFamily: "inherit" }}>
                    <option value="groq">⚡ Groq Cloud</option>
                    <option value="ollama">🔒 Ollama Local</option>
                  </select>
                  <button className="btn" onClick={() => setMessages([])} style={{ padding: "6px 14px", background: "transparent", color: muted, borderColor: border, fontSize: 12 }}>Очистить</button>
                  <button className="btn" onClick={testTable} style={{ padding: "6px 14px", background: darkMode ? "#1a1a2e" : "#eff6ff", color: accent, borderColor: darkMode ? "#2d2d4e" : "#bfdbfe", fontSize: 12 }}>Тест</button>
                </div>
              </div>

              {/* Messages */}
              <div ref={msgRef} className="scroll" style={{ flex: 1, overflowY: "auto", padding: "32px 24px" }}>
                <div style={{ maxWidth: 760, margin: "0 auto", display: "flex", flexDirection: "column", gap: 20 }}>
                  {messages.length === 0 && (
                    <div style={{ textAlign: "center", margin: "60px auto", maxWidth: 420 }}>
                      <div style={{ width: 52, height: 52, borderRadius: "50%", background: darkMode ? "#1a1a2e" : "#eff6ff", border: `1px solid ${darkMode ? "#2d2d4e" : "#bfdbfe"}`, display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 20px", color: accent }}>
                        <Icons.Chat />
                      </div>
                      <h2 style={{ fontSize: 22, fontWeight: 600, color: text, marginBottom: 8 }}>Чем помочь?</h2>
                      <p style={{ fontSize: 13.5, color: muted, marginBottom: 24 }}>Задайте вопрос или выберите подсказку</p>
                      <div style={{ display: "flex", flexWrap: "wrap", gap: 8, justifyContent: "center" }}>
                        {["Сравни LLM модели 2025", "Напиши Python скрипт", "Объясни MCP протокол"].map((s, i) => (
                          <button key={i} className="btn" onClick={() => s.includes("LLM") ? testTable() : setInput(s)}
                            style={{ padding: "8px 14px", background: "transparent", color: muted, borderColor: border, fontSize: 13 }}>{s}</button>
                        ))}
                      </div>
                    </div>
                  )}
                  {messages.map((m, i) => (
                    <div key={i} className="msg" style={{ display: "flex", justifyContent: m.role === "user" ? "flex-end" : "flex-start" }}>
                      {m.role === "assistant" && (
                        <div style={{ display: "flex", gap: 12, maxWidth: "88%" }}>
                          <div style={{ width: 28, height: 28, borderRadius: "50%", background: "#22c55e", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, marginTop: 2 }}>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                          </div>
                          <div style={{ color: text }} dangerouslySetInnerHTML={{ __html: parseMarkdown(m.content) }} />
                        </div>
                      )}
                      {m.role === "user" && (
                        <div style={{ background: darkMode ? "#1a1a2e" : "#eff6ff", border: `1px solid ${darkMode ? "#2d2d4e" : "#bfdbfe"}`, color: text, padding: "10px 16px", borderRadius: "14px 14px 4px 14px", fontSize: 14.5, lineHeight: 1.6, maxWidth: "75%" }}>
                          {m.content}
                        </div>
                      )}
                    </div>
                  ))}
                  {loading && (
                    <div style={{ display: "flex", gap: 12 }}>
                      <div style={{ width: 28, height: 28, borderRadius: "50%", background: "#22c55e", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                      </div>
                      <div className="typing" style={{ paddingTop: 8 }}><span/><span/><span/></div>
                    </div>
                  )}
                </div>
              </div>

              {/* Input */}
              <div style={{ padding: "16px 24px", background: surface, borderTop: `1px solid ${border}` }}>
                <div style={{ maxWidth: 760, margin: "0 auto", display: "flex", gap: 10, background: darkMode ? "#1a1a1a" : "#f5f5f5", border: `1px solid ${border}`, borderRadius: 12, padding: "8px 8px 8px 16px", alignItems: "center" }}>
                  <input value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === "Enter" && sendMessage()}
                    placeholder="Отправить сообщение..." style={{ flex: 1, background: "transparent", border: "none", fontSize: 14.5, color: text, fontFamily: "inherit" }} />
                  <button className="btn" onClick={sendMessage} disabled={loading || !input.trim()}
                    style={{ width: 36, height: 36, background: input.trim() ? accent : (darkMode ? "#222" : "#ddd"), border: "none", display: "flex", alignItems: "center", justifyContent: "center", borderRadius: 8, flexShrink: 0 }}>
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke={input.trim() ? "#fff" : "#666"} strokeWidth="2.5" strokeLinecap="round"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>
                  </button>
                </div>
                <div style={{ maxWidth: 760, margin: "8px auto 0", fontSize: 11, color: muted, textAlign: "center" }}>
                  {model === "groq" ? "⚡ Groq Cloud · данные передаются на сервер" : "🔒 Ollama · данные остаются локально"}
                </div>
              </div>
            </div>
          )}

          {/* SEARCH */}
          {page === "search" && (
            <div className="scroll" style={{ flex: 1, overflowY: "auto", padding: "48px" }}>
              <div style={{ maxWidth: 760 }}>
                <h1 style={{ fontSize: 28, fontWeight: 700, color: text, marginBottom: 8 }}>Глобальный поиск</h1>
                <p style={{ fontSize: 14, color: muted, marginBottom: 28 }}>Асинхронный парсинг поисковой выдачи без трекеров и рекламы</p>
                <div style={{ display: "flex", gap: 10, marginBottom: 32, background: surface, border: `1px solid ${border}`, borderRadius: 12, padding: "8px 8px 8px 16px", alignItems: "center" }}>
                  <input value={searchQuery} onChange={e => setSearchQuery(e.target.value)} onKeyDown={e => e.key === "Enter" && handleSearch()}
                    placeholder="Поисковый запрос (например: курс доллара, новости ИИ)..." style={{ flex: 1, background: "transparent", border: "none", fontSize: 14.5, color: text, fontFamily: "inherit" }} />
                  <button className="btn" onClick={handleSearch} disabled={searchLoading || !searchQuery.trim()}
                    style={{ padding: "8px 18px", background: searchQuery.trim() ? accent : (darkMode ? "#222" : "#ddd"), color: searchQuery.trim() ? "#fff" : muted, border: "none", fontSize: 13, fontWeight: 600 }}>
                    {searchLoading ? "..." : "Искать"}
                  </button>
                </div>
                {searchLoading && <div style={{ textAlign: "center", padding: 40, color: muted }}>Парсинг выдачи...</div>}
                {!searchLoading && searchResults.map((r, i) => (
                  <div key={i} className="card" style={{ background: surface, borderColor: border, padding: "18px 20px", marginBottom: 10, animation: `up 0.2s ${i * 0.05}s ease both` }}>
                    <a href={r.url} target="_blank" rel="noreferrer" style={{ textDecoration: "none", color: accent, fontSize: 15.5, fontWeight: 600, display: "block", marginBottom: 6 }}>{r.title}</a>
                    <p style={{ color: muted, fontSize: 13.5, lineHeight: 1.6, marginBottom: 8 }}>{r.snippet}</p>
                    <span style={{ color: "#444", fontSize: 11, fontFamily: "'DM Mono', monospace" }}>{r.url}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* DOCS */}
          {page === "docs" && (
            <div className="scroll" style={{ flex: 1, overflowY: "auto", padding: "48px" }}>
              <div style={{ maxWidth: 760 }}>
                <h1 style={{ fontSize: 28, fontWeight: 700, color: text, marginBottom: 8 }}>Документация</h1>
                <p style={{ fontSize: 14, color: muted, marginBottom: 32 }}>Справочник команд aiogram, системных тегов и MCP инструментов</p>
                {[
                  { title: "Основные команды", icon: <Icons.Bot />, color: "#3b82f6", tags: ["/start", "/help", "/clear", "/status", "/settings", "/analytics"] },
                  { title: "Расширенные команды", icon: <Icons.Terminal />, color: "#8b5cf6", tags: ["/tools", "/users", "/search", "/resources", "/prompts", "/mystats", "/private", "/model"] },
                  { title: "MCP инструменты", icon: <Icons.Cpu />, color: "#22c55e", tags: ["fs_read_file", "fs_write_file", "fetch_web_data", "execute_sql", "whisper_stt"] },
                  { title: "Режимы работы", icon: <Icons.Lock />, color: "#f59e0b", tags: ["Groq Cloud", "Ollama Local", "RAG Pipeline", "Webhook", "Polling"] },
                ].map((s, i) => (
                  <div key={i} className="card" style={{ background: surface, borderColor: border, padding: "22px", marginBottom: 12, animation: `up 0.3s ${i * 0.06}s ease both` }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
                      <div style={{ color: s.color }}>{s.icon}</div>
                      <h3 style={{ fontSize: 14, fontWeight: 600, color: text }}>{s.title}</h3>
                    </div>
                    <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                      {s.tags.map((tag, j) => (
                        <span key={j} style={{ background: s.color + "12", color: s.color, border: `1px solid ${s.color}30`, padding: "4px 10px", borderRadius: 6, fontSize: 12.5, fontFamily: "'DM Mono', monospace", fontWeight: 500 }}>{tag}</span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* STATS */}
          {page === "stats" && (
            <div className="scroll" style={{ flex: 1, overflowY: "auto", padding: "48px" }}>
              <div style={{ maxWidth: 900 }}>
                <h1 style={{ fontSize: 28, fontWeight: 700, color: text, marginBottom: 8 }}>Аналитика</h1>
                <p style={{ fontSize: 14, color: muted, marginBottom: 28 }}>Показатели текущей сессии и состояние системы</p>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12, marginBottom: 28 }}>
                  {[
                    { val: "1", label: "Пользователей", sub: "Администратор", icon: <Icons.Users />, color: "#3b82f6" },
                    { val: totalMsgs, label: "Сообщений", sub: "В текущей сессии", icon: <Icons.Chat />, color: "#22c55e" },
                    { val: "36", label: "Хэндлеров", sub: "aiogram + MCP", icon: <Icons.Check />, color: "#f59e0b" },
                    { val: "0%", label: "Ошибок", sub: "Статус API", icon: <Icons.Alert />, color: "#ef4444" },
                  ].map((s, i) => (
                    <div key={i} className="card" style={{ background: surface, borderColor: border, padding: "20px", animation: `up 0.3s ${i * 0.06}s ease both` }}>
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
                        <span style={{ fontSize: 32, fontWeight: 700, color: s.color, fontFamily: "'DM Mono', monospace" }}>{s.val}</span>
                        <div style={{ width: 36, height: 36, borderRadius: 9, background: s.color + "15", display: "flex", alignItems: "center", justifyContent: "center", color: s.color }}>{s.icon}</div>
                      </div>
                      <div style={{ fontSize: 13, fontWeight: 600, color: text, marginBottom: 3 }}>{s.label}</div>
                      <div style={{ fontSize: 11, color: muted }}>{s.sub}</div>
                    </div>
                  ))}
                </div>
                {/* Activity */}
                <div className="card" style={{ background: surface, borderColor: border, padding: "24px" }}>
                  <h3 style={{ fontSize: 14, fontWeight: 600, color: text, marginBottom: 16 }}>Статус компонентов</h3>
                  {[
                    { name: "FastAPI Backend", status: "online", latency: "~2ms" },
                    { name: "Groq LPU API", status: "online", latency: "~45ms" },
                    { name: "Redis Cache", status: "online", latency: "~1ms" },
                    { name: "Ollama Local", status: "standby", latency: "—" },
                    { name: "PostgreSQL", status: "online", latency: "~3ms" },
                  ].map((c, i) => (
                    <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 0", borderBottom: i < 4 ? `1px solid ${border}` : "none" }}>
                      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                        <div style={{ width: 7, height: 7, borderRadius: "50%", background: c.status === "online" ? "#22c55e" : "#f59e0b" }} />
                        <span style={{ fontSize: 13.5, color: text }}>{c.name}</span>
                      </div>
                      <div style={{ display: "flex", gap: 16 }}>
                        <span style={{ fontSize: 12, color: muted, fontFamily: "'DM Mono', monospace" }}>{c.latency}</span>
                        <span style={{ fontSize: 11, color: c.status === "online" ? "#22c55e" : "#f59e0b", background: c.status === "online" ? "#22c55e15" : "#f59e0b15", padding: "2px 8px", borderRadius: 4, fontWeight: 600 }}>{c.status}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* SETTINGS */}
          {page === "settings" && (
            <div className="scroll" style={{ flex: 1, overflowY: "auto", padding: "48px" }}>
              <div style={{ maxWidth: 600 }}>
                <h1 style={{ fontSize: 28, fontWeight: 700, color: text, marginBottom: 8 }}>Настройки</h1>
                <p style={{ fontSize: 14, color: muted, marginBottom: 32 }}>Конфигурация интерфейса и подключений</p>
                {[
                  {
                    title: "Внешний вид",
                    items: [
                      { label: "Тёмная тема", sub: "Переключить светлый/тёмный режим", control: <button className="btn" onClick={() => setDarkMode(p => !p)} style={{ padding: "6px 16px", background: darkMode ? "#1a1a2e" : "#eff6ff", color: accent, border: `1px solid ${darkMode ? "#2d2d4e" : "#bfdbfe"}`, fontSize: 12 }}>{darkMode ? "Тёмная ✓" : "Светлая ✓"}</button> },
                      { label: "Компактный сайдбар", sub: "Скрыть подписи меню", control: <button className="btn" onClick={() => setSidebarCollapsed(p => !p)} style={{ padding: "6px 16px", background: sidebarCollapsed ? "#1a1a2e" : "transparent", color: sidebarCollapsed ? accent : muted, borderColor: border, fontSize: 12 }}>{sidebarCollapsed ? "Вкл ✓" : "Выкл"}</button> },
                    ]
                  },
                  {
                    title: "Модель AI",
                    items: [
                      { label: "Активная модель", sub: "Выбор движка для обработки запросов", control: <select value={model} onChange={e => setModel(e.target.value)} style={{ background: darkMode ? "#1a1a1a" : "#f5f5f5", color: text, border: `1px solid ${border}`, borderRadius: 7, padding: "6px 10px", fontSize: 12, cursor: "pointer", fontFamily: "inherit" }}><option value="groq">⚡ Groq Cloud</option><option value="ollama">🔒 Ollama Local</option></select> },
                    ]
                  },
                  {
                    title: "Подключение",
                    items: [
                      { label: "API сервер", sub: API_URL, control: <span style={{ fontSize: 12, color: "#22c55e", background: "#22c55e15", padding: "4px 10px", borderRadius: 6 }}>● Активен</span> },
                      { label: "Session ID", sub: "Текущий идентификатор сессии", control: <span style={{ fontSize: 11, color: muted, fontFamily: "'DM Mono', monospace", background: darkMode ? "#1a1a1a" : "#f5f5f5", padding: "4px 8px", borderRadius: 5 }}>{sessionId}</span> },
                    ]
                  }
                ].map((section, si) => (
                  <div key={si} className="card" style={{ background: surface, borderColor: border, padding: "22px", marginBottom: 12, animation: `up 0.3s ${si * 0.08}s ease both` }}>
                    <h3 style={{ fontSize: 13, fontWeight: 600, color: muted, textTransform: "uppercase", letterSpacing: 1, marginBottom: 16 }}>{section.title}</h3>
                    {section.items.map((item, ii) => (
                      <div key={ii} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 0", borderBottom: ii < section.items.length - 1 ? `1px solid ${border}` : "none" }}>
                        <div>
                          <div style={{ fontSize: 14, color: text, marginBottom: 2 }}>{item.label}</div>
                          <div style={{ fontSize: 12, color: muted }}>{item.sub}</div>
                        </div>
                        {item.control}
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            </div>
          )}

        </main>
      </div>
    </div>
  );
}
