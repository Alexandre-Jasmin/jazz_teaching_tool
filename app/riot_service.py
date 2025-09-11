from config import Config
from app.models.riot_api import RiotAPI

riot_api = RiotAPI(Config.RIOT_API_KEY)
queues = riot_api.get_queues()
challenges_config = riot_api.get_challenges_config()
