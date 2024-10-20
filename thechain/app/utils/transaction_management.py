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
                local BOOLEAN
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
                INSERT INTO Transactions (content, datetime, sync)
                VALUES (
                    json_object(
                        'operation', 'INSERT',
                        'table', '{table}',
                        'timestamp', CURRENT_TIMESTAMP,
                        'details', json_object({', '.join([f"'{col}', NEW.{col}" for col in self.get_columns(cursor, table)] )})
                    ),
                    CURRENT_TIMESTAMP,
                    true
                );
            END;
            """

            # create triggers of insertion ops
            create_update_trigger = f"""
            CREATE TRIGGER IF NOT EXISTS after_update_{table}
            AFTER UPDATE ON {table}
            BEGIN
                INSERT INTO Transactions (content, datetime, sync)
                VALUES (
                    json_object(
                        'operation', 'UPDATE',
                        'table', '{table}',
                        'timestamp', CURRENT_TIMESTAMP,
                        'details', json_object(
                            {', '.join([f"'old_{col}', OLD.{col}, 'new_{col}', NEW.{col}" for col in self.get_columns(cursor, table)])}
                        )
                    ),
                    CURRENT_TIMESTAMP,
                    false
                );
            END;
            """

            # create trigger of delete ops
            create_delete_trigger = f"""
            CREATE TRIGGER IF NOT EXISTS after_delete_{table}
            AFTER DELETE ON {table}
            BEGIN
                INSERT INTO Transactions (content, datetime, sync)
                VALUES (
                    json_object(
                        'operation', 'DELETE',
                        'table', '{table}',
                        'timestamp', CURRENT_TIMESTAMP,
                        'details', json_object({', '.join([f"'{col}', OLD.{col}" for col in self.get_columns(cursor, table)] )})
                    )
                    CURRENT_TIMESTAMP,
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

    def local_transactions(self, transactions: list[str]):
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

    def insert_tx(content: str):
        raise NotADirectoryError()  # TODO: have to be able to distingush tx from local or outside to control brocasting behavior
    
    def isin(tx) -> bool:
        raise NotImplementedError()
    
    def remove_tx(tx) -> bool:
        raise NotImplementedError()

    def undo_tx(tx) -> bool:
        raise NotImplementedError()  # TODO: have to make sure undo sql not trigger insert to tx
    
    def undo_txes(self, txes):  # TODO
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA foreign_keys = OFF;")

        try:
            for tx in txes:
                log_entry = json.loads(tx["content"])
                operation = log_entry.get('operation')
                table = log_entry.get('table')
                details = log_entry.get('details')

                if operation == 'INSERT':
                    where_clause = ' AND '.join([f"{col} = ?" for col in details.keys()])
                    where_values = tuple(details.values())
                    sql = f"DELETE FROM {table} WHERE {where_clause}"
                    cursor.execute(sql, where_values)

                elif operation == 'UPDATE':
                    old_values = details.get('old')
                    if not old_values:
                        raise ValueError("Missing old values for UPDATE rollback")
                    set_clause = ', '.join([f"{col} = ?" for col in old_values.keys()])
                    set_values = tuple(old_values.values())
                    where_clause = "id = ?"
                    where_value = (details['id'],)
                    sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
                    cursor.execute(sql, set_values + where_value)

                elif operation == 'DELETE':
                    columns = ', '.join(details.keys())
                    placeholders = ', '.join(['?' for _ in details])
                    values = tuple(details.values())
                    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                    cursor.execute(sql, values)

                else:
                    raise ValueError(f"Unsupported operation type: {operation}")

            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.execute("PRAGMA foreign_keys = ON;")
            self.conn.close()
