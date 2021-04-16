import time
import random
import requests
import json
import asyncio
import websockets


buyLimit = 1000
sellLimit = 1100
currentBotState = 'Idle'
runLoop = 'Looprun:true'
currentPrice = 1000
eurBalance = 500
coinBalance = 0


class InfoFromBinance:
    symbol =''
    def __init__(self,symbol):
        self.symbol=symbol
    def getSymbolPrice(self):
        global currentPrice
        #do Http magic
        #response = requests.get('https://api.binance.com/api/v3/avgPrice?symbol=' + self.symbol)
        #print(response)  
        
        if currentBotState == 'Buy':
            currentPrice = currentPrice-random.randrange(0,1000,1)/1000
        else:
            currentPrice = currentPrice+random.randrange(0,1000,1)/1000

        return currentPrice
    def sellSymbol(self):
        #do Http magic
        return 'Succes Sell'
    def buySymbol(self):
        #do Http magic
        return 'Succes Buy'

class BotState:

    def __init__(self, name):
        self.name = name
        
    def setCurrentBotState(self,state):
        global currentBotState
        currentBotState = state
    def setSelllimit(self,limit):
        global sellLimit
        sellLimit = limit
    def setBuyLimit(self,limit):
        global buyLimit
        buyLimit = limit

    def CheckBasics(self):
        print('start check basics on class ' + self.name)

    def DoStateAction(self):
        raise NotImplementedError

class BotStates:
    class BotStateSell(BotState):
        def __init__(self):
            super().__init__('Sell')
            self.CheckBasics()

        def DoStateAction(self):
            print('get current price via API')
            binance = InfoFromBinance('ETHEUR')
            currentPrice = binance.getSymbolPrice()

            print('If Price (' + str(currentPrice) + ') higher than ' + str(sellLimit))
            
            if  currentPrice > sellLimit:
                print('Sell coins')
                print(binance.sellSymbol())
                print('Set Buy Limit to Sell - 1%')
                super().setBuyLimit(sellLimit*0.99)
                print('Set state to Buy')
                super().setCurrentBotState('Buy')
                pass
            else:
                print('Don\'t Sell coins')
                pass
            

        def CheckBasics(self):
            super().CheckBasics()
            
           
        
    class BotStateBuy(BotState):
        def __init__(self):
            super().__init__('Buy')
            self.CheckBasics()

        def DoStateAction(self):
            print('get current price via API')
            binance = InfoFromBinance('ETHEUR')
            currentPrice = binance.getSymbolPrice()

            print('If Price (' + str(currentPrice) + ') lower than ' + str(buyLimit))
            
            if  currentPrice < buyLimit:
                print('Buy coins')
                print(binance.buySymbol())
                print('Set Sell Limit to Buy + 2%')
                super().setSelllimit(buyLimit*1.02)
                print('Set state to Sell')
                super().setCurrentBotState('Sell')

                pass
            else:
                print('Don\'t Buy coins')
                pass
        def CheckBasics(self):
            super().CheckBasics()

    class BotStateIdle(BotState):
        def __init__(self):
            super().__init__('Idle')
            self.CheckBasics()

        def DoStateAction(self):
            print('check current price via API')

        def CheckBasics(self):
            super().CheckBasics()
            super().setCurrentBotState('Buy')
pass

async def hello(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send("""{
  "method": "SUBSCRIBE",
  "params": [
    "btcusdt@aggTrade",
    "btcusdt@depth"
  ],
  "id": 1
}""")
        x = await websocket.recv()
        print(x)
asyncio.get_event_loop().run_until_complete(
    hello('wss://testnet.binance.vision/ws'))


