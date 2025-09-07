from config import RIOT_API_INSTANCE, UTILITIES

class LeaguePlayer():

    def __init__(self, summoner_name, server):

        self.summoner_name = summoner_name
        self.server = server
        self.name, self.tag = UTILITIES.split_summoner_name(self.summoner_name)
        RIOT_API_INSTANCE.set_region(self.server)

        accountData = RIOT_API_INSTANCE.get_account(summoner_name=self.name, tag=self.tag)
        summonerData = RIOT_API_INSTANCE.get_summoner(puuid=accountData["puuid"])
        championData = RIOT_API_INSTANCE.get_champion_mastery(puuid=accountData["puuid"])
        challengesData = RIOT_API_INSTANCE.get_challenges(puuid=accountData["puuid"])
        self.data = {
            "accountData": accountData,
            "summonerData": summonerData,
            "championData": championData,
            "challengesData": challengesData
        }

    #on init, load basic information
    #check in database for information