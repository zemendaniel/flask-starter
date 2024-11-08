from flask import g
from user import UserRepository
from persistence.model.team import Team
from persistence.repository.__init__ import filter


class TeamRepository(UserRepository):
    @staticmethod
    def search(query: str, ascending: bool, *extra_filters):
        """
        search in PostRepository

        :param query: the query
        :param ascending: if you want it ascending
        :param extra_filters: list of filters in this format: Table.column == stuff ("," for and, "|" or)
        :return: list of search results
        """

        statement = filter(Team, Team.name1.like(f"%{query}%")
                                          | Team.name2.like(f"%{query}%")
                                          | Team.name3.like(f"%{query}%")
                                          | Team.name_extra.like(f"%{query}%")
                                          | Team.teachers.like(f"%{query}%")
                                          | Team.language.like(f"%{query}%")
                                          | Team.category.like(f"%{query}%")
                                          | Team.school.like(f"%{query}%")
                                          | Team.team_name.like(f"%{query}%")
                                          | TeamRepository.year_criteria()
                                          , *extra_filters)

        if ascending:
            statement = statement.order_by(Team.id)
        else:
            statement = statement.order_by(Team.id.desc())

        return g.session.scalars(statement)

    @staticmethod
    def year_criteria(query):
        criteria = (Team.year1.like(f"%{query}%")
                    | Team.year2.like(f"%{query}%")
                    | Team.year3.like(f"%{query}%")
                    | Team.year_extra.like(f"%{query}%")
                    )

        return criteria

