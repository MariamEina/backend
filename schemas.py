from pydantic import BaseModel # type: ignore


class UserPhotoResponse(BaseModel):
    id: int
    nia: str
    dni: str
    photo: str

    class Config:
        from_attributes = True