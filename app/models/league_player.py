import json
from config import RIOT_API_INSTANCE, UTILITIES, Config, LEAGUE_CHAMPIONS, LOL_CHALLENGES_CONFIG

class LeaguePlayer():

    def __init__(self, summoner_name: str, server: str):

        self.summoner_name = summoner_name
        self.server = server
        self.name, self.tag = UTILITIES.split_summoner_name(self.summoner_name)
        
        RIOT_API_INSTANCE.set_region(self.server)
        self.accountPatch = RIOT_API_INSTANCE.get_current_server_versions()
        self.accountData = RIOT_API_INSTANCE.get_account(summoner_name=self.name, tag=self.tag)
        self.summonerData = RIOT_API_INSTANCE.get_summoner(puuid=self.accountData["puuid"])
        self.championData = RIOT_API_INSTANCE.get_champion_mastery(puuid=self.accountData["puuid"])
        self.challengesData = RIOT_API_INSTANCE.get_challenges(puuid=self.accountData["puuid"])
        self.challengesConfig = LOL_CHALLENGES_CONFIG

        challengesDict = {}
        for definition in self.challengesConfig:
            challengeId = definition["id"]
            name = definition["localizedNames"]["en_US"]["name"]
            description = definition["localizedNames"]["en_US"]["description"]
            challengesDict[challengeId] = {"title": name, "description": description}
        for challenge in self.challengesData["challenges"]:
            challengeId = challenge["challengeId"]
            if challengeId in challengesDict:
                challenge["title"] = challengesDict[challengeId]["title"]
                challenge["description"] = challengesDict[challengeId]["description"]

        champion_map = {}
        for champion in LEAGUE_CHAMPIONS["data"].values():
            champion_map[int(champion["key"])] = champion["name"]
        for entry in self.championData:
            champ_id = entry["championId"]
            entry["championName"] = champion_map.get(champ_id, "Unknown")
            entry["lastPlayTimePretty"] = UTILITIES.timestamp_to_date_time(int(entry["lastPlayTime"]))

        #filename = "test.json"
        #path = Config.get_data_path(filename)

    def refresh_stats():
        return 0 