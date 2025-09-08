from config import RIOT_API_INSTANCE, Config

class DataDragon:
    BASE_URL = "https://ddragon.leagueoflegends.com/cdn"

    def __init__(self):

        self.version = RIOT_API_INSTANCE.get_version_history()

        self.img_dir = Config.BASE_DIR / "app" / "static" / "imgs"
        self.data_dir = Config.DATA_DIR / "lol"

    def update_latest_champion_json(self):
        x = 0

#! used in lol_manager.html page to update assets