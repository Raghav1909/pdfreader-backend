from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    no_of_pages: Mapped[int] = mapped_column(nullable=True) 