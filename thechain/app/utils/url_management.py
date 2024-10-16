from .db_management import DbConnection
from ..config import SEED_URLS


class UrlData(DbConnection):
    TABNAME = "Urls"
    
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS Urls')
        cursor.execute('''
            CREATE TABLE Urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL
            )
        ''')

        # url_list = [
        #     'http://localhost:7573',  # the broadcasting node
        #            ]
        for url in SEED_URLS:
            cursor.execute('INSERT INTO Urls (url) VALUES (?)', (url,))

        self.conn.commit()
        self.conn.close()
        # return self

    def get_urls(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT `url` FROM `Urls`')
        rows = cursor.fetchall()
        self.conn.close()
        return [x[0] for x in rows]

    def extend_urls(self, urls: list[str]):
        cursor = self.conn.cursor()
        cursor.executemany('INSERT INTO Urls (url) VALUES (?)', [
            (str(url),) for url in urls])
        self.conn.commit()
        self.conn.close()

    def remove_urls(self, urls: list[str]):
        cursor = self.conn.cursor()
        cursor.executemany('DELETE FROM Urls WHERE url = (?)', [
            (str(url),) for url in urls])
        self.conn.commit()
        self.conn.close()


# def extend_urls(urls):
#     return UrlData().extend_urls(urls)
