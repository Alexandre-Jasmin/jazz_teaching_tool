# Full Documentation

# LeaguePlayer Class (app/models/league_player.py)

## Overview

The `LeaguePlayer` class is a Python abstraction around a **League of Legends player profile**.
It fetches data from the **Riot Games API** (via `RIOT_API_INSTANCE`) and processes it into a structured representation containing:

* **Account info**
* **Summoner profile details**
* **Champion mastery history**
* **Challenges progress and thresholds**
* **Match history with summaries**

The class separates **data fetching** from **data processing** through helper methods (`_process_matches`, `_process_challenges`, `_process_champions`).

---

## Dependencies

This class relies on:

* **Standard Library**

  * `json`: Used for reading/writing cached match data.
  * `datetime`: For converting timestamps to human-readable forms.

* **Project Modules** (`config.py`)

  * `RIOT_API_INSTANCE`: Wrapper for Riot Games API calls.
  * `UTILITIES`: Helper functions (e.g., splitting summoner name, time formatting, JSON file I/O).
  * `Config`: Configuration (e.g., file directories for match storage).
  * `LEAGUE_CHAMPIONS`: Static champion dataset (from Riot Data Dragon).
  * `LOL_CHALLENGES_CONFIG`: Static challenge definitions (IDs, names, thresholds).
  * `QUEUES`: Static list of queue types (`queueId → description`).

---

## Initialization

```python
player = LeaguePlayer("SummonerName#Tag", "euw1")
```

When initialized:

1. Splits summoner name & tag (`SummonerName#Tag` → `SummonerName`, `Tag`).

2. Configures the API region.

3. Fetches all major Riot API data related to the player:

   * Account metadata
   * Summoner profile
   * Champion mastery list
   * Challenge progress
   * Recent matches

4. Initializes empty containers for processed data:

   * `self.matchesData` → full raw match JSONs.
   * `self.historyData` → simplified match summaries.

5. Calls private processors to enrich raw data:

   * `_process_champions()`
   * `_process_challenges()`
   * `_process_matches()`

---

## Attributes

| Attribute          | Type         | Description                                                            |
| ------------------ | ------------ | ---------------------------------------------------------------------- |
| `summoner_name`    | `str`        | Full summoner name with tag.                                           |
| `server`           | `str`        | Server/region (e.g., `"euw1"`, `"na1"`).                               |
| `name`             | `str`        | Extracted summoner name (before `#`).                                  |
| `tag`              | `str`        | Extracted tag (after `#`).                                             |
| `accountPatch`     | `dict`       | Current Riot patch/version metadata.                                   |
| `accountData`      | `dict`       | Riot account info (includes PUUID).                                    |
| `summonerData`     | `dict`       | Summoner profile (icon, level, etc.).                                  |
| `championData`     | `list[dict]` | Champion mastery entries for this player.                              |
| `challengesData`   | `dict`       | Challenge progress for this player.                                    |
| `matchData`        | `list[str]`  | List of recent match IDs (from Riot API).                              |
| `matchesData`      | `list[dict]` | Raw match JSON data (cached).                                          |
| `historyData`      | `list[dict]` | Simplified match summaries (champion, KDA, outcome).                   |
| `challengesConfig` | `list[dict]` | Static config of challenge definitions (localized names + thresholds). |

---

## Methods

### 🔹 `_process_matches() -> None`

Processes all matches in `self.matchData` and populates:

* `self.matchesData` with full match JSON.
* `self.historyData` with simplified summaries.

**Workflow**:

1. Load each match from cache (`Config.MATCHES_DIR`) or fetch from API.
2. Locate this player in the match using PUUID.
3. Extract match-specific details:

   * Champion played
   * Level
   * K/D/A and computed KDA ratio
   * Queue type (mapped from `QUEUES`)
   * Match outcome (`Win` / `Loss`)
   * Duration
   * Time ago (human-readable from timestamp)

**Edge cases**:

* If queue ID is not found in `QUEUES`, `"Private Custom Game"` is used.
* If `deaths == 0`, KDA is set to `kills + assists` to avoid division by zero.

---

### 🔹 `_process_challenges() -> None`

Processes challenge progress and enriches them with metadata.

**Workflow**:

1. Build a dictionary (`challenge_defs`) of static challenge definitions:

   * ID → title, description, thresholds (sorted by required value).
2. For each challenge in `self.challengesData`:

   * Add title and description.
   * Attach sorted thresholds.
   * Compute the **next threshold** (first rank above current value).

**Edge cases**:

* If no thresholds are left, `("None", 0)` is set as the next threshold.
* If challenge ID not in `challenge_defs`, it’s skipped silently.

---

### 🔹 `_process_champions() -> None`

Enriches champion mastery data.

**Workflow**:

1. Build a `championId → championName` map using static `LEAGUE_CHAMPIONS`.
2. For each mastery entry:

   * Add `championName`.
   * Convert `lastPlayTime` (epoch ms) to a human-readable date string.

**Edge cases**:

* If champion ID is not found in static data, `"Unknown"` is used.

---

### 🔹 `_build_champion_map() -> dict[int, str]`

Static helper method.
Builds `{championKey: championName}` mapping from `LEAGUE_CHAMPIONS`.

---

### 🔹 `_calculate_kda(kills: int, deaths: int, assists: int) -> float`

Computes **Kill/Death/Assist ratio**.

* If `deaths == 0`: returns `kills + assists`.
* Otherwise: `(kills + assists) / deaths`.

---

### 🔹 `_get_queue_description(queue_id: int) -> str`

Maps a `queueId` to a human-readable description using `QUEUES`.

* Returns `"Private Custom Game"` if unknown.

---

### 🔹 `_get_outcome(win_flag: bool, outcome_dict: dict[str, bool]) -> str`

Maps the boolean `win` flag to `"Win"` or `"Loss"`.

* Returns `"Unknown outcome"` if mapping fails.

---

### 🔹 `_get_next_threshold(value: float, thresholds: list[tuple[str, float]]) -> tuple[str, float]`

Finds the **next rank threshold** a player hasn’t reached yet.

* Returns `(rank, value)` of the next tier.
* Returns `("None", 0)` if the player has maxed out.

---

## Example Usage

```python
player = LeaguePlayer("Faker#KR1", "kr")

print(player.summonerData["summonerLevel"])  
# -> 550

print(player.championData[0]["championName"])  
# -> "Ahri"

print(player.historyData[0])  
# -> {
#   'champion': 'Ahri',
#   'level': 18,
#   'kda_string': '10 / 2 / 8',
#   'kda': 9.0,
#   'queue': 420,
#   'queue_description': 'Ranked Solo/Duo',
#   'when': 1725891845000,
#   'time_ago': '2 hours ago',
#   'outcome': 'Win',
#   'duration': 1802
# }
```

---

## Design Notes

* **Caching**: Matches are cached locally under `Config.MATCHES_DIR`. Prevents re-fetching the same match ID.
* **Extensibility**:

  * You could add `_process_items()` or `_process_runes()` in the future for richer match data.
  * Challenges are designed to handle **dynamic Riot challenge configs**.
* **Error tolerance**: Unknown queue IDs, missing champion IDs, and missing challenge definitions all degrade gracefully with default values.

---