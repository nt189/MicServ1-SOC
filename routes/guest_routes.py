from fastapi import APIRouter, status
from controllers.guest_controller import create_guest_session, get_guest_features
from models.guest_models import GuestSession, GuestFeatures 

router = APIRouter(prefix="/api/guest", tags=["Usuarios Invitados"])

@router.post("/session", status_code=status.HTTP_201_CREATED, response_model=GuestSession)
async def create_session():
    return await create_guest_session()

@router.get("/features", status_code=status.HTTP_200_OK, response_model=GuestFeatures)
async def read_features():
    return await get_guest_features()
