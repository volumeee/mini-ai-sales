import axios from "axios";

/**
 * In development, Vite proxy handles /api → http://localhost:8000
 * In production (Docker/nginx), nginx proxies /api → backend:8000
 * So we only need a base URL override for non-proxied setups.
 */
const API_BASE_URL = import.meta.env.VITE_API_URL || "";

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// ─── Request interceptor: attach JWT token ───────────────────────────────────

client.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ─── Response interceptor: handle 401 ────────────────────────────────────────

client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("username");
      // Only redirect if NOT on login page to avoid refresh loops
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  },
);

// ─── API functions ───────────────────────────────────────────────────────────

export const authApi = {
  login: (username, password) =>
    client.post("/api/login", { username, password }),
};

export const salesApi = {
  getAll: (page = 1, limit = 20, search = "") => {
    const params = { page, limit };
    if (search) params.search = search;
    return client.get("/api/sales", { params });
  },
};

export const predictApi = {
  predict: (jumlah_penjualan, harga, diskon) =>
    client.post("/api/predict", { jumlah_penjualan, harga, diskon }),
};

export default client;
