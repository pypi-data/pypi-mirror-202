from gc_google_services_api.bigquery import execute_query

from ms_marathon_api.marathon.parsers.parse_table1 import \
    build_table1_export_query
from ms_marathon_api.marathon.queries.bigquery import INSERT_TABLE1
from ms_marathon_api.marathon.queries.sql_server import SELECT_ALL_TABLE1
from ms_marathon_api.sql_server.connection import SQLServer


class SQLMarathon(SQLServer):
    def migrate_table1(self):
        data_to_migrate = self.execute_query(query=SELECT_ALL_TABLE1)
        export_query = build_table1_export_query(data=data_to_migrate)

        execute_query(INSERT_TABLE1.format(values=export_query))
