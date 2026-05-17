from fastapi import APIRouter, status, Depends, Response, Request
from models.authentication_models import User, UserLogin, ForgotPasswordRequest, ResetPasswordRequest
from controllers.authentication_controller import register, login, logout
from controllers.authentication_controller import refresh_token, forgot_password, reset_password
from middleware.authentication_middleware import get_valid_token

router = APIRouter()

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_route(user: User, response: Response):
    return await register(user, response)

@router.post('/login', status_code=status.HTTP_200_OK)
async def login_route(userLogin: UserLogin, response: Response):
    return await login(userLogin, response)

@router.post('/logout', status_code=status.HTTP_200_OK)
async def logout_route(response: Response, token: str = Depends(get_valid_token)):
    return await logout(token, response)

@router.post('/refresh-token', status_code=status.HTTP_200_OK)
async def refresh_token_route(request: Request, response: Response):
    refresh_token_val = request.cookies.get("refreshToken")
    if not refresh_token_val:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Refresh token no encontrado en las cookies.")
    return await refresh_token(refresh_token_val, response)

@router.post('/forgot-password', status_code=status.HTTP_200_OK)
async def forgot_password_route(request: ForgotPasswordRequest):
    return await forgot_password(request.email)

@router.post('/reset-password', status_code=status.HTTP_200_OK)
async def reset_password_route(request: ResetPasswordRequest):
    return await reset_password(request.token, request.new_password)
