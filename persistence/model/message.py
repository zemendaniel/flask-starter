from alchemical import Model
from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Message(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String(4096), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    team_id: Mapped[int] = mapped_column(ForeignKey('team.id'), nullable=False)
    team: Mapped["Team"] = relationship("Team", back_populates="messages")
    sender_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    sender: Mapped["User"] = relationship("User")

    def save(self):
        MessageRepository.save(self)

    def delete(self):
        MessageRepository.delete(self)

    @property
    def sender_name(self):
        if self.sender:
            return self.sender.name
        return "Törölt felhasználó"


from persistence.repository.message import MessageRepository
from persistence.model.team import Team
