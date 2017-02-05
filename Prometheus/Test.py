'''
Created on Feb 4, 2017

@author: leitaohuang
'''
from Prometheus.Outlier import Outlier
from Config import dbconfig
from OkcoinFutureAPI import OKCoinFuture
import time

apikey = 'fdcaed15-7d45-4de2-8ddf-9111c77375e6'
secretkey = 'ECEE466D8AF35C5F812CB9F4EA3023A0'
okcoinRESTURL = 'www.okcoin.com'   #请求注意：国内账号需要 修改为 www.okcoin.cn  
 
buy_this_week={'contract_type':'this_week','type':'buy'}
sell_this_week = {'contract_type':'this_week','type':'sell'}
buy_next_week={'contract_type':'next_week','type':'buy'}
sell_next_week={'contract_type':'next_week','type':'sell'}

atom_trades=[buy_this_week,sell_this_week,buy_next_week,sell_next_week]
hedge_1={'buy':buy_this_week,'sell':sell_next_week}
hedge_2={'buy':buy_next_week,'sell':sell_this_week}


my_outlier = Outlier(dbconfig)
##slope, intercept, r_value, p_value, std_err  = my_outlier.generate_linear('btc_usd', '1min', 'this_week')

hedge_1_position = 0
hedge_2_position = 0

while True:
    time.sleep(0.2)
    sample_mean = my_outlier.generate_anchor('btc_usd', '1min', 'this_week')
    print(sample_mean)
    
    okcoinFuture = OKCoinFuture(okcoinRESTURL,apikey,secretkey)
    
    this_week_depth = okcoinFuture.future_depth('btc_usd','this_week','5')
    this_week_depth_asks = this_week_depth['asks']
    this_week_depth_bids = this_week_depth['bids']
    '''
    print('this_week_depth_asks')
    print(this_week_depth_asks)
    
    print('this_week_depth_bids')
    print(this_week_depth_bids)
    '''
    
    next_week_depth = okcoinFuture.future_depth('btc_usd','next_week','5')
    next_week_depth_asks = next_week_depth['asks']
    next_week_depth_bids = next_week_depth['bids']
    '''
    print('next_week_depth_asks')
    print(next_week_depth_asks)
    print('next_week_depth_bids')
    print(next_week_depth_bids)
    '''
    potential_diff1 = (next_week_depth_bids[0][0] - this_week_depth_asks[0][0]) - sample_mean
    potential_diff2 = (next_week_depth_asks[0][0] - this_week_depth_bids[0][0]) - sample_mean
    print(potential_diff1)
    print(potential_diff2)
    
    ##open hedge1 position
    if(potential_diff1 > 1.7 and hedge_1_position == 0):
        print (time.strftime("%d/%m/%Y : %H:%M:%S"))
        print('open hedge_1')
        print(hedge_1)
        print('strategy: sell next_week contract at price %.3f with amount %d, and buy this_week contract at price %.3f with amount %d' % \
          (next_week_depth_bids[0][0],next_week_depth_bids[0][1],this_week_depth_asks[0][0],this_week_depth_asks[0][1]))
        hedge_1_position += 1
    ##close hedge1 position, means open hedge2
    if(potential_diff2 < 0.1 and hedge_1_position == 1):
        print (time.strftime("%d/%m/%Y : %H:%M:%S"))
        print('close hedge_1')
        print(hedge_2)
        print('strategy: buy next_week contract at price %.3f with amount %d, and sell this_week contract at price %.3f with amount %d' % \
          (next_week_depth_asks[0][0],next_week_depth_asks[0][1],this_week_depth_bids[0][0],this_week_depth_bids[0][1]))        
        hedge_1_position -= 1
    ##open hedge2 position
    if(potential_diff2 < -1.7 and hedge_2_position == 0):
        print (time.strftime("%d/%m/%Y : %H:%M:%S"))
        print('open hedge_2')
        print(hedge_2)
        print('strategy: buy next_week contract at price %.3f with amount %d, and sell this_week contract at price %.3f with amount %d' % \
          (next_week_depth_asks[0][0],next_week_depth_asks[0][1],this_week_depth_bids[0][0],this_week_depth_bids[0][1]))        
        hedge_2_position += 1
    ##close hedge2 position, means open hedge1
    if(potential_diff1 > -0.1 and hedge_2_position == 1):
        print (time.strftime("%d/%m/%Y : %H:%M:%S"))
        print('close hedge_2')
        print(hedge_1)
        print('strategy: sell next_week contract at price %.3f with amount %d, and buy this_week contract at price %.3f with amount %d' % \
          (next_week_depth_bids[0][0],next_week_depth_bids[0][1],this_week_depth_asks[0][0],this_week_depth_asks[0][1]))        
        hedge_2_position -= 1
        
    '''
    print('strategy: sell next_week contract at price %.3f with amount %d, and buy this_week contract at price %.3f with amount %d' % \
          (next_week_depth_bids[0][0],next_week_depth_bids[0][1],this_week_depth_asks[0][0],this_week_depth_asks[0][1]))
    print(potential_diff1)
    print('strategy: buy next_week contract at price %.3f with amount %d, and sell this_week contract at price %.3f with amount %d' % \
          (next_week_depth_asks[0][0],next_week_depth_asks[0][1],this_week_depth_bids[0][0],this_week_depth_bids[0][1]))
    print(potential_diff2)
    
    
    if(abs(potential_diff1 - sample_mean) > 1.7):
        if position==0:
            print ('deviation is:')
            print (potential_diff1 - sample_mean)
            print(next_week_depth_bids[0][0])
            print(next_week_depth_bids[0][1])
            print(this_week_depth_asks[0][0])
            print(this_week_depth_asks[0][1])
            print('order strategy: sell next_week contract at price %.3f with amount %d, and buy this_week contract at price %.3f with amount %d' % \
                (next_week_depth_bids[0][0],next_week_depth_bids[0][1],this_week_depth_asks[0][0],this_week_depth_asks[0][1]))
            position+=1
    
    if(abs(potential_diff1 - sample_mean) < 0.1):
    '''

