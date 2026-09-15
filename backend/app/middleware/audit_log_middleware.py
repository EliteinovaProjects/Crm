from fastapi import Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.system_log import SystemLog
import time


async def audit_log_middleware(request: Request, call_next):
    start_time = time.time()
    
    # Get the original response
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log the request
    db = next(get_db())
    try:
        log_entry = SystemLog(
            endpoint=str(request.url.path),
            method=request.method,
            user_id=getattr(request.state, "user_id", None),
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            status_code=response.status_code,
            processing_time=process_time
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        db.rollback()
    finally:
        db.close()
    
    return response
