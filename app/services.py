import os
from dotenv import load_dotenv

from .models import Classroom
from .models import RiotAPI

load_dotenv()

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
RIOT_API_INSTANCE = RiotAPI(RIOT_API_KEY)

def load_classroom(classroom_id):
    loadedClassroom = Classroom(puuid=classroom_id)
    return loadedClassroom

def get_summoner(summoner_name, server):

    name, tag = RIOT_API_INSTANCE.split_summoner_name(summoner_name)
    if name == None:
        return {"message": f"Failed to split the summoner name ({summoner_name})"}
    
    RIOT_API_INSTANCE.set_region(server)
    accountData = RIOT_API_INSTANCE.get_account(summoner_name=name, tag=tag)
    summonerData = RIOT_API_INSTANCE.get_summoner(puuid=accountData["puuid"])

    return summonerData

def get_match_data(match_id):
    return 0