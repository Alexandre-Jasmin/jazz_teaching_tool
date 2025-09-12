from app.models import LeaguePlayer, LeagueMatch
from app.errors import SummonerNotFound, MatchNotFound, ServiceError

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