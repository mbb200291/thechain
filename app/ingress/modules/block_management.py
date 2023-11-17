import hashlib

from ...config import TAU
from ...utils.db_management import DbConnection


class BlockData(DbConnection):
    def create_table(self):
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

    def hang_block(self, pow_token, predicessor):
        cursor = self.conn.cursor()
        
        # check whether or not exist 
        cursor.execute("SELECT * FROM Blocks WHERE id = ? AND current_tip = 1",
                       (predicessor,))
        predicessor_exist = cursor.fetchone() is not None  # TODO: 需改成假使predicessor不存在則阻止插入

        cursor.execute("SELECT * FROM Blocks WHERE predicessor = ?",
                       (predicessor,))
        condition2_met = cursor.fetchone() is not None
        
        if 
        
        # append
        cursor.execute(
            'INSERT INTO Blocks (id, current_tip, predicessor) VALUES (?, ?)', (
                pow_token,
                0,
                predicessor,
                )
            )
        self.conn.commit()
        self.conn.close()

def convert_bytes_to_binstr(x: bytes) -> str:
    return "{:08b}".format(int(x.hex(), 16)) 


def count_leading_zero(binstr) -> int:
    count = 0
    for i in binstr:
        if i == '0':
            count += 1
    return count


def verify_block_attribute(block) -> bool:
    hasher_md5 = hashlib.md5()
    pow_token = block['pow_token']
    return (
        (hasher_md5(block['block_content']) == pow_token[:16])  # slice on bytes (8 bits)
        and (hasher_md5(block['predicessor']) == pow_token[16:32])
        and (hasher_md5(block['proposer_pk']) == pow_token[32:48])
    )
    
    
def verify_block_pow(x: bytes) -> bool:
    sha256 = hashlib.sha256()
    sha256.update(x)
    binary_str = convert_bytes_to_binstr(sha256.digest())
    leading_zero = count_leading_zero(binary_str)
    return leading_zero >= TAU


def verify(block) -> bool:
    return verify_block_attribute(block) and verify_block_pow(block['pow_token'])

def hang_block(block):
    BlockData()