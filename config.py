# Crypto
fiat_currency = 'eur'
fiat_currency_suffix = '€'
fiat_currency_prefix = ''
crypto_currencies = ['xmr', 'eth', 'btc']
crypto_interval = 40000 # in milliseconds

# Weather
weather_interval = 40000 # in milliseconds
weather_location = 'Helsinki'
fetch_weather = True

# General
delimeter = ' | '
use_emoji = True # use emoji instead of name
suffix = '     .'
debug = False

blocks = [
    # command       name           icon     update interval in milliseconds
    ("price xmr",   "Monero 🔒",   "🔒",    1000),
    ("price eth",   "Ethereum 🍸", "🍸",    1000),
    ("price btc",   "Bitcoin 💰",  "💰",    1000),
    ("weather",     "Weather ⛅",  "⛅",    1000),
    ("time",        "Time {}",     "{}",    1000),
    ("date",        "Date 📅",     "📅",    1000),
    # ("datetime",    "Date&Time",   "DT",    1000),
    # ("cmd fortune", "Fortune",     "🇫",    10000),
]