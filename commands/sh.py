import subprocess

class Block:
    def __init__(self, data):        
        self.content = 'Loading'
        self.override_icon = False
        self.cmd = data.get('cmd', '')
    def fetch(self):
        p = subprocess.run(["bash", "-c", self.cmd], capture_output=True)
        self.content = p.stdout.decode('utf-8')