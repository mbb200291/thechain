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
                predicessor TEXT NULL,
                depth INT NOT NULL
            )
        ''')
                # pow_token TEXT NOT NULL
                # block_content TEXT NOT NULL
                # proposer_pk TEXT NOT NULL
                # nounce TEXT NOT NULL

        cursor.execute('INSERT INTO Blocks (id, depth) VALUES (?, ?)', (
            "thegenesisblock",
            0,
            ))
    
        self.conn.commit()
        self.conn.close()

    
    def check_block_existence(self, pow_token):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM my_table WHERE id = ?", (pow_token,))
        data = cursor.fetchone()
        return bool(data)

    def hang_block(self, pow_token, predicessor):
        
        cursor = self.conn.cursor()

        # append
        cursor.execute(
            '''INSERT INTO Blocks (id, depth)  
               SELECT (?), (depth + 1)
               FROM Blocks 
               WHERE id=(?);
               ''', (
                pow_token,
                predicessor,
                )
            )
        self.conn.commit()
        self.conn.close()

    def get_tip(self) -> str:
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            SELECT id FROM Blocks WHERE depth IN (SELECT MAX(depth) FROM Blocks) LIMIT 1;
            ''')
        row = cursor.fetchone()
        tip_id = row
        self.conn.close()
        if row:
            return tip_id
        return None
        
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
    return (
        verify_block_attribute(block)
        and verify_block_pow(block['pow_token'])
        and BlockData().check_block_existence(block['pow_token'])
        )

def hang_block(block):
    return BlockData().hang_block(
        block['pow_token'],
        block['predicessor']
    )
