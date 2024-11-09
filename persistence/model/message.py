from alchemical import Model
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Message(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    team_id: Mapped[int] = mapped_column(ForeignKey('team.id'), nullable=False)
    team: Mapped["Team"] = relationship("Team", back_populates="messages")

    def save(self):
        MessageRepository.save(self)

    def delete(self):
        MessageRepository.delete(self)


from persistence.repository.message import MessageRepository
from persistence.model.team import Team
