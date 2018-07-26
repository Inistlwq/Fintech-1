#coding:utf-8
import pandas as pd
import datetime

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


