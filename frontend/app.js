const API_URL = "http://127.0.0.1:8000/api/query"; // FastAPI later

const el = (id) => document.getElementById(id);

const questionEl = el("question");
const runBtn = el("runBtn");
const clearBtn = el("clearBtn");
const mockToggle = el("mockToggle");
const statusEl = el("status");

const outputEl = el("output");
const sqlBlockEl = el("sqlBlock");
const resultsTableEl = el("resultsTable");
const explanationEl = el("explanation");
const rowCountEl = el("rowCount");
const copySqlBtn = el("copySqlBtn");

function setStatus(message, kind = "") {
  statusEl.className = `status ${kind}`.trim();
  statusEl.textContent = message;
}

function setLoading(isLoading) {
  runBtn.disabled = isLoading;
  runBtn.textContent = isLoading ? "Running..." : "Run";
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderTable(columns, rows) {
  let html = "<thead><tr>";
  for (const c of columns) html += `<th>${escapeHtml(c)}</th>`;
  html += "</tr></thead><tbody>";

  for (const row of rows) {
    html += "<tr>";
    for (const cell of row) html += `<td>${escapeHtml(cell)}</td>`;
    html += "</tr>";
  }
  html += "</tbody>";
  resultsTableEl.innerHTML = html;
}

function showOutput({ sql, columns, rows, explanation }) {
  sqlBlockEl.textContent = sql || "";
  explanationEl.textContent = explanation || "";
  rowCountEl.textContent = `${rows?.length ?? 0} row(s)`;

  renderTable(columns || [], rows || []);
  outputEl.classList.remove("hidden");
}

function mockResponse(question) {
  // A few deterministic mock examples (helps demo UI before backend exists)
  const q = question.toLowerCase();

  if (q.includes("top") && (q.includes("customer") || q.includes("customers"))) {
    return {
      sql:
`SELECT c.full_name AS customer, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_spent
FROM customers c
JOIN orders o ON o.customer_id = c.id
JOIN order_items oi ON oi.order_id = o.id
WHERE o.status IN ('paid','shipped','delivered')
GROUP BY c.id
ORDER BY total_spent DESC
LIMIT 5;`,
      columns: ["customer", "total_spent"],
      rows: [
        ["Maria Petrova", 2412.50],
        ["Ivan Ivanov", 2199.10],
        ["Elena Dimitrova", 1988.00],
        ["Georgi Nikolov", 1875.45],
        ["Alex Stoyanov", 1750.30],
      ],
      explanation:
        "This query joins customers, orders, and order items, then sums spending per customer for completed orders. It sorts customers by total spent and returns the top 5."
    };
  }

  if (q.includes("late") || q.includes("delayed")) {
    return {
      sql:
`SELECT COUNT(*) AS late_deliveries
FROM shipments
WHERE delivered_at IS NOT NULL
  AND (julianday(delivered_at) - julianday(shipped_at)) > promised_days;`,
      columns: ["late_deliveries"],
      rows: [[42]],
      explanation:
        "This query counts delivered shipments where the actual delivery time exceeds the promised number of days."
    };
  }

  return {
    sql:
`SELECT p.category, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM order_items oi
JOIN products p ON p.id = oi.product_id
GROUP BY p.category
ORDER BY revenue DESC
LIMIT 10;`,
    columns: ["category", "revenue"],
    rows: [
      ["Electronics", 15230.80],
      ["Home", 11210.55],
      ["Sports", 8944.10],
      ["Beauty", 7210.20],
      ["Books", 6330.00],
    ],
    explanation:
      "This query aggregates revenue by product category by summing quantity × unit price across all order items, then returns the top categories by revenue."
  };
}

async function callBackend(question) {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Backend error (${res.status}): ${text || res.statusText}`);
  }

  return await res.json();
}

async function onRun() {
  const question = questionEl.value.trim();
  if (!question) {
    setStatus("Please enter a question first.", "warn");
    outputEl.classList.add("hidden");
    return;
  }

  setStatus("", "");
  setLoading(true);

  try {
    let payload;
    if (mockToggle.checked) {
      payload = mockResponse(question);
      setStatus("Mock mode is ON — showing sample output (backend not required).", "good");
    } else {
      payload = await callBackend(question);
      setStatus("Query executed successfully.", "good");
    }
    showOutput(payload);
  } catch (err) {
    console.error(err);
    outputEl.classList.add("hidden");
    setStatus(err.message || "Something went wrong.", "bad");
  } finally {
    setLoading(false);
  }
}

function onClear() {
  questionEl.value = "";
  outputEl.classList.add("hidden");
  setStatus("", "");
  questionEl.focus();
}

async function onCopySql() {
  const sql = sqlBlockEl.textContent || "";
  if (!sql) return;
  try {
    await navigator.clipboard.writeText(sql);
    setStatus("SQL copied to clipboard.", "good");
    setTimeout(() => setStatus("", ""), 1200);
  } catch {
    setStatus("Could not copy SQL (browser permission).", "warn");
  }
}

runBtn.addEventListener("click", onRun);
clearBtn.addEventListener("click", onClear);
copySqlBtn.addEventListener("click", onCopySql);

questionEl.addEventListener("keydown", (e) => {
  // Ctrl/Cmd + Enter to run
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") onRun();
});

// Default welcome state
setStatus("Mock mode is ON. Turn it OFF after the backend is running.", "warn");
