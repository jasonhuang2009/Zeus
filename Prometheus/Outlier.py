'''
Created on Jan 24, 2017

@author: leitaohuang
'''
from numpy import arange,array,ones
from scipy import stats 

class Outlier(object):
    __futures_trade_queue = None
    __spot_trade_queue = None
    __line = None
    __mydb = None
    
    config = {'regression_cycle':30}


    def __init__(self, dbconfig):
        print('tbd')
    ##end of def
    
    def get_sequence(self):
        print('tbd')
    ##end of def
        
    def generate_linear(self,xi,y):
        return stats.linregress(xi,y)
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
    