from ...utils.db_management import DbConnection


class IpData(DbConnection):
    def create_table(self):
        cursor = self.conn.cursor()
        
        cursor.execute('DROP TABLE IF EXISTS Transections')
        
        cursor.execute('''
            CREATE TABLE Transections (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL,
                datetime Datetime NOT NULL
            )
        ''')

        self.conn.commit()
        self.conn.close()
