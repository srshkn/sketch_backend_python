
from src.db import Base
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID, TEXT
import uuid
from sqlalchemy.orm import Mapped, mapped_column


# Таблица пользователей
class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(TEXT, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
