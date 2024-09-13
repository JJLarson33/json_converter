import sqlite3


# Class object for database connection for the purpose of caching the connection
# and keeping the program efficient without a need to re-open a connection
# in every function in the main method.
class ConnManager:
    # Class-level variable to cache the connection
    _connection = None

    # Class method to create the database connection if there isn't one
    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            # If no database connection, create one connecting to 'this_database.db'
            # and return connection object
            cls._connection = sqlite3.connect("this_database.db")
        return cls._connection

    # Class method to execute commit changes to database with
    # given string queries and parameters optional
    @classmethod
    def execute_query(cls, query, params=None):
        # Reuse the cached connection
        connection = cls.get_connection()
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()

    # Class method to execute fetchall queries to database
    # with given string queries and parameters optional
    @classmethod
    def fetch_data(cls, query, params=None):
        # Reuse the cached connection
        connection = cls.get_connection()
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()

    # Class method to close connection
    @classmethod
    def close_connection(cls):
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None
