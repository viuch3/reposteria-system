import { get } from "./api.js";
import { requireAuth } from "./auth.js";

const salesToday = document.querySelector("[data-kpi-sales-today]");
const salesMonth = document.querySelector("[data-kpi-sales-month]");
const productionsToday = document.querySelector("[data-kpi-productions]");
const averageTicket = document.querySelector("[data-kpi-average-ticket]");
const lowStockBadge = document.querySelector("[data-kpi-low-stock]");
const salesOverview = document.querySelector("[data-sales-overview]");
const lowStockList = document.querySelector("[data-low-stock-list]");
const recentSales = document.querySelector("[data-recent-sales]");
const topProducts = document.querySelector("[data-top-products]");

function formatCurrency(value) {
  return new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  }).format(value);
}

function renderMiniList(target, items, formatter, emptyText = "Sin datos") {
  if (!target) {
    return;
  }

  if (!items.length) {
    target.innerHTML = `<div class="mini-item"><span>${emptyText}</span><strong>--</strong></div>`;
    return;
  }

  target.innerHTML = items.map(formatter).join("");
}

async function initDashboard() {
  await requireAuth();

  const [summary, overview, lowStock, recent, top] = await Promise.all([
    get("/dashboard/summary"),
    get("/dashboard/sales-overview"),
    get("/dashboard/low-stock"),
    get("/dashboard/recent-sales"),
    get("/dashboard/top-products"),
  ]);

  salesToday.textContent = formatCurrency(summary.sales_today);
  salesMonth.textContent = formatCurrency(summary.sales_month);
  productionsToday.textContent = summary.productions_today;
  averageTicket.textContent = formatCurrency(summary.average_ticket);
  lowStockBadge.textContent = `${summary.low_stock_products} alertas`;

  renderMiniList(
    salesOverview,
    overview,
    (item) =>
      `<div class="mini-item"><span>${item.date}</span><strong>${formatCurrency(item.total)}</strong></div>`,
    "Sin ventas registradas",
  );

  renderMiniList(
    lowStockList,
    lowStock,
    (item) =>
      `<div class="mini-item"><span>${item.name}</span><strong>${item.current_stock} ${item.unit_of_measure}</strong></div>`,
    "Sin alertas de stock",
  );

  renderMiniList(
    recentSales,
    recent,
    (item) =>
      `<div class="mini-item"><span>${item.sale_date} ${item.sale_time}</span><strong>${formatCurrency(item.total)}</strong></div>`,
    "Sin ventas recientes",
  );

  renderMiniList(
    topProducts,
    top,
    (item) =>
      `<div class="mini-item"><span>${item.name}</span><strong>${item.quantity_sold}</strong></div>`,
    "Sin productos vendidos",
  );
}

initDashboard().catch(() => {
  renderMiniList(salesOverview, [], () => "", "No fue posible cargar dashboard");
});
