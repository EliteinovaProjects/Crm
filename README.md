# Crm

Customer Relationship Management (CRM) application.

- `backend/` — FastAPI + SQLAlchemy + Alembic (PostgreSQL / Neon)
- `frontend/` — Vite + React (SPA)

## Local development

```bash
# Backend  -> http://localhost:8000
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend -> http://localhost:5173  (proxies /api to :8000)
cd frontend
npm install
npm run dev
```

## Deployment

See **[DEPLOYMENT.md](./DEPLOYMENT.md)** for deploying the frontend and backend
to Vercel and the database to Neon (including environment variables, running
migrations, and troubleshooting).