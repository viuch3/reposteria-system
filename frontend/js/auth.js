export function getStoredToken() {
  return localStorage.getItem("reposteria_token");
}

export function setStoredToken(token) {
  localStorage.setItem("reposteria_token", token);
}

export function clearStoredToken() {
  localStorage.removeItem("reposteria_token");
}
