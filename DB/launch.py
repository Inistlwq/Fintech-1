#coding:utf-8
'''
初始化数据库，更新数据库数据
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from DB.models import *
import os
import pandas as pd
import tushare as ts
import datetime
import time
import sys

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''
注：对于字符编码问题，可以将字符编码统一转换成unicode,再将系统默认编码转化为utf-8
'''
'''
脚本用于初始化项目数据库以及更新项目数据库
'''
class launcher(object):

    def __init__(self,DB_name):
        '''
        :param DB_name:主要是为了方便拓展数据模块，允许用户使用多个不同的数据集
        '''
        db_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], DB_name)
        engine = create_engine('sqlite:///%s' % db_path, echo=False, encoding='utf-8')
        Sesstion = sessionmaker(bind=engine)
        self._session = Sesstion()
        Base = declarative_base()
        Base.metadata.create_all(engine)


    @property
    def session(self):
        return self._session

    def log(self, string):
        print('updater:' + string)

    def update_stocks(self):
        '''
        基于tushare数据，更新股票列表数据
        :return:
        '''
        df = ts.get_stock_basics()
        for security in df.index:
            print(security)
            '''
            如果数据库中有该股票的基本信息，正常，否则会引发异常
            '''
            try:
                self._session.query(Stock).filter(Stock.security == security).one()
            except:
                name = df.ix[security]['name']
                name = unicode(name)
                stock = Stock(security=security, name=name)
                self._session.add(stock)
                self._session.commit()

    def update_stock_history(self, security,dic = None):
        '''
        基于tushare数据，更新股票历史信息
        :param security:
        :return:
        '''
        stock = self._session.query(Stock).filter(Stock.security == security).one()  # 获取股票基本信息
        date_list = [history.date for history in
                     self._session.query(StockHistory).filter(StockHistory.stock == stock.security).all()]
        try:
            df = ts.get_hist_data(security)
        except:
            self.log('请求超时，正在重试。。。')
            time.sleep(300)
            self.update_stock_history(security)
            return
        if isinstance(df, pd.DataFrame) and df.empty:#tushare股票数据为空
            return False
        elif isinstance(df, pd.DataFrame) and not df.empty:#tushare股票数据不为空
            for date in df.index:
                if pd.to_datetime(date) not in date_list:
                    if not dic:
                        pass
                    else:
                        for key in dic:
                            df[key] = dic[key]
                    if 'turnover' in df.columns:
                        turnover = df.ix[date]['turnover']
                    else:
                        turnover = -1
                    stock_history_item = StockHistory(id='%s/%s' % (security, date),
                                                      date=datetime.datetime.strptime(date, '%Y-%m-%d'),
                                                      open=df.ix[date]['open'],
                                                      close=df.ix[date]['close'],
                                                      high=df.ix[date]['high'],
                                                      low=df.ix[date]['low'],
                                                      volume=df.ix[date]['volume'],
                                                      price_change=df.ix[date]['price_change'],
                                                      p_change=df.ix[date]['p_change'],
                                                      ma5=df.ix[date]['ma5'],
                                                      ma10=df.ix[date]['ma10'],
                                                      ma20=df.ix[date]['ma20'],
                                                      v_ma5=df.ix[date]['v_ma5'],
                                                      v_ma10=df.ix[date]['v_ma10'],
                                                      v_ma20=df.ix[date]['v_ma20'],
                                                      turnover=turnover)
                    stock.history.append(stock_history_item)
                else:
                    pass
            self._session.commit()
            return True
        else:
            return False

    def update_all_stock_history(self):
        '''
        自动更新全部历史数据
        （目前已知有一些来自tushare的数据并不是14列，会有一些数据不全的情况）
        :return:
        '''
        stocks = self._session.query(Stock).all()
        length = float(len(stocks))
        progress = 0
        for stock in stocks:
            self.log('updating %s' % stock.security)
            #更新股票数据
            try:
                temp = self.update_stock_history(stock.security)
            except KeyError:#有一些数据信息不全,缺少换手率(turnover)
                dic = {}
                info = sys.exc_info()
                dic[info[1][0]] = -1
                temp = self.update_stock_history(stock.security,dic)

            if temp:#更新成功
                self.log('%s updating finish' % stock.security)
            else:#更新失败
                info = sys.exc_info()
                self.log('%s updating fail (%s:%s)' % (stock.security,info[0],info[1]))

            progress += 1#进度条
            self.log('当前进度：%f%%' % (100*progress/length))

    def fix(self):
        '''
        将一些停牌或者历史数据出现错误的数据从数据库中移除
        :return:
        '''
        stocks = self._session.query(Stock).all()
        for stock in stocks:
            result = self.session.query(StockHistory).filter(StockHistory.stock == stock.security).all()
            if not result:
                data = ts.get_hist_data(stock.security)
                if isinstance(data,pd.DataFrame) and not data.empty:
                    print ('update',stock.security)
                    try:
                        self.update_stock_history(stock.security)
                    except:
                        pass
                else:
                    print (stock.security)
                    pass
                    #return stock.security

    def update_HS300s(self):
        '''
        基于tushare，更新HS300s指标数据
        :return:
        '''
        data = ts.get_hs300s()
        if isinstance(data, pd.DataFrame) and not data.empty:
            for i in range(len(data)):
                id = '%s/%s' % (data.loc[i]['code'], data.loc[i]['date'])
                HS300s_item = HS300s(id = id,
                                     security = data.loc[i]['code'],
                                     name = data.loc[i]['name'],
                                     date = data.loc[i]['date'],
                                     weight = data.loc[i]['weight'])
                try:
                    self._session.query(HS300s).filter(HS300s.id == id).one()
                except:
                    self._session.add(HS300s_item)
                self._session.commit()

    def update_stock_tick(self,security):
        stock = self._session.query(Stock).filter(Stock.security == security).one()  # 获取股票基本信息
        history_date_list = security._session.query(StockHistory.date).filter(Stock.security == security).all()

#if __name__ == '__main__':
#自动更新数据谷
l = launcher('test.sqlite3')
l.update_stocks()#更新股票列表
l.update_all_stock_history()
l.fix()
l.update_HS300s()