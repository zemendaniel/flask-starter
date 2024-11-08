from flask import g
from persistence.model.school import School
from user import UserRepository
from persistence.repository import filter


class SchoolRepository(UserRepository):
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
