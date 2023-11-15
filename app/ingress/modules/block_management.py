import hashlib

from ...config import TAU
from ...utils.db_management import DbConnection


class BlockData(DbConnection):
    def create(self):
        cursor = self.conn.cursor()

        cursor.execute('DROP TABLE IF EXISTS Blocks')

        cursor.execute('''
            CREATE TABLE Blocks (
                id TEXT PRIMARY KEY,
                current_tip INTEGER NOT NULL,
                predicessor TEXT NULL
            )
        ''')
                # pow_token TEXT NOT NULL
                # block_content TEXT NOT NULL
                # proposer_pk TEXT NOT NULL
                # nounce TEXT NOT NULL

        cursor.execute('INSERT INTO Blocks (id, current_tip) VALUES (?, ?)', (
            "thegenesisblock",
            1,
            ))
    
        self.conn.commit()
        self.conn.close()

    # def get_ips(self):
                
    #     cursor = self.conn.cursor()
    #     cursor.execute('SELECT * FROM ip_addresses')
    #     rows = cursor.fetchall()
    #     for row in rows:
    #         print(row)
        
    #     self.conn.close()
    #     return rows

    # def extend_ips(self, ips: list[str]):
    #     cursor = self.conn.cursor()
    #     cursor.executemany('INSERT INTO ip_addresses (ip_address) VALUES (?)', [(ip,) for ip in ips])
    #     self.conn.commit()
    #     self.conn.close()


def convert_bytes_to_binstr(x: bytes) -> str:
    return "{:08b}".format(int(x.hex(), 16)) 


def count_leading_zero(binstr) -> int:
    count = 0
    for i in binstr:
        if i == '0':
            count += 1
    return count


def verify_block(x: bytes) -> bool:
    sha256 = hashlib.sha256()
    sha256.update(x)
    hash_result = convert_bytes_to_binstr(sha256.digest())
    leading_zero = count_leading_zero(hash_result)
    return leading_zero >= TAU
