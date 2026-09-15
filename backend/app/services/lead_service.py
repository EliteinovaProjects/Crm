from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.lead import Lead
from app.models.lead_field import LeadField, LeadFieldValue
from app.repositories.lead_repository import LeadRepository
from app.core.id_generator import generate_lead_id
import pandas as pd
import io


class LeadService:
    def __init__(self, db: Session):
        self.db = db
        self.lead_repository = LeadRepository(db)

    def create_lead(self, lead_data: dict, field_values: Optional[List[dict]] = None) -> Lead:
        lead_data["id"] = generate_lead_id()
        lead = self.lead_repository.create(lead_data)
        
        if field_values:
            for field_value_data in field_values:
                field_value_data["lead_id"] = lead.id
                self.lead_repository.add_field_value(
                    lead.id, 
                    field_value_data["field_id"], 
                    field_value_data["value"]
                )
        
        return lead

    def get_lead(self, lead_id: str) -> Optional[Lead]:
        return self.lead_repository.get_by_id(lead_id)

    def get_leads(self, skip: int = 0, limit: int = 100, filters: Optional[dict] = None) -> List[Lead]:
        base_query = self.db.query(Lead).filter(Lead.is_deleted == False)
        
        if filters:
            if filters.get("agent_id"):
                base_query = base_query.filter(Lead.assigned_agent_id == filters["agent_id"])
            if filters.get("status_id"):
                base_query = base_query.filter(Lead.status_id == filters["status_id"])
            if filters.get("source_id"):
                base_query = base_query.filter(Lead.source_id == filters["source_id"])
            if filters.get("category_id"):
                base_query = base_query.filter(Lead.category_id == filters["category_id"])
            if filters.get("start_date"):
                base_query = base_query.filter(Lead.created_at >= filters["start_date"])
            if filters.get("end_date"):
                base_query = base_query.filter(Lead.created_at <= filters["end_date"])
        
        return base_query.offset(skip).limit(limit).all()

    def update_lead(self, lead_id: str, lead_data: dict, field_values: Optional[List[dict]] = None) -> Lead:
        lead = self.lead_repository.get_by_id(lead_id)
        if not lead:
            raise ValueError("Lead not found")
        
        lead = self.lead_repository.update(lead, lead_data)
        
        if field_values:
            # Update field values
            for field_value_data in field_values:
                existing_value = self.db.query(LeadFieldValue).filter(
                    LeadFieldValue.lead_id == lead_id,
                    LeadFieldValue.field_id == field_value_data["field_id"]
                ).first()
                
                if existing_value:
                    existing_value.value = field_value_data["value"]
                    self.db.commit()
                else:
                    self.lead_repository.add_field_value(
                        lead_id,
                        field_value_data["field_id"],
                        field_value_data["value"]
                    )
        
        return lead

    def delete_lead(self, lead_id: str) -> Lead:
        lead = self.lead_repository.get_by_id(lead_id)
        if not lead:
            raise ValueError("Lead not found")
        
        return self.lead_repository.soft_delete(lead)

    def restore_lead(self, lead_id: str) -> Lead:
        lead = self.lead_repository.get_by_id(lead_id)
        if not lead:
            raise ValueError("Lead not found")
        
        return self.lead_repository.restore(lead)

    def bulk_assign_leads(self, lead_ids: List[str], agent_ids: List[str]) -> List[Lead]:
        # Distribute leads among agents
        leads = self.db.query(Lead).filter(Lead.id.in_(lead_ids)).all()
        
        for i, lead in enumerate(leads):
            agent_id = agent_ids[i % len(agent_ids)]
            self.lead_repository.update(lead, {"assigned_agent_id": agent_id})
        
        return leads

    def bulk_update_leads(self, lead_ids: List[str], update_type: str, update_value: str) -> List[Lead]:
        update_data = {}
        if update_type == "category":
            update_data["category_id"] = update_value
        elif update_type == "source":
            update_data["source_id"] = update_value
        else:
            raise ValueError("Invalid update type")
        
        return self.lead_repository.bulk_update(lead_ids, update_data)

    def import_leads_from_excel(self, file_content: bytes, import_options: dict) -> Dict[str, Any]:
        try:
            df = pd.read_excel(io.BytesIO(file_content))
            
            leads_data = []
            for _, row in df.iterrows():
                lead_data = {
                    "id": generate_lead_id(),
                    "name": row.get("Name", ""),
                    "mobile_number": str(row.get("Mobile", "")),
                    "account": row.get("Account", ""),
                    "email": row.get("Email", ""),
                    "address": row.get("Address", ""),
                    "description": row.get("Description", ""),
                    "assigned_agent_id": import_options.get("agent_id"),
                    "source_id": import_options.get("source_id"),
                    "status_id": import_options.get("status_id"),
                    "category_id": import_options.get("category_id"),
                    "follow_up_date": import_options.get("follow_up_date")
                }
                
                # Handle restore/update options
                if import_options.get("restore_deleted"):
                    existing_lead = self.lead_repository.get_by_mobile(lead_data["mobile_number"])
                    if existing_lead and existing_lead.is_deleted:
                        self.lead_repository.restore(existing_lead)
                        continue
                
                if import_options.get("reassign_existing"):
                    existing_lead = self.lead_repository.get_by_mobile(lead_data["mobile_number"])
                    if existing_lead and not existing_lead.is_deleted:
                        self.lead_repository.update(existing_lead, {
                            "assigned_agent_id": import_options.get("agent_id"),
                            "source_id": import_options.get("source_id"),
                            "status_id": import_options.get("status_id"),
                            "category_id": import_options.get("category_id")
                        })
                        continue
                
                leads_data.append(lead_data)
            
            created_leads = self.lead_repository.bulk_create(leads_data)
            
            return {
                "success": True,
                "imported_count": len(created_leads),
                "leads": [lead.id for lead in created_leads]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "imported_count": 0
            }

    def export_leads_to_excel(self, export_options: dict) -> bytes:
        leads = self.get_leads(
            skip=0, 
            limit=10000,  # Large limit for export
            filters=export_options
        )
        
        data = []
        for lead in leads:
            lead_dict = {
                "ID": lead.id,
                "Name": lead.name,
                "Mobile": lead.mobile_number,
                "Alternate Number": lead.alternate_number,
                "Email": lead.email,
                "Account": lead.account,
                "Address": lead.address,
                "Description": lead.description,
                "Created At": lead.created_at.isoformat()
            }
            data.append(lead_dict)
        
        df = pd.DataFrame(data)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Leads')
        
        output.seek(0)
        return output.getvalue()

    def get_sample_excel_template(self) -> bytes:
        sample_data = {
            "Name": ["John Doe", "Jane Smith"],
            "Mobile": ["1234567890", "0987654321"],
            "Account": ["Account A", "Account B"],
            "Email": ["john@example.com", "jane@example.com"],
            "Address": ["123 Main St", "456 Oak Ave"],
            "Description": ["Sample lead 1", "Sample lead 2"]
        }
        
        df = pd.DataFrame(sample_data)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sample')
        
        output.seek(0)
        return output.getvalue()

    def get_lead_stats(self) -> Dict[str, Any]:
        return self.lead_repository.get_stats()

    def get_field_values(self, lead_id: str) -> List[LeadFieldValue]:
        return self.lead_repository.get_field_values(lead_id)
