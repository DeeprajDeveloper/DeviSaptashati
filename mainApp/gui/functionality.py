from mainApp.constants import (DataQueries as Query)
from utilities.sqlite_util import dql_fetch_all_rows
import config


def test_database_connection():
    results = dql_fetch_all_rows(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['common']['getTestQuery'], return_list=False)
    return results
