import { get, post } from "./api.js";
import { requireAuth } from "./auth.js";

const productSelect = document.querySelector("[data-sale-product]");
const quantityInput = document.querySelector("[data-sale-quantity]");
const unitPriceInput = document.querySelector("[data-sale-unit-price]");
const channelSelect = document.querySelector("[data-sale-channel]");
const timeInput = document.querySelector("[data-sale-time]");
const addItemButton = document.querySelector("[data-sale-add-item]");
const submitButton = document.querySelector("[data-sale-submit]");
const cartList = document.querySelector("[data-sale-cart]");
const totalValue = document.querySelector("[data-sale-total]");
const messageBox = document.querySelector("[data-sale-message]");

let productsCache = [];
let cart = [];

function formatCurrency(value) {
  return new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  }).format(value);
}

function updateUnitPriceFromSelect() {
  const selectedId = Number(productSelect?.value || 0);
  const product = productsCache.find((item) => item.id === selectedId);
  if (product && unitPriceInput) {
    unitPriceInput.value = product.sale_price;
  }
}

function renderCart() {
  if (!cartList || !totalValue) {
    return;
  }

  if (!cart.length) {
    cartList.innerHTML =
      '<div class="mini-item"><span>Sin productos</span><strong>Agrega items</strong></div>';
    totalValue.textContent = formatCurrency(0);
    return;
  }

  const total = cart.reduce((sum, item) => sum + item.subtotal, 0);
  totalValue.textContent = formatCurrency(total);
  cartList.innerHTML = cart
    .map(
      (item, index) => `
        <div class="mini-item">
          <span>${item.name} x${item.quantity}</span>
          <strong>${formatCurrency(item.subtotal)}</strong>
          <button class="button button-ghost" type="button" data-remove-index="${index}">Quitar</button>
        </div>
      `,
    )
    .join("");

  cartList.querySelectorAll("[data-remove-index]").forEach((button) => {
    button.addEventListener("click", () => {
      cart.splice(Number(button.dataset.removeIndex), 1);
      renderCart();
    });
  });
}

async function loadProductsForSale() {
  productsCache = await get("/products/");
  if (!productSelect) {
    return;
  }

  const activeProducts = productsCache.filter((product) => product.status === "activo");
  productSelect.innerHTML = activeProducts
    .map(
      (product) =>
        `<option value="${product.id}">${product.name} (${product.current_stock} disponibles)</option>`,
    )
    .join("");
  updateUnitPriceFromSelect();
}

function addItemToCart() {
  const productId = Number(productSelect?.value || 0);
  const quantity = Number(quantityInput?.value || 0);
  const unitPrice = Number(unitPriceInput?.value || 0);
  const product = productsCache.find((item) => item.id === productId);

  if (!product || quantity <= 0 || unitPrice <= 0) {
    messageBox.textContent = "Selecciona un producto y una cantidad valida.";
    return;
  }

  cart.push({
    product_id: product.id,
    name: product.name,
    quantity,
    unit_price: unitPrice.toFixed(2),
    subtotal: quantity * unitPrice,
  });

  messageBox.textContent = "Producto agregado al carrito.";
  quantityInput.value = "1";
  renderCart();
}

async function submitSale() {
  if (!cart.length) {
    messageBox.textContent = "Agrega al menos un producto al carrito.";
    return;
  }

  const today = new Date().toISOString().slice(0, 10);
  const payload = {
    sale_date: today,
    sale_time: timeInput.value || "10:00:00",
    sales_channel: channelSelect.value,
    notes: "Venta registrada desde frontend",
    details: cart.map((item) => ({
      product_id: item.product_id,
      quantity: item.quantity,
      unit_price: item.unit_price,
    })),
  };

  try {
    messageBox.textContent = "Registrando venta...";
    await post("/sales/", payload);
    messageBox.textContent = "Venta registrada correctamente.";
    cart = [];
    renderCart();
    await loadProductsForSale();
  } catch (error) {
    messageBox.textContent =
      error instanceof Error ? error.message : "No fue posible registrar la venta.";
  }
}

async function initSalesPage() {
  await requireAuth();
  await loadProductsForSale();
  renderCart();

  productSelect?.addEventListener("change", updateUnitPriceFromSelect);
  addItemButton?.addEventListener("click", addItemToCart);
  submitButton?.addEventListener("click", submitSale);
}

initSalesPage().catch(() => {
  messageBox.textContent = "No fue posible cargar el modulo de ventas.";
});
