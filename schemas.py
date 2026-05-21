<<<<<<< HEAD
from pydantic import BaseModel, computed_field

class UserPhotoResponse(BaseModel):
    id: int
    nia: str
    dni: str
    photo: str

    @computed_field
    def photo_url(self) -> str:
        return f"/uploads/{self.photo}"
=======
from pydantic import BaseModel # type: ignore


class UserPhotoResponse(BaseModel):
    id: int
    nia: str
    dni: str
    photo: str

    class Config:
        from_attributes = True
>>>>>>> 8daf375c1bac7d03115267e4ba65a66ef7d53413
