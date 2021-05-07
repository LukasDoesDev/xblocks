import subprocess, threading, requests, json, datetime, time, importlib, sys

config = importlib.import_module('config')

blocks_cached_data = {}
threads = []

def reload_config():
    global config
    config = importlib.import_module('config')

def setroot(name):
    reload_config()
    name = name + config.suffix
    return subprocess.run(["xsetroot", "-name", name])

def get_clock_icon():
    clock_pos = datetime.datetime.now().strftime("%I")
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

def block_to_str(block):
    prefix = block[2] if config.use_emoji else block[1]
    temp_blocks_cache = blocks_cached_data
    if 'crypto' in temp_blocks_cache:
        temp_blocks_cache.pop('crypto')
    content = temp_blocks_cache.get(block[0], 'Loading')
    if type(content) == tuple:
        content = content[0]
    if prefix == '{}' and block[0] == 'time':
        prefix = prefix.format(get_clock_icon())
    return prefix + ' ' + content

def construct_multi_price_url(inputs, outputs):
    return f'''https://min-api.cryptocompare.com/data/pricemulti?fsyms={','.join(inputs)}&tsyms={','.join(outputs)}'''

def create_listener_thread(listener):
    t = threading.Thread(
        target=listener['function'],
        daemon=True,
        name=listener.get('name', 'Generic listener thread'),
        args=listener.get('args', None)
    )
    return t

def block_fn(block):
    t = threading.currentThread()
    if not block:
        return do_exit()
    while getattr(t, "do_run", True):
        # TODO do stuff here
        if callable(block[0]):
            blocks_cached_data[block[0]] = block[0]()
        elif 'price ' in block[0]:
            # is crypto handler
            cryptos_cache = blocks_cached_data.get('price', 'Loading')
            if cryptos_cache == 'Loading':
                crypto_price = cryptos_cache
            else:
                # crypto_price = cryptos_cache[0].get(config.fiat_currency.upper(), {})
                # crypto_price = crypto_price.get(block[0].replace('price ', '').upper(), 'Error!')

                crypto_price = cryptos_cache[0].get(block[0].replace('price ', '').upper(), {})
                crypto_price = crypto_price.get(config.fiat_currency.upper(), 'Error!')

                crypto_price = f'{config.fiat_currency_prefix}{crypto_price}'
                crypto_price = f'{crypto_price}{config.fiat_currency_suffix}'
            blocks_cached_data[block[0]] = (crypto_price, datetime.datetime.now())
        elif 'cmd ' in block[0]:
            command = block[0].replace('cmd ', '')
            proc = subprocess.run(["bash", "-c", command], capture_output=True)
            raw_output = proc.stdout
            output_str = raw_output.decode('utf-8')
            blocks_cached_data[block[0]] = output_str
        elif block[0] == 'time':
            blocks_cached_data[block[0]] = time.strftime('%H:%M:%S')
        elif block[0] == 'date':
            blocks_cached_data[block[0]] = datetime.date.today().strftime('%d.%m.%Y')
        elif block[0] == 'datetime':
            blocks_cached_data[block[0]] = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        else:
            pass # is invalid
        time.sleep(block[3] / 1000)
    if config.debug:
        print("Stopped " + t.name + " thread.")

def fetch_fn(options):
    name = options['name']
    get_url = options['get_url']
    use_json = options['use_json']
    cache_key = options['cache_key']
    get_interval = options['get_interval']

    if config.debug:
        print('Fetch thread ' + name + ' started')
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        def get_data():
            if config.debug:
                print('Fetch thread ' + name + ' getting data')
            global blocks_cached_data
            url = get_url()
            res = requests.get(url)
            data = res.json() if use_json else res.text
            blocks_cached_data[cache_key] = (data, datetime.datetime.now())
        def check_get():
            if not blocks_cached_data.get(cache_key):
                return get_data()
            # diff between last request and right now
            time_diff = (datetime.datetime.now() - blocks_cached_data[cache_key][1])
            time_diff_ms = time_diff.total_seconds() * 1000

            # if more diff than interval
            if time_diff_ms > get_interval():
                return get_data()
            
            time.sleep(1)
        check_get()
    if config.debug:
        print('Stopped ' + name + ' thread.')

def create_crypto_thread():
    def get_crypto_url():
        reload_config()
        return construct_multi_price_url(config.crypto_currencies, [config.fiat_currency])
    def get_crypto_interval():
        reload_config()
        return config.crypto_interval
    t = create_listener_thread({
        'function': fetch_fn,
        'name': 'crypto',
        'args': [{
            'name': 'crypto',
            'get_url': get_crypto_url,
            'cache_key': 'price',
            'get_interval': get_crypto_interval,
            'use_json': True,
        }],
    })
    t.start()
    threads.append(t)

def create_weather_thread():
    def get_weather_interval():
        reload_config()
        return config.weather_interval
    t = create_listener_thread({
        'function': fetch_fn,
        'name': 'crypto',
        'args': [{
            'name': 'weather',
            'get_url': lambda: 'https://wttr.in/' + config.weather_location + '?format=%t',
            'cache_key': 'weather',
            'get_interval': get_weather_interval,
            'use_json': False,
        }],
    })
    t.start()
    threads.append(t)

def create_blocks_threads():
    global threads
    stop_threads()
    threads = []
    for block in config.blocks:
        t = create_listener_thread({
            'function': block_fn,
            'name': block[1],
            'args': [block] # have to use either [block] or (block,)
        })
        t.start()
        threads.append(t)

def stop_threads():
    for t in threads:
        if config.debug:
            print("Trying to stop " + t.name + " thread.")
        t.do_run = False
    for t in threads:
        if not t.is_alive():
            t.join() # Waits until thread terminates

def do_exit():
    if config.debug:
        print("Trying to stop listener threads.")
    stop_threads()
    if config.debug:
        print("Stopped listener threads.")
        print("Trying to stop main thread.")
    setter_thread.do_run = False
    setter_thread.join() # Waits until thread terminates

if __name__ == "__main__":
    create_blocks_threads()
    if len(config.crypto_currencies) > 0:
        create_crypto_thread()
    if config.fetch_weather:
        create_weather_thread()
    def setter_thread_fn():
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            blocks_strs = map(block_to_str, config.blocks)
            root_str = config.delimeter.join(blocks_strs)
            print(root_str)
            if '--no-setroot' not in sys.argv:
                setroot(root_str)
            time.sleep(1)
        if config.debug:
            print("Stopped main thread.")
    setter_thread = threading.Thread(target=setter_thread_fn, daemon=True, name='setter_thread')
    setter_thread.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("Recieved SIGINT, stopping xblocks")
            if config.debug:
                print("Cache:", blocks_cached_data)
                print("Threads:", threads)
            do_exit()
            break
