# Crypto
fiat_currency = 'eur'
fiat_currency_suffix = '€'
fiat_currency_prefix = ''
crypto_interval = 40000 # in milliseconds

# General
delimeter = ' '
suffix = '     .'
interval = 1000 # setroot interval in milliseconds

blocks = [
    # command       icon     update interval in milliseconds
    # ('crypto',  '🔒', 1000,  {'currency': 'xmr'}),
    # ('crypto',  '🍸', 1000,  {'currency': 'eth'}),
    # ('crypto',  '💰', 1000,  {'currency': 'btc'}),
    ('weather', '☀', 1000,  {'location': 'Helsinki'}),
    ('netup',   '🔺', 2000,  {}),
    ('netdown', '🔻', 2000,  {}),
    ('date',    '🗓', 1000,  {}),
    ('time',    '',   1000,  {'override_icon': True}),
    # ('sh',      '🇫', 10000, {'cmd': 'fortune'}),
]


fetch_weather = any(map(lambda b: b[0] == 'weather', blocks))
crypto_blocks = filter(lambda b: b[0] == 'crypto', blocks)
crypto_currencies = list(map(lambda b: b[3]['currency'], crypto_blocks))
