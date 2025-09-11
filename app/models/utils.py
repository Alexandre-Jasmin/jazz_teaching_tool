import re, json
from datetime import datetime
from pathlib import Path
from typing import Any

class Utilities:

    def split_summoner_name(self, summoner_name: str) -> tuple:
        try:
            match = re.split(r'[^a-zA-Z0-9 ]+', summoner_name)
            if len(match) < 2:
                return None, None
            return match[0], match[1]
        except Exception as e:
            return None, None
        
    def time_ago(self, event_time: datetime) -> str:
        compared_time = datetime.now()
        if event_time > compared_time:
            return 'How did you play in the future?'
        difference = (compared_time-event_time).total_seconds()
        if difference > 86400:
            time_formatted = int(difference/86400)
            if time_formatted == 1:
                time_string = f'{time_formatted} day ago'
            else:
                time_string = f'{time_formatted} days ago'
        elif difference > 3600:
            time_formatted = int(difference/3600)
            if time_formatted == 1:
                time_string = f'{time_formatted} hour ago'
            else:
                time_string = f'{time_formatted} hours ago'
        elif difference > 60:
            time_formatted = int(difference / 60)
            if time_formatted == 1:
                time_string = f'{time_formatted} minute ago'
            else:
                time_string = f'{time_formatted} minutes ago'
        elif difference < 60:
            return f'{difference} seconds ago'
        return time_string

    def timestamp_to_date_time(self, timestamp: int) -> str:
        dt = datetime.fromtimestamp(timestamp / 1000)
        day = dt.day
        if 10 <= day % 100 <= 20:  # Special case for teens
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        formatted_date = dt.strftime(f'%A, %B {day}{suffix} %Y %H:%M')
        return formatted_date
    
    def read_json_file(self, file_path: str | Path) -> Any:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {e}")

    def dump_json_file(self, file_path: str | Path, my_data: Any) -> None:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(my_data, f, indent=4)

    def format_game_duration(self, game_duration: int) -> str:
        try:
            hours, remainder = divmod(game_duration, 3600)
            minutes, seconds = divmod(remainder, 60)
        except Exception as e:
            return "Invalid Game Duration"
        
        parts = []
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if seconds > 0 or not parts:
            parts.append(f"{seconds}s")

        return " ".join(parts)
