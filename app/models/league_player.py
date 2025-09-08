import json
from config import RIOT_API_INSTANCE, UTILITIES, Config

class LeaguePlayer():

    def __init__(self, summoner_name: str, server: str):

        self.summoner_name = summoner_name
        self.server = server
        self.name, self.tag = UTILITIES.split_summoner_name(self.summoner_name)
        
        RIOT_API_INSTANCE.set_region(self.server)
        self.accountData = RIOT_API_INSTANCE.get_account(summoner_name=self.name, tag=self.tag)
        self.summonerData = RIOT_API_INSTANCE.get_summoner(puuid=self.accountData["puuid"])
        #! add championName to every champion
        #! sort by champion level from the start
        #! format points 671,123
        #! turn last played into a datetime
        #! get required to go next level
        self.championData = RIOT_API_INSTANCE.get_champion_mastery(puuid=self.accountData["puuid"])
        self.challengesData = RIOT_API_INSTANCE.get_challenges(puuid=self.accountData["puuid"])
        
        filename = "test.json"
        path = Config.get_data_path(filename)
        with open(path, "r", encoding="utf-8") as f:
            testData = json.load(f)

    def refresh_stats():
        return 0 