from fastapi import APIRouter, Depends, status
from models.user_models import UserUpdate
from controllers.users_controller import (
    get_user_profile,
    update_user_profile,
    delete_user_profile,
    get_user_by_id
)
from middleware.authentication_middleware import get_valid_token

router = APIRouter()

@router.get("/profile", status_code=status.HTTP_200_OK)
async def read_profile(token: str = Depends(get_valid_token)):
    return await get_user_profile(token)

@router.put("/profile", status_code=status.HTTP_200_OK)
async def update_profile(data: UserUpdate, token: str = Depends(get_valid_token)):
    return await update_user_profile(token, data)

@router.delete("/profile", status_code=status.HTTP_200_OK)
async def delete_profile(token: str = Depends(get_valid_token)):
    return await delete_user_profile(token)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def read_user_by_id(id: str, token: str = Depends(get_valid_token)):
    return await get_user_by_id(id, token)