# Tommie Branch

# Arguments
import sys
import argvparser
# Origin imports
import time
import random
import requests
import json
import asyncio
import websocket

# DAANCODE je ne comprend pas
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

## Tommie Code - INIT AND TAKE PARAMETERS OR HARVEST INPUT
# Tel items in list en prop die in count var
def checkArg():
    global dicter
    global coin
    global wallet
    global sleep
    global ticks

    # Bij meer dan 4 items in list, waarschijnlijk params meegegeven
    count = len(sys.argv)
    if (count > 4):
        coin = sys.argv[1]
        wallet = sys.argv[2]
        sleep = sys.argv[3]
        ticks = sys.argv[4]
        print("Parameters taken from command prompt")
        print("Coin: " + coin + " | Wallet: " + wallet + " | Sleep: " + sleep + " | Ticks: " + ticks)
    else:
        print("This script can be run with paramaters eg. python script.py coin wallet sleep ticks")
        coin = input("Enter coin: ")
        wallet = input("Enter wallet size: ")
        sleep = input("Enter duration in s: ")
        ticks = input("Enter ticks: ")
        print("Coin: " + coin + " | Wallet: " + wallet + " | Sleep: " + sleep + " | Ticks: " + ticks)

    # Prep var for DaanCode
    dicter['wallet'] = wallet
    dicter['ticker'] = coin
    dicter['sleep'] = sleep
    dicter['counter'] = ticks

## Tommie code - Schrijf result naar result.csv
def writeResult():
    global dicter
    global coin
    global wallet
    global sleep
    global ticks
    filename = coin + "-" + wallet + "-" + sleep + "-" + ticks

    printwallet = float(dicter['wallet'])
    round(printwallet,2)
    printwallet = str(printwallet)

    # Open the file in append en read mode ('a+')
    with open( "results\" + filename + ".csv", "a+") as file_object:
        # naar start!
        file_object.seek(0)
        # Als niet leeg dan append '\n'
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write("\n")
        # Append voeg toe aan einde file
        file_object.write(coin + "," + wallet + "," + sleep + "," + ticks + "," + printwallet)


#DAAN DINGEN
def on_message(ws, message):
    json_data = json.loads(message)
    global bla
    global dicter
    int(dicter['count'])
    if int(bla) == 0:
        bla = 1
    else:
        if int(dicter['count'])==int(dicter['counter']):
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
    writeResult()

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
        time.sleep(int(dicter['sleep']))
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())

if __name__ == "__main__":
    #Tommie functie om params te pakken of input te vragen
    checkArg()
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws",
                              on_open = on_open,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)

    ws.run_forever()
