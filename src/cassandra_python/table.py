"""
Class for handling Cassandra table operations.
"""

class CassandraTable:
    """
    Class for handling Cassandra table operations.
    """
    
    def __init__(self, session, keyspace, table_name):
        """
        Initialize the CassandraTable with a session, keyspace, and table name.
        
        :param session: Cassandra session object
        :param keyspace: Name of the keyspace
        :param table_name: Name of the table
        """
        self.session = session
        self.keyspace = keyspace
        self.table_name = table_name

    def create_table(self, schema):
        """
        Create a table with the given schema.
        
        :param schema: Table schema as a string
        """
        query = f"CREATE TABLE IF NOT EXISTS {self.keyspace}.{self.table_name} ({schema})"
        self.session.execute(query)

    def drop_table(self):
        """
        Drop the table.
        """
        query = f"DROP TABLE IF EXISTS {self.keyspace}.{self.table_name}"
        self.session.execute(query)

    def insert_data(self, data):
        """
        Insert data into the table.
        
        :param data: Data to insert as a dictionary
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {self.keyspace}.{self.table_name} ({columns}) VALUES ({placeholders})"
        self.session.execute(query, tuple(data.values()))

    def query_data(self, condition=""):
        """
        Query data from the table with an optional condition.
        
        :param condition: WHERE condition for the query
        :return: Result of the query
        """
        query = f"SELECT * FROM {self.keyspace}.{self.table_name}"
        if condition:
            query += f" WHERE {condition} ALLOW FILTERING"
        return self.session.execute(query)