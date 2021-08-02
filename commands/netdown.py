import util

class Block:
    def __init__(self, _data):
        self.rx_prev = 0
        self.rx_speed = 0
        
        self.content = 'Loading'.rjust(8)
        self.override_icon = False
    def fetch(self):
        rx = util.get_net_bytes('rx')

        if rx > 0:
            self.rx_speed = rx - self.rx_prev

        self.rx_prev = rx
        
        rx_speed_str = util.HumanBytes.format(self.rx_speed, True)

        self.content = f'{rx_speed_str.rjust(8)}'