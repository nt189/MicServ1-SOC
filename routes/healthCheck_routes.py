from fastapi import APIRouter, HTTPException
from config.db import check_db_connection

router = APIRouter()

@router.get("/", tags=["Health Check"])
async def root():
    return {
        "service": "MicServ1-SOC - Identity Service",
        "status": "online",
        "description": "API operativa"
    }

@router.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy"}

@router.get("/db/connection/health", tags=["Health Check"])
async def db_health_check():
    is_connected = await check_db_connection()
    if is_connected:
        return {"status": "connected", "database": "MongoDB"}
    else:
        raise HTTPException(status_code=503, detail="Database connection failed")
