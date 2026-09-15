from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.user import User, UserRole
from app.models.agent_group import AgentGroup


class AgentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, agent_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == agent_id).first()

    def get_all_agents(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).filter(
            User.role == UserRole.EMPLOYEE
        ).offset(skip).limit(limit).all()

    def get_active_agents(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).filter(
            User.role == UserRole.EMPLOYEE,
            User.is_active == True
        ).offset(skip).limit(limit).all()

    def create_agent(self, agent_data: dict) -> User:
        from app.core.security import get_password_hash
        hashed_password = get_password_hash(agent_data.pop("password"))
        agent_data["role"] = UserRole.EMPLOYEE
        db_agent = User(**agent_data, hashed_password=hashed_password)
        self.db.add(db_agent)
        self.db.commit()
        self.db.refresh(db_agent)
        return db_agent

    def update_agent(self, agent: User, agent_data: dict) -> User:
        for key, value in agent_data.items():
            if hasattr(agent, key) and value is not None:
                setattr(agent, key, value)
        self.db.commit()
        self.db.refresh(agent)
        return agent

    def delete_agent(self, agent: User) -> bool:
        self.db.delete(agent)
        self.db.commit()
        return True

    def get_agent_leads_count(self, agent_id: str) -> int:
        from app.models.lead import Lead
        return self.db.query(Lead).filter(
            Lead.assigned_agent_id == agent_id,
            Lead.is_deleted == False
        ).count()


class AgentGroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, group_id: str) -> Optional[AgentGroup]:
        return self.db.query(AgentGroup).filter(AgentGroup.id == group_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[AgentGroup]:
        return self.db.query(AgentGroup).offset(skip).limit(limit).all()

    def create(self, group_data: dict) -> AgentGroup:
        db_group = AgentGroup(**group_data)
        self.db.add(db_group)
        self.db.commit()
        self.db.refresh(db_group)
        return db_group

    def update(self, group: AgentGroup, group_data: dict) -> AgentGroup:
        for key, value in group_data.items():
            if hasattr(group, key) and value is not None:
                setattr(group, key, value)
        self.db.commit()
        self.db.refresh(group)
        return group

    def delete(self, group: AgentGroup) -> bool:
        self.db.delete(group)
        self.db.commit()
        return True
