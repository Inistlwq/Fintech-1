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

from models import *

'''
数据接口，将数据库与外部程序链接，从数据库中抽取数据，返回格式化的数据。
'''
class DataInterface(object):
    def __init__(self):
        # 导入项目配置
        import settings
        c = settings.ConfigModule()
        self._settings = c.settings
        # 链接数据库
        db_path = self._settings['DB']['db_path']
        engine = create_engine('sqlite:///%s' % db_path, echo=False, encoding='utf-8')
        Sesstion = sessionmaker(bind=engine)
        self._session = Sesstion()

    def stocks(self):
        result = {'code':[],
                  'security':[],
                  'name':[],
                  'exchange_id':[],
                  'list_date':[],
                  'delist_date':[],
                  'list_status':[],
                  'is_hs':[]}
        stocks = self._session.query(Stock).all()
        for stock in stocks:
            for key in result.keys():
                result[key].append(stock.__dict__[key])
        return pd.DataFrame(result)
    def trade_cal(self):
        result = {'exchange_id':[],
                  'cal_date':[],
                  'isopen':[],
                  'pretrade_date':[]}
        dates = self._session.query(Trade_calendar).all()
        for date in dates:
            for key in result.keys():
                result[key].append(date.__dict__[key])
        return pd.DataFrame(result)

    def stock_history_data(self,security):
        result = {'date':[],
                  'open':[],
                  'close':[],
                  'high':[],
                  'low':[],
                  'price_change':[],
                  'pct_change':[],
                  'volume':[],
                  'amount':[],
                  'turnover_rate':[],
                  'volume_ratio':[],
                  'pe':[],
                  'pe_ttm':[],
                  'pb':[],
                  'ps':[],
                  'ps_ttm':[],
                  'total_share':[],
                  'float_share':[],
                  'free_share':[],
                  'total_mv':[],
                  'circ_mv':[]}

        stock = self._session.query(Stock).filter(Stock.security==security).one()
        datas = self._session.query(StockHistory).filter(StockHistory.stock == stock.code).all()
        for item in datas:
            for key in result.keys():
                result[key].append(item.__dict__[key])
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

   # import matplotlib.pyplot as plt
    di = DataInterface()
    #print (di.stocks())
    #print di.trade_cal()
    data = di.stock_history_data('000001')['open']
    print data
    #plt.plot(data)
    #plt.show()
    # (di.HS300s('2'))
    #di.HS300s_list()