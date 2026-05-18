from fastapi import HTTPException, status, Depends, Request
from config.db import db
from controllers.authentication_controller import security

async def get_valid_token(request: Request) -> str:
    token = request.cookies.get("accessToken")
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se proporcionó token de acceso."
        )

    token_revoked = await db.revoked_tokens.find_one({"token": token})
    if token_revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no válido o sesión expirada."
        )
    return token


