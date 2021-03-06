#coding:utf-8
'''
初始化数据库，更新数据库数据
'''
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import *
import pandas as pd
import tushare as ts
import datetime
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''
注：对于字符编码问题，可以将字符编码统一转换成unicode,再将系统默认编码转化为utf-8
'''
'''
脚本用于初始化项目数据库以及更新项目数据库
'''
def date_pre(date):
    date = '%s-%s-%s' % (date[0:4], date[4:6], date[6:8])
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    return date
class launcher(object):

    def __init__(self):
        '''
        :param DB_name:主要是为了方便拓展数据模块，允许用户使用多个不同的数据集
        '''
        #导入项目配置
        import settings
        c = settings.ConfigModule()
        self._settings = c.settings
        #链接数据库
        db_path = self._settings['DB']['db_path']
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

    def update_trade_calendar(self):
        '''
        先清空数据库中的交易日历再重新插入
        :return:
        '''
        #删除数据
        temp = self._session.query(Trade_calendar).all()
        for item in temp:
            self._session.delete(item)
        self._session.commit()
        #插入数据
        ts.set_token(self._settings['DB']['ts_token'])
        pro = ts.pro_api()
        df = pro.trade_cal()
        for i in range(len(df)):
            exchange_id = df.loc[i]['exchange_id']
            cal_date = df.loc[i]['cal_date']
            id = exchange_id + cal_date
            #处理日期
            cal_date = '%s-%s-%s' % (cal_date[0:4], cal_date[4:6], cal_date[6:8])
            cal_date = datetime.datetime.strptime(cal_date, '%Y-%m-%d')
            is_open = df.loc[i]['is_open']
            cal_item = Trade_calendar(id=id,
                                      exchange_id=exchange_id,
                                      cal_date=cal_date,
                                      isopen=is_open)
            self._session.add(cal_item)
        self._session.commit()

    def update_log_init(self):
        stock_list = self._session.query(Stock).all()
        for stock in stock_list:
            log = Update_log(code=stock.code,
                             #stock = stock.security,
                             last_update = None)

            stock.update_log.append(log)
            self._session.add(log)
        self._session.commit()

    def update_stocks(self):
        '''
        基于tushare数据，更新股票列表数据
        先删除数据库中的股票列表，再重新插入
        :return:
        '''
        #删除数据
        temp = self._session.query(Stock).all()
        for item in temp:
            self._session.delete(item)
        self._session.commit()
        #插入数据
        ts.set_token(self._settings['DB']['ts_token'])
        pro = ts.pro_api()
        df = pro.stock_basic( fields='ts_code,symbol,name,exchange_id,list_status,list_date,delist_date,list_status,is_hs')
        for i in range(len(df)):
            ts_code = df.loc[i]['ts_code']
            security = df.loc[i]['symbol']
            name = unicode(df.loc[i]['name'])
            exchange_id = df.loc[i]['exchange_id']
            list_status = df.loc[i]['list_status']
            #处理上市时间
            list_date = df.loc[i]['list_date']
            list_date = '%s-%s-%s' % (list_date[0:4],list_date[4:6],list_date[6:8])
            list_date = datetime.datetime.strptime(list_date,'%Y-%m-%d')
            #处理休市时间
            delist_date = df.loc[i]['delist_date']
            if delist_date:
                delist_date = '%s-%s-%s' % (delist_date[0:4],delist_date[4:6],delist_date[6:8])
                datetime.datetime.strptime(delist_date, '%Y-%m-%d')
            is_hs = df.loc[i]['is_hs']
            #存入数据库
            stock_item = Stock(code=ts_code,
                               security=security,
                               name=name,
                               exchange_id=exchange_id,
                               list_status=list_status,
                               list_date=list_date,
                               delist_date = delist_date,
                               is_hs = is_hs)
            self._session.add(stock_item)
        self._session.commit()

    def update_stock_history(self,ts_code):
        '''
        基于tushare数据，更新股票历史信息
        :param security:
        :return:
        '''
        #检查数据库中已有的数据
        stock = self._session.query(Stock).filter(Stock.code == ts_code).one()
        exist_list = self._session.query(StockHistory).filter(StockHistory.stock==ts_code).all()
        exist_list = [item.date for item in exist_list]
        #更新数据
        ts.set_token(self._settings['DB']['ts_token'])
        pro = ts.pro_api()
        history_data = pro.daily(ts_code=ts_code).set_index('trade_date')
        history_fractor = pro.daily_basic(ts_code=ts_code).set_index('trade_date')
        for date in history_data.index:
            if date_pre(date) not in exist_list:
                id = ts_code+date
                trade_date = date_pre(date)
                open = history_data.loc[date]['open']
                close = history_data.loc[date]['close']
                high = history_data.loc[date]['high']
                low = history_data.loc[date]['low']
                price_change = history_data.loc[date]['change']
                pct_change = history_data.loc[date]['pct_change']
                volume = history_data.loc[date]['vol']
                amount = history_data.loc[date]['amount']
                if date in history_fractor.index:
                    turnover_rate = history_fractor.loc[date]['turnover_rate']
                    volume_ratio = history_fractor.loc[date]['volume_ratio']
                    pe = history_fractor.loc[date]['pe']
                    pe_ttm = history_fractor.loc[date]['pe_ttm']
                    pb = history_fractor.loc[date]['pb']
                    ps = history_fractor.loc[date]['ps']
                    ps_ttm = history_fractor.loc[date]['ps_ttm']
                    total_share = history_fractor.loc[date]['total_share']
                    float_share = history_fractor.loc[date]['float_share']
                    free_share = history_fractor.loc[date]['free_share']
                    total_mv = history_fractor.loc[date]['total_mv']
                    circ_mv = history_fractor.loc[date]['circ_mv']
                else:
                    turnover_rate = None
                    volume_ratio = None
                    pe = None
                    pe_ttm = None
                    pb = None
                    ps = None
                    ps_ttm =None
                    total_share = None
                    float_share = None
                    free_share =None
                    total_mv =None
                    circ_mv = None

                history_item = StockHistory(id=id,
                                            stock = ts_code,
                                            date = trade_date,
                                            open = open,
                                            close = close,
                                            high = high,
                                            low = low,
                                            price_change=price_change,
                                            pct_change=pct_change,
                                            volume=volume,
                                            amount=amount,
                                            turnover_rate=turnover_rate,
                                            volume_ratio=volume_ratio,
                                            pe=pe,
                                            pe_ttm = pe_ttm,
                                            pb=pb,
                                            ps=ps,
                                            ps_ttm = ps_ttm,
                                            total_share=total_share,
                                            float_share=float_share,
                                            free_share=free_share,
                                            total_mv=total_mv,
                                            circ_mv=circ_mv)

                self.session.add(history_item)
                stock.history.append(history_item)
        self._session.commit()

    def update_all_stock_history(self):
        '''
        自动更新全部历史数据
        （目前已知有一些来自tushare的数据并不是14列，会有一些数据不全的情况）
        :return:
        '''
        def view_process():
            self.count+=1
            print 'process:%.2f%%' % (self.count*100/self.length)

        stocks = self._session.query(Stock).all()
        self.length = len(stocks)
        self.count = 0.

        for stock in stocks:
            try:
                self.update_stock_history(stock.code)
                log = self._session.query(Update_log).filter(Update_log.stock == stock.security).one()
                log.last_update = datetime.datetime.today()
                self._session.commit()
            except:
                print '%s fail'%(stock.code)
            view_process()

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
        '''
        目前仅能更新当日的股票历史分笔数据
        :param security:
        :return:
        '''
        stock = self._session.query(Stock).filter(Stock.security == security).one()  # 获取股票基本信息
        df = ts.get_today_ticks(security)
        df  = df.set_index('time')
        for time in df.index:
            temp = datetime.datetime.today().strftime('%Y-%m-%d')+' '+time
            date = datetime.datetime.strptime(temp, "%Y-%m-%d %H:%M:%S")
            stock_tick_item = Tick_data(id = security+'#'+temp,
                                        time = date,
                                        price = df.loc[time]['price'],
                                        change = df.loc[time]['change'],
                                        volume = df.loc[time]['volume'],
                                        amount = df.loc[time]['amount'],
                                        type = unicode(df.ix[time]['type']))
            try:
                self._session.query(Tick_data).filter(Tick_data.id == security+'#'+temp).one()
            except:
                stock.tick_data.append(stock_tick_item)
        self._session.commit()
        
    def test(self):
        temp = self._session.query(StockHistory).filter(StockHistory.stock == '000002.SZ').all()
        print len(temp)
        #for item in list(temp):
            #print item
            #self._session.delete(item)
        #self._session.commit()
if __name__ == '__main__':
    def init_db():
        def wrapper(func):
            print 'running %s' %(func.__name__)
            func()
            print '%s finish' % (func.__name__)

        l = launcher()
        wrapper(l.update_stocks)#更新股票列表
        wrapper(l.update_trade_calendar)#更新交易日历
        wrapper(l.update_log_init)#初始化更新日志
        wrapper(l.update_all_stock_history)#更新所有股票的历史数据
    init_db()
    def test():
        l = launcher()
        log = l._session.query(Update_log).all()
        for item in log:
            print item.code,item.stock,item.last_update
            break
    #test()