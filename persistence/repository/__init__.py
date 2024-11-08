def filter(table, *args):
    """
        filter filters stuff

        :param table: the table in witch to filter
        :param args: list of filters in this format: Table.column == stuff ("," for and, "|" or)
        :return: a statement that filters stuff you just have tu run it like: g.session.scalars(result of this filter)
        """
    statement = (
        table
        .select()
    )
    for arg in args:
        statement = statement.where(arg)

    return statement
