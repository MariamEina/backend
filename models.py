<<<<<<< HEAD
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database import Base


class UserPhoto(Base):
    __tablename__ = "user_photos"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    nia: Mapped[str] = mapped_column(
        String(50)
    )

    dni: Mapped[str] = mapped_column(
        String(50)
    )

    photo: Mapped[str] = mapped_column(
        String(255)
=======
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database import Base


class UserPhoto(Base):
    __tablename__ = "user_photos"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    nia: Mapped[str] = mapped_column(
        String(50)
    )

    dni: Mapped[str] = mapped_column(
        String(50)
    )

    photo: Mapped[str] = mapped_column(
        String(255)
>>>>>>> 8daf375c1bac7d03115267e4ba65a66ef7d53413
    )