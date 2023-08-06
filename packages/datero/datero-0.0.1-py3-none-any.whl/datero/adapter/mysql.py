"""MySQL database queries"""

class MySQL:
    """MySQL database queries"""

    @staticmethod
    def schema_list_table():
        """Command to create foreign table which will return schemas list"""
        return """
            CREATE FOREIGN TABLE IF NOT EXISTS {full_table_name} (schema_name TEXT)
            SERVER {server}
            OPTIONS (dbname 'information_schema', table_name 'schemata')
        """

    @staticmethod
    def table_list_table():
        """Command to create foreign table which will return tables list"""
        return  """
            CREATE FOREIGN TABLE IF NOT EXISTS {full_table_name} (table_schema TEXT, table_name TEXT, table_type TEXT)
            SERVER {server}
            OPTIONS (dbname 'information_schema', table_name 'tables')
        """

    @staticmethod
    def schema_list():
        """Query to return schemas list"""
        return  """
            SELECT tab.schema_name      AS schema_name
              FROM {full_table_name}    tab
             WHERE tab.schema_name      NOT IN ('mysql', 'sys', 'information_schema', 'performance_schema')
        """

    @staticmethod
    def table_list():
        """Query to return tables list"""
        return  """
            SELECT tab.table_schema     AS table_schema
                 , tab.table_name       AS table_name
                 , tab.table_type       AS table_type
              FROM {full_table_name}    tab
             WHERE tab.table_schema     NOT IN ('mysql', 'sys', 'information_schema', 'performance_schema')
               AND tab.table_type       IN ('BASE TABLE', 'VIEW');
        """
