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

    language_id: Mapped[int] = mapped_column(ForeignKey('language.id'), nullable=False)
    language: Mapped["Language"] = relationship()

    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=False)
    category: Mapped["Category"] = relationship()

    school_id: Mapped[int] = mapped_column(ForeignKey('school.id'), nullable=False)
    school: Mapped["School"] = relationship()

    school_approved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    admin_approved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    additional_info_needed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    @property
    def ready(self) -> bool:
        return self.school_approved and self.admin_approved and (not self.additional_info_needed)

    @staticmethod
    def create_team(form):
        team = Team()
        team.role = 'team'
        team.name1 = form.name1.data.strip()
        team.name2 = form.name2.data.strip()
        team.name3 = form.name3.data.strip()
        team.year1 = form.year1.data
        team.year2 = form.year2.data
        team.year3 = form.year3.data
        team.teachers = form.teachers.data.strip()
        team.language_id = form.language.data
        team.category_id = form.category.data
        team.school_id = form.school.data
