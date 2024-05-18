# Installation

    ```bash
    pip install -r requirements.txt
    ```

# Setup

    ```bash
    python scripts/create_db.py
    ```

# Launch App

## mac

    ```bash
    source .venv/bin/activate

    uvicorn main:app --host 0.0.0.0 --port 7573 --reload
    uvicorn main:app --host 0.0.0.0 --port 7573
    ```

# base64 encoding

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
