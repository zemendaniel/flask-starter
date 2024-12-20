from flask import g
from select import select
from sqlalchemy import func
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

        statement = filter(School, School.school_name.ilike(f"%{query}%")
                           | School.address.ilike(f"%{query}%")
                           | School.contact_name.ilike(f"%{query}%")
                           | School.contact_email.ilike(f"%{query}%"),
                           *extra_filters)

        if ascending:
            statement = statement.order_by(School.school_name)
        else:
            statement = statement.order_by(School.school_name.desc())

        return g.session.scalars(statement).all()

    @staticmethod
    def application_form_criteria(choice):
        if choice == '0': return None
        if choice == '1':
            return School.application_form == None
        if choice == '2':
            return School.application_form != None

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

    @staticmethod
    def find_by_user_id(user_id):
        statement = (
            School.select().where(School.user_id == user_id)
        )
        return g.session.scalar(statement)

    @staticmethod
    def count_of_schools():
        return g.session.scalar(func.count(School.id))


from persistence.model.school import School
