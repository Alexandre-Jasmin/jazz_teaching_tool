import json
from config import RIOT_API_INSTANCE, UTILITIES, Config, LEAGUE_CHAMPIONS

class LeaguePlayer():

    def __init__(self, summoner_name: str, server: str):

        self.summoner_name = summoner_name
        self.server = server
        self.name, self.tag = UTILITIES.split_summoner_name(self.summoner_name)
        RIOT_API_INSTANCE.set_region(self.server)

        accountData = RIOT_API_INSTANCE.get_account(summoner_name=self.name, tag=self.tag)
        summonerData = RIOT_API_INSTANCE.get_summoner(puuid=accountData["puuid"])
        championData = RIOT_API_INSTANCE.get_champion_mastery(puuid=accountData["puuid"])
        challengesData = RIOT_API_INSTANCE.get_challenges(puuid=accountData["puuid"])
        
        filename = "test.json"
        path = Config.get_data_path(filename)
        with open(path, "r", encoding="utf-8") as f:
            testData = json.load(f)

        self.data = {
            "server": self.server,
            "testing": testData,
            "accountData": accountData,
            "summonerData": summonerData,
            "championData": championData,
            "challengesData": challengesData
        }

    #on init, load basic information
    #check in database for information