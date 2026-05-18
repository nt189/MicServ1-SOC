from models.guest_models import GuestSession, GuestFeatures
import uuid

async def create_guest_session() -> GuestSession:
    guest_id = str(uuid.uuid4())
    session_token = str(uuid.uuid4())
    return GuestSession(
        guestId=guest_id,
        sessionToken=session_token,
        expiresIn=3600
    )

async def get_guest_features() -> GuestFeatures:
    return GuestFeatures(
        features=[
            "Explorar catálogo",
            "Ver artículos destacados",
            "Acceso limitado a foros"
        ]
    )
