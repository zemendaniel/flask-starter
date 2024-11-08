from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import User


class Team(User):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    team_name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)

    name1: Mapped[str] = mapped_column(String(64), nullable=False)
    year1: Mapped[int] = mapped_column(Integer, nullable=False)
    name2: Mapped[str] = mapped_column(String(64), nullable=False)
    year2: Mapped[int] = mapped_column(Integer, nullable=False)
    name3: Mapped[str] = mapped_column(String(64), nullable=False)
    year3: Mapped[int] = mapped_column(Integer, nullable=False)
    name_extra: Mapped[str] = mapped_column(String(64), nullable=True)
    year_extra: Mapped[int] = mapped_column(Integer, nullable=True)
    teachers: Mapped[str] = mapped_column(String(255), nullable=False)

    language_id: Mapped[int] = mapped_column(ForeignKey('language.id'), nullable=True)
    language: Mapped["Language"] = relationship()

    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=False)
    category: Mapped["Category"] = relationship()

    school_id: Mapped[int] = mapped_column(ForeignKey('school.id'), nullable=True)
    school: Mapped["School"] = relationship()

    school_approved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    admin_approved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    declared_incomplete: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    @property
    def ready(self) -> bool:
        return (self.school_approved and self.admin_approved and (not self.declared_incomplete) and self.school_id
                and self.language_id)

    def team_form_update(self, form):
        self.name1 = form.name1.data.strip()
        self.name2 = form.name2.data.strip()
        self.name3 = form.name3.data.strip()
        self.year1 = form.year1.data
        self.year2 = form.year2.data
        self.year3 = form.year3.data
        self.teachers = form.teachers.data.strip()
        self.language_id = form.language_id.data
        self.category_id = form.category_id.data
        self.school_id = form.school_id.data