from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.sms_template import SMSTemplate


class SMSService:
    def __init__(self, db: Session):
        self.db = db

    def create_template(self, template_data: dict) -> SMSTemplate:
        from app.core.id_generator import generate_id
        template_data["id"] = generate_id("SMS", 6)
        template = SMSTemplate(**template_data)
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template

    def get_template(self, template_id: str) -> Optional[SMSTemplate]:
        return self.db.query(SMSTemplate).filter(SMSTemplate.id == template_id).first()

    def get_all_templates(self, skip: int = 0, limit: int = 100) -> List[SMSTemplate]:
        return self.db.query(SMSTemplate).offset(skip).limit(limit).all()

    def update_template(self, template_id: str, template_data: dict) -> SMSTemplate:
        template = self.get_template(template_id)
        if not template:
            raise ValueError("Template not found")
        
        for key, value in template_data.items():
            if hasattr(template, key) and value is not None:
                setattr(template, key, value)
        
        self.db.commit()
        self.db.refresh(template)
        return template

    def delete_template(self, template_id: str) -> bool:
        template = self.get_template(template_id)
        if not template:
            raise ValueError("Template not found")
        
        self.db.delete(template)
        self.db.commit()
        return True

    def send_sms(self, phone_number: str, template_id: str, variables: Optional[dict] = None) -> dict:
        """Send SMS using template and variables"""
        template = self.get_template(template_id)
        if not template:
            raise ValueError("Template not found")
        
        # Replace variables in template
        message = template.template_content
        if variables:
            for key, value in variables.items():
                message = message.replace(f"{{{key}}}", str(value))
        
        # In a real implementation, this would integrate with an SMS gateway
        # For now, we'll simulate the send
        return {
            "success": True,
            "message": "SMS sent successfully",
            "phone_number": phone_number,
            "message_content": message,
            "template_id": template_id
        }

    def send_bulk_sms(self, phone_numbers: List[str], template_id: str, variables: Optional[dict] = None) -> dict:
        """Send bulk SMS"""
        results = []
        for phone_number in phone_numbers:
            try:
                result = self.send_sms(phone_number, template_id, variables)
                results.append({
                    "phone_number": phone_number,
                    "success": True,
                    "message": result["message"]
                })
            except Exception as e:
                results.append({
                    "phone_number": phone_number,
                    "success": False,
                    "error": str(e)
                })
        
        return {
            "total": len(phone_numbers),
            "successful": len([r for r in results if r["success"]]),
            "failed": len([r for r in results if not r["success"]]),
            "results": results
        }
