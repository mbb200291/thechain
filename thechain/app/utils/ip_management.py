from .db_management import DbConnection
from ..config import SEED_IPS


class IpData(DbConnection):
    TABNAME = "Ips"
    
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS Ips')
        cursor.execute('''
            CREATE TABLE Ips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT NOT NULL
            )
        ''')

        for ip in SEED_IPS:
            cursor.execute('INSERT INTO Ips (ip) VALUES (?)', (ip,))

        self.conn.commit()
        self.conn.close()
        # return self

    def get_ips(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT `ip` FROM `Ips`')
        rows = cursor.fetchall()
        self.conn.close()
        return [x[0] for x in rows]

    def extend_ips(self, ips: list[str]):
        cursor = self.conn.cursor()
        cursor.executemany('INSERT INTO Ips (ip) VALUES (?)', [
            (str(ip),) for ip in ips])
        self.conn.commit()
        self.conn.close()

    def remove_ips(self, ips: list[str]):
        cursor = self.conn.cursor()
        cursor.executemany('DELETE FROM Ips WHERE ip = (?)', [
            (str(ip),) for ip in ips])
        self.conn.commit()
        self.conn.close()


# def extend_ips(ips):
#     return IpData().extend_ips(ips)
