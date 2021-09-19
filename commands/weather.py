import requests

class Block:
    def __init__(self, data):        
        self.content = 'Loading'.rjust(5)
        self.override_icon = False
        self.location = data.get('location', '')
    def fetch(self):
        url = 'https://wttr.in/' + self.location + '?format=%t'
        res = requests.get(url)
        if res.status_code > 299 or res.status_code < 200:
            self.content = 'Error'.rjust(5)
            return
        self.content = res.text.rjust(5)
