'''
Created on Jan 24, 2017

@author: leitaohuang
'''
##本策略利用BTC_USD 期货当周与下周之间的差价变动套利
from scipy import stats 
from numpy import arange,array,ones
from Hulk.MySQLClass import MySQL

class Outlier(object):
    __futures_trade_queue = None
    __spot_trade_queue = None
    __line = None
    __mydb = None
    
    ##set the default value of regression cycle to be 30 mins
    __regression_cycle = 60

    def __init__(self, dbconfig):
        self.__mydb = MySQL(dbconfig['host'],dbconfig['user'],dbconfig['passwd'],dbconfig['db'])

    ##end of def
    
    def get_sequence(self,symbol,kline_type,contract_type):
        return self.__mydb.get_future_kline_sequence(symbol, kline_type, contract_type, self.__regression_cycle)
    ##end of def
        
    def generate_linear(self,symbol,kline_type,contract_type):
        xi = arange(0,self.__regression_cycle)
        A = array([ xi, ones(self.__regression_cycle)])
        y=[]
        for row in self.get_sequence(symbol,kline_type,contract_type):
            y.append(row[0])
        y.reverse()
        return stats.linregress(xi,y)
    ##end of def
    
    def generate_anchor(self,symbol, kline_type, contract_type):
        slope, intercept, r_value, p_value, std_err  = self.generate_linear(symbol, kline_type, contract_type)
        return slope*self.__regression_cycle + intercept
    ##end of def
    
    def trade_trigger(self,market_depth):
        print('tbd')
        ## compare market_depth with latest line,we can come up with decision on trade command
        ##this function should return a paired trade order on both spot and future
    ##end of def 
    
    def trade_cancle_trigger(self,order_info):
        print('tbd')
        ## this function triggers cancel command depends on the order_info
    ## end of def
    
    def stoploss_trigger(self):
        print('tbd')
    ##end of def 
    