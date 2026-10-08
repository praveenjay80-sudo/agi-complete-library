const state = {
  kind: "book",
  categoryId: null,
  query: "",
  categories: [],
  items: [],
};

const BOOK_ICON = "📘";
const PAPER_ICON = "📄";

function ls(key, fallback = "") {
  return localStorage.getItem(key) || fallback;
}

async function api(path, opts) {
  const resp = await fetch(path, opts);
  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(`${resp.status} ${text}`);
  }
  return resp.json();
}

async function loadMeta() {
  const meta = await api("/api/meta");
  document.getElementById("stat-books").textContent = `${meta.books} books`;
  document.getElementById("stat-papers").textContent = `${meta.papers} papers`;
  document.getElementById("stat-categories").textContent = `${meta.categories} categories`;
  const updEl = document.getElementById("stat-updated");
  if (meta.last_update) {
    updEl.textContent = `last update: ${meta.last_update.finished_at} (+${meta.last_update.items_added})`;
  } else {
    updEl.textContent = "never auto-updated (seed only)";
  }
}

async function loadCategories() {
  state.categories = await api(`/api/categories?kind=${state.kind}`);
  const list = document.getElementById("category-list");
  list.innerHTML = "";
  const allRow = document.createElement("div");
  allRow.className = "category-item" + (state.categoryId === null ? " active" : "");
  allRow.innerHTML = `<span>All ${state.kind === "book" ? "Books" : "Papers"}</span>`;
  allRow.onclick = () => { state.categoryId = null; refreshCategoryActive(); loadItems(); };
  list.appendChild(allRow);

  for (const c of state.categories) {
    const row = document.createElement("div");
    row.className = "category-item" + (state.categoryId === c.id ? " active" : "");
    row.dataset.catId = c.id;
    row.innerHTML = `<span>${c.name}</span><span class="count">${c.item_count}</span>`;
    row.onclick = () => { state.categoryId = c.id; refreshCategoryActive(); loadItems(); };
    list.appendChild(row);
  }
}

function refreshCategoryActive() {
  document.querySelectorAll(".category-item").forEach((el) => {
    const id = el.dataset.catId ? Number(el.dataset.catId) : null;
    el.classList.toggle("active", id === state.categoryId);
  });
}

async function loadItems() {
  const params = new URLSearchParams({ kind: state.kind });
  if (state.categoryId) params.set("category_id", state.categoryId);
  if (state.query) params.set("q", state.query);
  state.items = await api(`/api/items?${params}`);
  renderGrid();
}

function renderGrid() {
  const grid = document.getElementById("item-grid");
  grid.innerHTML = "";
  if (!state.items.length) {
    grid.innerHTML = `<p class="hint">No items found.</p>`;
    return;
  }
  for (const item of state.items) {
    const card = document.createElement("div");
    card.className = "item-card";
    const thumb = item.kind === "book" && item.cover_url
      ? `<img class="item-thumb" src="${item.cover_url}" alt="">`
      : `<div class="item-thumb">${item.kind === "book" ? BOOK_ICON : PAPER_ICON}</div>`;
    const badge = item.added_by === "llm"
      ? `<span class="badge badge-llm">auto-added</span>`
      : `<span class="badge badge-seed">curated seed</span>`;
    card.innerHTML = `
      ${thumb}
      <div class="item-info">
        ${badge}
        <h3>${escapeHtml(item.title)}</h3>
        <p class="meta">${escapeHtml(item.authors || "")} ${item.year ? "· " + item.year : ""}</p>
        <p class="sig">${escapeHtml(item.significance || "")}</p>
      </div>`;
    card.onclick = () => openDetail(item);
    grid.appendChild(card);
  }
}

function escapeHtml(s) {
  const div = document.createElement("div");
  div.textContent = s || "";
  return div.innerHTML;
}

function openDetail(item) {
  const overlay = document.getElementById("detail-overlay");
  const content = document.getElementById("detail-content");
  const thumb = item.kind === "book" && item.cover_url
    ? `<img class="detail-cover" src="${item.cover_url}" alt="">`
    : `<div class="detail-icon">${item.kind === "book" ? BOOK_ICON : PAPER_ICON}</div>`;

  let signalBits = [];
  if (item.citation_count != null) signalBits.push(`${item.citation_count} citations (OpenAlex)`);
  if (item.google_books_rating != null) signalBits.push(`${item.google_books_rating}/5 on Google Books (${item.google_books_rating_count || 0} ratings)`);
  if (item.publisher) signalBits.push(`Publisher: ${item.publisher}`);
  if (item.venue) signalBits.push(`Venue: ${item.venue}`);

  let links = [];
  if (item.source_url) {
    const label = item.source_url.includes("arxiv.org") ? "arXiv" : item.source_url.includes("doi.org") ? "DOI" : "Source";
    links.push(`<a href="${item.source_url}" target="_blank" rel="noopener">${label}</a>`);
  }
  if (item.openalex_id) links.push(`<a href="https://openalex.org/${item.openalex_id}" target="_blank" rel="noopener">OpenAlex</a>`);

  content.innerHTML = `
    ${thumb}
    <div class="detail-content">
      <h2>${escapeHtml(item.title)}</h2>
      <p class="detail-meta">${escapeHtml(item.authors || "")} ${item.year ? "· " + item.year : ""} · ${escapeHtml(item.category_name)}</p>
      <p class="detail-sig">${escapeHtml(item.significance || "")}</p>
      ${signalBits.length ? `<div class="detail-signal">${signalBits.map(escapeHtml).join("<br>")}</div>` : ""}
      ${links.length ? `<div class="detail-links">${links.join("")}</div>` : ""}
    </div>
    <div class="explain-box">
      <button id="btn-explain" class="btn btn-primary">Explain this for beginners</button>
      <div id="explain-output" class="explain-output hidden"></div>
    </div>
  `;
  document.getElementById("btn-explain").onclick = () => explainForBeginners(item);
  overlay.classList.remove("hidden");
}

async function explainForBeginners(item) {
  const key = ls("agi_anthropic_key");
  const model = ls("agi_anthropic_model");
  const output = document.getElementById("explain-output");
  if (!key || !model) {
    output.classList.remove("hidden");
    output.textContent = "Add your Anthropic API key and pick a model in Settings first.";
    return;
  }
  output.classList.remove("hidden");
  output.textContent = "Thinking...";

  const prompt = `Explain the following ${item.kind} to a complete beginner with no AI/ML background, in plain, simple language. Ground your explanation ONLY in the real information given below -- do not invent facts, dates, or claims not present here. 2-4 short paragraphs.

Title: ${item.title}
Authors: ${item.authors || "unknown"}
Year: ${item.year || "unknown"}
${item.venue ? "Venue: " + item.venue : ""}
${item.publisher ? "Publisher: " + item.publisher : ""}
What it's known for: ${item.significance || "(no summary available)"}`;

  try {
    const resp = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "anthropic-dangerous-direct-browser-access": "true",
      },
      body: JSON.stringify({
        model,
        max_tokens: 600,
        messages: [{ role: "user", content: prompt }],
      }),
    });
    if (!resp.ok) {
      const t = await resp.text();
      throw new Error(`${resp.status}: ${t}`);
    }
    const data = await resp.json();
    output.textContent = data.content[0].text.trim();
  } catch (e) {
    output.textContent = "Could not generate explanation: " + e.message;
  }
}

async function refreshModels() {
  const key = document.getElementById("key-anthropic").value.trim();
  const select = document.getElementById("model-select");
  if (!key) {
    select.innerHTML = `<option value="">Enter an Anthropic key first</option>`;
    return;
  }
  select.innerHTML = `<option value="">Loading...</option>`;
  try {
    const models = await api("/api/anthropic/models", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ api_key: key }),
    });
    if (!models.length) {
      select.innerHTML = `<option value="">No Sonnet/Opus/Haiku models found on this key</option>`;
      return;
    }
    select.innerHTML = models.map((m) => `<option value="${m.id}">${m.display_name}</option>`).join("");
    const saved = ls("agi_anthropic_model");
    if (saved && models.some((m) => m.id === saved)) select.value = saved;
  } catch (e) {
    select.innerHTML = `<option value="">Error: ${e.message}</option>`;
  }
}

function openSettings() {
  document.getElementById("key-anthropic").value = ls("agi_anthropic_key");
  document.getElementById("key-googlebooks").value = ls("agi_googlebooks_key");
  document.getElementById("key-openalex").value = ls("agi_openalex_key");
  document.getElementById("settings-saved").classList.add("hidden");
  document.getElementById("covers-status").classList.add("hidden");
  const select = document.getElementById("model-select");
  const savedModel = ls("agi_anthropic_model");
  select.innerHTML = savedModel ? `<option value="${savedModel}">${savedModel}</option>` : `<option value="">Enter Anthropic key, then click Refresh models</option>`;
  document.getElementById("settings-overlay").classList.remove("hidden");
}

function saveSettings() {
  localStorage.setItem("agi_anthropic_key", document.getElementById("key-anthropic").value.trim());
  localStorage.setItem("agi_anthropic_model", document.getElementById("model-select").value);
  localStorage.setItem("agi_googlebooks_key", document.getElementById("key-googlebooks").value.trim());
  localStorage.setItem("agi_openalex_key", document.getElementById("key-openalex").value.trim());
  const saved = document.getElementById("settings-saved");
  saved.classList.remove("hidden");
}

async function fetchMissingCovers() {
  const key = document.getElementById("key-googlebooks").value.trim();
  const status = document.getElementById("covers-status");
  if (!key) {
    status.classList.remove("hidden");
    status.textContent = "Enter a Google Books API key above first.";
    return;
  }
  status.classList.remove("hidden");
  status.textContent = "Fetching covers...";
  try {
    const result = await api("/api/backfill_covers", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ google_books_key: key }),
    });
    status.textContent = `Checked ${result.checked} books, added ${result.covers_added} covers (${result.no_cover_found} had no match on Google Books).`;
    await loadItems();
  } catch (e) {
    status.textContent = "Failed: " + e.message;
  }
}

async function triggerUpdate() {
  const key = ls("agi_anthropic_key");
  const model = ls("agi_anthropic_model");
  const gbKey = ls("agi_googlebooks_key");
  const oaKey = ls("agi_openalex_key");
  const banner = document.getElementById("run-banner");
  if (!key || !model) {
    openSettings();
    return;
  }
  const btn = document.getElementById("btn-update");
  btn.disabled = true;
  btn.textContent = "Updating...";
  banner.classList.remove("hidden", "error");
  banner.textContent = "Running update: discovering new papers and books, verifying signals, and judging candidates with your selected model. This can take a minute...";

  try {
    const result = await api("/api/update", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ anthropic_key: key, anthropic_model: model, google_books_key: gbKey || null, openalex_key: oaKey || null }),
    });
    banner.textContent = `Update complete: saw ${result.candidates_seen} candidates, added ${result.items_added} items, created ${result.categories_created} new categories.`;
    await loadMeta();
    await loadCategories();
    await loadItems();
  } catch (e) {
    banner.classList.add("error");
    banner.textContent = "Update failed: " + e.message;
  } finally {
    btn.disabled = false;
    btn.textContent = "Update Now";
  }
}

async function openAudit() {
  const list = document.getElementById("audit-list");
  list.innerHTML = "Loading...";
  const rows = await api("/api/audit_log?limit=150");
  list.innerHTML = rows.map((r) => `
    <div class="audit-row">
      <span class="audit-action ${r.action}">${r.action}</span>
      <strong>${escapeHtml(r.item_title || r.reason || "")}</strong><br>
      ${r.objective_signal ? `<em>${escapeHtml(r.objective_signal)}</em><br>` : ""}
      ${r.llm_reasoning ? escapeHtml(r.llm_reasoning) : ""}
      <div class="hint">${r.created_at} · source: ${r.source || "n/a"}</div>
    </div>
  `).join("") || `<p class="hint">No audit entries yet.</p>`;
  document.getElementById("audit-overlay").classList.remove("hidden");
}

function wireEvents() {
  document.querySelectorAll(".kind-btn").forEach((btn) => {
    btn.onclick = () => {
      document.querySelectorAll(".kind-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      state.kind = btn.dataset.kind;
      state.categoryId = null;
      loadCategories();
      loadItems();
    };
  });

  let searchTimer;
  document.getElementById("search").oninput = (e) => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      state.query = e.target.value.trim();
      loadItems();
    }, 250);
  };

  document.getElementById("btn-update").onclick = triggerUpdate;
  document.getElementById("btn-settings").onclick = openSettings;
  document.getElementById("settings-close").onclick = () => document.getElementById("settings-overlay").classList.add("hidden");
  document.getElementById("btn-save-settings").onclick = saveSettings;
  document.getElementById("btn-refresh-models").onclick = refreshModels;
  document.getElementById("btn-fetch-covers").onclick = fetchMissingCovers;

  document.getElementById("btn-audit").onclick = openAudit;
  document.getElementById("audit-close").onclick = () => document.getElementById("audit-overlay").classList.add("hidden");

  document.getElementById("detail-close").onclick = () => document.getElementById("detail-overlay").classList.add("hidden");
  document.getElementById("detail-overlay").onclick = (e) => {
    if (e.target.id === "detail-overlay") e.target.classList.add("hidden");
  };
  document.getElementById("settings-overlay").onclick = (e) => {
    if (e.target.id === "settings-overlay") e.target.classList.add("hidden");
  };
  document.getElementById("audit-overlay").onclick = (e) => {
    if (e.target.id === "audit-overlay") e.target.classList.add("hidden");
  };
}

async function init() {
  wireEvents();
  await loadMeta();
  await loadCategories();
  await loadItems();
}

init();
