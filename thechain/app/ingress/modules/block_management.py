import hashlib
import base64

from ...config import TAU
from ...utils.db_management import DbConnection


class BlockData(DbConnection):
    def create_table(self):
        cursor = self.conn.cursor()

        cursor.execute('DROP TABLE IF EXISTS Blocks')

        cursor.execute('''
            CREATE TABLE Blocks (
                id TEXT PRIMARY KEY,
                depth INT NOT NULL,

                predicessor TEXT NULL,
                block_content TEXT NOT NULL,
                proposer_pk TEXT NOT NULL,
                nounce BLOB NOT NULL
            )
        ''')
        # pow_token TEXT NOT NULL
        # block_content TEXT NOT NULL
        # proposer_pk TEXT NOT NULL
        # nounce TEXT NOT NULL

        cursor.execute('INSERT INTO Blocks (id, depth, predicessor, block_content, proposer_pk, nounce) VALUES (?, ?, ?, ?, ?, ?)', (
                "thegenesisblock",
                0,
                '',
                '',
                '',
                bytes(),
            ))

        self.conn.commit()
        self.conn.close()

    def check_block_existence(self, pow_token):
        print('predicessor token:', pow_token)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM `Blocks` WHERE id = ?", (pow_token,))
        data = cursor.fetchone()
        return bool(data)

    def hang_block(
            self, pow_token, predicessor, block_content, proposer_pk, nounce):
        cursor = self.conn.cursor()

        # append
        cursor.execute(
            '''INSERT INTO Blocks (id, depth, predicessor, block_content, proposer_pk, nounce)
               VALUES (?, (SELECT (b.depth + 1) FROM Blocks as b WHERE b.id = ?), ?, ?, ?, ?);
               ''', (
                pow_token, predicessor, predicessor, block_content, proposer_pk, nounce
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


def bytes_to_binary_string(bytes_obj):
    return ''.join(format(byte, '08b') for byte in bytes_obj)


def count_leading_zero(token: bytes) -> int:
    token_str = bytes_to_binary_string(token)
    print('bins:', token_str)
    count = 0
    for i in token_str:
        if i == '0':
            count += 1
        else:
            break
    return count


def cal_md5(content: bytes):
    hasher = hashlib.md5()
    hasher.update(content)
    return hasher.digest()


# def cal_sh256(content: bytes):
#     hasher = hashlib.sha256()
#     hasher.update(content)
#     return hasher.digest()


def verify_block_attribute(block) -> bool:
    hasher = hashlib.sha256()
    hasher.update(cal_md5(block['block_content'].encode('utf8')))
    hasher.update(cal_md5(block['predicessor'].encode('utf8')))
    hasher.update(base64.b64decode(block['proposer_pk']))
    hasher.update(base64.b64decode(block['nounce']))
    return hasher.digest() == base64.b64decode(block['pow_token'])


def verify_block_pow(x: bytes) -> bool:
    leading_zero = count_leading_zero(x)
    return leading_zero >= TAU


def verify(block) -> bool:
    print(verify_block_pow(base64.b64decode(block['pow_token'])),  # have to smaller than tau
        verify_block_attribute(block),  # satisafy hash rule
        BlockData().check_block_existence(block['predicessor'])  # whether block already exist
        )
    return (
        verify_block_pow(base64.b64decode(block['pow_token']))  # have to smaller than tau
        and verify_block_attribute(block)  # satisafy hash rule
        and BlockData().check_block_existence(block['predicessor'])  # whether block already exist
        )


def hang_block(block):
    return BlockData().hang_block(
        block['pow_token'],
        block['predicessor'],
        block['block_content'],
        block['proposer_pk'],
        block['nounce'],
    )


# pow_token, predicessor, block_content, proposer_pk, nounce