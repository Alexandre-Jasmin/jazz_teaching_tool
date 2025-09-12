from config import Config
from app.constants import _utils
from app.services.riot_service import riot_api

class LeagueMatch:

    def __init__(self, match_id: str) -> None:
        
        self.match_id = match_id
        self.server, self.formated_match_id = _utils.split_summoner_name(self.match_id)
        riot_api.set_region(self.server)

        file_path = Config.MATCHES_DIR / f"{self.match_id}.json"
        if file_path.exists():
            self.data = _utils.read_json_file(file_path)
        else:
            self.data = riot_api.get_match(self.match_id)
