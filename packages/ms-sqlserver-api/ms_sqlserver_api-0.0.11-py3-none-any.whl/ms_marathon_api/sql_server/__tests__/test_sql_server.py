import unittest
from unittest.mock import Mock, patch

from ms_marathon_api.sql_server.connection import SQLServer

DRIVER_NAME = ("ODBC Driver 17 for SQL Server",)
SERVER_NAME = "TEST_SERVER"
DATABASE_NAME = "TEST_DB"
DATABASE_USERNAME = "TEST_DB_U"
DATABASE_PASSWORD = "TEST_DB_P"
TIMEOUT = 30


def generate_pyodbc_mock(pyodbc_mock):
    connect_mock = Mock()
    execute_mock = Mock()
    cursor_mock = Mock()
    execute_mock = Mock()

    cursor_mock.fetchall.return_value = [(1, "John"), (2, "Jane"), (3, "Bob")]
    cursor_mock.execute.return_value = execute_mock
    connect_mock.cursor.return_value = cursor_mock
    pyodbc_mock.connect.return_value = connect_mock

    return pyodbc_mock


class SQLServerTestSuite(unittest.TestCase):
    @patch("ms_marathon_api.sql_server.connection.pyodbc")
    def test_SQLServer_create_connection_to_database_when_is_instantiated(
        self,
        pyodbc_mock,
    ):
        pyodbc_mock = generate_pyodbc_mock(pyodbc_mock)
        SQLServer(
            driver_name=DRIVER_NAME,
            server_name=SERVER_NAME,
            database_name=DATABASE_NAME,
            database_username=DATABASE_USERNAME,
            database_password=DATABASE_PASSWORD,
            timeout=TIMEOUT,
        )

        pyodbc_mock.connect.assert_called_once_with(
            "DRIVER=('ODBC Driver 17 for SQL Server',);SERVER=TEST_SERVER;DATABASE=TEST_DB;UID=TEST_DB_U;PWD=TEST_DB_P;Connection Timeout=30;"  # noqa: E501
        )
        pyodbc_mock.connect().cursor.assert_called_once()

    @patch("ms_marathon_api.sql_server.connection.pyodbc")
    def test_SQLServer_execute_query_call_fetchall_from_cursor_connection(
        self,
        pyodbc_mock,
    ):
        pyodbc_mock = generate_pyodbc_mock(pyodbc_mock)
        sql_server_api = SQLServer(
            driver_name=DRIVER_NAME,
            server_name=SERVER_NAME,
            database_name=DATABASE_NAME,
            database_username=DATABASE_USERNAME,
            database_password=DATABASE_PASSWORD,
            timeout=TIMEOUT,
        )
        expected_results = [(1, "John"), (2, "Jane"), (3, "Bob")]
        query = "SELECT * FROM TABLE1"
        results = sql_server_api.execute_query(query)

        pyodbc_mock.connect().cursor().execute.assert_called_once_with(query)
        pyodbc_mock.connect().cursor().fetchall.assert_called_once()
        self.assertEqual(results, expected_results)
