try:
    import pyodbc
except ImportError:
    from types import SimpleNamespace

    pyodbc = SimpleNamespace()
    pyodbc.connect = lambda s: SimpleNamespace(cursor=lambda: None)


class SQLServer:
    def __init__(
        self,
        driver_name="ODBC Driver 17 for SQL Server",
        server_name="",
        database_name="",
        database_username="",
        database_password="",
        timeout=30,
    ) -> None:
        self.driver_name = driver_name
        self.server_name = server_name
        self.database_name = database_name
        self.database_username = database_username
        self.database_password = database_password
        self.timeout = timeout

        self.cursor = self.initialize_connection()

    def initialize_connection(self):
        cnxn = pyodbc.connect(
            f"DRIVER={self.driver_name};"
            f"SERVER={self.server_name};"
            f"DATABASE={self.database_name};"
            f"UID={self.database_username};"
            f"PWD={self.database_password};"
            f"Connection Timeout={self.timeout};"
        )

        cursor = cnxn.cursor()

        return cursor

    def execute_query(self, query):
        self.cursor.execute(query)

        return self.cursor.fetchall()
