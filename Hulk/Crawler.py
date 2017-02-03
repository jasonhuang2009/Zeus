'''
Created on Jan 23, 2017

@author: leitaohuang
'''
##初始化数据库相关配置
from Hulk.Trades import Trades
import time
from Hulk.Kline import Kline

dbconfig = {
    'name':'leitao_mysql',
    'host':'rm-2ze81w6e1675e0hd3o.mysql.rds.aliyuncs.com',
    'user':'leitao_mysql',
    'passwd':'Xiaoguai2009',
    'db':'BitCoin'
    }

credential_USD = {
    'apikey':'',
    'secretkey':'',
    'okcoinRESTURL':'www.okcoin.com'
    }

my_trades = Trades(dbconfig,credential_USD)
my_kline = Kline(dbconfig, credential_USD)

coin_types = ['btc_usd','ltc_usd']
contract_types = ['this_week','next_week']
types = ['1min']

count=0
while True:
    ##期货当周合约成交记录
    my_trades.collect_future_trades('btc_usd', 'this_week')
    my_trades.collect_future_trades('ltc_usd', 'this_week')
    
    ##期货下周合约成交记录
    my_trades.collect_future_trades('btc_usd', 'next_week')
    my_trades.collect_future_trades('ltc_usd', 'next_week')
    
    ##现货成交记录
    my_trades.collect_spot_trades('btc_usd')
    my_trades.collect_spot_trades('ltc_usd')
    
    ##期货当周合约日线记录
    my_kline.collect_future_kline('btc_usd', '1min', 'this_week')
    my_kline.collect_future_kline('ltc_usd', '1min', 'this_week')
    ##期货下周合约日线记录
    my_kline.collect_future_kline('btc_usd', '1min', 'next_week')
    my_kline.collect_future_kline('ltc_usd', '1min', 'next_week')
    ##现货1分钟日线
    my_kline.collect_spot_kline('btc_usd', '1min')
    my_kline.collect_spot_kline('ltc_usd','1min')
    
    print(count)
    count+=1
    print (time.strftime("%d/%m/%Y : %H:%M:%S"))
    time.sleep(2)
    
    