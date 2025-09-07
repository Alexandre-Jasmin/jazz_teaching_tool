import os
from dotenv import load_dotenv

from app.models.riot_api import RiotAPI
from app.models.utils import Utilities

load_dotenv()

class Config:
    RIOT_API_KEY = os.getenv("RIOT_API_KEY")

RIOT_API_INSTANCE = RiotAPI(Config.RIOT_API_KEY)
UTILITIES = Utilities()