#coding:utf-8

'''
样例程序，用户只需要设计每天需要进行的操作，不需要考虑各种时间切片问题
注：
在运行测试的过程中，策略讲作为变量传入
本策略在过去5日收盘价的均值大于上一日均值的情况下买入，剩下的时间卖出

'''

'''add project_path to sys'''
import sys
import os
project_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
sys.path.append(project_path)
'''main'''
from TestEngine.TestEngine import Engine
def test(context,engine):
    print '当前运行时间',context.current_time#当前运行时间
    hs300s = context.DataModule.stocks()[:50]#获取沪深300指数
    for stock in hs300s.index:
        s = hs300s.loc[stock]['security']
        data = context.DataModule.stock_history_data(s)
        if sum(data.iloc[0:5].close)/5 > data.iloc[5].close:
            print s,engine.buy(str(s),volume= 100)
        else:
            print context.StateModule.security_can_trade(s)
            print s,engine.sell(str(s),volume= 100)

if __name__ =='__main__':
    def history_trading_example():
        '''
        海知平台历史回测样例
        :return:
        '''
        #初始化回测引擎
        engine = Engine(user_name='海知平台测试接口样例',
                        password='Cloud25683',
                        #core = 'HaiZhi',
                        #type = 'HistoryTrading',
                        initial_time='2017-01-03',
                        #end_date='2018-1-5',
                        initial_money = 1000000)
        #运行回测引擎的策略
        #print engine.buy('600000',1000)
        engine.run_stratagy(test)

        print engine._core.history_to_csv()
        #讲海知平台的回测交割单输出到csv文件
        #engine._core.history_to_csv()

    def realtime_trading_example():
        '''
        海知平台实盘模拟样例
        :return:
        '''
        engine = Engine(#user_name='海知平台测试接口样例',
                        user_name = '18126352115',
                        password='Cloud25683',
                        core='HaiZhi',
                        type='RealTimeTrading',
                        initial_money=1000000)
        # 运行实盘模拟引擎的策略
        engine.run_stratagy(test)
    #realtime_trading_example()
    #history_trading_example()
    def other():
        #import matplotlib.pyplot as plt
        engine = Engine(user_name='海知平台测试接口样例',
                        password='Cloud25683',
                        core = 'HaiZhi',
                        type = 'HistoryTrading',
                        initial_time='2018-06-4',
                        end_date='2018-1-5',
                        initial_money=1000000,)

        print engine.context.current_time  
        print engine.buy('000001',1000)
        print engine._core.history_to_csv('records')
    #other()
    history_trading_example()
    #realtime_trading_example()
