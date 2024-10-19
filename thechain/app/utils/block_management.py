import hashlib
import base64
import random
import json

from ..config import TAU, GENESIS_BLOCK, PUBLIC_KEY
from .custlog import setup_logger
from .db_management import DbConnection
from .transaction_management import TransactionData


PUBLIC_KEY_BYTES = "" 
logger = setup_logger(__name__)

class BlockData(DbConnection):
    TABNAME = "Blocks"

    def create_table(self):
        cursor = self.conn.cursor()

        cursor.execute(f'DROP TABLE IF EXISTS {self.TABNAME}')

        cursor.execute(f'''
            CREATE TABLE {self.TABNAME} (
                pow_token TEXT PRIMARY KEY,
                predicessor TEXT NULL,
                transactions TEXT NOT NULL,
                proposer_pk TEXT NOT NULL,
                nounce BLOB NOT NULL,
                depth INT NOT NULL
            )
        ''')

        cursor.execute('INSERT INTO Blocks (pow_token, depth, predicessor, transactions, proposer_pk, nounce) VALUES (?, ?, ?, ?, ?, ?)', (
                GENESIS_BLOCK,
                0,
                '',
                '',
                '',
                bytes(),
            ))

        self.conn.commit()
        self.conn.close()
        # return self

    def check_block_existence(self, pow_token):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM `Blocks` WHERE pow_token = ?", (pow_token,))
        data = cursor.fetchone()
        return bool(data)

    def hang_block(
            self, pow_token, predicessor, transactions, proposer_pk, nounce):
        cursor = self.conn.cursor()

        # append
        cursor.execute(
            '''INSERT INTO Blocks (pow_token, depth, predicessor, transactions, proposer_pk, nounce)
               VALUES (
                ?, (SELECT (b.depth + 1) FROM Blocks as b WHERE b.pow_token = ?), ?, ?, ?, ?);
               ''', (
                pow_token, predicessor, predicessor, transactions, proposer_pk, nounce
                )
            )
        self.conn.commit()
        self.conn.close()
        return 1

    def get_tip_pow(self) -> str:
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            SELECT pow_token FROM Blocks WHERE depth = (SELECT MAX(depth) FROM Blocks) LIMIT 1;
            ''')
        tip_pow_token = cursor.fetchone()[0]
        self.conn.close()
        return tip_pow_token
    
    def get_block(self, id: str) -> str:
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            SELECT * FROM Blocks WHERE pow_token = ?;
            ''', id)
        row = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
        self.conn.close()
        return dict(zip(columns, row))
    
    def dump_all_blocks(self):
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            SELECT * FROM Blocks;
            ''')
        blocks = cursor.fetchall()
        self.conn.close()
        logger.debug(blocks)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, b)) for b in blocks]
        # return json.dumps(blocks)
        
    # def update_blocks(self, blocks: dict[str]):
    #     cursor = self.conn.cursor()

    #     # append
    #         # cursor.executemany("UPDATE employees SET salary = ? WHERE id = ?", updates)
    #     cursor.executemany(
    #         '''INSERT INTO Blocks (pow_token, depth, predicessor, transactions, proposer_pk, nounce)
    #            VALUES (
    #             ?, (SELECT (b.depth + 1) FROM Blocks as b WHERE b.pow_token = ?), ?, ?, ?, ?);
    #            ''', (
    #             [(block["pow_token"], block['pow_token'], block[''],
    #               transactions, proposer_pk, nounce) for block in blocks]
    #             )
    #         )
    #     self.conn.commit()
    #     self.conn.close()
    #     return 1

    def iter_lonest_tx(self):
        # transactions_seq = []
        cur_block = self.get_block(self.get_tip_pow())
        while cur_block["depth"] >= 0:
            # transactions_seq.append(cur_block["transactions"])
            yield cur_block["transactions"]
            cur_block = self.get_block(cur_block["predicessor"])
        # return transactions_seq
 
        
def bytes_to_binary_string(bytes_obj):
    return ''.join(format(byte, '08b') for byte in bytes_obj)


def count_leading_zero(token: bytes) -> int:
    token_str = bytes_to_binary_string(token)
    logger.debug('bins: ' + token_str)
    count = 0
    for i in token_str:
        if i == '0':
            count += 1
        else:
            break
    return count


def  bytes_encode(string: str) -> bytes:
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


def create_block(
    predicessor=None,
    transactions=None,
    ids=None,
):
    ids, transactions = TransactionData().get_unsync_transactions() if transactions is None else (transactions, ids)
    predicessor = BlockData().get_tip_pow() if predicessor is None else predicessor
    block = {
            "nounce": bytes_decode(create_nounce()),
            "predicessor": predicessor,
            "proposer_pk": PUBLIC_KEY,
            "transactions": transactions,
            }
    block["pow_token"] = bytes_decode(create_pow_token(
        bytes_encode(block["transactions"]),
        bytes_encode(block["predicessor"]),
        bytes_encode(block["proposer_pk"]),
        bytes_encode(block["nounce"]),
    ))
    return ids, block


def verify_block_attribute(block) -> bool:
    return create_pow_token(
        bytes_encode(block['transactions']),
        bytes_encode(block['predicessor']),
        bytes_encode(block['proposer_pk']),
        bytes_encode(block['nounce'])
    ) == bytes_encode(block['pow_token'])


def verify_block_pow(x: bytes) -> bool:
    leading_zero = count_leading_zero(x)
    logger.debug("leading zero: %d"%leading_zero)
    return leading_zero >= TAU


def verify(block) -> bool:
    logger.debug(f"#verify_block_pow: {verify_block_pow(bytes_encode(block['pow_token']))}")
    logger.debug(f'#verify_block_attribute: {verify_block_attribute(block)}') 
    logger.debug(f"#check_block_existence: {BlockData().check_block_existence(block['predicessor'])}")
    return (
        verify_block_pow(bytes_encode(block['pow_token']))  # have to smaller than tau
        and verify_block_attribute(block)  # satisafy hash rule
        and BlockData().check_block_existence(block['predicessor'])  # whether block already exist
        )
