from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routes import authentication_routes, healthCheck_routes
from routes import users_routes, guest_routes
from fastapi.middleware.cors import CORSMiddleware
from config.db import check_db_connection

app = FastAPI(
    title="MicServ1-SOC - Identity Service",
    description="Microservicio REST para la Gestión de Identidad y Clientes",
    version="1.0.0",
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Datos de entrada inválidos", "errors": exc.errors()},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healthCheck_routes.router, tags=["Health Check"])
app.include_router(authentication_routes.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(users_routes.router, prefix="/api/users", tags=["Gestión de Usuarios"])
app.include_router(guest_routes.router, prefix="/api/guest", tags=["Usuarios Invitados"])


# app.include_router(guest.router, prefix="/api/guest", tags=["Usuarios Invitados"])