from .models import Classroom, LeaguePlayer, LeagueMatch
from .errors import SummonerNotFound, MatchNotFound, ServiceError

def create_classroom():
    return

def load_classroom(classroom_id: str):
    try:
        loadedClassroom = Classroom(puuid=classroom_id)
    except Exception as e:
        return None
    return loadedClassroom  

def get_summoner(summoner_name: str, server: str) -> LeaguePlayer:
    try:
        player = LeaguePlayer(summoner_name, server)
        _ = player.accountData["puuid"]
        return player
    except KeyError:
        raise SummonerNotFound(f"'{summoner_name}' not found on server {server}")
    except Exception as e:
        raise ServiceError(f"Unexpected error while loading summoner: {e}")

def get_match_data(match_id: str) -> LeagueMatch:
    try:
        return LeagueMatch(match_id)
    except Exception as e:
        raise MatchNotFound(f"Match '{match_id}' could not be loaded: {e}")