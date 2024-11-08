from typing import List

from sqlalchemy import Integer, String, BLOB, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from alchemical import Model


class School(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    school_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_name: Mapped[str] = mapped_column(String(128), nullable=False)
    contact_email: Mapped[str] = mapped_column(String(128), nullable=False)
    application_form: Mapped[bytes] = mapped_column(BLOB, nullable=True) # todo ha nincs akkor nem lehet csapatot jovahagyni, az edit oldalon lehessen utolag feltolteni

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True, unique=True)
    user: Mapped["User"] = relationship("User", back_populates="team", uselist=False)

    teams: Mapped[List["Team"]] = relationship(
        cascade="all, delete-orphan",
        back_populates="school",)

    def form_update(self, form):
        self.contact_name = form.contact_name.data.strip()
        self.contact_email = form.contact_email.data.strip()
        self.address = form.address.data.strip()
        self.school_name = form.school_name.data.strip()

    def save(self):
        SchoolRepository.save(self)

    def delete(self):
        SchoolRepository.delete(self)


from persistence.repository.school import SchoolRepository
