from flask import g
from sqlalchemy import func

from persistence.model.school import School
from .user import UserRepository
from persistence.repository import filter


class SchoolRepository:
    @staticmethod
    def search(query: str, ascending: bool, *extra_filters):
        """
        search in PostRepository

        :param query: the query
        :param ascending: if you want it ascending
        :param extra_filters: list of filters in this format: Table.column == stuff ("," for and, "|" or)
        :return: list of search results
        """

        statement = filter(School.school_name.like(f"%{query}%")
                           | School.address.like(f"%{query}%")
                           | School.contact_name.like(f"%{query}%")
                           | School.contact_email.like(f"%{query}%")
                           , *extra_filters)

        if ascending:
            statement = statement.order_by(School.id)
        else:
            statement = statement.order_by(School.id.desc())

        return g.session.scalars(statement)

    @staticmethod
    def find_by_id(school_id):
        statement = (
            School
            .select()
            .where(School.id == school_id)
        )

        return g.session.scalar(statement)

    @staticmethod
    def find_all():
        statement = (
            School
            .select().order_by(School.school_name)
        )

        return g.session.scalars(statement).all()

    @staticmethod
    def find_by_name(name):
        name = name.lower()
        statement = (
            School
            .select()
            .where(func.lower(School.school_name) == name)
        )

        return g.session.scalar(statement)

    @staticmethod
    def delete(school):
        g.session.delete(school)
        g.session.commit()

    @staticmethod
    def save(school):
        g.session.add(school)
        g.session.commit()
