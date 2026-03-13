import { ApiError, get, post } from "./api.js";

const STORAGE_KEY = "reposteria_token";

export function getStoredToken() {
  return localStorage.getItem(STORAGE_KEY);
}

export function setStoredToken(token) {
  localStorage.setItem(STORAGE_KEY, token);
}

export function clearStoredToken() {
  localStorage.removeItem(STORAGE_KEY);
}

export async function fetchCurrentUser() {
  return get("/auth/me");
}

export async function login(email, password) {
  const response = await post("/auth/login", { email, password });
  setStoredToken(response.access_token);
  return response;
}

export function redirectToLogin() {
  window.location.href = "./login.html";
}

export async function requireAuth() {
  const token = getStoredToken();
  if (!token) {
    redirectToLogin();
    return null;
  }

  try {
    return await fetchCurrentUser();
  } catch (error) {
    clearStoredToken();
    if (error instanceof ApiError && error.status === 401) {
      redirectToLogin();
      return null;
    }
    throw error;
  }
}

const loginForm = document.querySelector("[data-login-form]");
if (loginForm) {
  const emailInput = document.querySelector("#email");
  const passwordInput = document.querySelector("#password");
  const messageBox = document.querySelector("[data-login-message]");
  const submitButton = loginForm.querySelector("button");

  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    submitButton.disabled = true;
    messageBox.textContent = "Validando acceso...";

    try {
      await login(emailInput.value.trim(), passwordInput.value);
      messageBox.textContent = "Acceso correcto. Redirigiendo...";
      window.location.href = "./dashboard.html";
    } catch (error) {
      messageBox.textContent =
        error instanceof Error ? error.message : "No fue posible iniciar sesion.";
    } finally {
      submitButton.disabled = false;
    }
  });
}
