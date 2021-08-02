import config

class Block:
    cache = None
    def __init__(self, data):        
        self.content = 'Loading'.rjust(10)
        self.override_icon = False
        self.currency = data.get('currency')
    def fetch(self):
        if Block.cache == None:
            self.content = 'Loading'.rjust(10)
            return
        crypto_price = Block.cache.get(self.currency.upper(), {})
        crypto_price = crypto_price.get(config.fiat_currency.upper(), 'Error!')

        crypto_price = f'{config.fiat_currency_prefix}{crypto_price}'
        crypto_price = f'{crypto_price}{config.fiat_currency_suffix}'

        self.content = crypto_price.rjust(10)