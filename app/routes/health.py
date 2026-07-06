from fastapi import APIRouter
from app.db import get_connection

router = APIRouter()

@router.get("/health")
def health_check():
    try:
        conn = get_connection()
        conn.close()

        return {
            "status": "ok",
            "database": "connected"
        }

    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "detail": str(e)
        }