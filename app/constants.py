from config import Config
from app.models.utils import Utilities
from app.models.riot_api import RiotAPI

RIOT_API_INSTANCE = RiotAPI(Config.RIOT_API_KEY)
_utils = Utilities()
ARENA_AUGMENTS_PATH = Config.DATA_DIR / "lol" / "en_us_arena_augments.json"
ARENA_AUGMENTS_DATA = _utils.read_json_file(ARENA_AUGMENTS_PATH)
LEAGUE_CHAMPIONS = _utils.read_json_file(Config.LEAGUE_CHAMPIONS_FILE)
QUEUES = RIOT_API_INSTANCE.get_queues()#!
LOL_CHALLENGES_CONFIG = RIOT_API_INSTANCE.get_challenges_config()#!
