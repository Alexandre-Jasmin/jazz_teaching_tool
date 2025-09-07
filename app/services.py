from .models import Classroom
from config import RIOT_API_INSTANCE, UTILITIES

def load_classroom(classroom_id):
    try:
        loadedClassroom = Classroom(puuid=classroom_id)
    except Exception as e:
        return None
    return loadedClassroom

def get_summoner(summoner_name, server):
    name, tag = UTILITIES.split_summoner_name(summoner_name)
    if name == None:
        return {"message": f"Failed to split the summoner name ({summoner_name})"}
    try:
        RIOT_API_INSTANCE.set_region(server)
        accountData = RIOT_API_INSTANCE.get_account(summoner_name=name, tag=tag)
        summonerData = RIOT_API_INSTANCE.get_summoner(puuid=accountData["puuid"])
    except Exception as e:
        return None
    return summonerData

def get_match_data(match_id):
    return 0