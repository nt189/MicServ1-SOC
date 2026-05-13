from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config.db import check_db_connection

app = FastAPI(
    title="MicServ1-SOC - Identity Service",
    description="Microservicio REST para la Gestión de Identidad y Clientes",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
# app.include_router(users.router, prefix="/api/users", tags=["Gestión de Usuarios"])
# app.include_router(guest.router, prefix="/api/guest", tags=["Usuarios Invitados"])

@app.get("/", tags=["Health Check"])
async def root():
    return {
        "service": "MicServ1-SOC - Identity Service",
        "status": "online",
        "description": "API operativa"
    }

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy"}

@app.get("/db/connection/health", tags=["Health Check"])
async def db_health_check():
    is_connected = await check_db_connection()
    if is_connected:
        return {"status": "connected", "database": "MongoDB"}
    else:
        raise HTTPException(status_code=503, detail="Database connection failed")
