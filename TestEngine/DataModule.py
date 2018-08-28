#coding:utf-8
from settings import ConfigModule
ConfigModule()

from DB.DataInterface import DataInterface
import datetime
import pandas as pd
import sys
'''
数据控制模块，主要是用于控制回测过程中的数据返回，防止用户获取回测日期当日的数据
'''
class DataModule(object):
    def __init__(self,StateModule):
        self._di = DataInterface()
        self._StateModule = StateModule
        self._cache = {#'stocks':[],
                       #'HS300s':[],
                       'stock_history_data':{}}

    def stocks(self):
        if 'stocks' not in self._cache:
            self._cache['stocks'] = self._di.stocks().set_index(u'code')
        return self._cache['stocks']

    def trade_cal(self):
        if 'trade_cal' not in self._cache:
            self._cache['trade_cal'] = self._di.trade_cal()
        return self._cache['trade_cal']

    def stock_history_data(self,security):
        '''

        :param security:
        :return:
        '''
        if str(security) not in self._cache['stock_history_data']:
            self._cache['stock_history_data'][security] = self._di.stock_history_data(security=security).sort_index()
        data = self._cache['stock_history_data'][security]
        #日期筛选，只返回当前回测时间之前的数据


        f = sys._getframe(1).f_code.co_name
        if  f !='sell' and f != 'buy':
            index = (self._StateModule.current_time - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            index = self._StateModule.current_time.strftime('%Y-%m-%d')
        data = data[:index]
        return data



    def HS300s(self,date = None):
        if 'HS300s' not in self._cache:
            self._cache['HS300s'] = self._di.HS300s()
        return self._cache['HS300s']

    def stock_name(self,security):
        stocks = self.stocks()
        name = stocks.loc[stocks.security==security]['name']
        if name.empty:
            return
        else:
            return list(name)[0].encode('utf-8')
if __name__ =='__main__':
    import StateModule
    StateModule = StateModule.StateModule(initial_time = '2018-5-31',initial_money=1000000)
    DM = DataModule(StateModule)
    #print DM.stock_history_data('000001').columns
    #print DM.stock_history_data('000001').index
    #print DM.trade_cal()
    #print DM.stocks().columns
    print DM.stock_name('000001')