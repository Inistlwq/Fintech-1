#coding:utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import distinct
import os
import pandas as pd
import tushare as ts
import datetime
import time

from DB.models import *

class DataInterface(object):
    def __init__(self):
        DB_name = 'test.sqlite3'
        db_path = os.path.join(os.path.split(os.path.abspath(__file__))[0],DB_name)
        engine = create_engine('sqlite:///%s' % db_path, echo=False, encoding='utf-8')
        Sesstion = sessionmaker(bind=engine)
        self._session = Sesstion()

    def stocks(self):
        result = {'security':[],
                  'name':[]}
        stocks = self._session.query(Stock).all()
        for stock in stocks:
            result['security'].append(stock.security)
            result['name'].append(stock.name)
        return pd.DataFrame(result)

    def stock_history_data(self,security):
        result = {'date':[],
                  'open':[],
                  'close':[],
                  'high':[],
                  'low':[],
                  'p_change':[],}

        datas = self._session.query(StockHistory).filter(StockHistory.stock == security).all()
        for item in datas:
            result['date'].append(item.date)
            result['open'].append(item.open)
            result['close'].append(item.close)
            result['high'].append(item.high)
            result['low'].append(item.low)
            result['p_change'].append(item.p_change)
        return pd.DataFrame(result).set_index('date')

    def HS300s_list(self):
        '''
        返回当前存储的HS300s指标的日期列表
        :return:
        '''
        data = self._session.query(distinct(HS300s.date)).all()
        return data

    def HS300s(self,date=None):
        '''
        返回特定日期的HS300s指标，默认返回最新的HS300s指标
        :param date:
        :return:
        '''
        result = {'security':[],
                  'name':[],
                  'date':[],
                  'weight':[]}
        if not date:#默认返回当前最新的HS300s
            date = self._session.query(func.min(HS300s.date)).first()#查找出目前最新的HS300s日期
        else:#当有日期输入时执行输入检查
            pass
        data = self._session.query(HS300s).filter(date == date).all()
        for item in data:
            result['security'].append(item.security)
            result['name'].append(item.name)
            result['date'].append(item.date)
            result['weight'].append(item.weight)
        return pd.DataFrame(result).set_index('security')

if __name__ == '__main__':
    di = DataInterface()
    #print (di.stocks())
    print (di.stock_history_data('600038'))
    # (di.HS300s('2'))
    #di.HS300s_list()