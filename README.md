# xblocks

> super-ultra configurable "blocks" for xsetroot

## Usage
```sh
python main.py
```

You can use the `--no-setroot` to just print what would get set.

## Configuration

### Crypto
Key|Default Value|Description
---|---|---
fiat_currency|`'eur'`|Fiat currency to use
fiat_currency_suffix|`'€'`|Fiat currency suffix
fiat_currency_prefix|`''`|Fiat currency prefix
crypto_currencies|`['xmr', 'eth', 'btc']`|Crypto currencies to fetch
crypto_interval|`20000`|Crypto currency fetch interval in milliseconds

### Weather
Key|Default Value|Description
---|---|---
weather_interval|`20000`|Weather currency fetch interval in milliseconds
weather_location|`'Helsinki'`|Weather location
fetch_weather|`True`|Whether to fetch the weather

### General
Key|Default Value|Description
---|---|---
General|value|desc
delimeter|`' \| '`|Delimeter for the blocks
use_emoji|`True`|Whether to use the full name or emoji of the block
suffix|`'     .'`|Suffix to follow the generated string on the root name set
debug|`False`|Whether to log more information

### Block types
Command|Example|Description
---|---|---
`price <currency>`|`price xmr`|Returns the specified cryptocurrency value in the configured fiat currency
`weather`|-|Returns the current weather from wttr.in
`time`|-|Returns the current time
`date`|-|Returns the current date
`datetime`|-|Returns the current date and time
`cmd <command>`|`cmd echo hi`|Returns the specified command's output

### Block specification
```py
("price xmr",   "Monero 🔒",   "🔒",    1000),
```
