from flask import g


class MessageRepository:
    @staticmethod
    def find_by_id(message_id):
        return g.session.scalar(Message.select().where(Message.id == message_id))

    @staticmethod
    def find_all():
        return g.session.scalars(Message.select().order_by(Message.id.desc())).all()

    @staticmethod
    def find_own_unread_amount():
        if g.role == "team":
            return g.user.team.messages.filter_by(read=False).count()
        return None

    @staticmethod
    def save(message):
        g.session.add(message)
        g.session.commit()

    @staticmethod
    def delete(message):
        g.session.delete(message)
        g.session.commit()


from persistence.model.message import Message
