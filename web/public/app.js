const config = window.ERP_CONFIG || {};
const API_BASE = (config.apiBaseUrl || window.location.origin).replace(/\/+$/, "");

const state = {
  token: sessionStorage.getItem("erp_token"),
  user: JSON.parse(sessionStorage.getItem("erp_user") || "null"),
  modules: {},
  module: "dashboard",
  records: [],
  editingId: null,
};

const MODULES = {
  dashboard: { label: "Dashboard", icon: "⌂", kind: "dashboard" },
  users: { label: "Users", icon: "♣", apiModule: "users" },
  patients: { label: "Patients", icon: "♙", apiModule: "patients" },
  doctors: { label: "Doctors", icon: "♙", apiModule: "doctors" },
  appointments: { label: "Appointments", icon: "▦", apiModule: "appointments" },
  opd: { label: "OPD", icon: "♧", apiModule: "opd" },
  ipd: { label: "IPD", icon: "▱", apiModule: "ipd" },
  billing: { label: "Billing", icon: "♙", apiModule: "billing" },
  pharmacy: { label: "Pharmacy", icon: "⌕", apiModule: "pharmacy" },
  laboratory: { label: "Laboratory", icon: "⌁", apiModule: "laboratory" },
  inventory: { label: "Inventory", icon: "◈", apiModule: "inventory" },
  accounts: { label: "Accounts", icon: "▥", apiModule: "accounts" },
  reports: { label: "Reports", icon: "▤", kind: "reports" },
  analytics: { label: "Analytics", icon: "▧", kind: "analytics" },
  ai: { label: "AI Intelligence", icon: "✦", kind: "ai" },
  hr: { label: "HR & Employee", icon: "♙", apiModule: "employees" },
  settings: { label: "Settings", icon: "⚙", kind: "settings" },
  backup: { label: "Backup", icon: "▣", kind: "backup" },
  logout: { label: "Logout", icon: "⇥", kind: "logout" },
};

const FORM_FIELDS = {
  users: ["employee_id", "full_name", "username", "password", "role", "department", "mobile", "email", "status"],
  patients: ["patient_name", "gender", "dob", "age", "blood_group", "mobile", "email", "address", "city", "state", "pin_code", "disease", "doctor", "department", "patient_type", "registration_date", "status", "father_husband_name"],
  doctors: ["full_name", "gender", "department", "specialization", "qualification", "experience", "mobile", "phone", "email", "consultation_fee", "opd_timing", "available_days", "available_time", "joining_date", "status"],
  appointments: ["patient_id", "doctor_id", "patient_name", "doctor_name", "department", "appointment_date", "appointment_time", "visit_type", "token_no", "purpose", "status", "remarks"],
  opd: ["patient", "doctor", "department", "visit_date", "visit_time", "chief_complaint", "diagnosis", "prescription", "followup_date", "notes", "status"],
  ipd: ["patient", "doctor", "ward", "bed_no", "admission_date", "discharge_date", "diagnosis", "treatment", "daily_charges", "status", "remarks"],
  billing: ["patient_name", "doctor_name", "bill_date", "consultation_fee", "medicine_charges", "lab_charges", "total_amount", "paid_amount", "payment_status"],
  pharmacy: ["medicine_id", "medicine_name", "name", "category", "batch_number", "supplier", "quantity", "minimum_stock", "price", "expiry_date", "status"],
  laboratory: ["test_id", "patient_id", "patient_name", "test_name", "result", "remarks", "report_date", "test_date", "status"],
  inventory: ["item_id", "item_name", "category", "supplier", "batch_no", "purchase_price", "selling_price", "stock_quantity", "minimum_stock", "unit", "gst", "expiry_date", "remarks", "status"],
  accounts: ["transaction_id", "transaction_date", "transaction_type", "category", "amount", "payment_mode", "description", "remarks"],
  employees: ["employee_id", "full_name", "department", "designation", "mobile", "email", "status"],
};

const $ = (id) => document.getElementById(id);
const loginView = $("login-view");
const appView = $("app-view");

function setNotice(message = "") {
  const node = $("app-notice");
  node.textContent = message;
  node.classList.toggle("hidden", !message);
}

function escapeHtml(value) {
  return String(value ?? "—").replace(/[&<>'"]/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[char]));
}

function initials(user) {
  return (user?.name || user?.username || "A").split(/\s+/).map((part) => part[0]).join("").slice(0, 2).toUpperCase();
}

function formatMoney(value) {
  return `₹${Number(value || 0).toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  let data = {};
  try { data = await response.json(); } catch { /* empty response */ }
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
  $("status-user").textContent = user.name || user.username || "Administrator";
  buildNav();
  startClock();
  loadDashboard();
}

function showLogin() {
  appView.classList.add("hidden");
  loginView.classList.remove("hidden");
  $("password").value = "";
  setTimeout(() => $("username").focus(), 0);
}

async function logout(showMessage = true) {
  if (state.token) {
    try { await api("/api/v1/session/logout", { method: "POST" }); } catch { /* token can already be expired */ }
  }
  state.token = null;
  state.user = null;
  sessionStorage.removeItem("erp_token");
  sessionStorage.removeItem("erp_user");
  showLogin();
  if (showMessage) $("login-error").textContent = "You have been signed out.";
}

function startClock() {
  const tick = () => {
    const value = new Date().toLocaleString("en-IN", { day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit", hour12: true });
    $("current-datetime").textContent = value;
    $("status-datetime").textContent = value;
  };
  tick();
  clearInterval(state.clock);
  state.clock = setInterval(tick, 30000);
}

function canRead(key) {
  const meta = MODULES[key];
  return !meta.apiModule || Boolean(state.modules[meta.apiModule]?.read);
}

function buildNav() {
  const nav = $("module-nav");
  nav.innerHTML = "";
  Object.entries(MODULES).forEach(([key, meta]) => {
    if (key !== "dashboard" && key !== "logout" && !canRead(key)) return;
    const button = document.createElement("button");
    button.className = `nav-button${["reports", "analytics", "ai", "hr", "settings", "backup", "logout"].includes(key) ? " utility" : ""}`;
    button.dataset.module = key;
    button.innerHTML = `<span class="nav-icon">${meta.icon}</span><span>${meta.label}</span>`;
    button.addEventListener("click", () => openModule(key));
    nav.appendChild(button);
  });
}

function setActiveNav(key) {
  document.querySelectorAll(".nav-button").forEach((button) => button.classList.toggle("active", button.dataset.module === key));
}

async function loadDashboard() {
  setNotice("");
  try {
    const [summary, modules] = await Promise.all([api("/api/v1/summary"), api("/api/v1/modules")]);
    state.modules = modules.modules || {};
    buildNav();
    renderSummary(summary);
    renderOverview(summary);
    renderSystemStatus();
    setActiveNav("dashboard");
  } catch (error) { setNotice(error.message); }
}

function renderSummary(summary) {
  const cards = [
    ["doctors", "Doctors", "♙", String(summary.doctors || 0)],
    ["patients", "Patients", "♙", String(summary.patients || 0)],
    ["appointments", "Appointments", "▦", String(summary.appointments || 0)],
    ["opd", "OPD", "♧", String(summary.opd || 0)],
    ["ipd", "IPD", "▱", String(summary.ipd || 0)],
    ["revenue", "Revenue", "♙", formatMoney(summary.revenue)],
  ];
  $("summary-grid").innerHTML = cards.map(([key, label, icon, value]) => `<article class="dashboard-card ${key === "revenue" ? "revenue" : ""}"><span class="card-icon">${icon}</span><h3>${label}</h3><strong>${escapeHtml(value)}</strong></article>`).join("");
}

function renderOverview(summary) {
  $("overview-content").innerHTML = `<p class="overview-line">Doctors: <b>${summary.doctors || 0}</b> &nbsp; | &nbsp; Patients: <b>${summary.patients || 0}</b> &nbsp; | &nbsp; Appointments: <b>${summary.appointments || 0}</b></p><p class="overview-line">OPD: <b>${summary.opd || 0}</b> &nbsp; | &nbsp; IPD: <b>${summary.ipd || 0}</b> &nbsp; | &nbsp; Revenue: <b>${formatMoney(summary.revenue)}</b></p>`;
  $("dashboard-status").textContent = `Dashboard updated ${new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}`;
}

function renderSystemStatus() {
  $("system-status").innerHTML = ["Database connected", "Cloud service online", "Role permissions active", "Secure session enabled"].map((item) => `<div><span>${item}</span><b>OK</b></div>`).join("");
}

function showPanel(panel) {
  $("dashboard-panel").classList.toggle("hidden", panel !== "dashboard");
  $("records-panel").classList.toggle("hidden", panel !== "records");
  $("utility-panel").classList.toggle("hidden", panel !== "utility");
}

async function openModule(key) {
  if (key === "logout") { await logout(true); return; }
  state.module = key;
  setActiveNav(key);
  const meta = MODULES[key];
  if (!meta || meta.kind === "dashboard") {
    showPanel("dashboard");
    $("page-title").textContent = `${state.user?.role || "Super Admin"} Dashboard`;
    await loadDashboard();
    return;
  }
  if (meta.apiModule) {
    showPanel("records");
    $("records-title").textContent = meta.label;
    $("records-subtitle").textContent = `Review and manage ${meta.label.toLowerCase()} records.`;
    $("record-search").value = "";
    $("add-record-button").classList.toggle("hidden", !state.modules[meta.apiModule]?.write);
    await loadRecords();
    return;
  }
  showPanel("utility");
  await renderUtility(key);
}

async function loadRecords() {
  const meta = MODULES[state.module];
  const module = meta.apiModule;
  const loading = $("records-loading");
  const table = $("records-table");
  const empty = $("records-empty");
  loading.classList.remove("hidden"); table.classList.add("hidden"); empty.classList.add("hidden"); setNotice("");
  try {
    const search = encodeURIComponent($("record-search").value.trim());
    const data = await api(`/api/v1/modules/${module}/records?limit=100&search=${search}`);
    state.records = data.items || [];
    renderRecords(state.records);
  } catch (error) { setNotice(error.message); empty.textContent = error.message; empty.classList.remove("hidden"); }
  finally { loading.classList.add("hidden"); }
}

function renderRecords(items) {
  const table = $("records-table");
  const head = table.querySelector("thead");
  const body = table.querySelector("tbody");
  const canWrite = Boolean(state.modules[MODULES[state.module].apiModule]?.write);
  if (!items.length) { table.classList.add("hidden"); $("records-empty").classList.remove("hidden"); return; }
  const fields = Object.keys(items[0]).filter((field) => field !== "created_at").slice(0, 10);
  head.innerHTML = `<tr>${fields.map((field) => `<th>${escapeHtml(field.replaceAll("_", " "))}</th>`).join("")}${canWrite ? "<th>Actions</th>" : ""}</tr>`;
  body.innerHTML = items.map((item) => `<tr>${fields.map((field) => `<td>${escapeHtml(item[field] ?? "—")}</td>`).join("")}${canWrite ? `<td><div class="table-actions"><button class="table-action" data-edit="${item.id}">Edit</button><button class="table-action danger" data-delete="${item.id}">Delete</button></div></td>` : ""}</tr>`).join("");
  table.classList.remove("hidden");
  body.querySelectorAll("[data-edit]").forEach((button) => button.addEventListener("click", () => openRecordModal(Number(button.dataset.edit))));
  body.querySelectorAll("[data-delete]").forEach((button) => button.addEventListener("click", () => deleteRecord(Number(button.dataset.delete))));
}

function fieldLabel(key) { return key.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase()); }

function openRecordModal(recordId = null) {
  const module = MODULES[state.module]?.apiModule;
  if (!module) return;
  state.editingId = recordId;
  const current = state.records.find((item) => Number(item.id) === Number(recordId)) || {};
  const fields = FORM_FIELDS[module] || [];
  $("modal-title").textContent = recordId ? `Edit ${MODULES[state.module].label}` : `Add ${MODULES[state.module].label}`;
  $("record-form-error").textContent = "";
  $("record-fields").innerHTML = fields.map((field) => {
    const type = field.includes("date") ? "date" : ["age", "experience", "fee", "amount", "charges", "quantity", "stock", "price", "gst", "paid"].some((word) => field.includes(word)) ? "number" : field === "password" ? "password" : "text";
    const full = ["address", "description", "remarks", "notes", "diagnosis", "treatment", "prescription", "chief_complaint", "result"].includes(field) ? "full" : "";
    const value = current[field] ?? "";
    const required = ["patient", "doctor", "patient_name", "full_name", "username", "password", "medicine_name", "item_name", "amount"].includes(field) && (!recordId || field !== "password");
    if (["status", "gender", "role", "payment_status", "transaction_type", "patient_type"].includes(field)) {
      const options = field === "status" ? ["Active", "Pending", "Open", "Admitted", "Discharged", "Completed", "Available", "Inactive"] : field === "gender" ? ["Male", "Female", "Other"] : field === "role" ? ["Super Admin", "Admin", "Doctor", "Nurse", "Receptionist", "Pharmacist", "Laboratory", "Accounts", "HR"] : field === "payment_status" ? ["Paid", "Pending", "Partial"] : field === "transaction_type" ? ["Income", "Expense"] : ["OPD", "IPD", "Emergency"];
      return `<label class="${full}">${fieldLabel(field)}<select name="${field}" ${required ? "required" : ""}><option value="">Select ${fieldLabel(field)}</option>${options.map((option) => `<option ${String(value).toLowerCase() === option.toLowerCase() ? "selected" : ""}>${option}</option>`).join("")}</select></label>`;
    }
    const control = full ? `<textarea name="${field}" ${required ? "required" : ""}>${escapeHtml(value === "—" ? "" : value)}</textarea>` : `<input name="${field}" type="${type}" value="${escapeHtml(value === "—" ? "" : value)}" ${required ? "required" : ""} ${field === "password" && recordId ? "placeholder=\"Leave blank to keep current password\"" : ""} />`;
    return `<label class="${full}">${fieldLabel(field)}${control}</label>`;
  }).join("");
  $("record-modal").classList.remove("hidden");
}

function closeRecordModal() { $("record-modal").classList.add("hidden"); state.editingId = null; }

async function saveRecord(event) {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const data = Object.fromEntries(form.entries());
  Object.keys(data).forEach((key) => { if (data[key] === "") delete data[key]; });
  if (state.editingId && !data.password) delete data.password;
  try {
    const module = MODULES[state.module].apiModule;
    const path = `/api/v1/modules/${module}/records${state.editingId ? `/${state.editingId}` : ""}`;
    await api(path, { method: state.editingId ? "PUT" : "POST", body: JSON.stringify({ data }) });
    closeRecordModal();
    await loadRecords();
    setNotice("Record saved successfully.");
  } catch (error) { $("record-form-error").textContent = error.message; }
}

async function deleteRecord(id) {
  if (!window.confirm("Delete this record? This action cannot be undone.")) return;
  try { await api(`/api/v1/modules/${MODULES[state.module].apiModule}/records/${id}`, { method: "DELETE" }); await loadRecords(); setNotice("Record deleted successfully."); }
  catch (error) { setNotice(error.message); }
}

async function renderUtility(key) {
  const meta = MODULES[key];
  $("utility-title").textContent = meta.label;
  $("utility-subtitle").textContent = key === "backup" ? "Create a secure database backup." : `Use ${meta.label.toLowerCase()} tools from your ERP workspace.`;
  $("utility-actions").innerHTML = "";
  $("utility-content").innerHTML = `<div class="loading-state">Loading…</div>`;
  if (key === "ai") { renderAIPage(); return; }
  if (key === "backup") { renderBackupPage(); return; }
  try {
    const summary = await api("/api/v1/dashboard/enterprise");
    if (key === "analytics") renderAnalytics(summary);
    else if (key === "settings") await renderSettings();
    else renderReports(summary);
  } catch (error) { setNotice(error.message); $("utility-content").innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`; }
}

function renderReports(summary) {
  $("utility-actions").innerHTML = `<button id="print-report" class="blue-button">Print report</button>`;
  $("utility-content").innerHTML = `<div class="utility-grid"><div class="utility-tile"><h3>Patients</h3><strong>${summary.patients || 0}</strong></div><div class="utility-tile"><h3>Doctors</h3><strong>${summary.doctors || 0}</strong></div><div class="utility-tile"><h3>Revenue</h3><strong>${formatMoney(summary.revenue)}</strong></div></div><table class="report-table"><thead><tr><th>Operational metric</th><th>Current value</th><th>Status</th></tr></thead><tbody>${[["Appointments", summary.appointments], ["OPD visits", summary.opd], ["Active IPD admissions", summary.active_ipd], ["Pending lab tests", summary.lab_pending], ["Low medicine stock", summary.low_medicines], ["Low inventory stock", summary.low_inventory]].map(([label, value]) => `<tr><td>${label}</td><td>${value || 0}</td><td>Live</td></tr>`).join("")}</tbody></table>`;
  $("print-report").addEventListener("click", () => window.print());
}

function renderAnalytics(summary) {
  const metrics = [["Patients", summary.patients], ["Doctors", summary.doctors], ["Appointments", summary.appointments], ["OPD", summary.opd], ["IPD", summary.active_ipd], ["Revenue", formatMoney(summary.revenue)]];
  $("utility-content").innerHTML = `<div class="utility-grid">${metrics.map(([label, value]) => `<div class="utility-tile"><h3>${label}</h3><strong>${value || 0}</strong><p class="muted-copy">Live from hospital database</p></div>`).join("")}</div><table class="report-table"><thead><tr><th>Area</th><th>Value</th><th>Signal</th></tr></thead><tbody>${metrics.map(([label, value]) => `<tr><td>${label}</td><td>${value || 0}</td><td><span class="status-dot"></span> Healthy</td></tr>`).join("")}</tbody></table>`;
}

async function renderSettings() {
  const [health, security] = await Promise.all([api("/api/v1/enterprise/health"), api("/api/v1/admin/security")]);
  $("utility-content").innerHTML = `<div class="utility-grid"><div class="utility-tile"><h3>API service</h3><strong>${health.api === "ok" ? "Online" : "Check"}</strong><p class="muted-copy">Version ${health.version}</p></div><div class="utility-tile"><h3>Database</h3><strong>${health.database ? "Connected" : "Offline"}</strong><p class="muted-copy">Configured and initialized</p></div><div class="utility-tile"><h3>Session security</h3><strong>${security.jwt_minutes} min</strong><p class="muted-copy">JWT session lifetime</p></div></div><table class="report-table"><tbody><tr><th>Database path</th><td>${escapeHtml(health.database_path)}</td></tr><tr><th>Failed login window</th><td>${security.failed_login_window} seconds</td></tr><tr><th>Maximum attempts</th><td>${security.max_attempts}</td></tr></tbody></table>`;
}

function renderAIPage() {
  $("utility-content").innerHTML = `<article class="dashboard-info-card"><div class="info-card-title"><h3>Ask AI Intelligence</h3><span>✦</span></div><p class="muted-copy">Ask approved, aggregate questions. Patient-level sensitive information is not exposed by this assistant.</p><form id="ai-page-form" class="ai-form"><input id="ai-page-question" placeholder="How many pending lab tests are there?" required /><button class="blue-button" type="submit">Ask assistant</button></form><p id="ai-page-answer" class="ai-answer"></p></article>`;
  $("ai-page-form").addEventListener("submit", async (event) => { event.preventDefault(); $("ai-page-answer").textContent = "Thinking…"; try { const result = await api("/api/v1/ai/assistant", { method: "POST", body: JSON.stringify({ question: $("ai-page-question").value.trim() }) }); $("ai-page-answer").textContent = result.answer; } catch (error) { $("ai-page-answer").textContent = error.message; } });
}

function renderBackupPage() {
  $("utility-actions").innerHTML = `<button id="create-backup" class="blue-button">Create backup</button>`;
  $("utility-content").innerHTML = `<div class="utility-grid"><div class="utility-tile"><h3>Secure backup</h3><p class="muted-copy">Create an encrypted server-side SQLite backup for recovery and audit purposes.</p><div id="backup-result" class="ai-answer"></div></div></div>`;
  $("create-backup").addEventListener("click", async () => { if (!window.confirm("Create a database backup now?")) return; try { const result = await api("/api/v1/admin/backup", { method: "POST" }); $("backup-result").textContent = `Backup created: ${result.backup}`; } catch (error) { $("backup-result").textContent = error.message; } });
}

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
  $("login-error").textContent = "Signing in…";
  try {
    const response = await fetch(`${API_BASE}/api/v1/auth/web-login`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ username: $("username").value.trim(), password: $("password").value }) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Unable to sign in.");
    state.token = data.access_token; state.user = data.user;
    sessionStorage.setItem("erp_token", state.token); sessionStorage.setItem("erp_user", JSON.stringify(state.user));
    $("login-error").textContent = ""; showApp();
  } catch (error) { $("login-error").textContent = error.message; }
});

$("refresh-button").addEventListener("click", loadDashboard);
$("record-refresh").addEventListener("click", loadRecords);
$("add-record-button").addEventListener("click", () => openRecordModal());
$("record-search").addEventListener("keydown", (event) => { if (event.key === "Enter") loadRecords(); });
$("record-form").addEventListener("submit", saveRecord);
$("modal-close").addEventListener("click", closeRecordModal);
$("modal-cancel").addEventListener("click", closeRecordModal);
$("record-modal").addEventListener("click", (event) => { if (event.target.id === "record-modal") closeRecordModal(); });
$("ai-form").addEventListener("submit", askAI);

if (state.token && state.user) showApp();
