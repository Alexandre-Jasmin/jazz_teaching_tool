from .models import Classroom, LeaguePlayer

def create_classroom():
    return

def load_classroom(classroom_id: str):
    try:
        loadedClassroom = Classroom(puuid=classroom_id) # we load an existing classroom
    except Exception as e:
        return None
    return loadedClassroom  

def get_summoner(summoner_name: str, server: str):
    try:
        loadedPlayer = LeaguePlayer(summoner_name, server)
    except Exception as e:
        return None
    return loadedPlayer

def get_match_data(match_id: str):
    return 0