from flask import g
from sqlalchemy import func
from persistence.repository.__init__ import filter
from io import BytesIO


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
            Team.name1.ilike(f"%{query}%")
            | Team.name2.ilike(f"%{query}%")
            | Team.name3.ilike(f"%{query}%")
            | Team.name_extra.ilike(f"%{query}%")
            | Team.teachers.ilike(f"%{query}%")
            | Team.language.has(Language.name.ilike(f"%{query}%"))  # Requires join on `Language`
            | Team.category.has(Category.name.ilike(f"%{query}%"))  # Requires join on `Category`
            | Team.school.has(School.school_name.ilike(f"%{query}%"))
            | Team.team_name.ilike(f"%{query}%"),
            *extra_filters  # Additional filters
        )

        if ascending:
            statement = statement.order_by(Team.team_name.asc())
        else:
            statement = statement.order_by(Team.team_name.desc())

        return g.session.scalars(statement).all()

    @staticmethod
    def completeness_criteria(value):
        if value == '0':
            return Team._declared_incomplete == True

        if value == '1':
            return Team.school_approved == True

        if value == '2':
            return Team.admin_approved == True

        return None

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

    @staticmethod
    def create_csv_file():
        teams = TeamRepository.find_all()
        if not teams:
            return None

        header_line = [';'.join(["Felhasználónév", "Csapatnév", "Első tag neve", "Első tag évfolyama", "Második tag neve",
                       "Második tag évfolyama", "Harmadik tag neve", "Harmadik tag évfolyama", "Póttag neve",
                       "Póttag évfolyama", "Felkészítő tanár(ok)", "Programnyelv", "Kategória", "Iskola neve",
                       "Iskola által jóváhagyva", "Szervező által jóváhagyva", "Hiánypótlásra szorul"])]
        team_lines = [team.to_csv_line() for team in teams]

        csv = "\n".join(header_line + team_lines)
        return BytesIO(csv.encode('utf-8'))

    @staticmethod
    def count_of_teams():

        return g.session.scalar(func.count(Team.id))

    @staticmethod
    def count_of_teams_by_school(school_name):
        condition = (
            Team.school.has(School.school_name == school_name)
        )
        return g.session.query(Team).filter(condition).count()

    @staticmethod
    def percentage_of_language(language_name):
        this_language_team = (
            Team.language.has(Language.name == language_name)
        )

        a = g.session.query(Team.id).filter(this_language_team).count()
        b = g.session.scalar(func.count(Team.id))
        if b == 0:
            return 0

        return round((a/b)*100, 2)

    @staticmethod
    def percentage_of_category(category_name):
        this_category_team = (
            Team.category.has(Category.name == category_name)
        )

        a = g.session.query(Team.id).filter(this_category_team).count()
        b = g.session.scalar(func.count(Team.id))
        if b == 0:
            return 0

        return round((a/b)*100, 2)

    @staticmethod
    def percentage_of_language_by_school(language_name, school_name):
        this_language = (
            Team.school.has(School.school_name == school_name)
                and Team.language.has(Language.name == language_name)
        )

        all_language = (
            Team.school.has(School.school_name == school_name)
        )
        a = g.session.query(Team.id).filter(this_language).count()
        b = g.session.query(Team.id).filter(all_language).count()

        if b == 0:
            return 0

        return round((a/b)*100, 2)


from ..model.category import Category
from ..model.language import Language
from ..model.school import School
from persistence.model.team import Team
