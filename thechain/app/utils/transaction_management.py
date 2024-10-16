import json

from .db_management import DbConnection


class TransactionData(DbConnection):
    TABNAME = "Transactions"

    def create_table(self):
        cursor = self.conn.cursor()
        
        cursor.execute('DROP TABLE IF EXISTS Transactions')
        
        cursor.execute('''
            CREATE TABLE Transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                datetime Datetime NOT NULL,
                sync BOOLEAN
            )
        ''')

        self.conn.commit()
        self.conn.close()
        # return self

    def get_unsync_transactions(self) -> str:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT content FROM Transactions WHERE sync = false", ()
        )
        transactions = cursor.fetchall()
        self.conn.close()
        return json.dumps(transactions)

    def bind_target_tabs(self, excluded_tables: list[str]):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [row[0] for row in cursor.fetchall()]

        for table in tables:
            if table in excluded_tables:
                continue
            
            # create triggers insertion ops
            create_insert_trigger = f"""
            CREATE TRIGGER IF NOT EXISTS after_insert_{table}
            AFTER INSERT ON {table}
            BEGIN
                INSERT INTO Transactions (content, datetime)
                VALUES (
                    json_object(
                        'operation', 'INSERT',
                        'table', '{table}',
                        'details', json_object({', '.join([f"'{col}', NEW.{col}" for col in self.get_columns(cursor, table)] )})
                    ), 
                    CURRENT_TIMESTAMP
                );
            END;
            """

            # create triggers of insertion ops
            create_update_trigger = f"""
            CREATE TRIGGER IF NOT EXISTS after_update_{table}
            AFTER UPDATE ON {table}
            BEGIN
                INSERT INTO Transactions (content, datetime)
                VALUES (
                    json_object(
                        'operation', 'UPDATE',
                        'table', '{table}',
                        'details', json_object(
                            {', '.join([f"'old_{col}', OLD.{col}, 'new_{col}', NEW.{col}" for col in self.get_columns(cursor, table)])}
                        ), 
                    CURRENT_TIMESTAMP
                    )
                );
            END;
            """

            # create trigger of delete ops
            create_delete_trigger = f"""
            CREATE TRIGGER IF NOT EXISTS after_delete_{table}
            AFTER DELETE ON {table}
            BEGIN
                INSERT INTO Transactions (content, datetime)
                VALUES (
                    json_object(
                        'operation', 'DELETE',
                        'table', '{table}',
                        'details', json_object({', '.join([f"'{col}', OLD.{col}" for col in self.get_columns(cursor, table)] )})
                    ), 
                    CURRENT_TIMESTAMP
                );
            END;
            """
            
            cursor.execute(create_insert_trigger)
            cursor.execute(create_update_trigger)
            cursor.execute(create_delete_trigger)

        self.conn.commit()
        self.conn.close()

    def get_columns(self, cursor, table_name):
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [row[1] for row in cursor.fetchall()]
        return columns
