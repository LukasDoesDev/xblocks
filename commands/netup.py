import util

class Block:
    def __init__(self, _data):
        self.tx_prev = 0
        self.tx_speed = 0
        
        self.content = 'Loading'.rjust(8)
        self.override_icon = False
    def fetch(self):
        tx = util.get_net_bytes('tx')

        if self.tx_prev > 0:
            self.tx_speed = tx - self.tx_prev

        self.tx_prev = tx

        tx_speed_str = util.HumanBytes.format(self.tx_speed, True)

        self.content = f'{tx_speed_str.rjust(8)}'