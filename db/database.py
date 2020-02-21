import sqlite3
from sqlite3 import Error


class Db:
    def __init__(self, name):
        self.name = name
        print("Nome del database: *", self.name, "*...")

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database
            If the database doesn't exist it will create a new one
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
            return conn
        except Error as e:
            print(e)

        return conn

    def create_table(self, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

# if __name__ == '__main__':
#     create_connection(r"C:\sqlite\db\pythonsqlite.db")