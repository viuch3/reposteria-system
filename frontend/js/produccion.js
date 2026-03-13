import { get, post } from "./api.js";
import { requireAuth } from "./auth.js";

const productSelect = document.querySelector("[data-production-product]");
const quantityInput = document.querySelector("[data-production-quantity]");
const batchInput = document.querySelector("[data-production-batch]");
const expirationInput = document.querySelector("[data-production-expiration]");
const submitButton = document.querySelector("[data-production-submit]");
const messageBox = document.querySelector("[data-production-message]");
const recipeList = document.querySelector("[data-production-recipe]");
const productionTable = document.querySelector("[data-production-body]");

let productsCache = [];

function renderRecipe(recipeItems) {
  if (!recipeList) {
    return;
  }

  if (!recipeItems.length) {
    recipeList.innerHTML =
      '<div class="mini-item"><span>Sin receta</span><strong>Configurar en backend</strong></div>';
    return;
  }

  recipeList.innerHTML = recipeItems
    .map(
      (item) => `
        <div class="mini-item">
          <span>Insumo ${item.supply_id}</span>
          <strong>${item.supply_quantity}</strong>
        </div>
      `,
    )
    .join("");
}

function renderProductions(productions) {
  if (!productionTable) {
    return;
  }

  if (!productions.length) {
    productionTable.innerHTML =
      '<tr><td colspan="5" class="empty-state">No hay producciones registradas.</td></tr>';
    return;
  }

  productionTable.innerHTML = productions
    .map((item) => {
      const productName =
        productsCache.find((product) => product.id === item.product_id)?.name ||
        `Producto ${item.product_id}`;
      return `
        <tr>
          <td>${item.production_date}</td>
          <td>${productName}</td>
          <td>${item.quantity_produced}</td>
          <td>${item.batch}</td>
          <td>${item.expiration_date || "Sin fecha"}</td>
        </tr>
      `;
    })
    .join("");
}

async function loadProductionPageData() {
  const [products, productions] = await Promise.all([
    get("/products/"),
    get("/productions/"),
  ]);

  productsCache = products.filter((item) => item.status === "activo");

  if (productSelect) {
    productSelect.innerHTML = productsCache
      .map((product) => `<option value="${product.id}">${product.name}</option>`)
      .join("");
  }

  renderProductions(productions);
  await loadRecipePreview();
}

async function loadRecipePreview() {
  if (!productSelect?.value) {
    renderRecipe([]);
    return;
  }

  try {
    const recipe = await get(`/recipes/products/${productSelect.value}`);
    renderRecipe(recipe);
  } catch (error) {
    renderRecipe([]);
  }
}

async function handleProductionSubmit() {
  const payload = {
    product_id: Number(productSelect.value),
    quantity_produced: Number(quantityInput.value || 0),
    production_date: new Date().toISOString().slice(0, 10),
    batch: batchInput.value.trim(),
    expiration_date: expirationInput.value || null,
    notes: "Produccion registrada desde frontend",
  };

  try {
    messageBox.textContent = "Registrando produccion...";
    await post("/productions/", payload);
    messageBox.textContent = "Produccion registrada correctamente.";
    quantityInput.value = "1";
    batchInput.value = "";
    expirationInput.value = "";
    await loadProductionPageData();
  } catch (error) {
    messageBox.textContent =
      error instanceof Error ? error.message : "No fue posible registrar la produccion.";
  }
}

async function initProductionPage() {
  await requireAuth();
  await loadProductionPageData();

  productSelect?.addEventListener("change", loadRecipePreview);
  submitButton?.addEventListener("click", handleProductionSubmit);
}

initProductionPage().catch(() => {
  if (messageBox) {
    messageBox.textContent = "No fue posible cargar el modulo de produccion.";
  }
});
