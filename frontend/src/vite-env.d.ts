/// <reference types="vite/client" />

interface ImportMetaEnv {
  /**
   * Base URL of the deployed backend API.
   * Example: https://crm-backend-xxxx.vercel.app
   * Leave unset to use the same-origin `/api` prefix (Vite dev proxy / Vercel routing).
   */
  readonly VITE_API_URL?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}