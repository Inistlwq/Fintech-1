#coding:utf-8
from DB.DataInterface import DataInterface
import datetime
import pandas as pd
class DataModule(object):
    def __init__(self,StateModule):
        self._di = DataInterface()
        self._StateModule = StateModule
        self._cache = {#'stocks':[],
                       #'HS300s':[],
                       'stock_history_data':{}}

    def stocks(self):
        if 'stocks' not in self._cache:
            self._cache['stocks'] = self._di.stocks()
        return self._cache['stocks']

    def stock_history_data(self,security):
        '''

        :param security:
        :return:
        '''
        if str(security) not in self._cache['stock_history_data']:
            self._cache['stock_history_data'][security] = self._di.stock_history_data(security=security)
        data = self._cache['stock_history_data'][security]
        #日期筛选，只返回当前回测时间之前的数据
        before = self._StateModule.current_time.strftime('%Y-%m-%d')

        return data[:before]


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
            return list(name)[0]
if __name__ =='__main__':
    import StateModule
    StateModule = StateModule.StateModule(initial_time = '2018-5-31',initial_money=1000000)
    DM = DataModule(StateModule)
    print DM.stock_history_data('600008')