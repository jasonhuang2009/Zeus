'''
Created on Jan 23, 2017

@author: leitaohuang
this is a test for github
'''


from OkcoinFutureAPI import OKCoinFuture
from OkcoinSpotAPI import OKCoinSpot
import datetime
from Hulk.MySQLClass import MySQL

class Trades(object):
    __my_future_client = None
    __my_spot_client = None
    __mydb = None
    

    def __init__(self,dbconfig,credential):
        self.__my_future_client = OKCoinFuture(credential['okcoinRESTURL'],credential['apikey'],credential['secretkey'])
        self.__my_spot_client = OKCoinSpot(credential['okcoinRESTURL'],credential['apikey'],credential['secretkey'])
        self.__mydb = MySQL(dbconfig['host'],dbconfig['user'],dbconfig['passwd'],dbconfig['db'])
    
    
        
    def collect_future_trades(self,symbol,contract_type):
        hjson = self.__my_future_client.future_trades(symbol,contract_type)
        
        collected = 0
        for i in range(0,len(hjson)):
            amount =  float(hjson[i]['amount'])
            date = hjson[i]['date']
            date = datetime.datetime.fromtimestamp(date)
            date = date.strftime("%Y-%m-%d %H:%M:%S")
            date_ms = hjson[i]['date_ms'] / 1000
            date_ms = datetime.datetime.fromtimestamp(date_ms)
            date_ms = date_ms.strftime("%Y-%m-%d %H:%M:%S")
            price = float(hjson[i]['price'])
            tid = hjson[i]['tid']
            trade_type = hjson[i]['type']
            if self.__mydb.future_trade_exist(symbol, date_ms, tid, contract_type) == 0:
                self.__mydb.insert_trades(amount,date,date_ms,price,tid,trade_type,symbol,0,contract_type)
                collected = collected+1
        print (symbol +' ' + contract_type +' future trade history' + ' is done! collected ' + str(collected) + ' records!')
    ##end of def collect_future_trades
    
    def collect_spot_trades(self,symbol):
        max_trade_id = self.__mydb.get_max_trade_id(symbol,1)
       
        hjson = self.__my_spot_client.trades(symbol,max_trade_id)
        
        collected = 0
        for i in range(0,len(hjson)):
            amount =  float(hjson[i]['amount'])
            date = hjson[i]['date']
            date = datetime.datetime.fromtimestamp(date)
            date = date.strftime("%Y-%m-%d %H:%M:%S")
            date_ms = hjson[i]['date_ms'] / 1000
            date_ms = datetime.datetime.fromtimestamp(date_ms)
            date_ms = date_ms.strftime("%Y-%m-%d %H:%M:%S")
            price = float(hjson[i]['price'])
            tid = hjson[i]['tid']
            trade_type = hjson[i]['type']
            if tid > max_trade_id:
                self.__mydb.insert_trades(amount,date,date_ms,price,tid,trade_type,symbol,1)
                collected = collected+1
        print (symbol +' spot trade history' + ' is done! collected ' + str(collected) + ' records!')
    ##end of def collect_spot_trades