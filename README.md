# Installation

## create venv

```bash
python -m venv '.venv'
```

## load env

### mac

```bash
source .venv/bin/activate
```

### powershell

```powershell
.venv/Scripts/activate
```

## install reqs

```bash
pip install -r requirements.txt
```

# Setup

```bash
python scripts/create_db.py
```

# Launch App

## ingress backend

```bash
uvicorn main:app --host 0.0.0.0 --port 7573 --reload  # dev
uvicorn main:app --host 0.0.0.0 --port 7573

```

[swagger page](http://0.0.0.0:7573/docs)

## egress backend

```bash
python egress.py
```
