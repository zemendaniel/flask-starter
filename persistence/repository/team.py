from flask import g
from sqlalchemy import func

from .user import UserRepository
from persistence.model.team import Team
from persistence.repository.__init__ import filter
from ..model.category import Category
from ..model.language import Language
from ..model.school import School


class TeamRepository:
    @staticmethod
    def search(query: str, ascending: bool, *extra_filters):
        """
        search in PostRepository

        :param query: the query
        :param ascending: if you want it ascending
        :param extra_filters: list of filters in this format: Table.column == stuff ("," for and, "|" or)
        :return: list of search results
        """

        statement = filter(
            Team,
            Team.name1.like(f"%{query}%")
            | Team.name2.like(f"%{query}%")
            | Team.name3.like(f"%{query}%")
            | Team.name_extra.like(f"%{query}%")
            | Team.teachers.like(f"%{query}%")
            | Team.language.has(Language.name.like(f"%{query}%"))  # Requires join on `Language`
            | Category.name.like(f"%{query}%")  # Requires join on `Category`
            | School.school_name.like(f"%{query}%")  # Requires join on `School`
            | Team.team_name.like(f"%{query}%"),
            *extra_filters  # Additional filters
        )

        if ascending:
            statement = statement.order_by(Team.id)
        else:
            statement = statement.order_by(Team.id.desc())

        return g.session.scalars(statement).all()

    @staticmethod
    def year_criteria(query):
        criteria = (Team.year1.like(f"%{query}%")
                    | Team.year2.like(f"%{query}%")
                    | Team.year3.like(f"%{query}%")
                    | Team.year_extra.like(f"%{query}%")
                    )

        return criteria

    @staticmethod
    def find_all():
        return g.session.scalars(Team.select().order_by(Team.id.desc())).all()

    @staticmethod
    def save(team):
        g.session.add(team)
        g.session.commit()

    @staticmethod
    def delete(team):
        g.session.delete(team)
        g.session.commit()

    @staticmethod
    def find_by_id(team_id):
        return g.session.scalar(Team.select().where(Team.id == team_id))

    @staticmethod
    def find_by_name(name):
        name = name.lower()
        statement = (
            Team
            .select()
            .where(func.lower(Team.team_name) == name)
        )

        return g.session.scalar(statement)
