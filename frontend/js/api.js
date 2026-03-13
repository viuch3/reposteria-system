export const API_BASE_URL = "http://127.0.0.1:8000/api/v1";
const STORAGE_KEY = "reposteria_token";

export class ApiError extends Error {
  constructor(message, status, details = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.details = details;
  }
}

async function parseResponse(response) {
  const contentType = response.headers.get("content-type") || "";
  const isJson = contentType.includes("application/json");
  const data = isJson ? await response.json() : await response.text();

  if (!response.ok) {
    const message =
      (isJson && (data.detail || data.message)) ||
      "Ocurrio un error al comunicarse con la API.";
    throw new ApiError(message, response.status, data);
  }

  return data;
}

export async function apiRequest(path, options = {}) {
  const token = localStorage.getItem(STORAGE_KEY);
  const headers = new Headers(options.headers || {});

  if (!headers.has("Content-Type") && options.body) {
    headers.set("Content-Type", "application/json");
  }

  if (token && !headers.has("Authorization")) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  return parseResponse(response);
}

export function get(path) {
  return apiRequest(path, { method: "GET" });
}

export function post(path, body) {
  return apiRequest(path, {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export function patch(path, body) {
  return apiRequest(path, {
    method: "PATCH",
    body: JSON.stringify(body),
  });
}

export function del(path) {
  return apiRequest(path, { method: "DELETE" });
}
