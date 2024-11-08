from typing import List
from alchemical import Model
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Category(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)

    teams: Mapped[List["Team"]] = relationship()

    def save(self):
        CategoryRepository.save(self)

    def delete(self):
        CategoryRepository.delete(self)


from persistence.repository.category import CategoryRepository
