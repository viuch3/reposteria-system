import { get, post } from "./api.js";
import { requireAuth } from "./auth.js";

const tableBody = document.querySelector("[data-supplies-body]");
const form = document.querySelector("[data-supply-form]");
const formMessage = document.querySelector("[data-supply-message]");
const expiringList = document.querySelector("[data-expiring-list]");
const lowStockList = document.querySelector("[data-low-stock-list]");

function formatDate(value) {
  if (!value) {
    return "Sin fecha";
  }
  return new Date(`${value}T00:00:00`).toLocaleDateString("es-CO");
}

function renderSupplyTable(supplies) {
  if (!tableBody) {
    return;
  }

  if (!supplies.length) {
    tableBody.innerHTML =
      '<tr><td colspan="5" class="empty-state">No hay insumos registrados.</td></tr>';
    return;
  }

  tableBody.innerHTML = supplies
    .map(
      (supply) => `
        <tr>
          <td>${supply.name}</td>
          <td>${supply.category || "Sin categoria"}</td>
          <td>${supply.current_stock} ${supply.unit_of_measure}</td>
          <td>${formatDate(supply.expiration_date)}</td>
          <td>$ ${supply.unit_cost}</td>
        </tr>
      `,
    )
    .join("");
}

function renderMiniList(target, items, formatter) {
  if (!target) {
    return;
  }

  if (!items.length) {
    target.innerHTML =
      '<div class="mini-item"><span>Sin alertas</span><strong>Todo en orden</strong></div>';
    return;
  }

  target.innerHTML = items.map(formatter).join("");
}

async function loadSupplies() {
  const [supplies, lowStock] = await Promise.all([
    get("/supplies/"),
    get("/supplies/low-stock"),
  ]);

  const expiring = [...supplies]
    .filter((item) => item.expiration_date)
    .sort((a, b) => a.expiration_date.localeCompare(b.expiration_date))
    .slice(0, 3);

  renderSupplyTable(supplies);
  renderMiniList(
    expiringList,
    expiring,
    (item) =>
      `<div class="mini-item"><span>${item.name}</span><strong>${formatDate(
        item.expiration_date,
      )}</strong></div>`,
  );
  renderMiniList(
    lowStockList,
    lowStock,
    (item) =>
      `<div class="mini-item"><span>${item.name}</span><strong>${item.current_stock} ${item.unit_of_measure}</strong></div>`,
  );
}

async function handleCreateSupply(event) {
  event.preventDefault();
  formMessage.textContent = "Guardando insumo...";

  const formData = new FormData(form);
  const payload = {
    name: formData.get("name"),
    category: formData.get("category"),
    current_stock: Number(formData.get("current_stock") || 0),
    min_stock: Number(formData.get("min_stock") || 0),
    max_stock: Number(formData.get("max_stock") || 0),
    unit_of_measure: formData.get("unit_of_measure"),
    unit_cost: formData.get("unit_cost"),
    supplier: formData.get("supplier"),
    expiration_date: formData.get("expiration_date") || null,
  };

  try {
    await post("/supplies/", payload);
    form.reset();
    formMessage.textContent = "Insumo creado correctamente.";
    await loadSupplies();
  } catch (error) {
    formMessage.textContent =
      error instanceof Error ? error.message : "No fue posible guardar el insumo.";
  }
}

async function initSuppliesPage() {
  await requireAuth();
  await loadSupplies();

  if (form) {
    form.addEventListener("submit", handleCreateSupply);
  }
}

initSuppliesPage().catch(() => {
  if (tableBody) {
    tableBody.innerHTML =
      '<tr><td colspan="5" class="empty-state">No fue posible cargar insumos.</td></tr>';
  }
});
