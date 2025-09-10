import json
from datetime import datetime
from config import (
    RIOT_API_INSTANCE,
    UTILITIES,
    Config,
    LEAGUE_CHAMPIONS,
    LOL_CHALLENGES_CONFIG, 
    QUEUES
)

class LeaguePlayer():

    def __init__(self, summoner_name: str, server: str) -> None:
        self.summoner_name = summoner_name
        self.server = server
        self.name, self.tag = UTILITIES.split_summoner_name(self.summoner_name)

        RIOT_API_INSTANCE.set_region(self.server)
        self.accountPatch = RIOT_API_INSTANCE.get_current_server_versions()

        self.accountData = RIOT_API_INSTANCE.get_account(
            summoner_name=self.name, tag=self.tag
        )
        self.summonerData = RIOT_API_INSTANCE.get_summoner(
            puuid=self.accountData["puuid"]
        )
        self.championData = RIOT_API_INSTANCE.get_champion_mastery(
            puuid=self.accountData["puuid"]
        )
        self.challengesData = RIOT_API_INSTANCE.get_challenges(
            puuid=self.accountData["puuid"]
        )
        self.matchData = RIOT_API_INSTANCE.get_matches_by_puuid(
            puuid=self.accountData["puuid"],
            count=50
        )
        self.rankedData = RIOT_API_INSTANCE.get_league_entries_by_puuid(
            self.accountData["puuid"]
        )
        self.currentMatch = RIOT_API_INSTANCE.get_current_match_by_puuid(
            self.accountData["puuid"]
        )

        self.matchesData: list[dict] = []
        self.historyData: list[dict] = []
        self.challengesConfig = LOL_CHALLENGES_CONFIG

        self._process_champions()
        self._process_challenges()
        self._process_matches()
        self._process_rank()
        #self._process_current_match()

    def _process_current_match(self) -> None:
        if self.currentMatch:
            for participant in self.currentMatch["participants"]:
                continue

    def _process_rank(self) -> None:
        for entry in self.rankedData:
            bottom = entry["wins"]+entry["losses"]
            if bottom <= 0:
                entry["winrate"] = 0
            else:
                winrate = (entry["wins"]/(entry["wins"]+entry["losses"]))*100
                entry["winrate"] = round(winrate, 1)

    def _process_matches(self) -> None:

        outcome_dict = {"Win": True, "Loss": False}

        for match_id in self.matchData:
            file_path = Config.MATCHES_DIR / f"{match_id}.json"

            if file_path.exists():
                matchData = UTILITIES.read_json_file(file_path)
            else:
                matchData = RIOT_API_INSTANCE.get_match(match_id=match_id)
                UTILITIES.dump_json_file(file_path, matchData)

            player_data = self._get_player_data(
                matchData["info"]["participants"],
                self.accountData["puuid"]
            )

            try:
                history_entry = {
                    "match_id": matchData["info"]["gameId"],
                    "platform_id": matchData["info"]["platformId"],
                    "match_length": matchData["info"]["platformId"],
                    "champion": player_data.get("championName", "Unknown"),
                    "level": player_data.get("champLevel", 0),
                    "kda_string": f"{player_data.get('kills', 0)} / {player_data.get('deaths', 0)} / {player_data.get('assists', 0)}",
                    "kda": self._calculate_kda(
                        player_data.get("kills", 0),
                        player_data.get("deaths", 0),
                        player_data.get("assists", 0),
                    ),
                    "queue": matchData.get("info", {}).get("queueId", -1),
                    "queue_description": self._get_queue_description(
                        matchData.get("info", {}).get("queueId", -1)
                    ),
                    "when": matchData.get("info", {}).get("gameEndTimestamp", 0),
                    "time_ago": UTILITIES.time_ago(
                        datetime.fromtimestamp(
                            matchData.get("info", {}).get("gameEndTimestamp", 0) / 1000
                        )
                    ) if matchData.get("info", {}).get("gameEndTimestamp") else "Unknown",
                    "outcome": self._get_outcome(
                        player_data.get("win", False), outcome_dict
                    ),
                    "duration": matchData.get("info", {}).get("gameDuration", 0),
                }
            except Exception as e:
                history_entry = {}
                continue

            self.historyData.append(history_entry)
            self.matchesData.append(matchData)

    def _process_challenges(self) -> None:
        
        challenge_defs = {
            definition["id"]: {
                "title": definition["localizedNames"]["en_US"]["name"],
                "description": definition["localizedNames"]["en_US"]["description"],
                "thresholds": sorted(
                    definition["thresholds"].items(), key=lambda x: x[1]
                ),
            }
            for definition in self.challengesConfig
        }

        for challenge in self.challengesData["challenges"]:
            challenge_id = challenge["challengeId"]
            if challenge_id not in challenge_defs:
                continue
            meta = challenge_defs[challenge_id]
            challenge.update(
                {
                    "title": meta["title"],
                    "description": meta["description"],
                    "threshold": meta["thresholds"],
                    "next_thresholds": self._get_next_threshold(
                        challenge["value"], meta["thresholds"]
                    ),
                }
            )

    def _process_champions(self) -> None:
        champion_map = self._build_champion_map()
        for entry in self.championData:
            champ_id = entry["championId"]
            entry["championName"] = champion_map.get(champ_id, "Unknown")
            entry["lastPlayTimePretty"] = UTILITIES.timestamp_to_date_time(int(entry["lastPlayTime"]))

    @staticmethod
    def _build_champion_map() -> dict[int, str]:
        return {int(champ["key"]): champ["name"] for champ in LEAGUE_CHAMPIONS["data"].values()}

    @staticmethod
    def _calculate_kda(kills: int, deaths: int, assists: int) -> float:
        kda = kills + assists if deaths == 0 else (kills + assists) / deaths
        return round(kda, 2)
    
    @staticmethod
    def _get_queue_description(queue_id: int) -> str:
        for q in QUEUES:
            if q["queueId"] == queue_id:
                return q["description"]
        return "Private Custom Game"
    
    @staticmethod
    def _get_outcome(win_flag: bool, outcome_dict: dict[str, bool]) -> str:
        return next(
            (label for label, value in outcome_dict.items() if value == win_flag),
            "Unknown outcome"
        )
    
    @staticmethod
    def _get_next_threshold(value: float, thresholds: list[tuple[str, float]]) -> tuple[str, float]:
        for rank, threshold_value in thresholds:
            if value < threshold_value:
                return rank, threshold_value
        return "None", 0
    
    @staticmethod
    def _get_player_data(participants: list[dict], my_puuid: str) -> dict:
        for participant in participants:
            if participant["puuid"] == my_puuid:
                return participant
        return {"status": "can't find information"}