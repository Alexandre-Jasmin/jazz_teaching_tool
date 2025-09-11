from config import Config
from app.constants import _utils, RIOT_API_INSTANCE

class LeagueMatch:

    def __init__(self, match_id: str) -> None:
        self.match_id = match_id
        self.server, self.formated_match_id = _utils.split_summoner_name(self.match_id)
        RIOT_API_INSTANCE.set_region(self.server)

        file_path = Config.MATCHES_DIR / f"{self.match_id}.json"
        if file_path.exists():
            self.data = _utils.read_json_file(file_path)
        else:
            self.data = RIOT_API_INSTANCE.get_match(self.match_id)
