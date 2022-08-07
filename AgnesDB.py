from datetime import datetime
from sqlite3 import DatabaseError
import mysql.connector
from IRepository import IRepository

class AgnesDB(IRepository):
    """
    Directly accesses local MySQL database for command CRUD
    """
    def __init__(self, host: str, user: str, password: str, database: str):
        self.last_quote_read = None
        try:
            self.__connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
        except DatabaseError as e:
            print("[Error]: Could not connect to database")
            raise e

        self.cursor = self.__connection.cursor()

    def give_quote(self) -> str:
        return self.__get_random_quote()

    def write_quote(self, quote: str, author: str):
        # TODO
        query = "INSERT INTO quotes (quote, author, timestamp) VALUES "
        query += f"({quote}, {author}, {datetime.now()})"

    def get_quote_info(self, quote_text: str):
        pass

    def __get_quote_by_id(self, quote_id: int):
        pass

    def __get_random_quote(self) -> str:
        query = "SELECT quote FROM quotes ORDER BY rand() LIMIT 1;"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.last_quote_read = result[0]
        return result[0]

    def __get_quote_containing_text(self, quote_text: str) -> list:
        query = f"SELECT quote FROM quotes WHERE quote LIKE %{quote_text}%"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def give_band_name(self):
        pass

    def write_band_name(self):
        pass

    def __get_random_band_name(self):
        pass

    def give_album_name(self):
        pass

    def write_album_name(self):
        pass

    def __get_random_album_name(self):
        pass

    def give_they_called_me(self):
        pass

    def write_they_called_me(self):
        pass

    def __get_random_they_calle_me(self):
        pass
