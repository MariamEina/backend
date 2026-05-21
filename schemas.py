from pydantic import BaseModel, computed_field

class UserPhotoResponse(BaseModel):
    id: int
    nia: str
    dni: str
    photo: str

    @computed_field
    def photo_url(self) -> str:
        return f"/uploads/{self.photo}"