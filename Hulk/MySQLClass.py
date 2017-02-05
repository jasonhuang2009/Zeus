'''
Created on Jan 23, 2017

@author: leitaohuang
'''

import datetime
import logging
import pymysql
import symbol


class MySQL(object):

    def __init__(self ,host,user,password,db):

        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = db
        self.__connection = None
        self.__session = None

    
    def openConnection(self):
        try:
            cnx = pymysql.connect(self.__host, self.__user, self.__password, self.__database)
            self.__connection = cnx
            self.__session    = cnx.cursor()
        except Exception as e:
            print ("Error %d: %s" % (e.args[0],e.args[1]))
    ## end of def openConnection
    
    def closeConnection(self):
        self.__session.close()
        self.__connection.close()
    ## end of def closeConnection
    
    
    ##below is for kline history
    ##get the max timestamp from last crawling, and use it as parameter since in the API call
    def get_max_timestamp(self,symbol,type,spot,contract_type='this_week'):
        self.openConnection()
        
        EPOCH = "1970-01-01 00:00:00"
        EPOCH = datetime.datetime.strptime(EPOCH, "%Y-%m-%d %H:%M:%S")+datetime.timedelta(hours=8)
        ##start_timestamp = (start_time - EPOCH).total_seconds() * 1000
        sql_str = ''
        max_datetime = ''
        max_timestamp = 0
        if symbol== 'btc_usd' and spot == 1:
            sql_str = 'select max(Timestamp) from Kline_BTC_USD where Type = "%s"' % \
            type
        elif symbol== 'ltc_usd' and spot == 1:
            sql_str = 'select max(Timestamp) from Kline_LTC_USD where Type = "%s"' % \
            type     
        elif symbol== 'btc_usd' and spot == 0:  
            sql_str = 'select max(Timestamp) from Kline_Futures_BTC_USD where Type = "%s" and contract_type = "%s"' % \
            (type,contract_type)
        elif symbol== 'ltc_usd' and spot == 0:  
            sql_str = 'select max(Timestamp) from Kline_Futures_LTC_USD where Type = "%s" and contract_type = "%s"' % \
            (type,contract_type)      
        elif symbol== 'btc_cny' and spot == 1:
            sql_str = 'select max(Timestamp) from Kline_BTC_CNY where Type = "%s"' % \
            type
        elif symbol== 'ltc_cny' and spot == 1:
            sql_str = 'select max(Timestamp) from Kline_LTC_CNY where Type = "%s"' % \
            type     
        elif symbol== 'btc_cny' and spot == 0:  
            sql_str = 'select max(Timestamp) from Kline_Futures_BTC_CNY where Type = "%s" and contract_type = "%s"' % \
            (type,contract_type)
        else:  
            sql_str = 'select max(Timestamp) from Kline_Futures_LTC_CNY where Type = "%s" and contract_type = "%s"' % \
            (type,contract_type)  
    
        try:
            self.__session.execute(sql_str)
            max_datetime = self.__session.fetchone()
            max_timestamp = ((max_datetime[0] - EPOCH).total_seconds())* 1000
        except Exception:
            logging.error(sql_str)
    
        self.closeConnection() 
        if max_timestamp==None:
            max_timestamp =0
        else:
            max_timestamp = max_timestamp - 0
     
        return max_timestamp

    def insert_kline(self,timestamp,type,open,high,low,close,amount,symbol,spot,amount_in_coin=0,contract_type='this_week'):
        self.openConnection()
        sql_str = ''
        if symbol== 'btc_usd' and spot == 1:
            sql_str = 'insert into Kline_BTC_USD (Timestamp,Type,Open,High,Low,Close,Amount,CreationDate) values("%s","%s","%.3f","%.3f","%.3f","%.3f","%.3f","%s")' % \
                (timestamp,type,open,high,low,close,amount,datetime.datetime.now())
        elif symbol== 'ltc_usd' and spot == 1:
            sql_str = 'insert into Kline_LTC_USD (Timestamp,Type,Open,High,Low,Close,Amount,CreationDate) values("%s","%s","%.3f","%.3f","%.3f","%.3f","%.3f","%s")' % \
                (timestamp,type,open,high,low,close,amount,datetime.datetime.now())
        elif symbol == 'btc_usd' and spot == 0:
            sql_str = 'insert into Kline_Futures_BTC_USD (Timestamp,Type,Open,High,Low,Close,Amount,Amount_in_Coin,CreationDate,Contract_type) values("%s","%s","%.3f","%.3f","%.3f","%.3f","%.3f","%.3f","%s","%s")' % \
                (timestamp,type,open,high,low,close,amount,amount_in_coin,datetime.datetime.now(),contract_type)
        elif symbol == 'ltc_usd' and spot == 0:
            sql_str = 'insert into Kline_Futures_lTC_USD (Timestamp,Type,Open,High,Low,Close,Amount,Amount_in_Coin,CreationDate,Contract_type) values("%s","%s","%.3f","%.3f","%.3f","%.3f","%.3f","%.3f","%s","%s")' % \
                (timestamp,type,open,high,low,close,amount,amount_in_coin,datetime.datetime.now(),contract_type)
        elif symbol== 'btc_cny' and spot == 1:
            sql_str = 'insert into Kline_BTC_CNY (Timestamp,Type,Open,High,Low,Close,Amount,CreationDate) values("%s","%s","%.3f","%.3f","%.3f","%.3f","%.3f","%s")' % \
                (timestamp,type,open,high,low,close,amount,datetime.datetime.now())
        elif symbol== 'ltc_cny' and spot == 1:
            sql_str = 'insert into Kline_BTC_CNY (Timestamp,Type,Open,High,Low,Close,Amount,CreationDate) values("%s","%s","%.3f","%.3f","%.3f","%.3f","%.3f","%s")' % \
                (timestamp,type,open,high,low,close,amount,datetime.datetime.now())
        elif symbol == 'btc_cny' and spot == 0:
            sql_str = 'insert into Kline_Futures_BTC_CNY (Timestamp,Type,Open,High,Low,Close,Amount,Amount_in_Coin,CreationDate,Contract_type) values("%s","%s","%.3f","%.3f","%.3f","%.3f","%.3f","%.3f","%s","%s")' % \
                (timestamp,type,open,high,low,close,amount,amount_in_coin,datetime.datetime.now(),contract_type)
        else:
            sql_str = 'insert into Kline_Futures_LTC_CNY (Timestamp,Type,Open,High,Low,Close,Amount,Amount_in_Coin,CreationDate,Contract_type) values("%s","%s","%.3f","%.3f","%.3f","%.3f","%.3f","%.3f","%s","%s")' % \
                (timestamp,type,open,high,low,close,amount,amount_in_coin,datetime.datetime.now(),contract_type)
        try:
            self.__session.execute(sql_str)
        except Exception:
            logging.error(sql_str)
            
        self.__connection.commit()        
        
        self.closeConnection()
        
    ##below is for trades history
    def insert_trades(self,amount,date,date_ms,price,tid,type,symbol,spot=1,contract_type='this_week'):
        self.openConnection()
        
        sql_str = ''
        if symbol == 'btc_usd' and spot == 1:
            sql_str = 'insert into Trade_BTC_USD (Amount,Date,Date_ms,Price,Tid,Type,CreationDate) values("%.3f","%s","%s","%.3f","%d","%s","%s")' % \
                (amount,date,date_ms,price,tid,type,datetime.datetime.now())
        elif symbol== 'ltc_usd' and spot == 1:
            sql_str = 'insert into Trade_LTC_USD (Amount,Date,Date_ms,Price,Tid,Type,CreationDate) values("%.3f","%s","%s","%.3f","%d","%s","%s")' % \
                (amount,date,date_ms,price,tid,type,datetime.datetime.now())
        elif symbol == 'btc_usd' and spot == 0:
            sql_str = 'insert into Trade_Futures_BTC_USD (Amount,Date,Date_ms,Price,Tid,Type,Contract_type,CreationDate) values("%.3f","%s","%s","%.3f","%d","%s","%s","%s")' % \
                (amount,date,date_ms,price,tid,type,contract_type,datetime.datetime.now())
        elif symbol== 'ltc_usd' and spot == 0:
            sql_str = 'insert into Trade_Futures_LTC_USD (Amount,Date,Date_ms,Price,Tid,Type,Contract_type,CreationDate) values("%.3f","%s","%s","%.3f","%d","%s","%s","%s")' % \
                (amount,date,date_ms,price,tid,type,contract_type,datetime.datetime.now())
        elif symbol == 'btc_cny' and spot == 1:
            sql_str = 'insert into Trade_BTC_CNY (Amount,Date,Date_ms,Price,Tid,Type,CreationDate) values("%.3f","%s","%s","%.3f","%d","%s","%s")' % \
                (amount,date,date_ms,price,tid,type,datetime.datetime.now())
        elif symbol== 'ltc_cny' and spot == 1:
            sql_str = 'insert into Trade_LTC_CNY (Amount,Date,Date_ms,Price,Tid,Type,CreationDate) values("%.3f","%s","%s","%.3f","%d","%s","%s")' % \
                (amount,date,date_ms,price,tid,type,datetime.datetime.now())
        elif symbol == 'btc_cny' and spot == 0:
            sql_str = 'insert into Trade_Futures_BTC_CNY (Amount,Date,Date_ms,Price,Tid,Type,Contract_type,CreationDate) values("%.3f","%s","%s","%.3f","%d","%s","%s","%s")' % \
                (amount,date,date_ms,price,tid,type,contract_type,datetime.datetime.now())
        ##below is trade history for ltc cny futures 
        ##symbol == 'ltc_cny' and commodity == 0
        else:
            sql_str = 'insert into Trade_Futures_LTC_CNY (Amount,Date,Date_ms,Price,Tid,Type,Contract_type,CreationDate) values("%.3f","%s","%s","%.3f","%d","%s","%s","%s")' % \
                (amount,date,date_ms,price,tid,type,contract_type,datetime.datetime.now())      

        try:
            self.__session.execute(sql_str)
        except Exception:
            logging.error(sql_str)
            
        self.__connection.commit()        
        
        self.closeConnection()
        ## end of def insert_trades
        
    def get_max_trade_id(self,symbol,spot=1,contract_type='this_week'):
        self.openConnection()
        
        sql_str = ''
        max_tid = 0
        if symbol == 'btc_usd' and spot == 1:
            sql_str = 'select max(tid) from trade_BTC_USD'
        elif symbol== 'ltc_usd' and spot == 1:
            sql_str = 'select max(tid) from trade_LTC_USD'
        elif symbol == 'btc_usd' and spot == 0:
            sql_str = 'select max(tid) from trade_futures_BTC_USD where contract_type = "%s"'% \
            contract_type
        elif symbol== 'ltc_usd' and spot == 0:
            sql_str = 'select max(tid) from trade_futures_LTC_USD where contract_type = "%s"'% \
            contract_type
        elif symbol == 'btc_cny' and spot == 1:
            sql_str = 'select max(tid) from trade_BTC_CNY'
        elif symbol== 'ltc_cny' and spot == 1:
            sql_str = 'select max(tid) from trade_LTC_CNY'
        elif symbol == 'btc_cny' and spot == 0:
            sql_str = 'select max(tid) from trade_futures_BTC_CNY and contract_type = "%s"'% \
            contract_type
        ##below is trade history for ltc cny futures 
        ##symbol == 'ltc_cny' and commodity == 0
        else:
            sql_str = 'select max(tid) from trade_futures_LTC_CNY and contract_type = "%s"'% \
            contract_type     
    
        try:
            self.__session.execute(sql_str)
            max_tid = self.__session.fetchone()[0]
        except Exception:
            logging.error(sql_str)
        ##conn.commit()
        
        self.closeConnection() 
        if max_tid==None:
            max_tid =0
        else:
            max_tid = max_tid - 0
        return max_tid         
        ##end of def get_max_trade_id
    
    def future_trade_exist(self,symbol,date_ms,tid,contract_type):
        such_future_trade_no = 0
        sql_str=''
        if symbol == 'btc_usd':
            sql_str='select count(*) from trade_futures_btc_usd where date_ms ="%s" and tid = "%d" and contract_type = "%s"'% \
            (date_ms,tid,contract_type)
        elif symbol == 'ltc_usd':
            sql_str='select count(*) from trade_futures_ltc_usd where date_ms ="%s" and tid = "%d" and contract_type = "%s"'% \
            (date_ms,tid,contract_type)
        elif symbol == 'btc_cny':
            sql_str='select count(*) from trade_futures_btc_cny where date_ms ="%s" and tid = "%d" and contract_type = "%s"'% \
            (date_ms,tid,contract_type)
        else:
            sql_str='select count(*) from trade_futures_ltc_cny where date_ms ="%s" and tid = "%d" and contract_type = "%s"'% \
            (date_ms,tid,contract_type)
            
        self.openConnection()
        try:
            self.__session.execute(sql_str)
            such_future_trade_no = self.__session.fetchone()[0]
        except Exception:
            logging.error(sql_str)
        ##conn.commit()
        
        self.closeConnection()   
        
        if such_future_trade_no == None:
            such_future_trade_no= 0
        else:
            such_future_trade_no = such_future_trade_no - 0
        
        return such_future_trade_no
    ##end of def
    
    def get_future_kline_sequence(self,symbol,kline_type,contract_type,count):
        
        sql_str=''
        sequence=None
        if symbol=='btc_usd':
            sql_str = 'select (next_week.close-this_week.Close) as diff_in_close from kline_futures_btc_usd as this_week,kline_futures_btc_usd as next_week where this_week.timestamp = next_week.timestamp and this_week.contract_type="this_week" and next_week.contract_type = "next_week" and this_week.Type = "%s" and next_week.type="%s" order by this_week.timestamp desc limit 0,%d' % \
            (kline_type,kline_type,count)
        elif symbol=='ltc_usd':
            sql_str = 'select (next_week.close-this_week.Close) as diff_in_close from kline_futures_ltc_usd as this_week,kline_futures_btc_usd as next_week where this_week.timestamp = next_week.timestamp and this_week.contract_type="this_week" and next_week.contract_type = "next_week" and this_week.Type = "%s" and next_week.type="%s" order by this_week.timestamp desc limit 0,%d' % \
            (kline_type,kline_type,count)
        elif symbol=='btc_cny':
            sql_str = 'select (next_week.close-this_week.Close) as diff_in_close from kline_futures_btc_cny as this_week,kline_futures_btc_usd as next_week where this_week.timestamp = next_week.timestamp and this_week.contract_type="this_week" and next_week.contract_type = "next_week" and this_week.Type = "%s" and next_week.type="%s" order by this_week.timestamp desc limit 0,%d' % \
            (kline_type,kline_type,count)     
        else:
            sql_str = 'select (next_week.close-this_week.Close) as diff_in_close from kline_futures_ltc_cny as this_week,kline_futures_btc_usd as next_week where this_week.timestamp = next_week.timestamp and this_week.contract_type="this_week" and next_week.contract_type = "next_week" and this_week.Type = "%s" and next_week.type="%s" order by this_week.timestamp desc limit 0,%d' % \
            (kline_type,kline_type,count)    
 
        self.openConnection()
        try:
            self.__session.execute(sql_str)
            sequence = self.__session.fetchall()
        except Exception:
            logging.error(sql_str)   
                
        self.closeConnection()
        
        return sequence 
        
    ##end of def
        