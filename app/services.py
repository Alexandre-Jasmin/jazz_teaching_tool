from .models import Classroom, LeaguePlayer

def load_classroom(classroom_id):
    try:
        loadedClassroom = Classroom(puuid=classroom_id)
    except Exception as e:
        return None
    return loadedClassroom

def get_summoner(summoner_name: str, server: str):
    try:
        myLeaguePlayer = LeaguePlayer(summoner_name, server)
        playerData = myLeaguePlayer.data
    except Exception as e:
        return None
    return playerData

def get_match_data(match_id):
    return 0