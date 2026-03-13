import { get, post } from "./api.js";
import { requireAuth } from "./auth.js";

const itemTypeSelect = document.querySelector("[data-inventory-item-type]");
const productSelect = document.querySelector("[data-inventory-product]");
const supplySelect = document.querySelector("[data-inventory-supply]");
const movementTypeSelect = document.querySelector("[data-inventory-movement-type]");
const quantityInput = document.querySelector("[data-inventory-quantity]");
const reasonInput = document.querySelector("[data-inventory-reason]");
const submitButton = document.querySelector("[data-inventory-submit]");
const messageBox = document.querySelector("[data-inventory-message]");
const tableBody = document.querySelector("[data-inventory-body]");

let productsCache = [];
let suppliesCache = [];

function renderOptions(selectElement, items, formatter) {
  if (!selectElement) {
    return;
  }

  selectElement.innerHTML = items
    .map((item) => `<option value="${item.id}">${formatter(item)}</option>`)
    .join("");
}

function toggleInventoryTarget() {
  const type = itemTypeSelect?.value || "product";
  const showProduct = type === "product";

  if (productSelect) {
    productSelect.disabled = !showProduct;
    productSelect.parentElement.style.opacity = showProduct ? "1" : "0.5";
  }

  if (supplySelect) {
    supplySelect.disabled = showProduct;
    supplySelect.parentElement.style.opacity = showProduct ? "0.5" : "1";
  }
}

function formatMovementType(value) {
  if (value === "entrada") {
    return "Entrada";
  }
  if (value === "salida") {
    return "Salida";
  }
  return "Merma";
}

function renderMovements(movements) {
  if (!tableBody) {
    return;
  }

  if (!movements.length) {
    tableBody.innerHTML =
      '<tr><td colspan="6" class="empty-state">No hay movimientos registrados.</td></tr>';
    return;
  }

  tableBody.innerHTML = movements
    .map((movement) => {
      const badgeClass =
        movement.movement_type === "entrada" ? "badge-success" : "badge-danger";
      const itemName =
        productsCache.find((item) => item.id === movement.product_id)?.name ||
        suppliesCache.find((item) => item.id === movement.supply_id)?.name ||
        "Item";

      return `
        <tr>
          <td>${new Date(movement.movement_date).toLocaleString("es-CO")}</td>
          <td><span class="badge ${badgeClass}">${formatMovementType(movement.movement_type)}</span></td>
          <td>${itemName}</td>
          <td>${movement.quantity}</td>
          <td>${movement.reason || "Sin motivo"}</td>
          <td>${movement.user_id}</td>
        </tr>
      `;
    })
    .join("");
}

async function loadReferenceData() {
  const [products, supplies, movements] = await Promise.all([
    get("/products/"),
    get("/supplies/"),
    get("/inventory/movements"),
  ]);

  productsCache = products;
  suppliesCache = supplies;

  renderOptions(
    productSelect,
    products.filter((item) => item.status === "activo"),
    (item) => `${item.name} (${item.current_stock})`,
  );
  renderOptions(
    supplySelect,
    supplies,
    (item) => `${item.name} (${item.current_stock} ${item.unit_of_measure})`,
  );
  renderMovements(movements);
  toggleInventoryTarget();
}

async function handleMovementSubmit() {
  const type = itemTypeSelect.value;
  const payload = {
    movement_type: movementTypeSelect.value,
    quantity: Number(quantityInput.value || 0),
    reason: reasonInput.value.trim(),
    product_id: type === "product" ? Number(productSelect.value) : null,
    supply_id: type === "supply" ? Number(supplySelect.value) : null,
  };

  try {
    messageBox.textContent = "Registrando movimiento...";
    await post("/inventory/movements", payload);
    messageBox.textContent = "Movimiento registrado correctamente.";
    reasonInput.value = "";
    quantityInput.value = "1";
    await loadReferenceData();
  } catch (error) {
    messageBox.textContent =
      error instanceof Error ? error.message : "No fue posible registrar el movimiento.";
  }
}

async function initInventoryPage() {
  await requireAuth();
  await loadReferenceData();

  itemTypeSelect?.addEventListener("change", toggleInventoryTarget);
  submitButton?.addEventListener("click", handleMovementSubmit);
}

initInventoryPage().catch(() => {
  if (messageBox) {
    messageBox.textContent = "No fue posible cargar el modulo de inventario.";
  }
});
