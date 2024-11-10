from flask import g
from . import filter

from persistence.model.language import Language


class MessageRepository:
    @staticmethod
    def search(query: str, *extra_filters):
        """
        search in PostRepository

        :param query: the query
        :param extra_filters: list of filters in this format: Table.column == stuff ("," for and, "|" or)
        :return: list of search results
        """

        statement = filter(Message, Message.team.has(Team.team_name.like(f"%{query}%"))
                           | Message.sender.has(User.name.like(f"%{query}%")),
                            *extra_filters)

        statement = statement.order_by(Message.id.desc())

        return g.session.scalars(statement).all()

    @staticmethod
    def find_by_id(message_id):
        return g.session.scalar(Message.select().where(Message.id == message_id))

    @staticmethod
    def find_all():
        return g.session.scalars(Message.select().order_by(Message.id.desc())).all()

    @staticmethod
    def save(message):
        g.session.add(message)
        g.session.commit()

    @staticmethod
    def delete(message):
        g.session.delete(message)
        g.session.commit()


from persistence.model.message import Message
from persistence.model.team import Team
from  persistence.model.user import User
