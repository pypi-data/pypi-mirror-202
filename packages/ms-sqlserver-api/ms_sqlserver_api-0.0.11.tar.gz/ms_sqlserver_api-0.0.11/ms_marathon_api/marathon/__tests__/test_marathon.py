import unittest
from unittest.mock import Mock, patch

from ms_marathon_api.marathon.api import SQLMarathon

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


class MarathonTestSuite(unittest.TestCase):
    @patch("ms_marathon_api.sql_server.connection.pyodbc")
    def test_SQLMarathon_create_connection_to_database_when_is_instantiated(
        self,
        pyodbc_mock,
    ):
        pyodbc_mock = generate_pyodbc_mock(pyodbc_mock)
        SQLMarathon(
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

    @patch("ms_marathon_api.marathon.api.execute_query")
    @patch("ms_marathon_api.sql_server.connection.pyodbc")
    def test_SQLMarathon_migrate_table1_generate_correct_export_query(
        self,
        pyodbc_mock,
        execute_query_mock,
    ):
        pyodbc_mock = generate_pyodbc_mock(pyodbc_mock)
        marathon_api = SQLMarathon(
            driver_name=DRIVER_NAME,
            server_name=SERVER_NAME,
            database_name=DATABASE_NAME,
            database_username=DATABASE_USERNAME,
            database_password=DATABASE_PASSWORD,
            timeout=TIMEOUT,
        )
        expected_export_query = "INSERT INTO TABLE1 (id, name) VALUES ('1','John'),('2','Jane'),('3','Bob')"  # noqa: E501

        marathon_api.migrate_table1()

        execute_query_mock.assert_called_once_with(expected_export_query)
