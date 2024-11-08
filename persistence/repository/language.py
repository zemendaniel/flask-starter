from flask import g
from sqlalchemy import func


class LanguageRepository:
    @staticmethod
    def find_by_id(category_id):
        return g.session.scalar(Language.select().where(Language.id == category_id))

    @staticmethod
    def find_all():
        return g.session.scalars(Language.select()).all()

    @staticmethod
    def find_by_name(name):
        name = name.lower()
        statement = (
            Language
            .select()
            .where(func.lower(Language.name) == name)
        )

        return g.session.scalar(statement)

    @staticmethod
    def save(language):
        g.session.add(language)
        g.session.commit()

    @staticmethod
    def delete():
        g.session.delete(language)
        g.session.commit()


from persistence.model.language import Language
