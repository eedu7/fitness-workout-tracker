from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class MuscleGroup(Base):
    __tablename__ = "muscle_group"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"<MuscleGroup: ID={self.id}, Name={self.name}>"

    def __str__(self) -> str:
        return self.__repr__()
