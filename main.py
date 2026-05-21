import os
import shutil
import uuid
from pathlib import Path
from typing import List, Generator

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
 

from database import Base, SessionLocal, engine
from models import UserPhoto
from schemas import UserPhotoResponse

# Configuración
UPLOAD_FOLDER: Path = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS: set[str] = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE: int = 2 * 1024 * 1024  # 2MB

# Crear tablas
Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Cambia esto si tu Angular usa otro puerto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
 

# Servir imágenes
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_FOLDER)), name="uploads")

# Dependencia para la base de datos con tipado
def get_db() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
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
) -> UserPhotoResponse:
    
    # 1. Validar extensión
    extension: str = Path(photo.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Formato no permitido")

    # 2. Validar tamaño
    real_file_size: int = 0
    # Leemos en trozos pequeños para no saturar la memoria RAM
    for chunk in photo.file:
        real_file_size += len(chunk)
        if real_file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="Archivo demasiado grande")
    
    photo.file.seek(0) # Reiniciar puntero

    # 3. Guardar archivo
    unique_filename: str = f"{uuid.uuid4()}{extension}"
    file_path: Path = UPLOAD_FOLDER / unique_filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        
        # 4. Guardar en BD
        new_user: UserPhoto = UserPhoto(nia=nia, dni=dni, photo=unique_filename)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user

    except Exception as e:
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error en servidor: {str(e)}")

@app.get("/photos", response_model=List[UserPhotoResponse])
def get_all_photos(db: Session = Depends(get_db)) -> List[UserPhotoResponse]:
    return db.query(UserPhoto).all()