from flask import g
from sqlalchemy import func


class CategoryRepository:
    @staticmethod
    def find_by_id(category_id):
        return g.session.scalar(Category.select().where(Category.id == category_id))

    @staticmethod
    def find_all():
        return g.session.scalars(Category.select()).all()

    @staticmethod
    def save(category):
        g.session.add(category)
        g.session.commit()

    @staticmethod
    def delete(category):
        g.session.delete(category)
        g.session.commit()

    @staticmethod
    def find_by_name(name):
        name = name.lower()
        statement = (
            Category
            .select()
            .where(func.lower(Category.name) == name)
        )

        return g.session.scalar(statement)


from persistence.model.category import Category
