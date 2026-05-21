import os
from pathlib import Path
from database import SessionLocal
from models import UserPhoto

# Configuración
UPLOAD_FOLDER = Path("uploads")

def clean_orphaned_files():
    # 1. Obtener todos los nombres de archivo registrados en la base de datos
    db = SessionLocal()
    try:
        registered_photos = {photo.photo for photo in db.query(UserPhoto).all()}
    finally:
        db.close()

    # 2. Iterar sobre los archivos en la carpeta uploads
    deleted_count = 0
    for file_path in UPLOAD_FOLDER.iterdir():
        if file_path.is_file():
            # Si el archivo no está en el set de fotos registradas, borrarlo
            if file_path.name not in registered_photos:
                print(f"Borrando archivo huérfano: {file_path.name}")
                file_path.unlink()
                deleted_count += 1
    
    print(f"Limpieza completada. Se eliminaron {deleted_count} archivos.")

if __name__ == "__main__":
    clean_orphaned_files()