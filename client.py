from binance import Client
import global_var

def init():
    # env_vars = {}
    # with open('.env') as f:
    #     for line in f:
    #         if line.startswith('#') or not line.strip():
    #             continue
    #         key, value = line.strip().split('=', 1)
    #         env_vars[key] = value
    env_vars = {
        'key':'hQriA7OidAQb5UP44YKyY9tTBtBqR6KMkd3eKK4227rg41m6G59ZdJXGhPT2vRdb',
        'sec':'kDosa6Eswxk2dnyzuX9O24fyuin7PXRS44CNlFRmfLKMI93yXOlbNe0g50n8A4UG',
        'net':'False'
    }
    if env_vars['net'] == 'True':
        env_vars['net'] = True
    else:
        env_vars['net'] = False
    global_var.clientObj = Client(env_vars['key'], env_vars['sec'], testnet=env_vars['net'])
    global_var.clientObj.get_server_time()

def getWallet():
    acc_info = global_var.clientObj.get_account()
    tmp_w = []
    for x in acc_info['balances']:
        tmp = {
            'asset':x['asset'],
            'free':float(x['free']),
            'locked':float(x['locked'])
        }
        if tmp['free'] != 0 or tmp['locked'] != 0:
            tmp_w.append(tmp)
    return tmp_w

def buymarket(symbol, quatity):
    try:
        global_var.clientObj.order_market_buy(symbol=symbol, quantity=quatity)
    except ValueError:
        pass

def sellmarket(symbol, quatity):
    try:
        global_var.clientObj.order_market_sell(symbol=symbol, quantity=quatity)
    except ValueError:
        pass
