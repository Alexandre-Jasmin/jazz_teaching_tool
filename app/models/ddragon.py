from config import Config
from app.services import RIOT_API_INSTANCE

class DataDragon:
    BASE_URL = "https://ddragon.leagueoflegends.com/cdn"

    def __init__(self):

        self.version = RIOT_API_INSTANCE.get_version_history()

        self.img_dir = Config.BASE_DIR / "app" / "static" / "imgs"
        self.data_dir = Config.DATA_DIR / "lol"

    def update_latest_champion_json(self):
        x = 0

    def update_latest_challenges_images(self):
        x = 0

    def update_champion_icons(self):
        x = 0