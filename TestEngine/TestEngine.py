#coding:utf-8
'''
评测引擎的总结口，在设计上，使用者只需要直接调用这个文件当中的接口就可以满足需求
'''
import datetime
from HaiZhiInterface.HaiZhiTestEngine import HaiZhiTestEngine,HistoryTrading,RealTimeTrading
import StateModule
import DataModule
from LocalEngine import LocalEngine
from TradeModule import TradeModule

'''装饰器'''

def input_checker(func):
    '''
    用于监测函数输入是否合法，code,volume均转化为str
    :param func:
    :return:
    '''
    def _input_checker(self,**kwargs):
        # 股票代码检查
        if isinstance(kwargs['code'], str):
            pass
        elif isinstance(kwargs['code'], int):
            kwargs['code'] = str(kwargs['code'])
            while len(kwargs['code']) < 6:
                kwargs['code'] = '0' + kwargs['code']
        else:
            raise TypeError, 'code must be str or int'
        # 股票交易量检查
        if isinstance(kwargs['volume'], str):
            pass
        elif isinstance(kwargs['volume'], int):
            kwargs['volume'] = str(kwargs['volume'])
        else:
            raise TypeError, 'volume must be str or int'
        #回测日期检查
        if isinstance(self._core,HistoryTrading):
            if 'date' not in kwargs:
                kwargs['date'] = self._current_time.strftime('%Y-%m-%d')
            elif isinstance(kwargs['date'],datetime.datetime):
                kwargs['date'] = datetime.datetime.strftime('%Y-%m-%d')
            elif isinstance(kwargs['date'],str):
                pass
            else:
                raise TypeError,'date must be str or datetime object'
        #返回函数
        #print kwargs
        res = func(self, **kwargs)
        return res
    return _input_checker

'''context类'''

class Context(object):
    '''
    上下文类，用来在回测引擎和测试程序中传递数据
    '''
    def __init__(self,StateModule,DataModule,user_data = {}):

        self._initial_time = StateModule.initial_time
        self._initial_money = StateModule.initial_money

        self._current_time = StateModule.current_time
        self._current_money = StateModule.current_money

        self.DataModule = DataModule

        self.user_data =user_data

    @property
    def current_time(self):
        return self._current_time

'''TestEngine类'''

class Engine(object):
    def __init__(self,
                 user_name = '',
                 password = '',
                 core = 'local',
                 type = 'HistoryTrading',
                 initial_time='2018-01-01',
                 end_date = datetime.datetime.today(),
                 initial_money=100000):
        '''
        测试引擎总接口，包括本地测试内核和海知平台测试内核。
        接口中需要根据不同的引擎内核进行相应的操作分流
        注：
        海知平台内核只提供交易必须的接口，回测模块本身不设置开始和结束时间，启动资金默认为1000000
        :param core:回测引擎内核，可以选择本地内核或者海知平台回测内核
        :param type: 实盘测试或者是历史回测（仅海知平台内核支持历史回测）
        '''
        #用户名和用户登录密码初始化
        if user_name and password:
            self._user_name = user_name
            self._password = password
        else:
            raise (ValueError,'请输入用户名和密码!')

        # 初始化各个模块
        self._StateModule = StateModule.StateModule(initial_time=initial_time, initial_money=initial_money)
        self._DataModule = DataModule.DataModule(self._StateModule)


        #初始化回测引擎核心组件
        if core == 'local':
            # 初始化结束日期
            if isinstance(end_date, str):
                self._end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            elif isinstance(end_date, datetime.datetime):
                self._end_date = end_date
            self._TradeModule = TradeModule(StateModule,DataModule)
            self._core = LocalEngine(self._StateModule,self._DataModule,self._TradeModule)

        elif core == 'HaiZhi':
            self._core = HaiZhiTestEngine(user_id = self._user_name, password= self._password,type = type)
            if type =='HistoryTrading':
                self._core.current_time = initial_time
                self._core.del_stratagy(user_name)
                self._core.create_stratagy(user_name)
                self._core.set_stratagy(user_name)
                #初始化结束日期
                if isinstance(end_date,str):
                    self._end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
                elif isinstance(end_date,datetime.datetime):
                    self._end_date = end_date

            elif type =='RealTimeTrading':
                initial_time = datetime.datetime.today().strftime('%Y-%m-%d')

        #初始化context
        self._context = Context(self._StateModule,self._DataModule)


    def _next_day(self):
        '''
        测试引擎跳转至下一天
        :return:
        '''
        self._StateModule.next_day()

        if isinstance(self._core,HaiZhiTestEngine):
            self._core.current_time = self._StateModule.current_time

    #@input_checker
    def buy(self,code,volume,price_type='now_price',price=None,date=None,effect_term = 1):
        #设置默认输入
        if not date:
            date = self._StateModule.current_time
        #向交易接口传递参数
        if isinstance(self._core,HaiZhiTestEngine):
            result = self._core.buy(code = code,
                           volume=volume,
                           price_type =price_type,
                           price = price,
                           date = date,
                           effect_term=effect_term)
            return result

        elif isinstance(self._core,LocalEngine):
            result = self._core.buy(security=code,
                                    volume=volume,
                                    price_type=price_type,
                                    price=price,)
            return result

    #@input_checker
    def sell(self, code, volume, price_type='now_price', price=None, date=None, effect_term=1):
        # 设置默认输入
        if not date:
            date = self._StateModule.current_time
        # 向交易接口传递参数
        if isinstance(self._core,HaiZhiTestEngine):
            result = self._core.sell(code = code,
                           volume=volume,
                           price_type =price_type,
                           price = price,
                           date = date,
                           effect_term=effect_term)
            return result
        elif isinstance(self._core,LocalEngine):
            result = self._core.sell(security=code,
                                    volume=volume,
                                    price_type=price_type,
                                    price=price, )
            return result

    @property
    def core(self):
        return self._core.__class__

    @property
    def context(self):
        '''
        在调用的过程中动态生成context与程序进行交互
        :return:
        '''
        self._context = Context(self._StateModule,self._DataModule,self._context.user_data)
        return self._context

    def run_stratagy(self, func,*args,**kwargs):
        '''
        讲当前的策略（函数）作为参数传入，同时，将context传入策略当中
        :param func:
        :param args:
        :param kwargs:
        :return:
        '''
        if isinstance(self._core, HaiZhiTestEngine):#海知测试引擎
            if self._core.core == HistoryTrading:#历史回测
                while self._StateModule.current_time < self._end_date:
                    func(self.context,self)
                    self._next_day()
            elif self._core.core == RealTimeTrading:#实盘模拟
                func(self.context, self)
        elif isinstance(self._core,LocalEngine):
            while self._StateModule.current_time < self._end_date:
                func(self.context, self)
                self._next_day()


if __name__ == '__main__':
    engine = Engine(user_name='18126352115',password='Cloud25683')
    print engine.context.current_time
    print engine.DataModule.stock_history_data('600848')
    for i in range(100):
        engine.next_day()
    print engine.context.current_time
    print engine.DataModule.stock_history_data('600848')
