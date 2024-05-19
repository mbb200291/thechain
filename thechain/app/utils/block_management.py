import hashlib
import base64
import random

from ..config import TAU, GENESIS_BLOCK
from .db_management import DbConnection


class BlockData(DbConnection):
    def create_table(self):
        cursor = self.conn.cursor()

        cursor.execute('DROP TABLE IF EXISTS Blocks')

        cursor.execute('''
            CREATE TABLE Blocks (
                id TEXT PRIMARY KEY,
                depth INT NOT NULL,

                predicessor TEXT NULL,
                transactions TEXT NOT NULL,
                proposer_pk TEXT NOT NULL,
                nounce BLOB NOT NULL
            )
        ''')
        # pow_token TEXT NOT NULL
        # transactions TEXT NOT NULL
        # proposer_pk TEXT NOT NULL
        # nounce TEXT NOT NULL

        cursor.execute('INSERT INTO Blocks (id, depth, predicessor, transactions, proposer_pk, nounce) VALUES (?, ?, ?, ?, ?, ?)', (
                GENESIS_BLOCK,
                0,
                '',
                '',
                '',
                bytes(),
            ))

        self.conn.commit()
        self.conn.close()

    def check_block_existence(self, pow_token):
        # print('predicessor token:', pow_token)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM `Blocks` WHERE id = ?", (pow_token,))
        data = cursor.fetchone()
        return bool(data)

    def hang_block(
            self, pow_token, predicessor, transactions, proposer_pk, nounce):
        cursor = self.conn.cursor()

        # append
        cursor.execute(
            '''INSERT INTO Blocks (id, depth, predicessor, transactions, proposer_pk, nounce)
               VALUES (
                ?, (SELECT (b.depth + 1) FROM Blocks as b WHERE b.id = ?), ?, ?, ?, ?);
               ''', (
                pow_token, predicessor, predicessor, transactions, proposer_pk, nounce
                )
            )
        self.conn.commit()
        self.conn.close()
        return 1

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


def base64decode(string: str) -> bytes:
    return base64.b64decode(string.encode('utf8'))


def base64encode(bytes_obj: bytes) -> str:
    return base64.b64encode(bytes).decode('ascii')


def cal_md5(content: bytes):
    hasher = hashlib.md5()
    hasher.update(content)
    return hasher.digest()


def create_nounce() -> bytes:
    rands = [random.randint(0, 255) for _ in range(16)]
    return bytes(rands)


def cal_md5(content: bytes):
    hasher = hashlib.md5()
    hasher.update(content)
    return hasher.digest()


def create_pow_token(
        transection: bytes,#str,
        pred: bytes,#str,
        publickey: bytes,
        nounce: bytes
        ) -> bytes:
    hasher = hashlib.sha256()
    hasher.update(transection),#.encode('utf8'))
    hasher.update(pred),#.encode('utf8'))
    hasher.update(publickey),
    hasher.update(nounce)
    return hasher.digest()


def create_block(
        powtoken: str,
        transactions: str,
        predicessor: str,
        proposer_pk: str,
        nounce: str):
    return {
        'powtoken': powtoken,
        'transactions': transactions,
        'predicessor': predicessor,
        'proposer_pk': proposer_pk,
        'nounce': nounce}


# def cal_sh256(content: bytes):
#     hasher = hashlib.sha256()
#     hasher.update(content)
#     return hasher.digest()


def verify_block_attribute(block) -> bool:
    
    # hasher = hashlib.sha256()
    # hasher.update(block['predicessor'].encode('utf8'))
    # hasher.update(block['transactions'].encode('utf8'))
    # hasher.update()
    # hasher.update()
    return create_pow_token(
        block['transactions'].encode('utf8'),
        base64decode(block['predicessor']),
        base64decode(block['proposer_pk']),
        base64decode(block['nounce'])
    ) == base64.b64decode(block['pow_token'])


def verify_block_pow(x: bytes) -> bool:
    leading_zero = count_leading_zero(x)
    print("leading zero:", leading_zero)
    return leading_zero >= TAU


def verify(block) -> bool:
    # print('>1', verify_block_pow(base64decode(block['pow_token'])))
    # print('>2', verify_block_attribute(block))
    # print('>3', BlockData().check_block_existence(block['predicessor']))
    return (
        verify_block_pow(base64decode(block['pow_token']))  # have to smaller than tau
        and verify_block_attribute(block)  # satisafy hash rule
        and BlockData().check_block_existence(block['predicessor'])  # whether block already exist
        )


# pow_token, predicessor, transactions, proposer_pk, nounce