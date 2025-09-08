import re
from datetime import datetime

class Utilities:

    def split_summoner_name(self, summoner_name):
        try:
            match = re.split(r'[^a-zA-Z0-9 ]+', summoner_name)
            if len(match) < 2:
                return None, None
            name = match[0]
            tag = match[-1]
            return name, tag
        except Exception as e:
            return None, None
        
    def time_ago(self, event_time):
        compared_time = datetime.now()
        if event_time > compared_time:
            return 'How did you play in the future?'
        difference = compared_time-event_time # in seconds, is always positive 
        if difference > 86400: # at least a day ago
            time_formatted = int(difference/86400)
            if time_formatted == 1:
                time_string = f'{time_formatted} day ago'
            else:
                time_string = f'{time_formatted} days ago'
        elif difference > 3600: # at least an hour ago
            time_formatted = int(difference/3600)
            if time_formatted == 1:
                time_string = f'{time_formatted} hour ago'
            else:
                time_string = f'{time_formatted} hours ago'
        elif difference > 60:# at least a minute
            if time_formatted == 1:
                time_string = f'{time_formatted} minute ago'
            else:
                time_string = f'{time_formatted} minutes ago'
        elif difference < 60:
            return f'{difference} seconds ago'
    
        return time_string

    def timestamp_to_date_time(self, timestamp):
        dt = datetime.fromtimestamp(timestamp / 1000)
        day = dt.day
        if 10 <= day % 100 <= 20:  # Special case for teens
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        formatted_date = dt.strftime(f'%A, %B {day}{suffix} %Y %H:%M')
        return formatted_date