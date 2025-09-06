# jaZZ Tool

*"Personal Flask Website"*

---

## Features

- **Classroom**
  - Manage classroom data
  - Uses a basic JSON database with backup
- **League of Legends API**
  - REST endpoints:
    - `/lol/summoner`
    - `/lol/match`

---

## Structure

- **run.py**
- **config.py**
- **app/**
  - models
    - `__init__.py`
    - `riot_api.py`
- **data/**
  - classroom.pkl
  - data.json
    - `/lol/summoner`
    - `/lol/match`