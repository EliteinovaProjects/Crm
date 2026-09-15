from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_admin
from app.models.user import User
from app.core.id_generator import generate_id
from app.services.excel_service import ExcelService

router = APIRouter(prefix="/toolbox/resources", tags=["Toolbox Resources"])


# Sound Library
@router.post("/sound-library")
def create_sound(
    sound_name: str,
    file_url: str,
    description: str = None,
    duration: str = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new sound library entry"""
    from app.models.sound_library import SoundLibrary
    
    sound = SoundLibrary(
        id=generate_id("SND", 6),
        sound_name=sound_name,
        file_url=file_url,
        description=description,
        duration=duration
    )
    db.add(sound)
    db.commit()
    db.refresh(sound)
    
    return {
        "id": sound.id,
        "sound_name": sound.sound_name,
        "file_url": sound.file_url,
        "description": sound.description,
        "duration": sound.duration,
        "created_at": sound.created_at.isoformat()
    }


@router.get("/sound-library")
def get_sound_library(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all sounds in library"""
    from app.models.sound_library import SoundLibrary
    
    sounds = db.query(SoundLibrary).offset(skip).limit(limit).all()
    
    return [
        {
            "id": sound.id,
            "sound_name": sound.sound_name,
            "file_url": sound.file_url,
            "description": sound.description,
            "duration": sound.duration,
            "created_at": sound.created_at.isoformat()
        }
        for sound in sounds
    ]


@router.get("/sound-library/{sound_id}")
def get_sound(
    sound_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get sound by ID"""
    from app.models.sound_library import SoundLibrary
    
    sound = db.query(SoundLibrary).filter(SoundLibrary.id == sound_id).first()
    if not sound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sound not found"
        )
    
    return {
        "id": sound.id,
        "sound_name": sound.sound_name,
        "file_url": sound.file_url,
        "description": sound.description,
        "duration": sound.duration,
        "created_at": sound.created_at.isoformat()
    }


@router.delete("/sound-library/{sound_id}")
def delete_sound(
    sound_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete sound from library"""
    from app.models.sound_library import SoundLibrary
    
    sound = db.query(SoundLibrary).filter(SoundLibrary.id == sound_id).first()
    if not sound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sound not found"
        )
    
    db.delete(sound)
    db.commit()
    
    return {"message": "Sound deleted successfully"}


# SMS Templates (already handled in sms_template_controller, but can be accessed here too)
@router.get("/sms-templates")
def get_sms_templates(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all SMS templates"""
    from app.models.sms_template import SMSTemplate
    
    templates = db.query(SMSTemplate).offset(skip).limit(limit).all()
    
    return [
        {
            "id": template.id,
            "template_name": template.template_name,
            "template_content": template.template_content,
            "created_at": template.created_at.isoformat()
        }
        for template in templates
    ]


@router.post("/sms-templates")
def create_sms_template(
    template_name: str,
    template_content: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new SMS template"""
    from app.models.sms_template import SMSTemplate
    
    template = SMSTemplate(
        id=generate_id("SMS", 6),
        template_name=template_name,
        template_content=template_content
    )
    db.add(template)
    db.commit()
    db.refresh(template)
    
    return {
        "id": template.id,
        "template_name": template.template_name,
        "template_content": template.template_content,
        "created_at": template.created_at.isoformat()
    }


# Agents Bulk Import (already handled in agent_controller, but can be accessed here too)
@router.post("/agents/bulk-import")
async def bulk_import_agents(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Bulk import agents from Excel file"""
    excel_service = ExcelService()
    from app.repositories.agent_repository import AgentRepository
    
    try:
        file_content = await file.read()
        agents_data = excel_service.parse_excel_file(file_content)
        
        agent_repository = AgentRepository(db)
        created_agents = []
        
        for agent_data in agents_data:
            try:
                agent = agent_repository.create_agent(agent_data)
                created_agents.append(agent)
            except Exception as e:
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


@router.get("/agents/sample-download")
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
