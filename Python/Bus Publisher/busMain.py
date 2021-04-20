# Tommie Branch


import sys      # passing arguments
import argvparser    # passing args

import time
import random
import requests
import json
import asyncio
import websocket

## SPIELERIJ

print ("The script has the name %s" % (sys.argv[0]))

## EINDE



#key RxdSpWXcboa3SqxhSaP1mElEaYeyL7vl43WWe9bdOO05VkGn3iNmYJsbPHara1Og
#secret GxLgnrfUbZIAb9u3vB0iXCLiG3jRBkK8eGk7euXFpWcDUb7k5b5anAK4wu4bWhu9
# "wss://stream.binance.com:9443/ws"
try:
    import thread
except ImportError:
    import _thread as thread
import time

dicter = {
    'coinz':0,
    'count':0
}
bla = 0

size = int(input('Walet size:'))
dicter['wallet'] = size
print(size)
ticker = input('ticker (coin@ticker):')
dicter['ticker'] = ticker
print(ticker)
sleep = int(input('sleep:'))
dicter['sleep'] = sleep
print(sleep)
counter = int(input('count:'))
dicter['counter'] = counter
print(counter)


def on_message(ws, message):
    json_data = json.loads(message)
    global bla
    global dicter
    int(dicter['count'])
    if int(bla) == 0:
        bla = 1
    else:
        if int(dicter['count'])>int(dicter['counter']):
            dicter['count'] = 0
            dicter['s'] = json_data['s']
            print(json_data['s'] + ' ' + json_data['c'])
            if float(format(float(json_data['c'])-float(dicter[json_data['s']]), '.8f'))>0:      # >= in dit systeem is een sell voor niet omhoog gaan niet erg
                print('HOLD')
                if  float(dicter['coinz']) == 0 :
                    dicter['coinz'] = format(float(dicter['wallet'])/float(json_data['c']), '.8f')
                    dicter['wallet'] = 0
                    print('BUY coinz: ' + dicter['coinz'])
            else:
                if float(dicter['coinz']) > 0:
                    print('SELL')
                    dicter['wallet'] = format(float(dicter['coinz'])*float(json_data['c']), '.8f')
                    dicter['coinz'] = 0
                print(dicter['wallet'])

        elif int(dicter['count']) == 0:
            #print(json_data['s'] + ' ' + json_data['c'])
            dicter[json_data['s']] = json_data['c']
            dicter['count'] = int(dicter['count'])+1
        else :
            dicter['count'] = int(dicter['count'])+1


        #print(dicter[json_data['s']])

def on_error(ws, error):
    print(error)

def on_close(ws):
    global dicter
    if float(dicter['wallet'])==0 :
        print('FINAL SELL')
        dicter['wallet'] = format(float(dicter['coinz'])*float(dicter[dicter['s']]), '.8f')
        dicter['coinz'] = 0
    print("### closed ###")
    print(dicter['wallet'])
    print(dicter['sleep'])
    print(dicter['count'])
    print("### closed ###")

def on_open(ws):
    global dicter
    dicter['count'] =0
    dicter['coinz']=0
    def run(*args):
        jsons = """{"method": "SUBSCRIBE","params": [],"id": 1}"""
        settingding ={
            'method':'SUBSCRIBE',
            'params':[dicter['ticker']+'busd@ticker'],
            'id':1
            }
        jsons = json.dumps(settingding)
        ws.send(jsons)
        time.sleep(dicter['sleep'])
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws",
                              on_open = on_open,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)

    ws.run_forever()
