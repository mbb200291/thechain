import hashlib
import base64
import random
import json

from ..config import TAU, GENESIS_BLOCK, PUBLIC_KEY
from .db_management import DbConnection
from .transaction_management import TransactionData


PUBLIC_KEY_BYTES = "" 


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
            SELECT id FROM Blocks WHERE depth = (SELECT MAX(depth) FROM Blocks) LIMIT 1;
            ''')
        tip_id = cursor.fetchone()[0]
        self.conn.close()
        return tip_id
    
    def dump_all_blocks(self) -> str:
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            SELECT * FROM Blocks;
            ''')
        blocks = cursor.fetchall()
        self.conn.close()
        return json.dumps(blocks)
        
    def update_blocks(self, blocks):
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


def bytes_encode(string: str) -> bytes:
    return base64.b64decode(string.encode('utf8'))  # base64-wise
    # return string.encode('utf8')  # base64-wise


def bytes_decode(bytes_obj: bytes) -> str:
    return base64.b64encode(bytes_obj).decode('ascii')  # base64-eise
    # return bytes_obj.decode('utf8')


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
        transaction: bytes,#str,
        pred: bytes,#str,
        publickey: bytes,
        nounce: bytes
        ) -> bytes:
    hasher = hashlib.sha256()
    hasher.update(transaction),#.encode('utf8'))
    hasher.update(pred),#.encode('utf8'))
    hasher.update(publickey),
    hasher.update(nounce)
    return hasher.digest()


# def create_block(
#         powtoken: str,
#         transactions: str,
#         predicessor: str,
#         proposer_pk: str,
#         nounce: str):
#     return {
#         'powtoken': powtoken,
#         'transactions': transactions,
#         'predicessor': predicessor,
#         'proposer_pk': proposer_pk,
#         'nounce': nounce}

def create_block():
    # global PUBLIC_KEY_BYTES
    # if PUBLIC_KEY_BYTES == "":
    #    PUBLIC_KEY_BYTES = bytes_encode(PUBLIC_KEY)
    block = {
            "nounce": bytes_decode(create_nounce()),
            "predicessor": BlockData().get_tip(),
            "proposer_pk": PUBLIC_KEY,
            "transactions": TransactionData(
                ).get_unsync_transactions(),
            }
    block["pow_token"] = bytes_decode(create_pow_token(
        bytes_encode(block["transactions"]),
        bytes_encode(block["predicessor"]),
        bytes_encode(block["proposer_pk"]),
        bytes_encode(block["nounce"]),
    ))
    return block
# def cal_sh256(content: bytes):
#     hasher = hashlib.sha256()
#     hasher.update(content)
#     return hasher.digest()

    # pow_token: str  # base64 encoded of sha256([md5(transactions, 128bits, 16bytes)] | predicessor pow_token, 256bits, 32bytes) | proposer_pk (depends on algorithm)) | nounce (128, 16bytes)]) """
    # transactions: str  # transaction string encoded in UTF8
    # predicessor: str  # pow_token of predicessor
    # proposer_pk: str  # public key (PEM format) (base64 encoded)
    # nounce: str  # nounce bytes (base64 encoded)
    

def verify_block_attribute(block) -> bool:
    return create_pow_token(
        bytes_encode(block['transactions']),
        bytes_encode(block['predicessor']),
        bytes_encode(block['proposer_pk']),
        bytes_encode(block['nounce'])
    ) == bytes_encode(block['pow_token'])


def verify_block_pow(x: bytes) -> bool:
    leading_zero = count_leading_zero(x)
    print("leading zero:", leading_zero)
    return leading_zero >= TAU


def verify(block) -> bool:
    print('>1', verify_block_pow(bytes_encode(block['pow_token'])))
    print('>2', verify_block_attribute(block))
    print('>3', BlockData().check_block_existence(block['predicessor']))
    return (
        verify_block_pow(bytes_encode(block['pow_token']))  # have to smaller than tau
        and verify_block_attribute(block)  # satisafy hash rule
        and BlockData().check_block_existence(block['predicessor'])  # whether block already exist
        )


# pow_token, predicessor, transactions, proposer_pk, nounce