from app.api.auth_controller import router as auth_router
from app.api.admin_dashboard_controller import router as admin_dashboard_router
from app.api.employee_dashboard_controller import router as employee_dashboard_router
from app.api.lead_controller import router as lead_router
from app.api.field_controller import router as field_router
from app.api.source_controller import router as source_router
from app.api.status_controller import router as status_router
from app.api.category_controller import router as category_router
from app.api.sms_template_controller import router as sms_template_router
from app.api.agent_controller import router as agent_router
from app.api.call_controller import router as call_router
from app.api.campaign_controller import router as campaign_router
from app.api.toolbox_settings_controller import router as toolbox_settings_router
from app.api.toolbox_functionality_controller import router as toolbox_functionality_router
from app.api.toolbox_accounts_controller import router as toolbox_accounts_router
from app.api.toolbox_resources_controller import router as toolbox_resources_router
from app.api.coin_controller import router as coin_router
from app.api.reminder_controller import router as reminder_router
from app.api.notification_controller import router as notification_router
from app.api.api_docs_controller import router as api_docs_router

__all__ = [
    "auth_router",
    "admin_dashboard_router",
    "employee_dashboard_router",
    "lead_router",
    "field_router",
    "source_router",
    "status_router",
    "category_router",
    "sms_template_router",
    "agent_router",
    "call_router",
    "campaign_router",
    "toolbox_settings_router",
    "toolbox_functionality_router",
    "toolbox_accounts_router",
    "toolbox_resources_router",
    "coin_router",
    "reminder_router",
    "notification_router",
    "api_docs_router"
]
