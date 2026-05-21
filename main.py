import os
import shutil
import uuid

from fastapi import FastAPI
from fastapi import File
from fastapi import Form
from fastapi import UploadFile
from fastapi import HTTPException
from fastapi import Depends

from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

from database import Base
from database import SessionLocal
from database import engine

from models import UserPhoto
from schemas import UserPhotoResponse

# crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()

UPLOAD_FOLDER: str = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# servir imagenes
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


# db dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload", response_model=UserPhotoResponse)
async def upload_user_photo(
    nia: str = Form(...),
    dni: str = Form(...),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not photo.content_type or not photo.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Solo imagenes"
        )

    extension = os.path.splitext(photo.filename)[1]

    unique_filename = f"{uuid.uuid4()}{extension}"

    file_path = f"{UPLOAD_FOLDER}/{unique_filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    new_user = UserPhoto(
        nia=nia,
        dni=dni,
        photo=unique_filename
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user