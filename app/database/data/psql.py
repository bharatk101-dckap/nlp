import pandas.io.sql as sqlio
from app.database.vizb.connection import db_connect


def psql_to_df(company_Id, query):
    """
    Returns data from psql in pandas dataframe format

    :param company_Id: Unique company key/ID
    :param query: SQL Query
    :return:
    """
    cur, conn = db_connect(company_Id)
    df = sqlio.read_sql_query(query, conn)
    return df


