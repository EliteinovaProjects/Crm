from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.middleware.audit_log_middleware import audit_log_middleware
from app.api import (
    auth_router,
    admin_dashboard_router,
    employee_dashboard_router,
    lead_router,
    field_router,
    source_router,
    status_router,
    category_router,
    sms_template_router,
    agent_router,
    call_router,
    campaign_router,
    toolbox_settings_router,
    toolbox_functionality_router,
    toolbox_accounts_router,
    toolbox_resources_router,
    coin_router,
    reminder_router,
    notification_router,
    api_docs_router,
    attendance_router
)

# Schema is managed by Alembic migrations (see backend/alembic) - run
# `alembic upgrade head` instead of relying on create_all here.

app = FastAPI(
    title="CRM API",
    description="Customer Relationship Management API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Audit log middleware
app.middleware("http")(audit_log_middleware)

# Include routers
app.include_router(auth_router)
app.include_router(admin_dashboard_router)
app.include_router(employee_dashboard_router)
app.include_router(lead_router)
app.include_router(field_router)
app.include_router(source_router)
app.include_router(status_router)
app.include_router(category_router)
app.include_router(sms_template_router)
app.include_router(agent_router)
app.include_router(call_router)
app.include_router(campaign_router)
app.include_router(toolbox_settings_router)
app.include_router(toolbox_functionality_router)
app.include_router(toolbox_accounts_router)
app.include_router(toolbox_resources_router)
app.include_router(coin_router)
app.include_router(reminder_router)
app.include_router(notification_router)
app.include_router(api_docs_router)
app.include_router(attendance_router)


@app.get("/")
def root():
    return {
        "message": "CRM API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "Crm API is healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
