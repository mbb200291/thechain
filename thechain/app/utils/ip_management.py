from .db_management import DbConnection
from ..config import SEED_URLS


class IpData(DbConnection):
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS IPs')
        cursor.execute('''
            CREATE TABLE IPs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT NOT NULL
            )
        ''')

        # ip_list = [
        #     'http://localhost:7573',  # the broadcasting node
        #            ]
        for ip in SEED_URLS:
            cursor.execute('INSERT INTO IPs (ip) VALUES (?)', (ip,))

        self.conn.commit()
        self.conn.close()

    def get_ips(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT `ip` FROM `IPs`')
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        self.conn.close()
        return [x[0] for x in rows]

    def extend_ips(self, ips: list[str]):
        cursor = self.conn.cursor()
        cursor.executemany('INSERT INTO IPs (ip) VALUES (?)', [
            (str(ip),) for ip in ips])
        self.conn.commit()
        self.conn.close()

    def remove_ips(self, ips: list[str]):
        cursor = self.conn.cursor()
        cursor.executemany('DELETE FROM IPs WHERE ip = (?)', [
            (str(ip),) for ip in ips])
        self.conn.commit()
        self.conn.close()


# def extend_ips(ips):
#     return IpData().extend_ips(ips)
