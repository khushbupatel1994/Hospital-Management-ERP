const config = window.ERP_CONFIG || {};
const API_BASE = (config.apiBaseUrl || window.location.origin).replace(/\/+$/, "");

const state = {
  token: sessionStorage.getItem("erp_token"),
  user: JSON.parse(sessionStorage.getItem("erp_user") || "null"),
  module: "patients",
  modules: {},
};

const icons = { patients: "♙", doctors: "✚", appointments: "◷", laboratory: "⌁", pharmacy: "◈", inventory: "▦", billing: "₹" };
const labels = { patients: "Patients", doctors: "Doctors", appointments: "Appointments", laboratory: "Laboratory", pharmacy: "Pharmacy", inventory: "Inventory", billing: "Billing" };
const summaryCards = [
  ["patients", "Registered patients", "active records"],
  ["doctors", "Medical staff", "doctors in system"],
  ["appointments", "Appointments", "all appointments"],
  ["today_appointments", "Today’s schedule", "appointments today"],
];

const $ = (id) => document.getElementById(id);
const loginView = $("login-view");
const appView = $("app-view");

function setNotice(message = "") {
  const node = $("app-notice");
  node.textContent = message;
  node.classList.toggle("hidden", !message);
}

function initials(user) {
  return (user?.name || user?.username || "A").split(/\s+/).map((part) => part[0]).join("").slice(0, 2).toUpperCase();
}

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  let data = null;
  try { data = await response.json(); } catch { data = {}; }
  if (response.status === 401 && state.token) {
    logout(false);
    throw new Error("Your session expired. Please sign in again.");
  }
  if (!response.ok) throw new Error(data.detail || data.message || `Request failed (${response.status})`);
  return data;
}

function showApp() {
  loginView.classList.add("hidden");
  appView.classList.remove("hidden");
  const user = state.user || {};
  $("user-name").textContent = user.name || user.username || "Administrator";
  $("user-role").textContent = user.role || "User";
  $("user-initials").textContent = initials(user);
  $("welcome-title").textContent = `Good to see you, ${(user.name || user.username || "there").split(" ")[0]}.`;
  buildNav();
  loadDashboard();
}

function showLogin() {
  appView.classList.add("hidden");
  loginView.classList.remove("hidden");
  $("password").value = "";
  $("username").focus();
}

function logout(showMessage = true) {
  state.token = null;
  state.user = null;
  sessionStorage.removeItem("erp_token");
  sessionStorage.removeItem("erp_user");
  showLogin();
  if (showMessage) $("login-error").textContent = "You have been signed out.";
}

function buildNav() {
  const nav = $("module-nav");
  nav.innerHTML = `<button class="nav-button active" data-module="dashboard"><span class="nav-icon">⌂</span>Dashboard</button>`;
  Object.entries(state.modules).filter(([, access]) => access.read).forEach(([module]) => {
    nav.insertAdjacentHTML("beforeend", `<button class="nav-button" data-module="${module}"><span class="nav-icon">${icons[module] || "•"}</span>${labels[module] || module}</button>`);
  });
  nav.querySelectorAll(".nav-button").forEach((button) => button.addEventListener("click", () => openModule(button.dataset.module)));
}

function setActiveNav(module) {
  document.querySelectorAll(".nav-button").forEach((button) => button.classList.toggle("active", button.dataset.module === module));
}

async function loadDashboard() {
  setNotice("");
  try {
    const [summary, modules] = await Promise.all([api("/api/v1/summary"), api("/api/v1/modules")]);
    state.modules = modules.modules || {};
    buildNav();
    renderSummary(summary);
    renderQuickModules();
  } catch (error) { setNotice(error.message); }
}

function renderSummary(summary) {
  $("summary-grid").innerHTML = summaryCards.map(([key, label, foot]) => `<article class="summary-card"><div class="summary-label">${label}</div><div class="summary-value">${Number(summary[key] || 0).toLocaleString()}</div><div class="summary-foot">${foot}</div></article>`).join("");
}

function renderQuickModules() {
  const available = Object.entries(state.modules).filter(([, access]) => access.read).slice(0, 6);
  $("quick-modules").innerHTML = available.length ? available.map(([module]) => `<button class="quick-module" data-module="${module}">${icons[module] || "•"} &nbsp; ${labels[module] || module}</button>`).join("") : `<div class="muted-copy">No modules available for this role.</div>`;
  $("quick-modules").querySelectorAll("[data-module]").forEach((button) => button.addEventListener("click", () => openModule(button.dataset.module)));
}

async function openModule(module) {
  if (module === "dashboard") {
    $("dashboard-panel").classList.remove("hidden");
    $("records-panel").classList.add("hidden");
    $("page-title").textContent = "Dashboard";
    setActiveNav("dashboard");
    return;
  }
  state.module = module;
  $("dashboard-panel").classList.add("hidden");
  $("records-panel").classList.remove("hidden");
  $("page-title").textContent = labels[module] || module;
  $("records-title").textContent = labels[module] || module;
  $("records-subtitle").textContent = `Review the latest ${String(labels[module] || module).toLowerCase()} records.`;
  $("record-search").value = "";
  setActiveNav(module);
  await loadRecords();
}

async function loadRecords() {
  const loading = $("records-loading");
  const table = $("records-table");
  const empty = $("records-empty");
  loading.classList.remove("hidden");
  table.classList.add("hidden");
  empty.classList.add("hidden");
  try {
    const search = encodeURIComponent($("record-search").value.trim());
    const data = await api(`/api/v1/modules/${state.module}/records?limit=50&search=${search}`);
    renderRecords(data.items || []);
  } catch (error) { setNotice(error.message); empty.textContent = error.message; empty.classList.remove("hidden"); }
  finally { loading.classList.add("hidden"); }
}

function renderRecords(items) {
  const table = $("records-table");
  const head = table.querySelector("thead");
  const body = table.querySelector("tbody");
  if (!items.length) { table.classList.add("hidden"); $("records-empty").classList.remove("hidden"); return; }
  const fields = Object.keys(items[0]).slice(0, 8);
  head.innerHTML = `<tr>${fields.map((field) => `<th>${field.replaceAll("_", " ")}</th>`).join("")}</tr>`;
  body.innerHTML = items.map((item) => `<tr>${fields.map((field) => `<td>${escapeHtml(item[field] ?? "—")}</td>`).join("")}</tr>`).join("");
  table.classList.remove("hidden");
}

function escapeHtml(value) { return String(value).replace(/[&<>'"]/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[char])); }

async function askAI(event) {
  event.preventDefault();
  const question = $("ai-question").value.trim();
  if (!question) return;
  $("ai-answer").textContent = "Thinking…";
  try { const result = await api("/api/v1/ai/assistant", { method: "POST", body: JSON.stringify({ question }) }); $("ai-answer").textContent = result.answer || "No answer returned."; }
  catch (error) { $("ai-answer").textContent = error.message; }
}

$("login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const errorNode = $("login-error");
  errorNode.textContent = "Signing in…";
  try {
    const result = await fetch(`${API_BASE}/api/v1/auth/web-login`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ username: $("username").value.trim(), password: $("password").value }) });
    const data = await result.json();
    if (!result.ok) throw new Error(data.detail || "Unable to sign in.");
    state.token = data.access_token; state.user = data.user;
    sessionStorage.setItem("erp_token", state.token); sessionStorage.setItem("erp_user", JSON.stringify(state.user));
    errorNode.textContent = ""; showApp();
  } catch (error) { errorNode.textContent = error.message; }
});
$("logout-button").addEventListener("click", () => logout(true));
$("refresh-button").addEventListener("click", loadDashboard);
$("record-refresh").addEventListener("click", loadRecords);
$("record-search").addEventListener("keydown", (event) => { if (event.key === "Enter") loadRecords(); });
$("ai-form").addEventListener("submit", askAI);

if (state.token && state.user) showApp();
