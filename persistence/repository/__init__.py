from sqlalchemy import or_, and_


def filter(table, *args):
    """
    filter function to generate a SQLAlchemy statement with dynamic filters and joins.

    :param table: the main table (model) to filter on.
    :param args: list of filters in this format: Table.column == value ("," for and, "|" for or).
    :return: a SQLAlchemy Select statement with the applied filters.
    """
    # Start building the statement with a select on the main table
    statement = table.select()

    for arg in args:
        if arg is not None:
            if isinstance(arg, Language):
                statement = statement.join(Team.language)

            statement = statement.where(arg)

    return statement


from persistence.model.team import Team
from persistence.model.language import Language

