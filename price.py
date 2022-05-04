from datetime import datetime
from time import sleep
from binance import Client

import global_var

def generateCandle(event):
    client = Client()
    while event.is_set() == False:
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        timestamp = int(timestamp/60) * 60000
        timestamp = timestamp - 60000 * 5
        klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, timestamp)
        for x in klines:
            if x[0] not in global_var.gcandle:
                print('*'*10)
                print(global_var.gcandle)
                if bool(global_var.gcandle):
                    glast_candle = list(global_var.gcandle.items())[-1]
                    if global_var.gmain_dlg is not None:
                        global_var.gmain_dlg.addRow(glast_candle[1])
            global_var.gcandle[x[0]] = {
                'time': str(datetime.fromtimestamp(x[0]/1000)),
                'o' : str(round(float(x[1]), 2)),
                'h' : str(round(float(x[2]), 2)),
                'l' : str(round(float(x[3]), 2)),
                'c' : str(round(float(x[4]), 2)),
                'v' : str(round(float(x[5]), 4))
            }
        btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
        if glast_candle != None:
            # getOffset(glast_candle[1]['c'], btc_price['price'])
            print("last: {last}   current: {cur}   off:{offset}".format(last=glast_candle[1]['c'], cur=btc_price['price'], offset=getOffset(glast_candle[1]['c'], btc_price['price'])))
            if global_var.gmain_dlg is not None:
                global_var.gmain_dlg.setStatus(btc_price['price'], getOffset(glast_candle[1]['c'], btc_price['price']))
        # print(btc_price)
        sleep(0.25)

def getOffset(a, b):
    a = float(a)
    b = float(b)
    offset = (b - a) / a * 100.0
    return offset
