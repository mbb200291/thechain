# Impletement Note

## Block Structure

| Category     | Description                                                          |
| ------------ | -------------------------------------------------------------------- |
| Predicessor  | The predicessor pow token. Also act as primary key of internal table |
| POW_TOKEN    | The SHA-256 encode block content.                                    |
| TRANSACTIONS | The message (transactions) intent to send/receive.                   |
| PROPOSER_PK  | The private key of proposer.                                         |
| NOUNCE       | The free bits for propser to attemp fit criteria                     |

code snippet

```python
def create_pow_token(
        transaction: bytes,,
        pred: bytes,,
        publickey: bytes,
        nounce: bytes
        ) -> bytes:
    hasher = hashlib.sha256()
    hasher.update(transaction),
    hasher.update(pred),
    hasher.update(publickey),
    hasher.update(nounce)
    return hasher.digest()
```

## Base64

### encode

char seq => map to utf8 as byte seq => interprete bytes seq by base64-wise => char seq

### decode

char seq => map to base64 byte seq => interterpte byte seq by utf8 => char seq

### base64 encoding

轉換流程

```python
import base64
text = "thegenesisblock="  # string literal
text_bytes = text.encode('utf8')  # 用utf8對每個char轉換為bytes構成的序列
text_bytes_b64 = base64.b64encode(btext)  # bytes序列用base64的模式（6bits一組）指派給64個char的某一個，這個char再用一個bytes來表示(ascii, 一個char佔1bytes)
text_bytes_b64_ascii = base64.b64decode(text_bytes_b64)  # 將ascii表示的bytes用base64的對應bits還原，拼起來後再用asicii的bytes來解讀
text_bytes_b64_ascii.decode('utf8')  # 用utf8來繪製對應的char list
```

ecnode binarys to base64 chars

```python
# ecnode binarys to base64 chars
rand_bits = bytes([1, 255])

print(rand_bits)  # b'\x01\xff'

print(base64.b64encode(rand_bits).decode('ascii'))  # Af8=
```

decode base64 encoded bits backto bites

```python
# decode base64 encoded bits backto bites
rand_b64_toks = "ABC="
print(base64.b64decode(rand_b64_toks.encode('ascii')))  # b'\x00\x10'

```

## TODO

- add triggering logic to select transactions on lognest block chain.
- logic to apply transactions onto target db
  - v1: create reverse operation on these operation step
  - v2: revese back to some of switch ppoint and re-apply targe transacitons
