import requests, time, os, re

#! Fix recurring current_version. Cache version on object init

#*RiotAPI class to interact with the Riot Games API
class RiotAPI:

    #*Init the object
    def __init__(self, api_key, region="na1"):

        self.region_to_platform = {
            "na1": "https://na1.api.riotgames.com",
            "euw1": "https://euw1.api.riotgames.com",
            "eun1": "https://eun1.api.riotgames.com",
            "kr": "https://kr.api.riotgames.com",
            "br1": "https://br1.api.riotgames.com",
            "oc1": "https://oc1.api.riotgames.com",
            "jp1": "https://jp1.api.riotgames.com",
            "tr1": "https://tr1.api.riotgames.com",
            "ru": "https://ru.api.riotgames.com",
            "la1": "https://la1.api.riotgames.com",
            "la2": "https://la2.api.riotgames.com",
            "ph2": "https://ph2.api.riotgames.com",
            "sg2": "https://sg2.api.riotgames.com",
            "th2": "https://th2.api.riotgames.com",
            "tw2": "https://tw2.api.riotgames.com",
            "vn2": "https://vn2.api.riotgames.com"
        }

        self.region_to_regional = {
            "br1": "https://americas.api.riotgames.com",
            "eun1": "https://europe.api.riotgames.com",
            "euw1": "https://europe.api.riotgames.com",
            "jp1": "https://asia.api.riotgames.com",
            "kr": "https://asia.api.riotgames.com",
            "la1": "https://americas.api.riotgames.com",
            "la2": "https://americas.api.riotgames.com",
            "na1": "https://americas.api.riotgames.com",
            "oc1": "https://sea.api.riotgames.com",
            "tr1": "https://europe.api.riotgames.com",
            "ru": "https://europe.api.riotgames.com",
            "ph2": "https://sea.api.riotgames.com",
            "sg2": "https://sea.api.riotgames.com",
            "th2": "https://sea.api.riotgames.com",
            "tw2": "https://sea.api.riotgames.com",
            "vn2": "https://sea.api.riotgames.com"
        }

        self.realm_urls = {
            "na": "https://ddragon.leagueoflegends.com/realms/na.json",
            "euw": "https://ddragon.leagueoflegends.com/realms/euw.json",
            "eune": "https://ddragon.leagueoflegends.com/realms/eune.json",
            "kr": "https://ddragon.leagueoflegends.com/realms/kr.json",
            "br": "https://ddragon.leagueoflegends.com/realms/br.json",
            "lan": "https://ddragon.leagueoflegends.com/realms/lan.json",
            "las": "https://ddragon.leagueoflegends.com/realms/las.json",
            "oce": "https://ddragon.leagueoflegends.com/realms/oce.json",
            "ru": "https://ddragon.leagueoflegends.com/realms/ru.json",
            "tr": "https://ddragon.leagueoflegends.com/realms/tr.json",
            "jp": "https://ddragon.leagueoflegends.com/realms/jp.json"
        }

        self.region_to_realm = {
            "br1": "br",      # Brazil
            "eun1": "eune",   # Europe Nordic & East
            "euw1": "euw",    # Europe West
            "jp1": "jp",      # Japan
            "kr": "kr",       # Korea
            "la1": "lan",     # Latin America North
            "la2": "las",     # Latin America South
            "na1": "na",      # North America
            "oc1": "oce",     # Oceania
            "tr1": "tr",      # Turkey
            "ru": "ru",       # Russia
            "ph2": "na",      # Philippines → likely using NA realm for now SEA servers (Garena migrated to Riot)
            "sg2": "na",      # Singapore
            "th2": "na",      # Thailand
            "tw2": "na",      # Taiwan
            "vn2": "na",      # Vietnam
        }

        self.api_key = api_key
        self.secret_key = os.urandom(24)
        self.ddragon_url = "https://ddragon.leagueoflegends.com"
        self.static_url = "https://static.developer.riotgames.com"
        self.retry_delay = 1.2
        self.region = region.lower()
        self.platform_url = self.region_to_platform.get(self.region)
        self.regional_url = self.region_to_regional.get(self.region)
        self.realm = self.region_to_realm.get(self.region)
        self.realm_url = self.realm_urls.get(self.realm)

        if not self.platform_url or not self.regional_url:
            raise ValueError(f"Region not valid {region}")

    #*Handle requests
    def _retry_request(self, url, headers, retries):
        retry_count = 0
        while retry_count < retries:
            response = requests.get(url, headers=headers, timeout=10)
            #The endpoints has a limit, sleep
            if not url.startswith((self.ddragon_url, self.static_url)):
                time.sleep(self.retry_delay)
            if response.status_code == 200:
                return response
            elif response.status_code == 404:
                return None
            else:
                retry_count += 1
                time.sleep(self.retry_delay * (2 ** (retry_count - 1)))

        return None

    def _handle_response(self, response):

        if not response:
            return None
        elif response.status_code == 200:
            return response.json()
        else:
            return None

    def _make_request(self, url, retries=5):

        if not url or not isinstance(url, str):
            raise ValueError("Invalid URL provided.")
        if retries < 1:
            raise ValueError("Retries must be greater than or equal to 1.")
        
        headers = {"X-Riot-Token": self.api_key}
        response = self._retry_request(url, headers, retries)
        return self._handle_response(response)

    #*Utils
    def set_region(self, region: str):
        region = region.lower()

        platform_url = self.region_to_platform.get(region)
        regional_url = self.region_to_regional.get(region)
        realm = self.region_to_realm.get(region)
        realm_url = self.realm_urls.get(realm)

        if not platform_url or not regional_url:
            raise ValueError(f"Region not valid: {region}")

        self.region = region
        self.platform_url = platform_url
        self.regional_url = regional_url
        self.realm = realm
        self.realm_url = realm_url

    #*Enpoints
    #*Returns current version for realm
    def get_current_server_versions(self):
        url = f"{self.ddragon_url}/realms/{self.realm}.json"
        return self._make_request(url)

    #*Returns champion.json
    def get_current_champions_json(self):
        current_version = self.get_current_server_versions()["dd"]
        url = f"{self.ddragon_url}/cdn/{current_version}/data/en_US/champion.json"
        return self._make_request(url)

    #*Returns champion information
    #!Champion Name is case sensitive because the API expects the exact casing used in the data source
    def get_champion_information(self, champion_name):
        current_version = self.get_current_server_versions()["dd"]
        url = f"{self.ddragon_url}/cdn/{current_version}/data/en_US/champion/{champion_name}.json"
        return self._make_request(url)

    #*Returns profile icon image url
    def get_profile_icon_url(self, icon_id):
        current_version = self.get_current_server_versions()["dd"]
        url = f"{self.ddragon_url}/cdn/{current_version}/img/profileicon/{icon_id}.png"
        return url
    
    #*Returns summoner.json
    def get_summoner_spells(self):
        current_version = self.get_current_server_versions()["dd"]
        url = f"{self.ddragon_url}/cdn/{current_version}/data/en_US/summoner.json"
        return self._make_request(url)
    
    #* Returns list of queues
    def get_queues(self):
        url = f"{self.static_url}/docs/lol/queues.json"
        return self._make_request(url)
    
    #*Returns a history of the league versions
    def get_version_history(self):
        url = f"{self.ddragon_url}/api/versions.json"
        return self._make_request(url)

    #*ACCOUNT-V1 [Summoner Name, Tag]
    #*ACCOUNT-V1 [PUUID]
    #*Returns puuid, gameName, tagLine
    def get_account(self, summoner_name=None, tag=None, puuid=None):
        if puuid:
            url = f"{self.regional_url}/riot/account/v1/accounts/by-puuid/{puuid}"
        elif summoner_name and tag:
            url = f"{self.regional_url}/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag}"
        else:
            raise ValueError(
                "Either 'puuid' or 'summoner_name' and 'tag' must be provided."
            )
        return self._make_request(url)

    #*CHAMPION-MASTERY-V4 [PUUID]
    def get_champion_mastery(self, puuid):
        url = f"{self.platform_url}/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}"
        return self._make_request(url)

    #*CHAMPION-MASTERY-V4-SCORE [PUUID]
    def get_champion_mastery_score(self, puuid):
        url = f"{self.platform_url}/lol/champion-mastery/v4/scores/by-puuid/{puuid}"
        return self._make_request(url)

    #*CHAMPION-MASTERY-V4-TOP [PUUID. AMOUNT]
    def get_top_champion_masteries(self, puuid, amount):
        url = f"{self.platform_url}/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top?count={amount}"
        return self._make_request(url)

    #*LEAGUE-V4 [Summoner Id]
    #*Returns league entries
    def get_league_entries_by_summoner_id(self, summoner_id):
        url = f"{self.platform_url}/lol/league/v4/entries/by-summoner/{summoner_id}"
        return self._make_request(url)
    
    #*LEAGUE-V4/GRAND LEAGUES
    #*Returns high elo league entries for soloQ in a list
    def get_high_tier_league_entries(self, league):
        leagues = ['challengerleagues', 'grandmasterleagues', 'masterleagues']
        if league in leagues:
            url = f"{self.platform_url}/lol/league/v4/{league}/by-queue/RANKED_SOLO_5x5"
            return self._make_request(url)
        else:
            return []
    
    #*LEAGUE-V4/NORMAL LEAGUES
    #*Returns a page for league and division
    def get_ranked_league_entries(self, league, division, page):
        leagues = ['BRONZE', 'SILVER', 'GOLD', 'IRON', 'PLATINUM', 'EMERALD', 'DIAMOND']
        divisions = ['IV', 'III', 'II', 'I']
        
        if league not in leagues:
            return []
        if division not in divisions:
            return []
        if not isinstance(page, int) or page < 1:
            return []
        
        url = f"{self.platform_url}/lol/league/v4/entries/RANKED_SOLO_5x5/{league}/{division}?page={page}"
        return self._make_request(url)

    #*LOL-CHALLENGES-V1 [PUUID]
    #*Returns challenges information
    def get_challenges(self, puuid):
        url = f"{self.platform_url}/lol/challenges/v1/player-data/{puuid}"
        return self._make_request(url)
    
    #*LOL-CHALLENGES-V1-CONFIG
    #*Returns configuration of challenges
    def get_challenges_config(self):
        url = f"{self.platform_url}/lol/challenges/v1/challenges/config"
        return self._make_request(url)

    #*MATCH-V5 [Match Id]
    #*Returns match information
    def get_match(self, match_id):
        url = f"{self.regional_url}/lol/match/v5/matches/{match_id}"
        return self._make_request(url)

    #*MATCH-V5 [PUUID] [startTime, endTime, queue, type, start, count]
    #* startTime: The matchlist started storing timestamps on June 16th, 2021. Any matches played before June 16th, 2021 won't be included in the results
    #* startTime & endTime: epoch timestamp in seconds
    #* queue: queueId (https://static.developer.riotgames.com/docs/lol/queues.json)
    #* start: defaults to 0
    #* count: defaults to 20, max 100
    #*Returns list of matches
    def get_matches_by_puuid(self, puuid, **kwargs):
        url = f"{self.regional_url}/lol/match/v5/matches/by-puuid/{puuid}/ids"
        if kwargs:
            url += "?"
            url += "&".join(
                [f"{key}={value}" for key, value in kwargs.items()])
        return self._make_request(url)
    
    #*MATCH-V5/TIMELINE [Match Id]
    #*Returns timeline match information
    def get_match_timeline(self, match_id):
        url = f"{self.regional_url}/lol/match/v5/matches/{match_id}/timeline"
        return self._make_request(url)

    #*SPECTATOR-V5 [PUUID]
    #*Returns current match information
    #!Arena matches do not show up
    def get_current_match_by_puuid(self, puuid):
        url = f"{self.platform_url}/lol/spectator/v5/active-games/by-summoner/{puuid}"
        return self._make_request(url)

    #*SUMMONER-V4 [PUUID]
    #*SUMMONER-V4 [Summoner Id]
    #*SUMMONER-V4 [Account Id]
    #*Returns id, accountId, puuid, profileIconId, revisionDate, summonerLevel
    def get_summoner(self, puuid=None, summoner_id=None, account_id=None):
        if puuid:
            url = f"{self.platform_url}/lol/summoner/v4/summoners/by-puuid/{puuid}"
        elif summoner_id:
            url = f"{self.platform_url}/lol/summoner/v4/summoners/{summoner_id}"
        elif account_id:
            url = f"{self.platform_url}/lol/summoner/v4/summoners/by-account/{account_id}"
        else:
            raise ValueError(
                "One of 'puuid', 'summoner_id', or 'account_id' must be provided."
            )
        return self._make_request(url)

#* Initialize RiotAPI with API key
