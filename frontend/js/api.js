export const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function apiRequest(path, options = {}) {
  return fetch(`${API_BASE_URL}${path}`, options);
}
