import time

def get_clock_icon():
    clock_pos = time.strftime("%I")
    if clock_pos == "00": clock_icon = "🕛"
    elif clock_pos == "01": clock_icon = "🕐"
    elif clock_pos == "02": clock_icon = "🕑"
    elif clock_pos == "03": clock_icon = "🕒"
    elif clock_pos == "04": clock_icon = "🕓"
    elif clock_pos == "05": clock_icon = "🕔"
    elif clock_pos == "06": clock_icon = "🕕"
    elif clock_pos == "07": clock_icon = "🕖"
    elif clock_pos == "08": clock_icon = "🕗"
    elif clock_pos == "09": clock_icon = "🕘"
    elif clock_pos == "10": clock_icon = "🕙"
    elif clock_pos == "11": clock_icon = "🕚"
    elif clock_pos == "12": clock_icon = "🕛"
    else: clock_icon = "❌"
    return clock_icon

class Block:
    def __init__(self, data):        
        self.content = 'Loading'
        self.override_icon = data.get('override_icon') == True
    def get_icon(self):
        return get_clock_icon()
    def fetch(self):
        self.content = time.strftime('%H:%M:%S')