import datetime

class Block:
    def __init__(self, _data):        
        self.content = 'Loading'
        self.override_icon = False
    def fetch(self):
        self.content = datetime.date.today().strftime('%d.%m.%Y')