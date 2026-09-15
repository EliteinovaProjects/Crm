from typing import Any, Dict, Optional
from fastapi import HTTPException, status


def success_response(data: Any = None, message: str = "Success", status_code: int = 200) -> Dict:
    return {
        "status": "success",
        "message": message,
        "data": data,
        "status_code": status_code
    }


def error_response(message: str, status_code: int = 400, details: Any = None) -> Dict:
    return {
        "status": "error",
        "message": message,
        "details": details,
        "status_code": status_code
    }


def raise_http_exception(status_code: int, message: str, details: Any = None):
    raise HTTPException(
        status_code=status_code,
        detail=error_response(message, status_code, details)
    )
