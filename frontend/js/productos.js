import { ApiError, get, post } from "./api.js";
import { requireAuth } from "./auth.js";

const tableBody = document.querySelector("[data-products-body]");
const searchInput = document.querySelector("[data-product-search]");
const form = document.querySelector("[data-product-form]");
const formMessage = document.querySelector("[data-product-message]");
const statsActive = document.querySelector("[data-products-active]");
const statsLow = document.querySelector("[data-products-low]");
const statsTop = document.querySelector("[data-products-top]");

function renderProducts(products) {
  if (!tableBody) {
    return;
  }

  if (!products.length) {
    tableBody.innerHTML =
      '<tr><td colspan="5" class="empty-state">No hay productos para mostrar.</td></tr>';
    return;
  }

  tableBody.innerHTML = products
    .map((product) => {
      const statusClass =
        product.status === "activo" ? "badge-success" : "badge-warning";

      return `
        <tr>
          <td>${product.code}</td>
          <td>${product.name}</td>
          <td>$ ${product.sale_price}</td>
          <td>${product.current_stock}</td>
          <td><span class="badge ${statusClass}">${product.status}</span></td>
        </tr>
      `;
    })
    .join("");
}

function updateSummary(products) {
  if (!statsActive || !statsLow || !statsTop) {
    return;
  }

  const activeProducts = products.filter((product) => product.status === "activo");
  const lowStockProducts = products.filter(
    (product) => product.current_stock <= product.min_stock,
  );
  const topProduct = products[0]?.name || "Sin datos";

  statsActive.textContent = `${activeProducts.length} activos`;
  statsLow.textContent = lowStockProducts[0]?.name || "Sin alertas";
  statsTop.textContent = topProduct;
}

async function loadProducts(query = "") {
  try {
    const path = query ? `/products/?q=${encodeURIComponent(query)}` : "/products/";
    const products = await get(path);
    renderProducts(products);
    updateSummary(products);
  } catch (error) {
    if (tableBody) {
      tableBody.innerHTML =
        '<tr><td colspan="5" class="empty-state">No fue posible cargar productos.</td></tr>';
    }
  }
}

async function handleCreateProduct(event) {
  event.preventDefault();
  formMessage.textContent = "Guardando producto...";

  const formData = new FormData(form);
  const payload = {
    code: formData.get("code"),
    name: formData.get("name"),
    description: formData.get("description"),
    category: formData.get("category"),
    sale_price: formData.get("sale_price"),
    cost_price: formData.get("cost_price"),
    current_stock: Number(formData.get("current_stock") || 0),
    min_stock: Number(formData.get("min_stock") || 0),
    max_stock: Number(formData.get("max_stock") || 0),
    unit_of_measure: formData.get("unit_of_measure"),
    status: formData.get("status"),
  };

  try {
    await post("/products/", payload);
    form.reset();
    formMessage.textContent = "Producto creado correctamente.";
    await loadProducts(searchInput?.value?.trim() || "");
  } catch (error) {
    formMessage.textContent =
      error instanceof Error ? error.message : "No fue posible guardar el producto.";
  }
}

async function initProductsPage() {
  try {
    await requireAuth();
    await loadProducts();
  } catch (error) {
    if (error instanceof ApiError && error.status === 403) {
      formMessage.textContent =
        "Tu usuario no tiene permisos suficientes para administrar productos.";
      return;
    }
  }

  if (searchInput) {
    searchInput.addEventListener("input", (event) => {
      loadProducts(event.target.value.trim());
    });
  }

  if (form) {
    form.addEventListener("submit", handleCreateProduct);
  }
}

initProductsPage();
