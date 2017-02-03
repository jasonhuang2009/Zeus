'''
Created on Jan 25, 2017

@author: leitaohuang
'''
from OkcoinFutureAPI import OKCoinFuture
from OkcoinSpotAPI import OKCoinSpot
import datetime
from Hulk.MySQLClass import MySQL

class Kline(object):
    __my_future_client = None
    __my_spot_client = None
    __mydb = None   
    
    
    def __init__(self,dbconfig,credential):
        self.__my_future_client = OKCoinFuture(credential['okcoinRESTURL'],credential['apikey'],credential['secretkey'])
        self.__my_spot_client = OKCoinSpot(credential['okcoinRESTURL'],credential['apikey'],credential['secretkey'])
        self.__mydb = MySQL(dbconfig['host'],dbconfig['user'],dbconfig['passwd'],dbconfig['db'])
        
    def collect_future_kline(self,symbol,type,contract_type):
        max_timestamp = self.__mydb.get_max_timestamp(symbol, type,0,contract_type)
        hjson = self.__my_future_client.future_kline(symbol, type, contract_type, 0, max_timestamp)
        
        collected = 0
        for i in range(0,len(hjson)) :
            timestamp = hjson[i][0]
            open = hjson[i][1]
            high = hjson[i][2]
            low = hjson[i][3]
            close = hjson[i][4]
            amount = hjson[i][5]
            amount_in_coin = hjson[i][6]
            
            dateArray = datetime.datetime.fromtimestamp(timestamp/1000)
            otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
            if timestamp > max_timestamp:
                self.__mydb.insert_kline(otherStyleTime, type, open, high, low, close, amount, symbol, 0, amount_in_coin, contract_type)     
                collected = collected+1  
        print (symbol + ' ' + type + ' ' + contract_type +' future kline history' + ' is done! collected ' + str(collected) + ' records!')
    ##end of def
    
    def collect_spot_kline(self,symbol,type):
        spot = 1
        since = 0
        max_timestamp = self.__mydb.get_max_timestamp(symbol,type,spot)
        hjson = self.__my_spot_client.kline(symbol, type, since, max_timestamp)
        
        collected = 0
        for i in range(0,len(hjson)) :
            timestamp = hjson[i][0]
            open = hjson[i][1]
            high = hjson[i][2]
            low = hjson[i][3]
            close = hjson[i][4]
            amount = hjson[i][5]
            
            dateArray = datetime.datetime.fromtimestamp(timestamp/1000)
            otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
            if timestamp > max_timestamp:
                self.__mydb.insert_kline(otherStyleTime, type, open, high, low, close, amount, symbol, spot)     
                collected = collected+1  
        print (symbol +' '+ type + ' spot kline history' + ' is done! collected ' + str(collected) + ' records!')
    ##end of def
