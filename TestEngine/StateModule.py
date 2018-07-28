#coding:utf-8
import pandas as pd
import datetime
import numpy as np

def standard_time_input(time):
    '''
    标准化输入的时间
    :param time:
    :return:
    '''
    if isinstance(time, datetime.datetime):
        pass
    elif isinstance(time,datetime.date):
        time = datetime.datetime(time)
    elif isinstance(time, str):
        time = datetime.datetime.strptime(time, "%Y-%m-%d")
    else:
        raise TypeError('The time input should be a datetime.timestamp or a string!')
    return time

class StateModule(object):
    def __init__(self,initial_time,initial_money):
        '''
        初始化状态控制模块
        :param initial_time:
        :param initial_money:
        '''
        self._initial_time = standard_time_input(initial_time)#设定的历史开始时间
        self._initial_money = initial_money#初始金钱

        self._current_time = self._initial_time#当前时间初始化为开始时间
        self._current_money = initial_money#当前现金初始化为初始现金

        self._position = pd.DataFrame({'date':[],'security':[],'hold':[],'can_trade':[]})
        self.trade_log = pd.DataFrame({'timestamp':[datetime.datetime(2010,1,1)],
                                       'security':['0'],
                                        'name':['海知科技'],
                                        'operation':['系统发放'],
                                       'price_order':[0],
                                       'price_deal':[0],
                                       'volume':[0],
                                       'fund_deal':[0],
                                       'fee':[0],
                                       'tax':[0],
                                       'other_fee':[0],
                                       'security_holding':[0],
                                       'happen_fund':[initial_money],
                                       'fund_remain':[initial_money]})
        self.trade_log = self.trade_log.set_index('timestamp')

    def next_day(self):
        '''
        跳转至下一个日期，自动跳过周六周日
        :return:
        '''
        self._current_time += datetime.timedelta(days=1)
        while self._current_time.weekday()==5 or self._current_time.weekday()==6:
            self._current_time += datetime.timedelta(days = 1)

    @property
    def initial_money(self):
        return self._initial_money

    @property
    def initial_time(self):
        return self._initial_time

    @property
    def current_time(self):
        return self._current_time

    @property
    def current_money(self):
        return self._current_money
    @current_money.setter
    def current_money(self,x):
        self._current_money = x

    def security_holding(self,security):
        security_holding = self.trade_log.loc[self.trade_log['security'] == str(security)]['security_holding']
        if security_holding.empty:
            return 0
        else:
            return security_holding[-1]

    def security_can_trade(self,security):
        log = self.trade_log.loc[self.trade_log['security'] == str(security)]
        if log.empty:
            return 0
        else:
            if self.current_time in log.index:
                log = log.reset_index()
                security_freeze = log.loc[(log['timestamp'] == self.current_time) &(log['operation'] == '买入')]['volume']
                security_can_trade = list(log['security_holding'])[-1]-np.sum(security_freeze)
                return security_can_trade
            else:

                return self.security_holding(security)


