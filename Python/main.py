import time
import random
import requests
import json


buyLimit = 100000
sellLimit = 1000
currentBotState = 'Idle'
runLoop = 'Looprun:true'
currentPrice = 100
eurBalance = 500
coinBalance = 0


class InfoFromBinance:
    symbol =''
    def __init__(self,symbol):
        self.symbol=symbol
    def getSymbolPrice(self):
        global currentPrice
        #do Http magic
        response = requests.get('https://api.binance.com/api/v3/avgPrice?symbol=' + self.symbol)
        print(response)  
       # 
       # if currentBotState == 'Buy':
       #     currentPrice = currentPrice-random.randrange(0,2,0.001)
       # else:
       #     currentPrice = currentPrice+random.randrange(0,2,0.001)

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


while runLoop == 'Looprun:true':
    with open('C:\\Git\\TraderBot\\Python\\config.txt', 'r') as file:
        data = file.read().replace('\n', '')
    runLoop = data  
    class_ = getattr(BotStates, 'BotState'+currentBotState)
    instance = class_()
    instance.DoStateAction()
    #to be replaced by event handler
    time.sleep(0.5) 

