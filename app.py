from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from routes import authentication_routes, healthCheck_routes
from routes import users_routes
from config.db import check_db_connection

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

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

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

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
# app.include_router(guest.router, prefix="/api/guest", tags=["Usuarios Invitados"])