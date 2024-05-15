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
