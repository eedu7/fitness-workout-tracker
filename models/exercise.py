from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(255))
    muscle_group: Mapped[str] = mapped_column(String(255))

    def __repr__(self):
        return f"<Exercise(id={self.id}, name={self.name}, category={self.category}, muscle_group={self.muscle_group})>"

    def __str__(self):
        return self.__repr__()
