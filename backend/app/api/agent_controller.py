from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_admin
from app.models.user import User
from app.schemas.agent_schemas import (
    AgentCreate, AgentUpdate, AgentResponse,
    AgentGroupCreate, AgentGroupUpdate, AgentGroupResponse
)
from app.repositories.agent_repository import AgentRepository, AgentGroupRepository
from app.services.excel_service import ExcelService

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post("/", response_model=AgentResponse)
def create_agent(
    agent_data: AgentCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new agent"""
    agent_repository = AgentRepository(db)
    
    try:
        agent = agent_repository.create_agent(agent_data.dict())
        return AgentResponse.from_orm(agent)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[AgentResponse])
def get_agents(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all agents"""
    agent_repository = AgentRepository(db)
    agents = agent_repository.get_all_agents(skip, limit)
    return [AgentResponse.from_orm(agent) for agent in agents]


@router.get("/active", response_model=List[AgentResponse])
def get_active_agents(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get active agents"""
    agent_repository = AgentRepository(db)
    agents = agent_repository.get_active_agents(skip, limit)
    return [AgentResponse.from_orm(agent) for agent in agents]


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(
    agent_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get agent by ID"""
    agent_repository = AgentRepository(db)
    agent = agent_repository.get_by_id(agent_id)
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    return AgentResponse.from_orm(agent)


@router.put("/{agent_id}", response_model=AgentResponse)
def update_agent(
    agent_id: str,
    agent_data: AgentUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update agent"""
    agent_repository = AgentRepository(db)
    
    try:
        agent = agent_repository.get_by_id(agent_id)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )
        
        updated_agent = agent_repository.update_agent(agent, agent_data.dict(exclude_unset=True))
        return AgentResponse.from_orm(updated_agent)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{agent_id}")
def delete_agent(
    agent_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete agent"""
    agent_repository = AgentRepository(db)
    
    try:
        agent = agent_repository.get_by_id(agent_id)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )
        
        agent_repository.delete_agent(agent)
        return {"message": "Agent deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{agent_id}/leads-count")
def get_agent_leads_count(
    agent_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get leads count for an agent"""
    agent_repository = AgentRepository(db)
    count = agent_repository.get_agent_leads_count(agent_id)
    return {"agent_id": agent_id, "leads_count": count}


# Agent Groups
@router.post("/groups/", response_model=AgentGroupResponse)
def create_agent_group(
    group_data: AgentGroupCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new agent group"""
    group_repository = AgentGroupRepository(db)
    
    try:
        group = group_repository.create(group_data.dict())
        return AgentGroupResponse.from_orm(group)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/groups/", response_model=List[AgentGroupResponse])
def get_agent_groups(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all agent groups"""
    group_repository = AgentGroupRepository(db)
    groups = group_repository.get_all(skip, limit)
    return [AgentGroupResponse.from_orm(group) for group in groups]


@router.get("/groups/{group_id}", response_model=AgentGroupResponse)
def get_agent_group(
    group_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get agent group by ID"""
    group_repository = AgentGroupRepository(db)
    group = group_repository.get_by_id(group_id)
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent group not found"
        )
    
    return AgentGroupResponse.from_orm(group)


@router.put("/groups/{group_id}", response_model=AgentGroupResponse)
def update_agent_group(
    group_id: str,
    group_data: AgentGroupUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update agent group"""
    group_repository = AgentGroupRepository(db)
    
    try:
        group = group_repository.get_by_id(group_id)
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent group not found"
            )
        
        updated_group = group_repository.update(group, group_data.dict(exclude_unset=True))
        return AgentGroupResponse.from_orm(updated_group)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/groups/{group_id}")
def delete_agent_group(
    group_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete agent group"""
    group_repository = AgentGroupRepository(db)
    
    try:
        group = group_repository.get_by_id(group_id)
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent group not found"
            )
        
        group_repository.delete(group)
        return {"message": "Agent group deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# Bulk import agents
@router.post("/import")
async def import_agents(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Import agents from Excel file"""
    excel_service = ExcelService()
    agent_repository = AgentRepository(db)
    
    try:
        file_content = await file.read()
        agents_data = excel_service.parse_excel_file(file_content)
        
        created_agents = []
        for agent_data in agents_data:
            try:
                agent = agent_repository.create_agent(agent_data)
                created_agents.append(agent)
            except Exception as e:
                # Continue with next agent if one fails
                continue
        
        return {
            "message": f"Successfully imported {len(created_agents)} agents",
            "imported_count": len(created_agents),
            "agents": [agent.id for agent in created_agents]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/sample/download")
async def download_agent_sample():
    """Download sample Excel sheet for agent import"""
    excel_service = ExcelService()
    
    try:
        sample_data = excel_service.generate_sample_agent_sheet()
        
        return StreamingResponse(
            iter([sample_data]),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=sample_agents.xlsx"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
