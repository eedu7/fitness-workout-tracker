from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("category.id"))
    muscle_group_id: Mapped[str] = mapped_column(Integer, ForeignKey("muscle_group.id"))

    def __repr__(self):
        return f"<Exercise(id={self.id}, name={self.name}, category={self.category_id}, muscle_group={self.muscle_group_id})>"

    def __str__(self):
        return self.__repr__()
