from ...utils.db_management import DbConnection


class IpData(DbConnection):
    def create_table(self):
        cursor = self.conn.cursor()

        cursor.execute('DROP TABLE IF EXISTS IPs')

        cursor.execute('''
            CREATE TABLE IPs (
                id INTEGER PRIMARY KEY,
                ip TEXT NOT NULL
            )
        ''')

        ip_list = [
            'localhost:7573',  # the broadcasting node
                   ]
        for ip in ip_list:
            cursor.execute('INSERT INTO IPs (ip) VALUES (?)', (ip,))

        self.conn.commit()
        self.conn.close()

    def get_ips(self):

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM ip')
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        self.conn.close()
        return rows

    def extend_ips(self, ips: list[str]):
        cursor = self.conn.cursor()
        cursor.executemany('INSERT INTO IPs (ip) VALUES (?)', [
            (ip,) for ip in ips])
        self.conn.commit()
        self.conn.close()


def get_ips():
    return IpData().get_ips()


def extend_ips(ips):
    return IpData().extend_ips()
