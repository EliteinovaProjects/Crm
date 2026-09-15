from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.lead_field import LeadField, LeadFieldValue, FieldType
from app.core.id_generator import generate_id


class FieldMappingService:
    def __init__(self, db: Session):
        self.db = db

    def create_field(self, field_data: dict) -> LeadField:
        field_data["id"] = generate_id("FLD", 6)
        field = LeadField(**field_data)
        self.db.add(field)
        self.db.commit()
        self.db.refresh(field)
        return field

    def get_field(self, field_id: str) -> Optional[LeadField]:
        return self.db.query(LeadField).filter(LeadField.id == field_id).first()

    def get_all_fields(self, skip: int = 0, limit: int = 100) -> List[LeadField]:
        return self.db.query(LeadField).offset(skip).limit(limit).all()

    def update_field(self, field_id: str, field_data: dict) -> LeadField:
        field = self.get_field(field_id)
        if not field:
            raise ValueError("Field not found")
        
        for key, value in field_data.items():
            if hasattr(field, key) and value is not None:
                setattr(field, key, value)
        
        self.db.commit()
        self.db.refresh(field)
        return field

    def delete_field(self, field_id: str) -> bool:
        field = self.get_field(field_id)
        if not field:
            raise ValueError("Field not found")
        
        self.db.delete(field)
        self.db.commit()
        return True

    def add_field_value(self, lead_id: str, field_id: str, value: str) -> LeadFieldValue:
        # Check if value already exists
        existing = self.db.query(LeadFieldValue).filter(
            LeadFieldValue.lead_id == lead_id,
            LeadFieldValue.field_id == field_id
        ).first()
        
        if existing:
            existing.value = value
            self.db.commit()
            self.db.refresh(existing)
            return existing
        
        field_value = LeadFieldValue(
            id=generate_id("FLV", 6),
            lead_id=lead_id,
            field_id=field_id,
            value=value
        )
        self.db.add(field_value)
        self.db.commit()
        self.db.refresh(field_value)
        return field_value

    def get_field_values_for_lead(self, lead_id: str) -> List[LeadFieldValue]:
        return self.db.query(LeadFieldValue).filter(
            LeadFieldValue.lead_id == lead_id
        ).all()

    def get_field_values_for_field(self, field_id: str) -> List[LeadFieldValue]:
        return self.db.query(LeadFieldValue).filter(
            LeadFieldValue.field_id == field_id
        ).all()

    def delete_field_value(self, value_id: str) -> bool:
        value = self.db.query(LeadFieldValue).filter(LeadFieldValue.id == value_id).first()
        if not value:
            raise ValueError("Field value not found")
        
        self.db.delete(value)
        self.db.commit()
        return True

    def get_fields_by_type(self, field_type: FieldType) -> List[LeadField]:
        return self.db.query(LeadField).filter(
            LeadField.field_type == field_type
        ).all()

    def get_required_fields(self) -> List[LeadField]:
        return self.db.query(LeadField).filter(
            LeadField.is_required == True
        ).all()
