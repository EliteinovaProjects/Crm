from typing import Optional, List
from sqlalchemy.orm import Session
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


class EmailService:
    def __init__(self, db: Session):
        self.db = db

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        from_email: Optional[str] = None
    ) -> dict:
        """Send email using SMTP"""
        try:
            # In a real implementation, you would configure SMTP settings
            # For now, we'll simulate the email send
            return {
                "success": True,
                "message": "Email sent successfully",
                "to_email": to_email,
                "subject": subject
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def send_bulk_email(
        self,
        to_emails: List[str],
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        from_email: Optional[str] = None
    ) -> dict:
        """Send bulk email"""
        results = []
        for email in to_emails:
            try:
                result = self.send_email(email, subject, body, html_body, from_email)
                results.append({
                    "email": email,
                    "success": True,
                    "message": result["message"]
                })
            except Exception as e:
                results.append({
                    "email": email,
                    "success": False,
                    "error": str(e)
                })
        
        return {
            "total": len(to_emails),
            "successful": len([r for r in results if r["success"]]),
            "failed": len([r for r in results if not r["success"]]),
            "results": results
        }

    def send_welcome_email(self, user_email: str, user_name: str) -> dict:
        """Send welcome email to new user"""
        subject = "Welcome to CRM System"
        body = f"""
        Dear {user_name},
        
        Welcome to the CRM System! Your account has been successfully created.
        
        You can now log in to the system using your credentials.
        
        Best regards,
        CRM Team
        """
        
        return self.send_email(user_email, subject, body)

    def send_lead_assignment_email(self, agent_email: str, lead_name: str) -> dict:
        """Send email when lead is assigned to agent"""
        subject = "New Lead Assigned"
        body = f"""
        Dear Agent,
        
        A new lead has been assigned to you:
        
        Lead Name: {lead_name}
        
        Please follow up with this lead at your earliest convenience.
        
        Best regards,
        CRM Team
        """
        
        return self.send_email(agent_email, subject, body)

    def send_reminder_email(self, user_email: str, reminder_title: str, reminder_date: str) -> dict:
        """Send reminder email"""
        subject = "Reminder Notification"
        body = f"""
        Dear User,
        
        You have a reminder:
        
        Title: {reminder_title}
        Date: {reminder_date}
        
        Please don't forget to complete this task.
        
        Best regards,
        CRM Team
        """
        
        return self.send_email(user_email, subject, body)
