import { get } from "./api.js";
import { requireAuth } from "./auth.js";

const dateFromInput = document.querySelector("[data-report-date-from]");
const dateToInput = document.querySelector("[data-report-date-to]");
const runButton = document.querySelector("[data-report-run]");
const snapshotList = document.querySelector("[data-report-snapshot]");
const salesBody = document.querySelector("[data-report-sales-body]");
const productionsBody = document.querySelector("[data-report-productions-body]");
const inventoryBody = document.querySelector("[data-report-inventory-body]");

function formatCurrency(value) {
  return new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  }).format(value);
}

function querySuffix() {
  const params = new URLSearchParams();
  if (dateFromInput?.value) {
    params.set("date_from", dateFromInput.value);
  }
  if (dateToInput?.value) {
    params.set("date_to", dateToInput.value);
  }
  const query = params.toString();
  return query ? `?${query}` : "";
}

function renderRows(target, rows, emptyCols, mapper) {
  if (!target) {
    return;
  }
  if (!rows.length) {
    target.innerHTML = `<tr><td colspan="${emptyCols}" class="empty-state">Sin resultados.</td></tr>`;
    return;
  }
  target.innerHTML = rows.map(mapper).join("");
}

async function loadReports() {
  const suffix = querySuffix();
  const [summary, sales, productions, inventory] = await Promise.all([
    get("/dashboard/summary"),
    get(`/reports/sales${suffix}`),
    get(`/reports/productions${suffix}`),
    get("/reports/inventory"),
  ]);

  snapshotList.innerHTML = `
    <div class="mini-item"><span>Ventas del dia</span><strong>${formatCurrency(summary.sales_today)}</strong></div>
    <div class="mini-item"><span>Ventas del mes</span><strong>${formatCurrency(summary.sales_month)}</strong></div>
    <div class="mini-item"><span>Produccion hoy</span><strong>${summary.productions_today}</strong></div>
    <div class="mini-item"><span>Stock bajo</span><strong>${summary.low_stock_products}</strong></div>
  `;

  renderRows(
    salesBody,
    sales,
    4,
    (item) => `
      <tr>
        <td>${item.sale_date}</td>
        <td>${item.sale_time}</td>
        <td>${formatCurrency(item.total)}</td>
        <td>${item.sales_channel}</td>
      </tr>
    `,
  );

  renderRows(
    productionsBody,
    productions,
    4,
    (item) => `
      <tr>
        <td>${item.production_date}</td>
        <td>${item.product_id}</td>
        <td>${item.quantity_produced}</td>
        <td>${item.batch}</td>
      </tr>
    `,
  );

  renderRows(
    inventoryBody,
    inventory,
    5,
    (item) => `
      <tr>
        <td>${new Date(item.movement_date).toLocaleString("es-CO")}</td>
        <td>${item.movement_type}</td>
        <td>${item.quantity}</td>
        <td>${item.reason || "Sin motivo"}</td>
        <td>${item.user_id}</td>
      </tr>
    `,
  );
}

async function initReportsPage() {
  await requireAuth();
  await loadReports();
  runButton?.addEventListener("click", loadReports);
}

initReportsPage().catch(() => {
  if (snapshotList) {
    snapshotList.innerHTML =
      '<div class="mini-item"><span>Error</span><strong>No fue posible cargar reportes.</strong></div>';
  }
});
