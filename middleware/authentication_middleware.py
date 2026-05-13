from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials

from config.db import db
from controllers.authentication_controller import security


async def get_valid_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    token_revoked = await db.revoked_tokens.find_one({"token": token})
    if token_revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no válido o sesión expirada."
        )
    return token
