import re

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