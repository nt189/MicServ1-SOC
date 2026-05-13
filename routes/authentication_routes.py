from fastapi import APIRouter, status, Depends
from models.authentication_models import User, UserLogin
from controllers.authentication_controller import register, login, logout
from controllers.authentication_controller import refresh_Token, forgot_password
from middleware.authentication_middleware import get_valid_token

router = APIRouter()

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_route(user: User):
    return await register(user)

@router.post('/login', status_code=status.HTTP_200_OK)
async def login_route(userLogin: UserLogin):
    return await login(userLogin)

@router.post('/logout', status_code=status.HTTP_200_OK)
async def logout_route(token: str = Depends(get_valid_token)):
    return await logout(token)

@router.post('/refresh-token', status_code=status.HTTP_200_OK)
async def refresh_token_route(refresh_token: str):
    return await refresh_Token(refresh_token)

@router.post('/forgot-password', status_code=status.HTTP_200_OK)
async def forgot_password_route(email: str):
    return await forgot_password(email)
