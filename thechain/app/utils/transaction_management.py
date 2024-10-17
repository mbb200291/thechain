import json

import sqlite3

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
                sync BOOLEAN,
                apply BOOLEAN
            )
        ''')

        self.conn.commit()
        self.conn.close()
        # return self

    def update_to_synced(self, ids: list[int]):
        cursor = self.conn.cursor()
        cursor.executemany(
            '''UPDATE Transactions
            SET sync = 1
            WHERE id = ?;
            ''', [(id,) for id in ids]
        )
        self.conn.commit()
        self.conn.close()
    
    def get_unsync_transactions(self) -> str:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, content FROM Transactions WHERE sync = false", ()
        )
        data = cursor.fetchall()
        if len(data) == 0:
            return [], ""
        ids, transactions = zip(*data)
        self.conn.close()
        return ids, json.dumps(transactions)

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
                INSERT INTO Transactions (content, datetime, sync, apply)
                VALUES (
                    json_object(
                        'sql', 'INSERT INTO {table} ({', '.join([col for col in self.get_columns(cursor, table)])}) VALUES ({', '.join(['?' for _ in self.get_columns(cursor, table)])})',
                        'parameters', json_array({', '.join([f"NEW.{col}" for col in self.get_columns(cursor, table)])})
                    ), 
                    CURRENT_TIMESTAMP,
                    false,
                    false
                );
            END;
            """

            # create triggers of insertion ops
            create_update_trigger = f"""
            CREATE TRIGGER IF NOT EXISTS after_update_{table}
            AFTER UPDATE ON {table}
            BEGIN
                INSERT INTO Transactions (content, datetime, sync, apply)
                VALUES (
                    json_object(
                        'sql', 'UPDATE {table} SET {', '.join([f"{col} = ?" for col in self.get_columns(cursor, table)])} WHERE id = ?',
                        'parameters', json_array(
                            {', '.join([f"NEW.{col}" for col in self.get_columns(cursor, table)])}, OLD.id
                        )
                    ),
                    CURRENT_TIMESTAMP,
                    false,
                    false
                );
            END;
            """

            # create trigger of delete ops
            create_delete_trigger = f"""
            CREATE TRIGGER IF NOT EXISTS after_delete_{table}
            AFTER DELETE ON {table}
            BEGIN
                INSERT INTO Transactions (content, datetime, sync, apply)
                VALUES (
                    json_object(
                        'sql', 'DELETE FROM {table} WHERE id = ?',
                        'parameters', json_array(OLD.id)
                    ), 
                    CURRENT_TIMESTAMP,
                    false,
                    false
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

    def apply_transactions(self, transactions: list[str]):
        cursor = self.conn.cursor()
        try:
            for content in transactions:
                log_entry = json.loads(content)
                sql = log_entry.get('sql')
                parameters = log_entry.get('parameters', [])
                cursor.execute(sql, parameters)
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            raise e
        finally:
            self.conn.close()

    