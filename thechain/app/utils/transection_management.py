from .db_management import DbConnection


class TransactionData(DbConnection):
    def create_table(self):
        cursor = self.conn.cursor()
        
        cursor.execute('DROP TABLE IF EXISTS Transections')
        
        cursor.execute('''
            CREATE TABLE Transections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                datetime Datetime NOT NULL,
                sync BOOLEAN
            )
        ''')

        self.conn.commit()
        self.conn.close()

    def dump_unsync_transactions(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT content FROM Transections WHERE sync = false", ()
        )
        transactions = cursor.fetchall()
        self.conn.close()
        return transactions