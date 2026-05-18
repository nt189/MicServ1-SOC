from pydantic import BaseModel

class GuestSession(BaseModel):
    guestId: str
    sessionToken: str
    expiresIn: int

class GuestFeatures(BaseModel):
    features: list[str]
