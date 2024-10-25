from alchemical import Model
from sqlalchemy import Integer, Text, Date
from sqlalchemy.orm import Mapped, mapped_column


class Post(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text(), nullable=False)
    date: Mapped[Date] = mapped_column(Date(), nullable=False)

    def form_update(self, form):
        self.content = form.content.data.strip()
        self.date = form.date.data

    def save(self):
        PostRepository.save(self)
        return self

    def delete(self):
        PostRepository.delete(self)


from persistence.repository.post import PostRepository
