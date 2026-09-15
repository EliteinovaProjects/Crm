from fastapi import APIRouter, Depends
from app.middleware.auth_middleware import get_current_admin
from app.models.user import User

router = APIRouter(prefix="/api-docs", tags=["API Documentation"])


@router.get("/")
def get_api_docs(
    current_user: User = Depends(get_current_admin)
):
    """Get API documentation"""
    return {
        "message": "API Documentation",
        "endpoints": {
            "authentication": {
                "login": "POST /auth/login",
                "register": "POST /auth/register",
                "get_current_user": "GET /auth/me",
                "update_user": "PUT /auth/me",
                "get_all_users": "GET /auth/users",
                "update_user_by_id": "PUT /auth/users/{user_id}",
                "delete_user": "DELETE /auth/users/{user_id}"
            },
            "leads": {
                "create_lead": "POST /leads/",
                "get_leads": "GET /leads/",
                "get_lead": "GET /leads/{lead_id}",
                "update_lead": "PUT /leads/{lead_id}",
                "delete_lead": "DELETE /leads/{lead_id}",
                "restore_lead": "POST /leads/{lead_id}/restore",
                "assign_leads": "POST /leads/assign",
                "bulk_update_leads": "POST /leads/bulk-update",
                "import_leads": "POST /leads/import",
                "export_leads": "POST /leads/export",
                "download_sample": "GET /leads/sample/download",
                "get_stats": "GET /leads/stats"
            },
            "fields": {
                "create_field": "POST /fields/",
                "get_fields": "GET /fields/",
                "get_field": "GET /fields/{field_id}",
                "update_field": "PUT /fields/{field_id}",
                "delete_field": "DELETE /fields/{field_id}",
                "add_field_value": "POST /fields/{lead_id}/values/{field_id}",
                "get_field_values": "GET /fields/{lead_id}/values"
            },
            "sources": {
                "create_source": "POST /sources/",
                "get_sources": "GET /sources/",
                "get_source": "GET /sources/{source_id}",
                "update_source": "PUT /sources/{source_id}",
                "delete_source": "DELETE /sources/{source_id}"
            },
            "statuses": {
                "create_status": "POST /statuses/",
                "get_statuses": "GET /statuses/",
                "get_status": "GET /statuses/{status_id}",
                "update_status": "PUT /statuses/{status_id}",
                "delete_status": "DELETE /statuses/{status_id}"
            },
            "categories": {
                "create_category": "POST /categories/",
                "get_categories": "GET /categories/",
                "get_category": "GET /categories/{category_id}",
                "update_category": "PUT /categories/{category_id}",
                "delete_category": "DELETE /categories/{category_id}"
            },
            "sms_templates": {
                "create_template": "POST /sms-templates/",
                "get_templates": "GET /sms-templates/",
                "get_template": "GET /sms-templates/{template_id}",
                "update_template": "PUT /sms-templates/{template_id}",
                "delete_template": "DELETE /sms-templates/{template_id}",
                "send_sms": "POST /sms-templates/send"
            },
            "agents": {
                "create_agent": "POST /agents/",
                "get_agents": "GET /agents/",
                "get_active_agents": "GET /agents/active",
                "get_agent": "GET /agents/{agent_id}",
                "update_agent": "PUT /agents/{agent_id}",
                "delete_agent": "DELETE /agents/{agent_id}",
                "get_agent_leads_count": "GET /agents/{agent_id}/leads-count",
                "create_agent_group": "POST /agents/groups/",
                "get_agent_groups": "GET /agents/groups/",
                "get_agent_group": "GET /agents/groups/{group_id}",
                "update_agent_group": "PUT /agents/groups/{group_id}",
                "delete_agent_group": "DELETE /agents/groups/{group_id}",
                "import_agents": "POST /agents/import",
                "download_sample": "GET /agents/sample/download"
            },
            "calls": {
                "initiate_call": "POST /calls/initiate",
                "update_call_status": "PUT /calls/{call_id}/status",
                "end_call": "PUT /calls/{call_id}/end",
                "get_call_log": "GET /calls/{call_id}",
                "get_my_calls": "GET /calls/agent/me",
                "get_lead_calls": "GET /calls/lead/{lead_id}",
                "get_call_stats": "GET /calls/stats/{agent_id}",
                "update_agent_status": "PUT /calls/agent/status",
                "set_campaign_ready": "PUT /calls/agent/campaign-ready"
            },
            "campaigns": {
                "create_campaign": "POST /campaigns/",
                "get_campaigns": "GET /campaigns/",
                "get_campaign": "GET /campaigns/{campaign_id}",
                "update_campaign": "PUT /campaigns/{campaign_id}",
                "delete_campaign": "DELETE /campaigns/{campaign_id}",
                "activate_campaign": "POST /campaigns/{campaign_id}/activate",
                "deactivate_campaign": "POST /campaigns/{campaign_id}/deactivate",
                "add_campaign_base": "POST /campaigns/{campaign_id}/base",
                "get_campaign_base": "GET /campaigns/{campaign_id}/base",
                "get_pending_calls": "GET /campaigns/{campaign_id}/base/pending",
                "update_call_status": "PUT /campaigns/base/{base_id}/status",
                "delete_campaign_base": "DELETE /campaigns/base/{base_id}",
                "add_campaign_field": "POST /campaigns/{campaign_id}/fields"
            },
            "toolbox_settings": {
                "create_ivr_flow": "POST /toolbox/settings/ivr-flows",
                "get_ivr_flows": "GET /toolbox/settings/ivr-flows",
                "get_ivr_flow": "GET /toolbox/settings/ivr-flows/{flow_id}",
                "update_ivr_flow": "PUT /toolbox/settings/ivr-flows/{flow_id}",
                "delete_ivr_flow": "DELETE /toolbox/settings/ivr-flows/{flow_id}",
                "create_sub_admin": "POST /toolbox/settings/sub-admins",
                "get_sub_admins": "GET /toolbox/settings/sub-admins"
            },
            "toolbox_functionality": {
                "create_contact": "POST /toolbox/functionality/contacts",
                "get_contacts": "GET /toolbox/functionality/contacts",
                "add_to_blacklist": "POST /toolbox/functionality/blacklist",
                "get_blacklist": "GET /toolbox/functionality/blacklist",
                "remove_from_blacklist": "DELETE /toolbox/functionality/blacklist/{item_id}",
                "get_system_logs": "GET /toolbox/functionality/system-logs",
                "create_holiday": "POST /toolbox/functionality/holidays",
                "get_holidays": "GET /toolbox/functionality/holidays",
                "create_break_reason": "POST /toolbox/functionality/break-reasons",
                "get_break_reasons": "GET /toolbox/functionality/break-reasons",
                "create_disposition": "POST /toolbox/functionality/dispositions",
                "get_dispositions": "GET /toolbox/functionality/dispositions",
                "create_api_integration": "POST /toolbox/functionality/api-integrations",
                "get_api_integrations": "GET /toolbox/functionality/api-integrations",
                "export_leads": "POST /toolbox/functionality/export/leads",
                "update_tts_config": "POST /toolbox/functionality/config/tts",
                "get_tts_config": "GET /toolbox/functionality/config/tts"
            },
            "toolbox_accounts": {
                "get_preferences": "GET /toolbox/accounts/preferences",
                "update_preferences": "PUT /toolbox/accounts/preferences",
                "get_payment_history": "GET /toolbox/accounts/payment-history",
                "create_did_number": "POST /toolbox/accounts/did-config",
                "get_did_numbers": "GET /toolbox/accounts/did-config",
                "update_did_number": "PUT /toolbox/accounts/did-config/{did_id}",
                "delete_did_number": "DELETE /toolbox/accounts/did-config/{did_id}"
            },
            "toolbox_resources": {
                "create_sound": "POST /toolbox/resources/sound-library",
                "get_sound_library": "GET /toolbox/resources/sound-library",
                "get_sound": "GET /toolbox/resources/sound-library/{sound_id}",
                "delete_sound": "DELETE /toolbox/resources/sound-library/{sound_id}",
                "get_sms_templates": "GET /toolbox/resources/sms-templates",
                "create_sms_template": "POST /toolbox/resources/sms-templates",
                "bulk_import_agents": "POST /toolbox/resources/agents/bulk-import",
                "download_agent_sample": "GET /toolbox/resources/agents/sample-download"
            },
            "coins": {
                "get_wallet": "GET /coins/wallet",
                "topup_coins": "POST /coins/topup",
                "deduct_coins": "POST /coins/deduct",
                "get_transactions": "GET /coins/transactions",
                "get_topup_history": "GET /coins/topup-history",
                "reset_monthly_coins": "POST /coins/reset-monthly"
            },
            "reminders": {
                "create_reminder": "POST /reminders/",
                "get_reminders": "GET /reminders/",
                "get_upcoming_reminders": "GET /reminders/upcoming",
                "get_reminder_history": "GET /reminders/history",
                "get_reminders_summary": "GET /reminders/summary",
                "get_reminder": "GET /reminders/{reminder_id}",
                "update_reminder": "PUT /reminders/{reminder_id}",
                "complete_reminder": "POST /reminders/{reminder_id}/complete",
                "delete_reminder": "DELETE /reminders/{reminder_id}"
            },
            "notifications": {
                "get_notifications": "GET /notifications/",
                "get_unread_count": "GET /notifications/unread-count",
                "get_notification": "GET /notifications/{notification_id}",
                "mark_as_read": "PUT /notifications/{notification_id}/read",
                "mark_all_as_read": "PUT /notifications/read-all",
                "delete_notification": "DELETE /notifications/{notification_id}"
            },
            "dashboard": {
                "admin_stats": "GET /admin/dashboard/stats",
                "employee_stats": "GET /employee/dashboard/stats"
            }
        }
    }
