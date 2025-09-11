import os, json
from pathlib import Path
from dotenv import load_dotenv

from app.models.riot_api import RiotAPI
from app.models.utils import Utilities

load_dotenv()

class Config:
    # --- Directories ---
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    MATCHES_DIR = DATA_DIR / "lol" / "matches"
    DOCS_FILE = BASE_DIR / "documentation.md"
    LEAGUE_CHAMPIONS_FILE = DATA_DIR / "lol" / "champions.json"

    # --- Secrets & API keys ---
    RIOT_API_KEY = os.getenv("RIOT_API_KEY")
    RIOT_API_KEY_DEV = os.getenv("RIOT_API_KEY_DEV")

    # --- Helpers ---
    @classmethod
    def get_data_path(cls, filename: str) -> Path:
        return cls.DATA_DIR / filename
    
    @classmethod
    def load_docs(cls) -> str:
        return cls.DOCS_FILE.read_text(encoding="utf-8")

# --- Global singletons ---
RIOT_API_INSTANCE = RiotAPI(Config.RIOT_API_KEY)
UTILITIES = Utilities()
LEAGUE_CHAMPIONS = json.load(open(Config.get_data_path("lol/champions.json"), encoding="utf-8"))
LOL_CHALLENGES_CONFIG = RIOT_API_INSTANCE.get_challenges_config()
QUEUES = RIOT_API_INSTANCE.get_queues()