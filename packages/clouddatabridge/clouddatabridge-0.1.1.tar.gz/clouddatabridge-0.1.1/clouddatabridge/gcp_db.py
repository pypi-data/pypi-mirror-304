import pymysql
import time

class GCPMySQLConnection:
    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.db_connection = None

    def get_db_connection(self, max_retries=5, retry_delay=5):
        """
        Establish a connection to the database with retry logic.
        """
        if self.db_connection and self.db_connection.open:
            return self.db_connection

        retries = 0
        while retries < max_retries:
            try:
                self.db_connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    db=self.database,
                    port=self.port,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor,
                    ssl={"use": True}
                )
                return self.db_connection

            except pymysql.OperationalError as e:
                retries += 1
                print(f"OperationalError: {e}. Retrying {retries}/{max_retries}...")
                time.sleep(retry_delay)

        raise pymysql.OperationalError(f"Failed to connect to the database after {max_retries} retries.")

    def execute_query(self, query):
        """
        Execute a SQL query and fetch all rows.
        """
        try:
            connection = self.get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows
        except pymysql.MySQLError as e:
            print(f"MySQL Error: {e}")
        finally:
            self.close_connection()

    def close_connection(self):
        """
        Close the database connection.
        """
        if self.db_connection:
            self.db_connection.close()
            self.db_connection = None