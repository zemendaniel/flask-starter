from alchemical import Model
from typing import List

from typing_extensions import Self

from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, InstanceState


class Team(Model):
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

    messages: Mapped[List["Message"]] = relationship("Message", back_populates="team", cascade="all, delete-orphan")
    has_unred_messages: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    language_id: Mapped[int | None] = mapped_column(ForeignKey('language.id'), nullable=True)
    language: Mapped["Language"] = relationship("Language", back_populates="teams")

    category_id: Mapped[int | None] = mapped_column(ForeignKey('category.id'), nullable=True)
    category: Mapped["Category"] = relationship("Category", back_populates="teams")

    school_id: Mapped[int | None] = mapped_column(ForeignKey('school.id'), nullable=True)
    school: Mapped["School"] = relationship()

    school_approved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    admin_approved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    declared_incomplete: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True, unique=True)
    user: Mapped["User"] = relationship("User", back_populates="team", uselist=False)

    @property
    def ready(self) -> bool:
        return (self.school_approved and self.admin_approved and (not self.declared_incomplete) and self.school_id
                and self.language_id)

    def team_form_update(self, form):
        team_name = form.team_name.data if hasattr(form, 'team_name') else None
        if team_name:
            self.team_name = team_name.strip()

        self.name1 = form.name1.data.strip()
        self.name2 = form.name2.data.strip()
        self.name3 = form.name3.data.strip()
        self.year1 = form.year1.data
        self.year2 = form.year2.data
        self.year3 = form.year3.data
        self.year_extra = form.year_extra.data
        self.name_extra = form.name_extra.data
        self.teachers = form.teachers.data.strip()

        language_id = form.language_id.data
        if language_id == 0:
            self.language_id = None
        else:
            self.language_id = language_id

        category_id = form.category_id.data
        if category_id == 0:
            self.category_id = None
        else:
            self.category_id = category_id

        school_id = form.school_id.data
        if school_id == 0:
            self.school_id = None
        else:
            self.school_id = school_id

    def save(self):
        TeamRepository.save(self)

    def delete(self):
        TeamRepository.delete(self)

    def to_csv_line(self):
        return (
            f"{self.user.name};{self.team_name};{self.name1};{self.year1};{self.name2};{self.year2};{self.name3};{self.year3};"
            f"{self.name_extra};{self.year_extra};{self.teachers};"
            f"{self.language.name if self.language else 'nincs'};"
            f"{self.category.name if self.category else 'nincs'};"
            f"{self.school.school_name if self.school else 'nincs'};"
            f"{'igen' if self.school_approved else 'nem'};"
            f"{'igen' if self.admin_approved else 'nem'};"
            f"{'igen' if self.declared_incomplete else 'nem'}"
        )


from persistence.repository.team import TeamRepository
from persistence.model.message import Message
