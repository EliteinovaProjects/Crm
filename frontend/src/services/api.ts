import axios from 'axios'

// In development we use the Vite proxy (`/api` -> http://localhost:8000).
// In production (Vercel) point directly at the deployed backend service by
// setting the VITE_API_URL environment variable, e.g.
//   VITE_API_URL=https://crm-backend-xxxx.vercel.app
// If VITE_API_URL is not set we fall back to the same-origin `/api` prefix,
// which works when Vercel routes `/api/*` to the backend service.
const rawBaseUrl = import.meta.env.VITE_API_URL as string | undefined

export const api = axios.create({
  baseURL: rawBaseUrl ? rawBaseUrl.replace(/\/+$/, '') : '/api',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)
